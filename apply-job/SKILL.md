---
name: apply-job
description: Apply to a job posting - fetches description, creates folder, tailors resume and cover letter, tracks application
argument-hint: <job-url>
---

# Job Application Workflow

Help apply to a job posting at: $ARGUMENTS

## Setup

Before using this skill, create these files in your project root. See `SETUP.md` for templates and guidance.

| File | Purpose |
|------|---------|
| `PROFILE.md` | Your background, strengths, gaps, target roles |
| `BULLETS.md` | Pre-written resume bullet variations by role focus |
| `CONTEXT.md` | Your scripts, tracker commands, workflow preferences |

---

## Workflow Steps

### 1. Fetch Job Description

Use WebFetch to extract the full job posting.

**If WebFetch fails** (JavaScript-rendered page, empty content): use Playwright MCP as fallback:
1. `browser_navigate` to the job URL
2. `browser_snapshot` to get full page content
3. Extract the JD from the snapshot

Identify: company name, role title, responsibilities, requirements, preferred qualifications.

### 2. Add to Tracker & Create Folder

```bash
python <YOUR_PROJECT_DIR>/sheets_tracker.py add "Company" "Role" "job-url" P1 High
```

Adapt this command to your tracker (Google Sheets, Notion, Airtable, etc.). See `CONTEXT.md` for your tracker commands.

### 3. Save Job Description

Save the full job description to a text file and upload to the job's folder.

### 4. Analyze Fit

Create a two-column fit analysis mapping their requirements to your experience:

```
REQUIREMENT                              YOUR EXPERIENCE
─────────────────────────────────────────────────────────────────────────────────
5+ years product management              [Your experience + metrics]

Cross-functional leadership              [Your experience + metrics]
─────────────────────────────────────────────────────────────────────────────────
GAPS: [List any significant gaps honestly]
```

Include specific metrics where possible. After analysis, identify:
- Which base resume is closest to this role's focus
- Any significant gaps to flag

Save as `Fit Analysis - Company.txt` and upload to the job's folder.

### 5. Tailor Resume

**Start from your ATS-optimized base resume** (Workday-friendly, proper heading styles).

**MANDATORY: Read BULLETS.md and swap in the right variations.**

Step-by-step:
1. Identify the role's focus (e.g., Data, API, Enterprise, AI/ML, Consumer, etc.)
2. Read BULLETS.md and find the matching variation for each section
3. Swap in the closest variation — do NOT leave bullets as the base version if a better variation exists
4. If no variation fits, write new language and add it to BULLETS.md for future use

**Only three things change per application: title, summary, and bullets.** Everything else is frozen.

**Avoid Overfitting:**
- DO swap in the right bullet variations from BULLETS.md
- DO adjust title and summary to match role focus
- DON'T rewrite bullets to parrot the job description verbatim
- DON'T invent accomplishments or metrics
- DON'T make it sound like a keyword dump
- KEEP your authentic voice

Keep EXACTLY as-is:
- All job titles and dates
- Company names
- Education, certifications, skills sections
- Overall structure and formatting

### 6. Write Cover Letter

Style: Direct, no fluff, ~250 words max. Format: `.docx`.

#### Cover Letter Strategy

The goal is **problem-solution** framing: identify what the company needs, position yourself as the answer.

**Before writing, research the company (5-10 min):**
- Search for recent news: product launches, funding rounds, partnerships, blog posts
- Check LinkedIn for the hiring manager's name and recent posts
- Look for team blog posts, conference talks, or product announcements
- Find ONE specific detail to reference in the closing

#### Structure

1. Date
2. Company name and department
3. RE: line with role title and job ID (address hiring manager by name if found)
4. **Opening hook** — Don't just state "I'm applying." Lead with the most compelling match between your experience and their core need. One sentence that makes them want to keep reading.
5. **Problem-solution body** — 2-3 sentences connecting your specific results to what they're trying to solve. Use metrics. Frame it as "you need X, I've done X."
6. **"What drew me to this role:"** with 2-3 bulleted points (bold label + description). Show genuine understanding of the company/product, not generic skills.
7. **Company-specific research line** — One sentence referencing something specific you found (a recent product launch, blog post, funding round). Example: *"I noticed your team recently launched [X] — it reinforced why this role felt worth applying for."* This single line signals real research and dramatically increases response rates.
8. **Confident closing** — Not "I'd welcome the opportunity" (flat). Use forward momentum: *"I'd love to walk you through how I'd approach [specific challenge]."*
9. "Sincerely," and name

#### Tone Guidelines

- Write like a peer, not a supplicant
- Lead with outcomes, not responsibilities
- Show you understand their product/market, not just the job description
- Every sentence should earn its place — cut anything generic
- Do not use em dashes

**Formatting specs:**
- Calibri 11pt, 1" margins
- No header — start with date
- Bullets: bold label + " – " + description
- 12pt spacing after paragraphs, 4pt after bullets

### 7. Upload to Drive

Upload:
- `Fit Analysis - Company.txt`
- `[LastName,FirstName]_[Company]_resume_[Year][Month].docx`
- `Cover Letter - Company.docx`

### 8. Present for Review

Show the candidate:
- **Full change log** with FROM/TO for each resume edit (format below)
- The cover letter text for review
- Reminder to mark as applied in the tracker after submitting

**Change Log Format (REQUIRED):**

```
## Resume Changes

**Title**
- FROM: "...previous focus area"
- TO: "...new focus area"

**Summary**
- FROM: "...previous framing..."
- TO: "...new framing..."
(show only changed phrases, not full paragraphs)

**[Company] Bullet [#]**
- FROM: "...previous bullet..."
- TO: "...new bullet..."
```

This keeps reviews concise while still catching overfitting.

### 9. Workday Detection

If the job URL contains `myworkdayjobs.com` or `wd1.myworkdayjobs`, prompt:

> "This is a Workday application. When you're ready to fill it out, navigate to the application and run `/workday-apply [Company]` — it'll handle work experience and standard questions via browser automation."

---

## Key Scripts

These scripts power the workflow. See `SETUP.md` for how to build or adapt them.

| Script | Purpose |
|--------|---------|
| `sheets_tracker.py` | Add jobs, mark applied, update status |
| `upload_to_drive.py` | Upload files to Drive folders |
| `read_docx.py` | Extract text from Word docs |

---

## Anti-Patterns

- Don't parrot the job description back as resume bullets
- Don't fabricate metrics or experience you don't have
- Don't write generic "tell me about yourself" cover letters
- Don't skip the fit analysis — it's the backbone of the tailoring decision
- Don't over-tailor — a keyword-stuffed resume reads worse than a clean one
