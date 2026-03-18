# Interview Prep Skill

Build structured interview prep docs for upcoming interviews.

## Trigger

- "prep for [company] interview"
- "interview prep for [company]"
- "build prep doc for [company]"
- `/interview-prep [company]`

## Instructions

### Step 1: Gather Context

Ask for (or infer from conversation/tracker):
1. **Company** — name
2. **Role** — title, JD link or key details
3. **Interview type** — phone screen, hiring manager, panel, final round, take-home
4. **Interviewer(s)** — names, titles (if known)
5. **Date/time** — when is it?

If a JD exists in `temp/` or the tracker, pull it automatically. If a previous prep doc exists for this company (earlier round), read it and build on it — don't start from scratch.

### Step 2: Research

Use WebSearch and WebFetch to gather:
- Company overview (funding, revenue, headcount, product suite, recent news)
- Interviewer LinkedIn profiles (background, what they'll probe)
- Industry/market context relevant to the role
- Glassdoor/culture signals (flag red flags honestly)
- Competitor landscape

Read these files for candidate context:
- `PROFILE.md` — background, strengths, gaps
- `STORIES.md` — prepared STAR stories
- `BULLETS.md` — resume bullet variations

### Step 3: Build Full Prep Doc

Save to `temp/Interview Prep - [Company].md` (or `Phone Screen Prep - [Company].md` for screens).

Structure:

```
# [Interview Type] Prep: [Company]
## [Role Title]
## [Date] | [Duration] with [Interviewer(s)]

---

## INTERVIEWER: [NAME]
- Background, tenure, what they'll likely probe
- How to win them over

(Repeat for each interviewer)

---

## COMPANY OVERVIEW
- What, founded, funding, revenue, headcount
- Product suite (flag which product is relevant to the role)
- Recent timeline (key events, leadership changes)
- Culture signals (honest — flag red flags)

---

## THEY NEED / YOU HAVE
| They Need | You Have |
|-----------|----------|
(Map JD requirements to the candidate's specific experience. Be honest about gaps — mark as **GAP** with mitigation framing)

---

## [30/60]-SECOND PITCH
(Tailored to this audience and role. End with why this company specifically.)

---

## LIKELY QUESTIONS & ANSWERS
(8-12 questions with polished answers. Pull from STORIES.md where applicable.)

### Interview-type specific sections:

**For phone screens:** Keep answers concise. Screener is filtering, not evaluating depth.

**For hiring manager calls:** Go deeper on product thinking, trade-offs, prioritization, saying no. Include domain fluency lines.

**For panels:** Prep per-interviewer — different angles for each panelist.

**For final rounds:** Include strategic vision questions, "how would you approach the first 90 days", and executive-level framing.

---

## DOMAIN FLUENCY LINES
4-6 natural phrases to drop into conversation. Sound like insights from a thoughtful outsider, not facts recited.

---

## QUESTIONS TO ASK
(Tailored per interviewer. Show strategic depth, not generic.)

---

## DO'S AND DON'TS
(3-5 of each, specific to this interview)
```

### Step 4: Build Quick Reference

Save to `temp/Quick Ref - [Company].md`.

Rules:
- **3 pages max** with clean page breaks
- Page 1: Audience, pitch, through-line, key stats
- Page 2: Condensed key answers (most likely questions only, 2-3 sentences each)
- Page 3: Domain fluency lines + questions to ask
- Questions to ask must start on their own page — never split across pages
- Brain-fart safety net, not a script to read

### Step 5: Upload to Drive (optional)

If configured, offer to upload both docs to the company's Drive folder using your Drive upload script.

## Setup

Create three files in your project root before using this skill:

- **`PROFILE.md`** — Your background, target roles, strengths, known gaps
- **`STORIES.md`** — Prepared STAR stories with metrics (keep 8-12, cover the major themes)
- **`BULLETS.md`** — Resume bullet variations by focus area (AI/data, commercial, leadership, etc.)

These files are read automatically during prep. The richer they are, the better the output.

## Constraints

- Always read PROFILE.md, STORIES.md, and BULLETS.md before drafting
- Be honest about gaps — never fabricate experience
- Domain fluency lines should sound natural, not rehearsed
- Answers should use the candidate's actual stories and numbers, not generic PM advice
- If building on a previous round's prep doc, note what's new/changed for this round
- Bullets over paragraphs
- Keep the Full Prep Doc thorough but scannable
- Quick Reference must be printable and useful under pressure
- **Cite sources for every company metric** (revenue, retention, NDR, headcount, valuation, etc.). Include the URL or source name inline so the candidate can verify. If a number cannot be sourced, mark it as **[UNVERIFIED]** — do not present it as fact.
- **Never fabricate or hallucinate company numbers.** If a research agent returns a metric, verify it with a second source or web search before including it. If it can't be verified, either drop it or flag it clearly.

## Anti-patterns

- Don't parrot the job description back as answers
- Don't fabricate metrics or experience the candidate doesn't have
- Don't fabricate company metrics — if you can't find a source, say so
- Don't write generic "tell me about yourself" answers — always tailored to the audience
- Don't bury red flags — surface them so the candidate can prepare for tough questions
- Don't skip the "They Need / You Have" table — it's the backbone of prep
