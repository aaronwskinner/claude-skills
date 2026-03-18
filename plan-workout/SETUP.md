# Plan-Workout Skill — Setup Guide

---

## 1. Google Sheets Spreadsheet

Create a Google Sheet with a tab named `workout` and the following columns (A–P):

| Col | Field | Notes |
|-----|-------|-------|
| A | Date | M/D/YYYY format |
| B | Workout | e.g. `Upper A`, `Lower B (Express — 40 min)` |
| C | Exercise | Exercise name |
| D | Set# | Set number |
| E | Load | Weight in lbs (or kg) |
| F | Reps | Reps completed |
| G | RIR | Reps in Reserve (0-3) |
| H | Volume | Formula: `=E{row}*F{row}` |
| I | Pain Flag | 0–5 scale (0 = no pain) |
| J | Status | `Completed` / `Skipped` / blank |
| K | Skip Reason | Why the set was skipped (or N/A) |
| L | Rest (sec) | Rest period in seconds |
| M | Notes | Last session context, load-up flags |
| N | Modification | What was changed from standard (or N/A) |
| O | Target Load | Used when returning from a modified exercise |
| P | isDeloadWeek | `YES` or blank |

**Spreadsheet ID:** Found in the URL: `https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit`

Update `SKILL.md` with your spreadsheet ID.

---

## 2. Google Sheets API Auth

The skill reads and writes to your spreadsheet via the Google Sheets API.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable **Google Sheets API** and **Google Drive API**
3. Create OAuth 2.0 credentials → Download as `credentials.json`
4. Run your script once to generate `token.json` (handles the OAuth flow)

Update `SKILL.md` with the path to your `token.json`.

**Python library:** `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 3. Wearable Recovery Script

The skill pulls recovery data (sleep, HRV, body battery) after planning sessions. Adapt to your wearable:

**Garmin:** [`garminconnect`](https://github.com/cyberjunky/python-garminconnect) Python library
**Oura:** [Oura API v2](https://cloud.ouraring.com/v2/docs)
**Whoop:** [WHOOP API](https://developer.whoop.com/)

Expected CLI interface:
```bash
python garmin_recovery.py --days 7
```

Writes to a `Recovery` tab in the same spreadsheet with columns: Date, Sleep Score, HRV, Resting HR, Body Battery, Stress.

If you don't use a wearable, skip step 7 in the workflow — it's optional.

---

## 4. Customize Your Program

Edit `SKILL.md` to match your training program:

**Exercise templates:** Replace the Lower A / Lower B / Upper A / Upper B templates with your own exercises. The skill works with any split (PPL, full body, 3-day, etc.).

**Injury modifications:** Add your own permanent modifications to the Injury Modifications section.

**Working weights:** The example loads in Lower A (225 lb squat, etc.) are placeholders — the skill reads your actual working weights from the spreadsheet history.

**Rotation:** Change the rotation order if you use a different split (e.g., Push/Pull/Legs would be `Push → Pull → Legs`).

---

## 5. Dashboard Tab (Optional)

The skill can refresh a `Dashboard` tab with volume totals and progression charts. This requires a separate `workout_charts.py` script that writes summary data to `Dashboard!A1`.

If you don't have a Dashboard tab, skip step 8 in the workflow.
