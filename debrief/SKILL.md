---
name: debrief
description: Process an interview transcript and extract actionable intel
argument-hint: <company>
---

# Interview Debrief Skill

Process an interview transcript and extract actionable intel — what went well, what to sharpen, what you learned about the role and process, and what needs to happen next.

## Trigger

- `/debrief [company]`
- "debrief [company]"
- "process the [company] transcript"
- Share a Google Docs transcript link after an interview

---

## Instructions

### Step 1: Get the Transcript

If a Google Docs URL is provided, fetch it via Drive API:

```python
import sys, io, json
sys.stdout.reconfigure(encoding='utf-8')
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

token_path = '<YOUR_TOKEN_PATH>'  # e.g. ~/job-search/token.json
with open(token_path) as f:
    token_data = json.load(f)

creds = Credentials.from_authorized_user_info(token_data)
service = build('drive', 'v3', credentials=creds)

# Extract doc ID from URL: the part between /d/ and /edit
file_id = '<DOC_ID>'

request = service.files().export_media(fileId=file_id, mimeType='text/plain')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()
fh.seek(0)
print(fh.read().decode('utf-8-sig'))
```

If no URL provided, ask for it or check if a transcript is already in the conversation.

### Step 2: Analyze the Transcript

Extract and organize:

**Call Summary**
- Who was on the call (name, title, tenure)
- Interview type (phone screen, hiring manager, panel, final round)
- Estimated duration

**What Went Well**
- Questions where answers landed strongly
- Moments of rapport or genuine connection
- Stories or experiences that resonated

**Key Intel**
- Interview process details (stages, who's involved, timeline)
- Candidate pool info (how many, where you stand)
- Role details revealed during the call (scope, team size, reporting structure, budget)
- Culture signals — what the team is like, how they work
- Red flags or concerns surfaced (be honest)
- Hiring urgency and timeline

**What the Next Interviewer Will Probe**
- Explicit hints about what the next round will focus on
- Inferred probing areas based on what was and wasn't covered

**Action Items**
- Follow-up deadlines (when to expect to hear back)
- Items to prepare for next round
- People to research (next interviewers)
- Anything you committed to sending or doing

### Step 3: Present the Debrief

Present a clean summary using the structure above. Use bullets, not paragraphs. Be direct about both positives and areas to sharpen.

### Step 4: Update Systems

After presenting the debrief, update all of the following:

**a. Update job tracker:**
```bash
python sheets_tracker.py status "[Company]" "Interviewing" "[Stage completed]"
python sheets_tracker.py action "[Company]" "[Next action + deadline]"
```

**b. Save interview memory:**
Write or update a memory file (e.g. `[company]-interview-status.md`) with structured intel from the debrief. Store in your Claude Code memory directory.

**c. Update todos:**
Add follow-up items (e.g. "Follow up with [recruiter] if no word by [date]").

**d. Update weekly plan:**
Add a mid-week adjustment note to `weekly-plan.md` if this changes the week's priorities.

### Step 5: Prep Recommendations

Based on what was learned, recommend:
- Should the prep doc for the next round be updated? What specifically needs to change?
- Are there new stories that should be mapped to likely next-round questions?
- Any new research needed (interviewer profiles, product deep-dive, competitive landscape)?

---

## Constraints

- Use Drive API export (not Docs API) for fetching transcripts — Docs API requires separate enablement
- Be honest about weak moments in the transcript — real feedback only
- Don't fabricate intel that isn't in the transcript — if something is ambiguous, flag it
- Update ALL systems (tracker, memory, todos, weekly plan) — don't skip steps
- **Fact-check any new company intel** (revenue, headcount, product details, org changes) extracted from the transcript against public sources before writing to memory. Interviewers sometimes share approximate or outdated numbers. Cross-reference with the company website, press releases, or revenue databases before saving as fact. If unverifiable, label as "per [interviewer name], unverified."

## Anti-patterns

- Don't just summarize the transcript — extract actionable intel
- Don't skip system updates — that's half the value of running this
- Don't sugarcoat weak answers — flag them so they can be sharpened for next round
- Don't present a wall of text — use structured format with clear headers
- Don't write unverified interviewer claims to memory as fact — always cross-reference first
