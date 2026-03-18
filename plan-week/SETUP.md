# Plan-Week Skill — Setup Guide

---

## 1. Memory Files

The skill reads and writes three markdown files. Store them in your Claude Code memory directory (`~/.claude/projects/<project>/memory/`) or any consistent location.

| File | Purpose |
|------|---------|
| `weekly-plan.md` | Current week's plan — read at start, overwritten at end |
| `weekly-history.md` | Running log of weekly completion scores |
| `career-strategy.md` | Your current strategic priorities — used to cross-check week goals |

### `weekly-plan.md` — starting template

```markdown
# Weekly Plan: [Date Range]

## Week Focus
[One sentence goal]

## Priorities (Force Ranked)
1. **P1:** ...
2. **P2:** ...
3. **P3:** ...
4. **P4:** ...

## Daily Plan

### Monday [Date]
- [ ] Task (P1)

...

## Time Blocks Created
| Day | Time | Block | Priority |
|-----|------|-------|----------|

## Mid-Week Adjustments

## End of Week Score
```

### `career-strategy.md` — starting template

```markdown
# Career Strategy

## Current Priorities
1. [Your #1 career goal right now]
2. [Your #2 career goal]
3. [Your #3 career goal]

## Target Role
[The role/level you're working toward]

## Current Initiatives
- [Active project or focus area]
- [Active project or focus area]
```

### `weekly-history.md` — starting template

```markdown
# Weekly History

| Week | P1 Completion | Overall | Notes |
|------|--------------|---------|-------|
```

---

## 2. Scripts

### `read_calendar.py`

Reads upcoming calendar events. Used to check for conflicts when building the daily plan.

```bash
python read_calendar.py events 7      # Next 7 days of events
python read_calendar.py available 5   # Available focus slots this week
```

Uses Google Calendar API. Auth via `credentials.json` + `token.json` (same as other Google API scripts).

### `calendar_manager.py`

Creates focus blocks on your calendar.

```bash
python calendar_manager.py focus "<title>" "<YYYY-MM-DD>" "<HH:MM>" "<HH:MM>" "<description>"
```

### `plan_week_dashboard.py`

Generates a visual HTML dashboard from `weekly-plan.md`. Opens in browser as the final step.

```bash
python plan_week_dashboard.py --generate
```

Reads from `weekly-plan.md` and writes to `~/temp/plan_week.html`.

---

## 3. Pairs Well With

This skill integrates directly with two others in this repo:

- **`/plan-workout`** — called during Step 5 to pre-populate gym sessions for the week
- **`/standup`** — reads `weekly-plan.md` each morning to surface today's tasks and flag mid-week adjustments

Running all three gives you a complete weekly operating rhythm: plan on Sunday, check in each morning, review on Friday.
