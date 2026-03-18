# Claude Code Skills

A collection of skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — drop-in prompt files that give Claude specialized, repeatable workflows.

## What are Skills?

Skills live in `.claude/skills/<skill-name>/` in your project (or `~/.claude/skills/` globally). Claude Code loads them automatically and makes them available as slash commands.

## Skills in This Repo

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
