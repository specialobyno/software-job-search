# Software Job Search

A job-search workspace for software engineers, run with [Claude Code](https://claude.com/claude-code). Every step is a slash command: it learns about you once, finds roles that fit, builds tailored ATS-friendly (applicant tracking system) CVs, drafts every application answer in your voice, fills the real application form in Chrome, and submits **only when you say "yes, submit"**. It then tracks every application, reads replies from Gmail, and prepares you for interviews.

## Quick start

1. **Make your own private copy.** This repo will hold your CVs and personal details, so never push them to a public repo. On GitHub, click **Use this template → Create a new repository → Private** (or clone this repo and let step 3 move it to a private repo for you).
2. **Clone it and open Claude Code in the folder:**
   ```bash
   git clone <your-private-repo-url> software-job-search
   cd software-job-search
   claude
   ```
3. **Install the tools.** In Claude Code, type: `Follow dependencies.md`. It installs Python, Node.js, WeasyPrint, Poppler and the GitHub CLI if they're missing, walks you through the Claude in Chrome extension and the optional Gmail connector, and checks everything works.
4. **Onboard:** `/onboard-me`. Have your CV ready (PDF or Word), ideally your LinkedIn profile as a PDF (LinkedIn → your profile → More → Save to PDF), and a few job postings you'd love. It reads them, asks only what it can't find, and builds your first CVs. It takes about an hour, you can stop at any point, and **you can run it again whenever you like** to fill gaps or add new information.
5. **Find and apply:** `/hunt`, then paste the `/apply …` command it gives you.

Not sure what to do next? `/help-me`.

## Commands

| Command | What it does |
|---|---|
| `/help-me` | What the repo can do, and your next step |
| `/onboard-me` | Interactive onboarding; re-run to continue, `/onboard-me <section>` to redo one part, `/onboard-me add` for something new |
| `/hunt [focus\|watchlist]` | Finds and scores matching roles; saves them to `found-jobs.md` with the CV to use |
| `/apply <url>[,<url>…]` | Researches the company, picks or tailors a CV, drafts every answer, fills the form, waits for your "yes, submit" |
| `/cv-pdf <job folder or CV source>` | Builds and verifies an ATS-friendly CV PDF |
| `/status` | Your pipeline: what needs attention, follow-ups due |
| `/inbox [30d]` | Reads application replies in Gmail and proposes updates (never sends anything) |
| `/interview <folder> [prep]` | Records interview notes and prepares you for the next stage |

## What's where

| Path | Contents |
|---|---|
| `profile.json` | Your facts: contact, right to work, salary, targets, career history (filled by `/onboard-me`) |
| `my_profile.md` · `facts.md` · `interview-stories.md` | Your story in depth · what can be claimed and what was said to employers · STAR interview stories |
| `intake/` | What you uploaded at onboarding (never sent to employers) |
| `CV/` | Your CVs (PDF) and their HTML sources; `CV/summary.md` says which to use when |
| `found-jobs.md` · `jobs/` · `applications.md` | Roles found · one folder per application · the tracker |
| `.claude/` | The rules (`CLAUDE.md`), the skills, and their scripts |

## Safety

- Nothing is submitted without your explicit "yes, submit" for that specific job.
- It never creates accounts, types passwords, solves CAPTCHAs or sends emails. Sites that need an account are prepared for you to submit yourself.
- It only claims what you told it. When a form asks something your profile doesn't cover, it writes a realistic answer from your real experience, marks it "crafted", and logs it in `facts.md` for you to confirm.
- A hook checks every drafted application for banned terms, wrong name fields, missing CVs and the salary rule.

## Requirements

macOS or Linux (on Windows, use WSL), Claude Code, Google Chrome with the Claude in Chrome extension, and a Claude plan that includes Claude Code. `dependencies.md` handles the rest.
