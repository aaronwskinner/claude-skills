# Apply-Job Skill — Setup Guide

This skill requires three context files you maintain once and reuse for every application, plus optional scripts for tracking and Drive integration.

---

## 1. Required Context Files

Create these in your project root (the directory where you run Claude Code for job searching).

### `PROFILE.md`

Your background, target roles, strengths, and known gaps. Claude reads this before every application to understand how to position you.

```markdown
# Candidate Profile

## Background
[X]+ years [domain] product management. [Degree], [School].
Based in [City]. Open to [remote/hybrid/onsite].

## Target Roles
- [Role type 1] (e.g., Senior Director, Product Management)
- [Role type 2]

## Strengths
- [Strength 1 with evidence]
- [Strength 2 with evidence]

## Known Gaps
- [Gap 1] — mitigation: [how you handle this in interviews]
- [Gap 2] — mitigation: [how you handle this]

## Quick Stats
- [Key metric 1] (e.g., "Led teams of 7-8 engineers")
- [Key metric 2] (e.g., "400% adoption growth")
- [Key metric 3] (e.g., "$1M annual savings")
```

---

### `BULLETS.md`

Pre-written resume bullet variations organized by role focus. This is the most important file — it's what makes tailoring fast and consistent without overfitting.

The core idea: **write each bullet 3-4 times, once per role type you target.** When applying to a job, Claude picks the closest variation rather than rewriting from scratch. This prevents keyword stuffing while still optimizing for the role.

#### How to Build It

**Step 1: List your high-impact bullets**

For each job on your resume, identify the 1-2 bullets with the strongest metrics. These are the ones worth writing variations for. Not every bullet needs variations — focus on the ones that move the needle.

**Step 2: Identify your 3-4 target role types**

Common examples:
- Data / Analytics
- Enterprise / B2B SaaS
- AI / ML / Automation
- Consumer / Growth
- API / Integrations / Platform

**Step 3: Rewrite each bullet through each lens**

Keep the metric the same. Change what you emphasize — the *type* of work, the *technology*, the *audience*, or the *outcome framing*.

#### Worked Example

```markdown
# Resume Bullets by Focus Area

## Title Line

| Focus | Title |
|-------|-------|
| **Data / Analytics** | Senior Product Manager – B2B Data Products & Analytics |
| **Enterprise / Platform** | Senior Product Manager – Enterprise Platforms & Multi-Product Systems |
| **AI / ML** | Senior Product Manager – AI Platforms & Autonomous Systems |
| **API / Integrations** | Principal Product Manager – API-First Platforms & Integrations |

---

## Summary

### Data / Analytics
> Senior Product Manager with 10+ years building B2B data products in SaaS.
> I've owned measurement and analytics systems end-to-end — shipping API-driven
> architectures and driving adoption through data transparency. Strong track record
> translating complex data into actionable customer insights.

### Enterprise / Platform
> Senior Product Manager with 10+ years building enterprise-grade platforms across
> SaaS. I've owned multi-module product lines end-to-end — defining roadmaps,
> shipping API-first architectures, and driving adoption with enterprise customers.

---

## Acme Corp — Bullet 1

**Default:**
Built a reporting platform serving 500+ enterprise clients, reducing time-to-insight
from 3 days to 4 hours and increasing client retention by 22%.

**Data / Analytics variation:**
Built a self-serve analytics platform that gave 500+ enterprise clients real-time
access to performance data, cutting reporting lag from 3 days to 4 hours and
improving retention 22%.

**Enterprise / Platform variation:**
Owned a multi-tenant reporting platform for 500+ enterprise accounts, reducing
time-to-insight from 3 days to 4 hours — cited as top retention driver in NPS surveys.

**AI / ML variation:**
Shipped an ML-powered anomaly detection layer on top of an enterprise reporting
platform, surfacing actionable alerts that reduced client churn 22% over 12 months.

---

## Acme Corp — Bullet 2
...
```

**Tips:**
- Write 3-4 variations per bullet, one per role focus you commonly target
- Each variation should be substantively different, not just a word swap — change what you emphasize, not just the adjectives
- Include the same core metric in every variation — metrics are non-negotiable
- If a new application doesn't fit any existing variation, write one and add it here — BULLETS.md grows over time
- A keyword-stuffed resume reads worse than a clean one — resist the urge to cram in JD language

---

### `CONTEXT.md`

Your scripts, tracker commands, and workflow preferences.

```markdown
# Job Search Context

## Tracker Commands
\`\`\`bash
python sheets_tracker.py list
python sheets_tracker.py add "Company" "Role" "url" P1 High
python sheets_tracker.py apply "Company"
python sheets_tracker.py status "Company" "Interviewing" "Phone Screen"
\`\`\`

## Resume Base Files
- `base/resume_ats_base.docx` — ATS-optimized, use for Workday applications
- `base/resume_[focus_a].docx` — [Focus A] variant
- `base/resume_[focus_b].docx` — [Focus B] variant

## Drive Structure
Jobs are organized in Drive as: `jobSearch[Year]/[Company] - [Role]/`

## Naming Convention
- Resume: `[LastName,FirstName]_[Company]_resume_[Year][Mon].docx`
- Cover Letter: `Cover Letter - [Company].docx`
- Fit Analysis: `Fit Analysis - [Company].txt`
```

---

## 2. Optional Scripts

These scripts make the workflow faster but aren't required. Build them in Python or adapt to your preferred tools.

### `sheets_tracker.py`

CLI for a Google Sheets job tracker. Commands: `add`, `list`, `apply`, `status`, `action`.

Uses Google Sheets API + a spreadsheet with columns: Company, Role, URL, Status, Stage, Priority, Fit, Notes, Applied Date.

**Auth:** Google OAuth2 via `credentials.json` + `token.json` (see [Google Sheets API quickstart](https://developers.google.com/sheets/api/quickstart/python)).

### `upload_to_drive.py`

Uploads a file to a specific Google Drive folder and optionally converts to Google Doc format.

```python
# Example usage
python upload_to_drive.py "path/to/file.docx" --folder-id "DRIVE_FOLDER_ID" --convert
```

### `read_docx.py`

Extracts plain text from a `.docx` file so Claude can read resume content without downloading from Drive.

```python
# Example usage
python read_docx.py "path/to/resume.docx"
```

---

## 3. Resume Base File

Create an ATS-optimized base resume in `.docx` format:
- Use standard heading styles (Heading 1, Heading 2) — required for Workday parsing
- Use MM/YYYY date format
- No tables, text boxes, or columns — ATS systems can't read them
- Save as `base/resume_ats_base.docx`

The skill tailors from this base for each application by swapping in bullet variations from `BULLETS.md`.
