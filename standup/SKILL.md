# Daily Standup Skill

Quick morning check-in. Review today's plan, confirm priorities, flag anything off-track.

## Commands

- `/standup` — Morning check-in, confirm today's plan

## Setup

This skill requires three custom scripts you build once and reuse daily. See `SETUP.md` for details.

| Script | Purpose |
|--------|---------|
| `health_data.py` | Pull recovery metrics from your wearable (Garmin, Oura, Whoop, etc.) |
| `standup_dashboard.py` | Build and serve an HTML dashboard from cached data |
| Trends data source | Web search (built into the skill — no script needed) |

Store a `standup-last-pull.md` file in your memory directory to track the last health data pull date.

---

## Your task

Run the daily morning standup. Keep it fast — 2-3 minutes.

**CRITICAL: Execute ALL steps below (1–5). Do not skip the dashboard, trends, or interactive review. Every step is required.**

### Step 1: Pull health/recovery data

Read your `standup-last-pull.md` memory file to get the last pull date.
Calculate how many days to pull (from last pull date to today, inclusive).
Use `--force` to refresh yesterday's data (wearables often update metrics after initial sync):

```bash
python ~/standup/health_data.py --days <N> --force
```

After a successful pull, update `standup-last-pull.md` with today's date.

### Step 2: Gather dashboard data and trends (do NOT open dashboard yet)

Fetch all data and save cache:

```bash
python ~/standup/standup_dashboard.py --save-cache
```

Then run web searches for today's trends across four categories:
- **Big Stories** — Top 2-3 major news headlines
- **AI & Product** — AI industry moves, model releases, product strategy news
- **Pipeline Intel** — News about companies you're tracking (job search, clients, competitors)
- **Hot Take** — One spicy/contrarian observation connecting the above

After synthesizing, save as structured JSON:

```bash
# Write to ~/temp/standup_trends.json
```

```json
{
  "sections": [
    {
      "title": "Big Stories",
      "items": [
        {"text": "Headline or summary", "url": "https://source-url.com"}
      ]
    },
    {
      "title": "AI & Product",
      "items": [...]
    },
    {
      "title": "Pipeline Intel",
      "items": [...]
    },
    {
      "title": "Hot Take",
      "items": [...]
    }
  ]
}
```

> **Verification rule:** Pipeline Intel items must be WebFetch-verified against the source URL before presenting as fact. Real URL + invented detail is a common hallucination pattern. Label unverified claims explicitly.

Inject trends into dashboard:

```bash
python ~/standup/standup_dashboard.py --inject-trends
```

The dashboard HTML is now ready — but stay in Claude Code for the interactive review first.

### Step 3: Interactive review

Facilitate the standup conversation using the data gathered in Step 2:

1. **Habits check:** Ask which habits are done. Check off completed items in your daily habits memory file.

2. **Email triage:** Based on the email panel, call out any emails needing urgent action — replies, deadlines, key updates.

3. **Alerts:** Flag any issues:
   - No tasks for today (suggest creating some)
   - Tasks don't align with top priorities
   - Overloaded schedule
   - Low recovery metrics

4. Ask: **"Anything change? Need to adjust today's plan?"**

5. If adjustments needed:
   - Update your weekly plan memory file
   - Add a note under "Mid-Week Adjustments" with today's date and reason
   - Offer to create/move calendar blocks using your calendar script

### Step 4: Confirm priorities

End with: **"Your top 3 for today:"** followed by the force-ranked list.

Wait for user confirmation before proceeding to Step 5.

### Step 5: Open dashboard (AFTER user confirms)

Only after the user confirms priorities, open the completed dashboard:

```bash
# macOS
open ~/temp/standup_dashboard.html

# Windows
start "" "C:/path/to/temp/standup_dashboard.html"

# Linux
xdg-open ~/temp/standup_dashboard.html
```

The user sees the full dashboard — recovery, calendar, email, priorities, tasks, AND trends with links — as the final send-off.
