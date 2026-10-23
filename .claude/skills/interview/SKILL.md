---
name: interview
description: "Record and prepare for job interviews. Ingests an interview summary (e.g. Read AI, Otter, Fireflies, the user's notes, or a recruiter email) into the job folder's interview-process.md, keeps the Stage, facts.md and research.md in sync, and builds prep notes for the next stage: likely questions with answer outlines, matching stories from interview-stories.md, gaps, questions to ask, salary notes. Use when the user shares an interview summary, schedules an interview, or asks to prepare for one."
metadata:
  version: 1.0.0
---

# /interview Skill

```
/interview <folder>            # then paste the summary, or say "prep" for the next stage
/interview <folder> prep       # build prep notes for the next stage
```

`<folder>` is the job's folder name under `jobs/`. If none is given, match the company named in the summary to a folder (ask if it's ambiguous).

## A. Recording an interview (a summary was shared)

1. **`jobs/<folder>/interview-process.md`** (create it from `interview-process-template.md` in this skill's folder if missing):
   - header: `**Current stage:**` one line on where things stand and what's awaited (the tracker shows it);
   - the **stage table** (#, stage, with, date, status): mark this stage done, and add the later stages the interviewer described;
   - a dated **section for this stage**: who, the source, a summary in plain bullets, **action items** as checkboxes (the user's and theirs), and **notes for the next stages**.
2. **Stage line:** `**Stage:** interviewing` in `forms.md` (keep `**Applied:**`); `offer`, `rejected` or `withdrawn` when the summary says so.
3. **`facts.md` Section 2:** add every claim the user made about their experience, especially numbers, team sizes, tools and anything **not** already in the CVs, `profile.json` or `my_profile.md`. Mark "In CVs/profile?" honestly. Flag contradictions with Section 1 or `profile.json` in chat; don't silently fix them.
4. **`research.md`:** new facts about the company (product, team, process, pay structure, the client for agency roles).
5. **`interview-stories.md`:** if a story was told with new details, update it; add a new story if one was told that isn't there (mark gaps **[fill in]**).
6. Rebuild the tracker: `python3 .claude/skills/status/scripts/build_tracker.py`.
7. Report: what was recorded, the action items, and anything said that isn't backed by the user's files.

## B. Preparing for the next stage (`prep`)

Add a `## Prep: <stage name> (<date>)` section to `interview-process.md`:

1. **Format:** who's interviewing, length, technical or not. If unknown, ask the user and draft a short email to the recruiter asking.
2. **Likely questions (8–12)** from the job description, `research.md` and the stage type (screening, technical, live coding, system design, behavioural, culture). For each, a 2–4 line answer outline in the user's voice, grounded in `facts.md` Section 1, `my_profile.md` and the stories. For system design, one or two designs close to the company's product, with the key trade-offs. For live coding, the language/framework they're likely to use and a warm-up exercise.
3. **Stories to have ready:** 3–5 from `interview-stories.md`, each with the question it answers. Point out **[fill in]** gaps worth closing first.
4. **Consistency check:** everything in `facts.md` Section 2 for this company, so earlier claims are repeated the same way.
5. **Gaps and how to handle them:** must-haves the user lacks, each with an honest one-line answer (adjacent experience + how they'd close it).
6. **Questions to ask them (5–7):** specific to the company, team and stage.
7. **Salary and terms:** what was already said, the salary rule's figure (`/apply` Step 6), and anything to clarify (base/bonus/equity split, contract type, benefits).

Keep it skimmable. No invented experience: if an answer needs a detail that isn't recorded, write **[fill in]**, and offer `/onboard-me stories` to capture it for good.

## Rules

- Never send emails or messages; draft them in chat.
- Every new claim goes into `facts.md`, so the next stage, CV or form stays consistent.
