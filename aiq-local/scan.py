#!/usr/bin/env python3
"""
AIQ Local - local-only AI-usage profiler for Claude Code.

Replicates the signals that AIQ Rank (aiqrank.com) collects from your
transcripts, but computes everything on your machine and uploads NOTHING.
There are no network imports in this file by design.

What it does:
  1. Scans ~/.claude/projects/**/*.jsonl (your Claude Code sessions).
  2. Aggregates volume + sophistication signals over a lookback window.
  3. Infers your role from your first user messages (same approach AIQ uses).
  4. Computes a TRANSPARENT composite score (weights/targets are constants
     below - tune them; they are our own heuristic, not AIQ's hidden formula).
  5. Appends each run to history.json next to this script for trend tracking.

Usage:
  python scan.py [--days N] [--json] [--no-log]

Pure stdlib. Windows-friendly.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # avoid cp1252 errors on Windows
except Exception:
    pass

# ---------------------------------------------------------------------------
# Signal definitions (mirrors AIQ Rank's scanner)
# ---------------------------------------------------------------------------
ORCHESTRATION_TOOLS = {"Agent"}
CONTEXT_LEVERAGE_TOOLS = {
    "TaskCreate", "TaskUpdate", "TaskList", "ScheduleWakeup",
    "CronCreate", "CronList", "CronDelete", "RemoteTrigger", "Monitor",
}
SKILL_TOOL = "Skill"
PLAN_MODE_TOOL = "ExitPlanMode"
AUTHORSHIP_FILES = ("/SKILL.md", "/.mcp.json", "/mcp.json", "/CLAUDE.md", "/AGENTS.md")

_COMMAND_NAME_RE = re.compile(r"<command-name>/([\w:-]+)</command-name>")
_CORRECTION_RE = re.compile(
    r"(?:^|[\s.,!?;:-])(?:no[,!.\s]|don'?t\b|stop\b|wait[,!.\s]|undo\b|revert\b|"
    r"incorrect\b|wrong\b|actually[,!.\s]|try\s+again\b|that'?s\s+not\b|nope\b)",
    re.IGNORECASE,
)
_CORRECTION_PREFIX = 120

ROLE_KEYWORDS = {
    "engineer": ["code", "function", "bug", "refactor", "compile", "migration", "schema", "commit", "branch"],
    "product": ["spec", "requirement", "user story", "roadmap", "feature", "prioritize", "stakeholder", "prd"],
    "marketing": ["marketing", "campaign", "copy", "landing page", "seo", "social", "content", "audience", "brand", "newsletter"],
    "sales": ["sales", "pipeline", "deal", "prospect", "outbound", "crm", "discovery call", "proposal", "cold email", "objection", "quote"],
    "revops": ["revops", "salesforce", "hubspot", "attribution", "funnel", "conversion rate", "lead scoring", "forecast", "quota"],
    "research": ["analyze", "data", "investigate", "summarize", "compare", "hypothesis"],
    "devops": ["deploy", "docker", "ci", "monitoring", "infrastructure", "kubernetes", "terraform"],
    "founder": ["fundraise", "investor", "pitch deck", "seed round", "cap table", "runway", "cofounder", "term sheet", "board update"],
    "executive": ["okr", "board meeting", "headcount", "org chart", "quarterly review", "budget", "strategy memo", "all-hands"],
}

# ---------------------------------------------------------------------------
# Composite score config - TRANSPARENT and tunable. This is our own grading,
# not AIQ Rank's server-side formula (which is closed). Each dimension scores
# 0-100 via pct(value, target); the weights below sum to 100.
# ---------------------------------------------------------------------------
WEIGHTS = {
    "orchestration": 25,   # using subagents, especially in parallel
    "context_leverage": 15,  # task/scheduling tools
    "planning": 10,        # plan mode
    "authorship": 20,      # building your own skills / MCP / CLAUDE.md
    "breadth": 15,         # variety of tools / skills / MCP servers used
    "consistency": 15,     # sustained, multi-day usage
}
# Targets are "strong usage over the window" thresholds. Hitting the target
# on a dimension = 100 for that dimension. Adjust to taste.
TARGETS = {
    "parallel_agent_turns": 20, "max_parallel_agents": 4, "orchestration_days": 12,
    "context_leverage_days": 10,
    "plan_mode_invocations": 10,
    "authorship_writes": 10,
    "distinct_tools": 15, "distinct_skills": 8, "distinct_mcp_servers": 4,
    "active_days": 20, "sessions": 40,
}
TIERS = [(80, "Orchestrator"), (60, "Power User"), (40, "Practitioner"), (0, "Exploring")]


def pct(value, target):
    if target <= 0:
        return 0.0
    return min(100.0, 100.0 * value / target)


def parse_ts(value):
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def content_to_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text":
                parts.append(b.get("text", ""))
        return " ".join(parts)
    return ""


def iter_tool_uses(content):
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                yield b


def transcript_files():
    home = Path(os.path.expanduser("~"))
    base = home / ".claude" / "projects"
    if not base.is_dir():
        return []
    out = []
    for p in base.rglob("*.jsonl"):
        parts = {x.lower() for x in p.parts}
        if "subagents" in parts:
            continue
        if "aiqrank" in str(p).lower():
            continue
        out.append(p)
    return out


def scan(days):
    now = datetime.now(timezone.utc)
    cutoff_ord = (now.astimezone().date()).toordinal() - days + 1

    totals = defaultdict(int)
    active_dates = set()
    orchestration_dates = set()
    context_leverage_dates = set()
    plan_mode_dates = set()
    tool_names = set()
    skill_names = set()
    mcp_servers = set()
    authored_skills = set()
    role_sample = []
    seen_first_user = set()           # sessionId -> captured first msg
    session_span = {}                 # sessionId -> [min_ts, max_ts]
    agents_by_request = defaultdict(int)  # requestId -> agent calls

    for f in transcript_files():
        try:
            fh = open(f, encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                etype = e.get("type")
                if etype not in ("user", "assistant"):
                    continue
                dt = parse_ts(e.get("timestamp"))
                if dt is None:
                    continue
                local_date = dt.astimezone().date()
                if local_date.toordinal() < cutoff_ord:
                    continue

                sid = e.get("sessionId") or "?"
                ts = dt.timestamp()
                span = session_span.get(sid)
                if span is None:
                    session_span[sid] = [ts, ts]
                else:
                    if ts < span[0]:
                        span[0] = ts
                    if ts > span[1]:
                        span[1] = ts

                active_dates.add(local_date)
                totals["messages"] += 1
                msg = e.get("message") or {}

                if etype == "user":
                    text = content_to_text(msg.get("content"))
                    if text:
                        totals["user_messages"] += 1
                        if _CORRECTION_RE.search(text[:_CORRECTION_PREFIX]):
                            totals["user_corrections"] += 1
                        if sid not in seen_first_user and len(role_sample) < 500:
                            seen_first_user.add(sid)
                            role_sample.append(text[:500])
                        for cmd in _COMMAND_NAME_RE.findall(text):
                            skill_names.add(cmd)
                            totals["skill_invocations"] += 1
                    continue

                # assistant
                usage = msg.get("usage") or {}
                totals["tokens_input"] += int(usage.get("input_tokens") or 0)
                totals["tokens_output"] += int(usage.get("output_tokens") or 0)
                totals["tokens_cache_read"] += int(usage.get("cache_read_input_tokens") or 0)
                totals["tokens_cache_creation"] += int(usage.get("cache_creation_input_tokens") or 0)

                content = msg.get("content")
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "thinking":
                            totals["reasoning_blocks"] += 1

                turn_tools = list(iter_tool_uses(content))
                agents_in_turn = sum(1 for t in turn_tools if t.get("name") in ORCHESTRATION_TOOLS)
                rid = e.get("requestId")
                if agents_in_turn and rid:
                    agents_by_request[rid] += agents_in_turn
                elif agents_in_turn:
                    if agents_in_turn > totals["max_parallel_agents"]:
                        totals["max_parallel_agents"] = agents_in_turn
                    if agents_in_turn >= 2:
                        totals["parallel_agent_turns"] += 1

                for t in turn_tools:
                    name = t.get("name", "")
                    if not name:
                        continue
                    totals["tool_calls"] += 1
                    tool_names.add(name)
                    if name == SKILL_TOOL:
                        sk = (t.get("input") or {}).get("skill")
                        if sk:
                            skill_names.add(sk)
                            totals["skill_invocations"] += 1
                    if name.startswith("mcp__"):
                        parts = name.split("__")
                        if len(parts) >= 3 and parts[1]:
                            mcp_servers.add(parts[1])
                    if name in ORCHESTRATION_TOOLS:
                        orchestration_dates.add(local_date)
                    if name in CONTEXT_LEVERAGE_TOOLS:
                        context_leverage_dates.add(local_date)
                    if name == PLAN_MODE_TOOL:
                        plan_mode_dates.add(local_date)
                        totals["plan_mode_invocations"] += 1
                    if name in ("Write", "Edit"):
                        path = ((t.get("input") or {}).get("file_path") or "").replace("\\", "/")
                        if "/.claude/skills/" in path and "/aiqrank/" not in path:
                            seg = path.split("/.claude/skills/", 1)[1].split("/", 1)[0]
                            if seg:
                                authored_skills.add(seg)
                        if any(path.endswith(suf) for suf in AUTHORSHIP_FILES):
                            totals["authorship_writes"] += 1

    # Fold parallel-agent tallies grouped by requestId into peaks.
    for rid, count in agents_by_request.items():
        if count > totals["max_parallel_agents"]:
            totals["max_parallel_agents"] = count
        if count >= 2:
            totals["parallel_agent_turns"] += 1

    for k in ("messages", "user_messages", "user_corrections", "skill_invocations",
              "tool_calls", "tokens_input", "tokens_output", "tokens_cache_read",
              "tokens_cache_creation", "reasoning_blocks", "parallel_agent_turns",
              "max_parallel_agents", "plan_mode_invocations", "authorship_writes"):
        totals.setdefault(k, 0)

    totals["sessions"] = len(session_span)
    totals["active_days"] = len(active_dates)
    totals["orchestration_days"] = len(orchestration_dates)
    totals["context_leverage_days"] = len(context_leverage_dates)
    totals["plan_mode_days"] = len(plan_mode_dates)
    totals["distinct_tools"] = len(tool_names)
    totals["distinct_skills"] = len(skill_names)
    totals["distinct_mcp_servers"] = len(mcp_servers)
    totals["authored_skills"] = len(authored_skills)
    totals["max_concurrent_sessions"] = peak_concurrency(session_span)

    return {
        "totals": dict(totals),
        "role": classify_role(role_sample),
        "skills_used": sorted(skill_names),
        "mcp_servers_used": sorted(mcp_servers),
        "authored_skill_names": sorted(authored_skills),
    }


def peak_concurrency(session_span):
    """Approx peak concurrent sessions via interval sweep over (start,end)."""
    events = []
    for start, end in session_span.values():
        events.append((start, 1))
        events.append((end, -1))
    events.sort()
    cur = peak = 0
    for _, delta in events:
        cur += delta
        if cur > peak:
            peak = cur
    return peak


def classify_role(messages):
    if not messages:
        return {"inferred_role": "engineer", "confident": False}
    corpus = " ".join(m.lower() for m in messages if isinstance(m, str))
    scores = {}
    for role, vocab in ROLE_KEYWORDS.items():
        matches = sum(corpus.count(kw) for kw in vocab)
        scores[role] = matches / len(vocab) if vocab else 0.0
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    if not ranked or ranked[0][1] == 0:
        return {"inferred_role": "engineer", "confident": False}
    top, top_s = ranked[0]
    runner = ranked[1][1] if len(ranked) > 1 else 0
    confident = runner == 0 or top_s / runner >= 1.5
    return {"inferred_role": top if confident else "engineer", "confident": confident,
            "top3": [(r, round(s, 2)) for r, s in ranked[:3]]}


def composite(totals):
    t = totals
    dims = {}
    dims["orchestration"] = round(
        0.45 * pct(t["parallel_agent_turns"], TARGETS["parallel_agent_turns"])
        + 0.30 * pct(t["max_parallel_agents"], TARGETS["max_parallel_agents"])
        + 0.25 * pct(t["orchestration_days"], TARGETS["orchestration_days"]), 1)
    dims["context_leverage"] = round(pct(t["context_leverage_days"], TARGETS["context_leverage_days"]), 1)
    dims["planning"] = round(pct(t["plan_mode_invocations"], TARGETS["plan_mode_invocations"]), 1)
    dims["authorship"] = round(pct(t["authorship_writes"], TARGETS["authorship_writes"]), 1)
    dims["breadth"] = round(
        0.4 * pct(t["distinct_tools"], TARGETS["distinct_tools"])
        + 0.3 * pct(t["distinct_skills"], TARGETS["distinct_skills"])
        + 0.3 * pct(t["distinct_mcp_servers"], TARGETS["distinct_mcp_servers"]), 1)
    dims["consistency"] = round(
        0.5 * pct(t["active_days"], TARGETS["active_days"])
        + 0.5 * pct(t["sessions"], TARGETS["sessions"]), 1)
    score = sum(WEIGHTS[k] * dims[k] for k in WEIGHTS) / 100.0
    tier = next(label for floor, label in TIERS if score >= floor)
    return round(score, 1), tier, dims


def history_path():
    # User-home so it survives wherever the skill is installed and never
    # writes into a cloned repo. Override with AIQ_LOCAL_HISTORY if you like.
    override = os.environ.get("AIQ_LOCAL_HISTORY")
    if override:
        return Path(override)
    return Path(os.path.expanduser("~")) / ".aiq-local" / "history.json"


def load_history():
    p = history_path()
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def append_history(record):
    p = history_path()
    hist = load_history()
    hist.append(record)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(hist, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass


def fmt_int(n):
    return f"{n:,}"


def render(result, score, tier, dims, days, prev):
    t = result["totals"]
    role = result["role"]
    L = []
    L.append("=" * 60)
    L.append(f"  AIQ LOCAL  -  last {days} days  (local-only, nothing uploaded)")
    L.append("=" * 60)
    delta = ""
    if prev is not None:
        d = round(score - prev, 1)
        arrow = "+" if d >= 0 else ""
        delta = f"   (prev {prev} -> {arrow}{d})"
    L.append(f"\n  COMPOSITE  {score}/100   [{tier}]{delta}")
    L.append("  (transparent heuristic - see WEIGHTS/TARGETS in scan.py)\n")
    L.append("  Dimension breakdown:")
    for k in WEIGHTS:
        bar = "#" * int(dims[k] / 5)
        L.append(f"    {k:<17} {dims[k]:5.1f}  (w{WEIGHTS[k]:>2}) {bar}")
    rl = role.get("inferred_role", "?")
    conf = "confident" if role.get("confident") else "low confidence -> default"
    L.append(f"\n  Inferred role: {rl}  ({conf})")
    if role.get("top3"):
        L.append("    top signals: " + ", ".join(f"{r}={s}" for r, s in role["top3"]))
    L.append("\n  Volume:")
    L.append(f"    active days {t['active_days']}   sessions {t['sessions']}   "
             f"messages {fmt_int(t['messages'])}   tool calls {fmt_int(t['tool_calls'])}")
    tok = t["tokens_input"] + t["tokens_output"] + t["tokens_cache_read"] + t["tokens_cache_creation"]
    L.append(f"    tokens (incl cache) {fmt_int(tok)}   reasoning blocks {fmt_int(t['reasoning_blocks'])}")
    L.append("\n  Sophistication signals:")
    L.append(f"    orchestration: {t['orchestration_days']} active days, "
             f"{t['parallel_agent_turns']} parallel-agent turns, peak {t['max_parallel_agents']} agents/turn")
    L.append(f"    context leverage: {t['context_leverage_days']} days using task/schedule tools")
    L.append(f"    plan mode: {t['plan_mode_invocations']} invocations on {t['plan_mode_days']} days")
    L.append(f"    authorship: {t['authorship_writes']} writes to SKILL/MCP/CLAUDE files; "
             f"{t['authored_skills']} distinct skills authored")
    L.append(f"    peak concurrent sessions: {t['max_concurrent_sessions']} (approx)")
    L.append(f"    breadth: {t['distinct_tools']} tools, {t['distinct_skills']} skills, "
             f"{t['distinct_mcp_servers']} MCP servers")
    cr = (100.0 * t["user_corrections"] / t["user_messages"]) if t["user_messages"] else 0
    L.append(f"    self-correction rate: {cr:.1f}%  ({t['user_corrections']}/{t['user_messages']} msgs)  [reported, not scored]")
    if result["authored_skill_names"]:
        L.append("\n  Skills you authored: " + ", ".join(result["authored_skill_names"]))
    L.append("=" * 60)
    return "\n".join(L)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of the report")
    ap.add_argument("--no-log", action="store_true", help="do not append to history.json")
    args = ap.parse_args(argv)

    result = scan(args.days)
    score, tier, dims = composite(result["totals"])

    if args.json:
        print(json.dumps({"days": args.days, "score": score, "tier": tier,
                          "dimensions": dims, **result}, indent=2))
        return 0

    hist = load_history()
    prev = hist[-1]["score"] if hist else None
    print(render(result, score, tier, dims, args.days, prev))

    if not args.no_log:
        append_history({
            "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "days": args.days, "score": score, "tier": tier,
            "dimensions": dims, "role": result["role"].get("inferred_role"),
            "totals": result["totals"],
        })
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
