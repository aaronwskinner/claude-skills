# Standup Skill — Setup Guide

This skill orchestrates a daily standup check-in by pulling health data, building a dashboard, gathering news trends, and facilitating an interactive priority review. You need to build or adapt three components.

---

## 1. Health Data Script (`health_data.py`)

Pulls recovery metrics from your wearable and writes them to a Google Sheet or local store.

**Expected CLI interface:**
```bash
python health_data.py --days <N> --force
```

**Metrics to pull (adapt to your wearable):**

| Metric | Garmin | Oura | Whoop |
|--------|--------|------|-------|
| Sleep score | ✓ | ✓ | ✓ |
| Body battery / readiness | ✓ | ✓ | ✓ |
| HRV | ✓ | ✓ | ✓ |
| Resting HR | ✓ | ✓ | ✓ |
| Sleep duration | ✓ | ✓ | ✓ |
| Steps | ✓ | — | — |
| Stress score | ✓ | — | — |

**Libraries:**
- Garmin: [`garminconnect`](https://github.com/cyberjunky/python-garminconnect)
- Oura: [Oura API v2](https://cloud.ouraring.com/v2/docs)
- Whoop: [WHOOP API](https://developer.whoop.com/)

---

## 2. Dashboard Script (`standup_dashboard.py`)

Builds an HTML dashboard from your data and injects the trends JSON.

**Expected CLI interface:**
```bash
python standup_dashboard.py --save-cache     # Pull and cache all panel data
python standup_dashboard.py --inject-trends  # Inject standup_trends.json into HTML
```

**Dashboard panels to build:**

- **Recovery** — today's health metrics from your wearable
- **Calendar** — today's events (Google Calendar API or similar)
- **Email** — unread counts + top items (Gmail API or similar)
- **Priorities** — pulled from your weekly plan memory file
- **Today's Tasks** — pulled from your weekly plan memory file
- **Trends** — injected from `standup_trends.json`

The dashboard is a single HTML file written to a temp directory and opened in the browser at the end of standup.

---

## 3. Memory Files

The skill reads and writes a few markdown memory files. Create these in your Claude Code memory directory (`~/.claude/projects/<project>/memory/`):

| File | Purpose |
|------|---------|
| `standup-last-pull.md` | Tracks last health data pull date |
| `daily-habits.md` | Morning checklist (vitamins, exercise, etc.) |
| `weekly-plan.md` | Current week priorities + daily tasks |

**`standup-last-pull.md` format:**
```markdown
Last pull: 2026-01-01
```

**`daily-habits.md` format:**
```markdown
# Daily Habits Checklist

## Morning
- [ ] Habit one
- [ ] Habit two
```

**`weekly-plan.md` format:**
```markdown
# Weekly Plan: [Date Range]

## Priorities (Force Ranked)
1. P1: ...
2. P2: ...

## Daily Plan

### [Day] [Date]
- [ ] Task (P1)
- [ ] Task (P2)
```

---

## 4. Temp Directory

The skill writes intermediate files to a temp directory. Create it:

```bash
mkdir -p ~/temp
```

Files written there:
- `standup_trends.json` — trends data (written by Claude, injected by dashboard script)
- `standup_dashboard.html` — final dashboard (written by dashboard script)
- `standup_cache.json` — cached panel data (written by dashboard script)
