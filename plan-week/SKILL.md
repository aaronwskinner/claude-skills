---
name: plan-week
description: Sunday evening weekly planning workflow
---

# Weekly Planning Skill

Plan the week ahead. Set priorities, build a daily task breakdown (Mon–Sun), create calendar focus blocks, and open a visual dashboard.

## Commands

- `/plan-week` — Run the full Sunday evening planning workflow
- `/plan-week test` — Dry run: builds the plan but writes to a temp file and skips creating real calendar blocks

## Setup

See `SETUP.md` for required scripts and memory files.

---

## Workflow

### Step 1: Gather Context

Read these memory files for current state:
- `weekly-plan.md` — last week's plan (if exists)
- `weekly-history.md` — completion trends over time
- `career-strategy.md` — current strategic priorities (used to cross-check week's goals)

Pull this week's calendar:
```bash
python ~/job-search/read_calendar.py events 7
python ~/job-search/read_calendar.py available 5
```

### Step 2: Score Last Week

If `weekly-plan.md` has a real plan (not a placeholder), score it:
- Count completed `[x]` vs incomplete `[ ]` tasks
- Report completion rate per priority level
- Note what carried forward and why

### Step 3: Set This Week's Priorities

Ask: **"What are your top priorities this week?"**

Rules:
- Maximum 4 priorities
- Each gets a P-level (P1 through P4)
- If the user says "everything is P1" — push back: *"If you could only finish ONE thing this week, what is it?"*
- Cross-reference against `career-strategy.md` current priorities
- Flag if this week's priorities don't align with stated career strategy

### Step 4: Build the Daily Plan

For **each day (Mon–Sun)**:

**Weekdays (Mon–Fri):**
- Assign 2-3 tasks from the priority list
- Check calendar for existing commitments
- Identify focus block opportunities in available slots
- Every task must tie to a P-level
- No vague tasks — be specific and completable

**Weekends (Sat–Sun):**
- Include personal activities (family, fitness, errands)
- Add 1-2 optional work tasks (lower priority, prep, learning)
- Account for personal schedule commitments
- Keep work items light — weekends are recovery + personal time

### Step 5: Plan Workout Sessions

Run `/plan-workout` to pull last performance data and pre-populate the coming week's sessions. If the user specified gym days during priority-setting, pass those along. Otherwise `/plan-workout` will ask.

### Step 6: Create Calendar Focus Blocks

For each major weekday work block:
```bash
python ~/job-search/calendar_manager.py focus "<title>" "<date>" "<HH:MM>" "<HH:MM>" "<description>"
```
- If a weekday has no focus blocks, flag it
- Do NOT create focus blocks on weekends

**Dry-run mode:** Skip this step. Show what blocks *would* be created instead.

### Step 7: Write the Weekly Plan

Overwrite `weekly-plan.md` with the full plan.

**Dry-run mode:** Write to `~/temp/weekly-plan-test.md` instead.

Use this structure:

```markdown
# Weekly Plan: [Date Range]

## Week Focus
[One sentence: what makes this a successful week]

## Priorities (Force Ranked)
1. **P1:** [Most important outcome]
2. **P2:** [Second priority]
3. **P3:** [Third priority]
4. **P4:** [Fourth if applicable]

## Daily Plan

### Monday [Date]
- [ ] [Task] (P1)
- [ ] [Task] (P2)

### Tuesday [Date]
...

### Saturday [Date]
- [ ] [Personal activity]
- [ ] [Optional work task] (P3)

### Sunday [Date]
- [ ] [Personal activity]
- [ ] Run /plan-week for next week

## Time Blocks Created
| Day | Time | Block | Priority |
|-----|------|-------|----------|

## Mid-Week Adjustments
[Empty — filled by /standup]

## End of Week Score
[Empty — filled by /review-week]
```

### Step 8: Generate Dashboard

```bash
python ~/plan_week_dashboard.py --generate
```

Open in browser:
```bash
# macOS
open ~/temp/plan_week.html

# Windows
start "" "C:/path/to/temp/plan_week.html"

# Linux
xdg-open ~/temp/plan_week.html
```

### Step 9: Confirm

Present the plan summary. Wait for confirmation before finalizing.
