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

**Structure:**

```markdown
# Resume Bullets by Focus Area

## [Company Name] — Bullet 1

**Default:**
[Your base bullet]

**[Focus Area A] variation:** (e.g., Data / Analytics)
[Rewritten bullet emphasizing data angle]

**[Focus Area B] variation:** (e.g., Enterprise / B2B)
[Rewritten bullet emphasizing enterprise angle]

**[Focus Area C] variation:** (e.g., AI / ML)
[Rewritten bullet emphasizing AI angle]

---

## [Company Name] — Bullet 2
...
```

**Tips:**
- Write 3-4 variations per bullet, one per role focus you commonly target
- Each variation should be substantively different, not just a word swap
- Include metrics in every variation — they're non-negotiable
- If a new application doesn't fit any variation, write one and add it here

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
