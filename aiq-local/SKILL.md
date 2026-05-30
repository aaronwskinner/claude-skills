---
name: aiq-local
description: Local-only AI-usage profiler. Scans your Claude Code transcripts and reports a transparent AIQ-style sophistication score (orchestration, context leverage, authorship, breadth, consistency) plus an inferred role. Nothing is uploaded. Use when someone asks for their AIQ, AI-usage score, or to track how their AI usage is trending.
allowed-tools: Bash(python:*), Bash(PYTHONIOENCODING=utf-8 python:*), Bash(py:*), Bash(PYTHONIOENCODING=utf-8 py:*), Read
---

# AIQ Local

A local replacement for AIQ Rank (aiqrank.com). It computes the same signals
AIQ Rank collects from your transcripts, but everything runs on your machine
and **nothing is uploaded**. `scan.py` has no network imports by design.

## What it measures

Reverse-engineered from the open-source `aiqrank/plugin` scanner:

- **Volume** - active days, sessions, messages, tool calls, tokens, reasoning blocks
- **Orchestration** - subagent (`Agent`) usage, parallel-agent turns, peak agents/turn
- **Context leverage** - `TaskCreate/Update/List`, `ScheduleWakeup`, `Cron*`, `RemoteTrigger`, `Monitor`
- **Planning** - `ExitPlanMode` usage
- **Authorship** - writes to `SKILL.md`, `.mcp.json`, `CLAUDE.md`/`AGENTS.md`
- **Breadth** - distinct tools, skills, MCP servers used
- **Role** - keyword match on first user messages (engineer / product / sales / founder / ...)

The composite score is **a transparent heuristic of our own** (weights and
targets are constants at the top of `scan.py` - tune them freely). AIQ Rank's
real score is computed server-side and is not public, so this is not their
number, just the same inputs graded openly.

## Run it

`scan.py` lives in this skill's folder. Run it with Python 3.7+:

```bash
# global install (~/.claude/skills/aiq-local/)
PYTHONIOENCODING=utf-8 python ~/.claude/skills/aiq-local/scan.py --days 30
```

On Windows, `~` is `%USERPROFILE%`. If the skill is installed in a project
instead, point at that project's `.claude/skills/aiq-local/scan.py`.

Flags:
- `--days N` - lookback window (default 30)
- `--html` - generate a self-contained HTML dashboard and open it in the browser (gauge, dimension radar, volume cards, signal table, and a score-trend chart from history). Writes to `~/.aiq-local/report.html`.
- `--out PATH` - override the `--html` output path
- `--no-open` - with `--html`, write the file but don't launch the browser
- `--json` - raw JSON instead of the report
- `--no-log` - don't append this run to history

For the visual dashboard, run with `--html`:

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/aiq-local/scan.py --days 30 --html
```

The dashboard reads `report_template.html` (next to `scan.py`) and injects the
scan data; it is fully self-contained and opens offline via `file://`.

Each run appends to `~/.aiq-local/history.json` (override with the
`AIQ_LOCAL_HISTORY` env var) so you can track the trend; the report shows the
delta vs your previous run.

## How to present results

1. Run the command (default 30 days unless a window is specified).
2. Show the report.
3. Add a 2-3 bullet read: current tier, the single biggest lever to raise the
   score (usually the lowest dimension, often planning), and the trend vs last
   run if history exists.

## Privacy

Reads only your own local transcripts under `~/.claude/projects/`. Computes
everything locally. Makes no network calls and writes only the local history
file. Safe to run on any machine.

## Known caveat (role inference)

Role uses naive substring counting (faithful to AIQ Rank's code), so short
keywords like `ci`, `data`, `code` over-match and can mislabel a product or
founder user as `devops`/`engineer`. To make roles accurate, switch the
matching in `classify_role` to word-boundary regex - this diverges from AIQ
but is more correct.
