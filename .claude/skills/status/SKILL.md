---
name: status
description: "Show where every job application stands. Rebuilds applications.md from each jobs/*/forms.md Stage line, lists what needs the user's attention (forms awaiting review, blocked applications, interviews, follow-ups due, applications gone cold), drafts follow-ups, and updates a Stage when told an application moved on. Use when asked for status, pipeline, tracker, follow-ups, or to mark an application submitted/rejected/interviewing/closed."
metadata:
  version: 1.0.0
---

# /status Skill

```
/status                                  # rebuild the tracker and report
/status <folder> <stage> [note]          # e.g. /status acme-senior-backend-engineer rejected "email 2026-11-02"
```

## The Stage line

Every `jobs/<folder>/forms.md` has one machine-readable line in its header:

```
**Stage:** submitted · **Applied:** 2026-10-14
```

| Stage | Meaning |
|---|---|
| `drafted` | `forms.md` written, form not filled |
| `filled` | Form filled in Chrome, waiting for "yes, submit" |
| `blocked` | Claude can't send it (sign-in wall, location block…); `**Status:**` says why |
| `unknown` | No record of whether it was sent: ask the user |
| `submitted` | Sent. `**Applied:**` holds the date (`~` = approximate) |
| `interviewing` | At least one interview; details in `interview-process.md` |
| `offer` | Offer received |
| `rejected` / `withdrawn` / `closed` | Finished (closed = no reply, or the role is gone) |

The free-text `**Status:**` line is for humans; the tracker reads the Stage line. `/apply`, `/interview` and `/inbox` keep it up to date.

## Workflow

1. **If a folder and stage were given:** edit that folder's Stage line (add `· **Applied:** <date>` when moving to `submitted`) and append the dated note to `**Status:**`. For `interviewing`, create `interview-process.md` if missing (layout in `/interview`). Set the matching `Status` in `found-jobs.md` if the role is listed there.
2. **Rebuild:** `python3 .claude/skills/status/scripts/build_tracker.py`. It writes `applications.md`: totals, "Needs your attention", every application, and interviews by CV and by source. Never edit `applications.md` by hand.
3. **Report in chat**, briefly:
   - totals by stage, and applications sent in the last 7 days against `profile.json` → `targets.applications_per_week`;
   - each "needs attention" item with its next action; group the `unknown` ones into one question ("Did you send these?");
   - **follow-ups:** for applications 10–20 days old with no reply, offer a short follow-up for each (2–3 sentences, polite, names the role and one specific reason for interest from `research.md`). Draft only, never send. With the Gmail connector, offer to save them as Gmail drafts; without a contact email, give the text for LinkedIn;
   - applications 21+ days old with no reply: suggest `closed` (ask first);
   - once there are enough interviews, anything worth noticing in "Interviews by CV / Source" (which CV or source converts).
4. Suggest `/inbox` if it hasn't been run recently, and `/hunt` if `found-jobs.md` has nothing new.

## Rules

- Never send messages or emails. Drafts only, and only when asked.
- Don't guess a stage. When unsure, use `unknown` and ask.
