---
name: help-me
description: "Explain what this job-search repo can do and what to run next: the workflow from setup to interviews, every slash command with an example, where things are saved, and the safety rules. Checks onboarding and the application tracker to suggest the next step. Use when the user asks for help, what they can do here, how the repo works, or what to do next."
metadata:
  version: 1.0.0
---

# /help-me Skill

(Named `/help-me` because `/help` is Claude Code's own built-in command.)

## 1. Check where the user is (quietly, two commands)

- `python3 .claude/skills/onboard-me/scripts/profile_check.py` → is onboarding complete, and what's missing?
- `command -v weasyprint pdftotext python3 git` → is the setup done?
- If `applications.md` lists applications, note the "Needs your attention" count.

## 2. Reply with this, kept short (adapt the "Next step" line)

**What this repo does:** it runs your job search with Claude Code. It finds roles that fit you, picks or builds the right CV, drafts every application answer in your voice, fills the real form in Chrome and submits only when you say "yes, submit". It tracks every application, reads replies from Gmail, and prepares you for interviews.

**The flow**

| Step | Command | Example |
|---|---|---|
| 0. Install the tools (once) | Say: `Follow dependencies.md` | |
| 1. Tell it about you (re-run any time to add more) | `/onboard-me` | `/onboard-me stories` · `/onboard-me add` · `/onboard-me status` |
| 2. Find jobs | `/hunt` | `/hunt fintech` · `/hunt watchlist` |
| 3. Apply | `/apply <url>[,<url>…]` | `/apply https://jobs.ashbyhq.com/acme/123` |
| 4. Track | `/status` | `/status acme-senior-backend-engineer rejected "email 2 Nov"` |
| 5. Pick up replies | `/inbox` | `/inbox 30d` (needs the Gmail connector) |
| 6. Interviews | `/interview <folder>` | paste the interview notes, or `/interview acme-senior-backend-engineer prep` |
| Any time | `/cv-pdf` | `/cv-pdf CV/source/<name>.html` to edit and rebuild a CV |

**Where things live:** your facts in `profile.json` (edited through `/onboard-me`); your story in `my_profile.md`; your CVs in `CV/`; found roles in `found-jobs.md`; one folder per application in `jobs/`; the tracker in `applications.md`; claims made in interviews and answers awaiting your confirmation in `facts.md`; STAR stories in `interview-stories.md`.

**Safety rules it always follows:** it never submits without your explicit "yes, submit" for that job; never creates accounts, enters passwords or solves CAPTCHAs (you do those); never sends emails or messages; never claims experience you didn't give it. When it has to word an answer for you, it marks it "crafted" and logs it in `facts.md` for you to confirm.

**Tips:** paste job links from anywhere (LinkedIn, email alerts) straight into `/apply`. Run `/onboard-me` again whenever something changes (a new job, project, certificate or preference). Commit often, and only push to a **private** GitHub repo, because this folder holds your personal data.

**Next step:** one line, from step 1: `Follow dependencies.md` if tools are missing; `/onboard-me` if onboarding is incomplete (name the missing sections); otherwise `/hunt`, or the top "Needs your attention" item from `applications.md`.

If the user asked about one command, explain just that one in more depth from its `SKILL.md`, instead of the full overview.
