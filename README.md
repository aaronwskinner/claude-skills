# Claude Code Skills

A collection of skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — drop-in prompt files that give Claude specialized, repeatable workflows.

## What are Skills?

Skills live in `.claude/skills/<skill-name>/` in your project (or `~/.claude/skills/` globally). Claude Code loads them automatically and makes them available as slash commands.

## Skills in This Repo

> Together, `apply-job` and `interview-prep` form a complete AI-native job search workflow — from application through final round.

### [`/apply-job`](./apply-job/)

Full job application workflow — from job posting URL to tailored resume, cover letter, and tracker entry.

Given a job URL, Claude fetches the JD, maps your experience to requirements, tailors your resume from pre-written bullet variations, writes a problem-solution cover letter with company-specific research, and uploads everything to Drive.

**Requires:** `PROFILE.md`, `BULLETS.md`, `CONTEXT.md` in your project root. See [`apply-job/SETUP.md`](./apply-job/SETUP.md).

**Trigger:** `/apply-job <job-url>`

---

### [`/interview-prep`](./interview-prep/)

Build structured interview prep docs for any upcoming interview — phone screens through final rounds.

Given a company, role, and interviewers, Claude researches the company, maps your experience to the JD, drafts a full prep doc with tailored Q&A, domain fluency lines, and questions to ask — plus a printable 3-page quick reference.

**Requires:** `PROFILE.md`, `STORIES.md`, `BULLETS.md` in your project root.

**Trigger:** `/interview-prep [company]` or "prep me for my [company] interview"

---

### [`/standup`](./standup/)

Daily morning check-in that pulls health/recovery data, builds a dashboard, gathers news trends, and facilitates an interactive priority review.

**Requires:** Custom scripts for health data and dashboard. See [`standup/SETUP.md`](./standup/SETUP.md).

**Trigger:** `/standup`

### [`/debrief`](./debrief/)

Process an interview transcript after a call. Extracts what went well, key intel about the role/process/team, what the next round will likely probe, and action items — then updates your tracker, memory files, and weekly plan automatically.

**Requires:** Google Drive API auth (to fetch transcripts from Google Docs) + tracker script. See [`apply-job/SETUP.md`](./apply-job/SETUP.md) for auth setup.

**Trigger:** `/debrief [company]` or share a Google Docs transcript link

---

### [`/plan-week`](./plan-week/)

Sunday evening planning workflow. Scores last week, sets force-ranked priorities (pushes back on "all P1"), builds a full Mon–Sun task breakdown, creates calendar focus blocks, and opens a visual dashboard.

Integrates with `/plan-workout` for gym sessions and feeds `/standup` each morning.

**Requires:** `weekly-plan.md`, `career-strategy.md`, `weekly-history.md` memory files + calendar scripts. See [`plan-week/SETUP.md`](./plan-week/SETUP.md).

**Trigger:** `/plan-week` (or `/plan-week test` for dry run)

---

### [`/review-week`](./review-week/)

End of week scoring. Counts completed vs. incomplete tasks per priority level, surfaces patterns (chronic carry-forwards, P1 neglect, overcommitment), updates history, and seeds next week's priorities.

Pairs with `/plan-week` — run it Friday or Sunday before planning the next week.

**Trigger:** `/review-week`

---

### [`/plan-workout`](./plan-workout/)

Plan the coming week's workout sessions. Reads your spreadsheet history, applies micro-progression (last reps + 1, load increase at 3x12), handles deload weeks, flags recovery issues from wearable data, and compresses sessions automatically when you have a shorter window.

**Requires:** Google Sheets workout tracker + optional wearable recovery script. See [`plan-workout/SETUP.md`](./plan-workout/SETUP.md).

**Trigger:** `/plan-workout`

---

## Installation

Copy any skill into your project's `.claude/skills/` directory:

```bash
git clone https://github.com/<your-username>/claude-skills.git

# Copy a skill into your project
cp -r claude-skills/interview-prep your-project/.claude/skills/

# Or install globally (available in all projects)
cp -r claude-skills/interview-prep ~/.claude/skills/
```

---

## License

MIT
