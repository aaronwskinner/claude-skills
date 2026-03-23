---
allowed-tools: Bash(py:*), Bash(python:*)
description: Plan the coming week's workout sessions — pull last performance, set targets, write to spreadsheet
---

## Your task

Plan and pre-populate workout sessions for the coming week in the workout tracking spreadsheet.

**Spreadsheet ID:** `<YOUR_SPREADSHEET_ID>`
**Credentials:** `<YOUR_TOKEN_PATH>`
**Sheet:** `workout`

### Column Structure (16 columns, A–P)

A=Date, B=Workout, C=Exercise, D=Set#, E=Load, F=Reps, G=RIR, H=Volume (=E*F), I=Pain Flag (0-5), J=Status, K=Skip Reason, L=Rest(sec), M=Notes, N=Modification, O=Target Load, P=isDeloadWeek

### Workout Rotation

4-day Upper/Lower split. Rotation order: **Upper A → Lower A → Upper B → Lower B**. Assign to available gym days in the coming week (typically 4 days, skip rest days).

### Exercise Templates

**All sessions start with:**
- Treadmill Walk: 5 min, incline (warmup — always row 1 of every session)

**Lower A:**
1. TKE Band Warmup (2x20, band)
2. Barbell Squat (4 warmup sets: 45x10, 95x8, 135x6, 185x3 + 4 working sets at 225)
3. Romanian Deadlift (3 sets at 225)
4. Reverse Lunge, DB (2 sets, 10 each leg) — replaces RFESS due to chondromalacia patella
5. Step-Up, DB high box (2 sets, 10 each leg) — glute/ham emphasis
6. Standing Calf Raise ⟷ Adductors (3 sets each, SUPERSET to save time)
7. Seated Leg Curl (3 sets, anchor finish)

**Lower B:**
- Use the most recent Lower B session as the template. Key exercises: Barbell Squat (lighter), Glute Bridge, Leg Press, Single-Leg Curl, Walking Lunges, Seated Calf Raise
- If Glute Bridge machine is unavailable, note "Sub: barbell hip thrust" in Notes

**Upper A:**
- Use the most recent Upper A session as the template. Key exercises: Incline DB Press, Iso-lateral High Row, Wide Multi-Axis Press, Neutral-Grip Pulldown, Cable Lateral Raise, Bayesian Cable Curl, Triceps Pressdown (rope or v-bar, NOT overhead extension — elbow pain)

**Upper B:**
- Use the most recent Upper B session as the template. Key exercises: Neutral-Grip DB Bench, Cable Row, High-to-Low Cable Fly, Face Pull/Rear-Delt Fly, Hammer Strength Machine Curl (replaces EZ-Bar curl for elbow), Rope Pushdown (replaces overhead triceps extension for elbow)

### Injury Modifications (always apply)

- **Chondromalacia patella:** No leg extensions. No RFESS. Use reverse lunges or step-ups instead. Add TKE band warmup before lower days.
- **Elbow (medial epicondylitis):** No overhead triceps extensions. Use rope pushdowns or close-grip bench. Prefer hammer curls over supinated curls. If pain-free last session, keep them; otherwise swap to a neutral-grip alternative.

> **Customize:** Replace injury modifications and exercise selections with your own. The examples above illustrate the format.

---

### Progression Logic

There are two progression models depending on exercise type:

#### Compound Movements (Squat, RDL, Bench, Row, Lunge, Press)

Rep target per set: **12**. Progression cascades down from set 1.

**How it works:**
1. Find the most recent session where that exercise was **Completed** (not Skipped)
2. For each set, the target is **last reps + 1** — but only after the set ABOVE it has hit 12
3. Once set 1 hits 12, set 2 starts progressing. Once set 2 hits 12, set 3 starts. And so on.
4. **Load increase trigger:** When ALL working sets hit **12 reps** (e.g., 4x12 on squat, 3x12 on RDL), increase load and reset all sets to 8.

**Example cascade (Barbell Squat at 225):**
- Session 1: 10, 8, 7 → targets: 11, 8, 7 (only set 1 progresses)
- Session 2: 12, 8, 7 → targets: 12, 9, 7 (set 1 hit 12, now set 2 progresses)
- Session 3: 12, 9, 8 → targets: 12, 10, 8
- ...eventually: 12, 12, 12 → **LOAD UP to 235**, reset to 8, 8, 8

**Load increase increments:**
- Barbell compounds: +10 lb
- Dumbbells: +5 lb per DB (10 lb total)
- Cable/machine: +1 pin (~10-15 lb)

#### Heavy Isolation / Accessory Movements (Hammer Strength Machine Curl, Rear-Delt Fly Machine, Cable Fly, Triceps Pushdown, Single-Arm Cable Row)

Rep target per set: **15**. Same cascade logic as compounds.
- **Load increase trigger:** When ALL working sets hit **15 reps**, increase load and reset to 3x10

#### Light Isolation Movements (Cable Lateral Raise, Face Pulls, Calves, Adductors, Band Work)

Rep target per set: **20**. Same cascade logic as compounds.
- **Load increase trigger:** When ALL working sets hit **20 reps**, increase load and reset to 3x12

#### General Rules (all exercises)

1. Add to Notes column: `Last [date]: [reps]. Target: [target_reps]`
2. If a load increase was triggered, note in Notes: `LOAD UP from [old] to [new] (hit Nx[ceiling])`
3. If the exercise was modified last time (Modification != N/A), also populate Target Load with the unmodified load from the session before that

### Deload Logic

Every 5th week is a deload. During deload weeks:
- Set isDeloadWeek = YES
- Use 60% of normal working load
- Cap sets at 2 per exercise (drop the last set)
- Keep all exercises in rotation (don't skip movements)

### Steps

1. Read all data from the spreadsheet to find:
   - The last session date for each workout type
   - The last performance (load, reps, RIR) for each exercise
   - Any pain flags or modifications from recent sessions
   - Current week number to check for deload

2. Ask which days he plans to train this week (or default to 4 days based on calendar availability). **For each day, also ask if there's a time constraint** — e.g. "Any days where you have less time than usual?"

### Time-Compressed Session Logic

If a session has a shortened window, apply this compression based on available time:

| Available Time | Mode | What Changes |
|---------------|------|-------------|
| 60+ min | Full | Normal session, nothing cut |
| 45–59 min | Compressed | Drop 1 warm-up set on compounds, cut last accessory exercise |
| 30–44 min | Express | Keep compounds only + 1 superset. Drop all isolated accessories. Cut warm-up to 2 sets max. |
| <30 min | Minimum Effective Dose | Main compound only (1 exercise), 3 working sets, straight to it |

**Priority order when cutting (never cut these):**
1. Treadmill walk (5 min incline) — always kept, every session, even <30 min
2. Main compound lift (Squat, RDL, Incline Press, Row) — always kept, always progressed
2. Second compound or key superset
3. Accessories (cables, curls, raises) — cut first
4. Warm-up sets — reduce but never eliminate entirely

**When writing a compressed session:**
- Note in the workout B column: e.g. `Lower A (Express — 40 min)`
- Add to session Notes: `Time-compressed: [X] cut. Full session targets preserved — pick up accessories next session.`
- Progression targets stay the same — just fewer exercises, not lighter loads

3. Build the session rows for each planned workout day:
   - Date (always include year: M/D/YYYY format), exercise order, loads, rep targets, rest periods
   - Notes with last-session context
   - All dropdowns pre-filled (Status blank for logging, Skip Reason = N/A, Modification = N/A)
   - Volume formula: =E{row}*F{row}

4. Write all rows to the spreadsheet after the last existing row

5. Present a summary showing:
   - Which workouts are planned for which days
   - Key progression targets for the week
   - Any exercises flagged for pain in recent sessions
   - Whether it's a deload week

6. Ask for confirmation before finalizing.

7. Pull Garmin recovery data for recent workout dates:
```bash
python "~/garmin_recovery.py" --days 7
```
   - This pulls sleep score, HRV, resting HR, body battery, and stress for the last 7 days
   - Data writes to the Recovery tab; charts on Dashboard auto-update
   - If sleep score < 60 or body battery < 30, flag it: "Recovery is low — consider reducing volume or intensity today"
   - Garmin tokens are at `~/.garminconnect/` (auto-refresh, ~1 year validity)

8. After confirmation, refresh the Dashboard tab data:
   - Recalculate total volume per session and key lift progression tables
   - Write updated data to `Dashboard!A1` and `Dashboard!E1` (same format as existing)
   - Charts auto-update from the data ranges — no need to recreate them
   - Script reference: `~/workout_charts.py` (only needed if charts are deleted)
