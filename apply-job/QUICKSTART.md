# Apply-Job Skill — Quickstart

Get set up in ~30 minutes. Claude helps you build the context files — you don't have to write them from scratch.

---

## Step 1: Install the skill

```bash
# Clone the repo
git clone https://github.com/aaronwskinner/claude-skills.git

# Copy the skill into your job search project
cp -r claude-skills/apply-job your-job-search/.claude/skills/apply-job

# Or install globally (available in all projects)
cp -r claude-skills/apply-job ~/.claude/skills/apply-job
```

---

## Step 2: Create your project directory

```bash
mkdir job-search
cd job-search
mkdir base temp
```

Your structure will look like:

```
job-search/
├── .claude/skills/apply-job/   ← the skill
├── base/                        ← your resume base file(s)
├── temp/                        ← working files per application
├── PROFILE.md                   ← your background (you'll create this)
├── BULLETS.md                   ← resume variations (you'll create this)
└── CONTEXT.md                   ← your scripts/commands (you'll create this)
```

---

## Step 3: Build your context files with Claude

Open Claude Code in your `job-search/` directory and run these prompts one at a time. Claude will interview you and generate the files.

### Build PROFILE.md

```
Help me create a PROFILE.md file for my job search. Ask me about my background,
target roles, years of experience, key metrics, strengths, and any gaps I'm
aware of. Then generate the file.
```

### Build BULLETS.md

```
Help me create a BULLETS.md file. I'll paste my current resume below.
For each bullet with strong metrics, help me write 3-4 variations targeting
different role types: [list your target role types, e.g. Data, Enterprise, AI/ML].
Keep the same core metrics in every variation — only change the emphasis.

[paste your resume here]
```

> **Tip:** Start with 2-3 jobs and your highest-impact bullets. You can expand BULLETS.md over time as you apply to more roles.

### Build CONTEXT.md

```
Help me create a CONTEXT.md file. I'll use [Google Sheets / Notion / Airtable]
as my job tracker. My resume files will live in base/ and follow the naming
convention [LastName,FirstName]_Company_resume_2026Mon.docx
```

---

## Step 4: Add your base resume

Save an ATS-optimized version of your resume as `base/resume_ats_base.docx`.

ATS requirements:
- Use standard heading styles (Heading 1, Heading 2) — required for Workday
- MM/YYYY date format
- No tables, text boxes, or columns
- Single-column layout

---

## Step 5: Test the skill

```
/apply-job https://jobs.example.com/some-role
```

Claude will fetch the JD, run the fit analysis, tailor your resume, and draft a cover letter.

---

## Step 6: Optional — add tracker and Drive scripts

See `SETUP.md` for how to build `sheets_tracker.py` and `upload_to_drive.py`. These automate the tracking and file management steps but aren't required to use the skill.

---

## Troubleshooting

**"Claude can't read my resume"**
Make sure your base resume is `.docx` format, not `.pdf`. If you have `read_docx.py` set up, Claude can extract the text directly. Otherwise, paste your resume text into the conversation.

**"The JD page didn't load"**
Some job sites (Greenhouse, Lever, Workday) render via JavaScript. Install [Playwright MCP](https://github.com/microsoft/playwright-mcp) and Claude will use it as a fallback automatically.

**"The bullet variations don't feel right"**
The first version of BULLETS.md is rarely perfect. After each application, note what variation you used and add it to the file. It gets better with every application.
