---
name: plan-workout
description: Plan the coming week's workout sessions — pull last performance, set targets, write to spreadsheet
---

# Workout Planning Skill

Pre-populate the coming week's workout sessions in a Google Sheets tracking spreadsheet. Reads last performance for each exercise, applies micro-progression logic, handles deload weeks, and accounts for time constraints.

## Commands

- `/plan-workout` — Plan sessions for the week ahead

## Setup

See `SETUP.md` for how to configure your spreadsheet and scripts.

---

## Your task

Plan and pre-populate workout sessions for the coming week.

**Spreadsheet ID:** `<YOUR_SPREADSHEET_ID>`
**Credentials:** `<YOUR_TOKEN_PATH>`
**Sheet:** `workout`

### Column Structure (16 columns, A–P)

A=Date, B=Workout, C=Exercise, D=Set#, E=Load, F=Reps, G=RIR, H=Volume (=E*F), I=Pain Flag (0-5), J=Status, K=Skip Reason, L=Rest(sec), M=Notes, N=Modification, O=Target Load, P=isDeloadWeek

---

### Workout Rotation

4-day Upper/Lower split. Rotation order: **Upper A → Lower A → Upper B → Lower B**. Assign to available gym days in the coming week (typically 4 days, skip rest days).

---

### Exercise Templates

**All sessions start with:**
- Treadmill Walk: 5 min, incline (warmup — always row 1 of every session)

**Lower A:**
1. TKE Band Warmup (2x20, band)
2. Barbell Squat (4 warmup sets: 45x10, 95x8, 135x6, 185x3 + 4 working sets — replace 225 with your working weight)
3. Romanian Deadlift (3 sets — replace 225 with your working weight)
4. Reverse Lunge, DB (2 sets, 10 each leg)
5. Step-Up, DB high box (2 sets, 10 each leg) — glute/ham emphasis
6. Standing Calf Raise ⟷ Adductors (3 sets each, SUPERSET to save time)
7. Seated Leg Curl (3 sets, anchor finish)

**Lower B:**
- Use the most recent Lower B session as the template. Key exercises: Barbell Squat (lighter), Glute Bridge, Leg Press, Single-Leg Curl, Walking Lunges, Seated Calf Raise
- If Glute Bridge machine is unavailable, note "Sub: barbell hip thrust" in Notes

**Upper A:**
- Use the most recent Upper A session as the template. Key exercises: Incline DB Press, Iso-lateral High Row, Wide Multi-Axis Press, Neutral-Grip Pulldown, Cable Lateral Raise, Bayesian Cable Curl, Triceps Pressdown

**Upper B:**
- Use the most recent Upper B session as the template. Key exercises: Neutral-Grip DB Bench, Cable Row, High-to-Low Cable Fly, Face Pull/Rear-Delt Fly, Hammer Curl, Rope Pushdown

> **Customize:** Replace exercise selections with your own rotation. The skill works with any split — PPL, full body, 3-day, etc. Update the templates to match your program.

---

### Injury Modifications

Add any permanent modifications here. These are applied automatically every session without being asked.

**Example format:**
- **[Condition]:** No [exercise]. Substitute [alternative]. Add [prehab] before [session type].

**Example entries:**
- **Chondromalacia patella:** No leg extensions. No RFESS. Use reverse lunges or step-ups instead. Add TKE band warmup before lower days.
- **Medial epicondylitis (elbow):** No overhead triceps extensions. Use rope pushdowns or close-grip bench. Prefer hammer curls over supinated curls.

---

### Progression Logic

For each exercise in the planned session:
1. Find the most recent session where that exercise was **Completed** (not Skipped)
2. Set the rep target to **last reps + 1** on each set (micro-progression)
3. **Load increase trigger:** When ALL working sets hit **12 reps** (i.e., 3x12 achieved), increase load by the smallest available increment and reset rep targets to 8:
   - Dumbbells: +5 lb per DB (10 lb total)
   - Barbell compounds: +10 lb
   - Cable/machine: +1 pin (~10-15 lb)
   - Example: Seated Leg Curl hits 130x12, 130x12, 130x12 → next session: 140x8, 140x8, 140x8
4. Add to Notes column: `Last [date]: [reps]. Target: [target_reps]`
5. If a load increase was triggered, note in Notes: `LOAD UP from [old] to [new] (hit 3x12)`
6. If the exercise was modified last time (Modification != N/A), also populate Target Load with the unmodified load from the session before that

---

### Deload Logic

Every 5th week is a deload. During deload weeks:
- Set isDeloadWeek = YES
- Use 60% of normal working load
- Cap sets at 2 per exercise (drop the last set)
- Keep all exercises in rotation (don't skip movements)

---

### Time-Compressed Session Logic

When a session has a shortened window, compress it based on available time:

| Available Time | Mode | What Changes |
|---------------|------|-------------|
| 60+ min | Full | Normal session, nothing cut |
| 45–59 min | Compressed | Drop 1 warm-up set on compounds, cut last accessory exercise |
| 30–44 min | Express | Keep compounds only + 1 superset. Drop all isolated accessories. Cut warm-up to 2 sets max. |
| <30 min | Minimum Effective Dose | Main compound only (1 exercise), 3 working sets, straight to it |

**Priority order when cutting (never cut these):**
1. Treadmill walk (5 min incline) — always kept, every session, even <30 min
2. Main compound lift — always kept, always progressed
3. Second compound or key superset
4. Accessories (cables, curls, raises) — cut first
5. Warm-up sets — reduce but never eliminate entirely

**When writing a compressed session:**
- Note in the Workout column: e.g. `Lower A (Express — 40 min)`
- Add to Notes: `Time-compressed: [X] cut. Full session targets preserved — pick up accessories next session.`
- Progression targets stay the same — fewer exercises, not lighter loads

---

### Steps

1. Read all data from the spreadsheet to find:
   - The last session date for each workout type
   - The last performance (load, reps, RIR) for each exercise
   - Any pain flags or modifications from recent sessions
   - Current week number to check for deload

2. Ask which days the user plans to train this week (or default to 4 days based on calendar availability). **For each day, also ask if there's a time constraint** — e.g. "Any days where you have less time than usual?"

3. Build the session rows for each planned workout day:
   - Date (always include year: M/D/YYYY format), exercise order, loads, rep targets, rest periods
   - Notes with last-session context
   - All dropdowns pre-filled (Status blank for logging, Skip Reason = N/A, Modification = N/A)
   - Volume formula: `=E{row}*F{row}`
   - Apply time-compression logic if a session has a shortened window

4. Write all rows to the spreadsheet after the last existing row

5. Present a summary showing:
   - Which workouts are planned for which days
   - Key progression targets for the week
   - Any exercises flagged for pain in recent sessions
   - Whether it's a deload week
   - Which sessions (if any) are time-compressed and what was cut

6. Ask for confirmation before finalizing.

7. Pull wearable recovery data for recent workout dates:
   ```bash
   python ~/garmin_recovery.py --days 7
   ```
   - Pulls sleep score, HRV, resting HR, body battery, stress for the last 7 days
   - Data writes to the Recovery tab; charts on Dashboard auto-update
   - If sleep score < 60 or body battery < 30, flag it: "Recovery is low — consider reducing volume or intensity"
   - Adapt this script to your wearable (Oura, Whoop, etc.) — see `SETUP.md`

8. After confirmation, refresh the Dashboard tab:
   - Recalculate total volume per session and key lift progression tables
   - Charts auto-update from data ranges
