---
name: hunt
description: "Find software engineering jobs that match the user's profile and CVs. Sweeps company ATS boards (Ashby, Greenhouse, Lever…) and remote job APIs, verifies location eligibility, scores and dedupes the roles against past applications, picks the best CV for each, and saves them to found-jobs.md ready for /apply. Use when asked to find, hunt, search or refresh jobs."
metadata:
  version: 1.0.0
---

# /hunt Skill

Find fresh, relevant roles, score them against the user's profile, and add new matches to `found-jobs.md`. Each saved role names the best CV from `CV/` and a ready-to-run `/apply` command. Never apply to jobs, submit forms, create accounts or message anyone: that is `/apply`, and only when the user runs it.

```
/hunt                  # full run
/hunt payments         # bias toward a focus (a domain, "staff", "fullstack", a city…)
/hunt watchlist        # only re-check the companies in the watchlist and the slug sweep
```

**Before anything:** if `profile.json` → `onboarding.completed` is empty, stop and suggest `/onboard-me`.

## Files

| File | Role |
|------|------|
| `.claude/skills/hunt/job-sites.md` | Sources, API endpoints, the **Automation** mode for each (obey it), and the ATS slug sweep list |
| `profile.json` | The search profile: `targets`, `right_to_work`, `salary.minimum`, `languages`, `job_search.regions` |
| `my_profile.md` | Experience depth, for the "why it fits" lines |
| `CV/summary.md` | CV index and selection decision tree |
| `found-jobs.md` | The output (newest run first; watchlist at the bottom) |
| `jobs/*/forms.md` | Every application, for dedupe |

## Workflow

### 1. Load context

1. **Search profile**, built from `profile.json` on every run: target titles and seniority, role types, core stack (and `also_capable`), preferred and avoided domains, work modes, locations, remote regions, time-zone overlap, employment types, right to work and sponsorship needs, `salary.minimum`, `exclude_companies`, `deal_breakers`.
2. Read `job-sites.md`, `found-jobs.md`, and from `CV/summary.md` the **CV Index** and **Selection Decision Tree**.
3. **Seen set** for dedupe: every URL in `found-jobs.md`, and the `**URL:**` of every `jobs/*/forms.md` (treat each folder's company + role as already applied, whatever its stage). Normalise URLs: drop query strings (`utm_*`, `gh_src`), a trailing `/application`, and lowercase the host.

### 2. Sweep the ATS board APIs (the main source)

Pull company boards straight from the public ATS APIs instead of searching for them (web search often ignores `site:` filters on ATS domains and returns stale aggregator pages).

- **Curl every slug** in `job-sites.md` → "ATS slug sweep", plus every watchlist company, on its board API (URL patterns in Tier 0). One request at a time.
- **Filter locally**: location (the user's countries/cities, their remote regions, "anywhere"), title (target titles and seniority), and core-stack terms in the description.
- **A 404 or a tiny body** (Ashby answers a missing slug with a 9-byte 404) means a wrong slug: move it to "Dead slugs" with the date, or find the real slug.
- **Grow the list** with every promising company from any source (probe the slug on Ashby, Greenhouse and Lever before adding it). Over time this list and the watchlist become the best sources.
- Report how many slugs were swept and how many kept roles came from the sweep.

**Search fallback**, two or three queries per run, only to discover new companies. Templates (swap in titles, stack and regions from the profile and the focus argument):

```
site:jobs.ashbyhq.com "<core tech>" senior <role type> remote <region>
site:boards.greenhouse.io OR site:job-boards.greenhouse.io "<core tech>" remote <region>
site:jobs.lever.co OR site:jobs.eu.lever.co "<core tech>" <role type> (<region> OR <country>)
```

### 3. Structured sources (API / RSS rows in `job-sites.md`)

Remote OK, Remotive (`category=software-dev` plus terms), Himalayas (plus the country search for the user's country), freehire (with the user's region/country), We Work Remotely feeds for the user's role types, and the current month's Hacker News "Who is hiring?" thread via the Algolia API, searching the core-stack terms plus "remote" and the user's region. Filter to target titles and stack before scoring.

### 4. Search-mode sites

The Tier 4 regional rows in `profile.json` → `job_search.regions` and the Tier 5 rows for the user's domains: a few `site:` queries per run, rotating so all get covered over several runs. Then fetch the individual public job pages. **Never** scrape or log into "Alerts only" or "Manual" sites; if the user pastes listings or forwards alerts from them, process those like any other source.

### 5. Verify each candidate

Open the actual posting (WebFetch, or Chrome when it's rendered client-side):
- **Live:** not a 404 or "no longer accepting applications".
- **Location eligible:** check the ATS's own location field and description, not the aggregator's tags. Reject "US only" (unless the user can work there), single-country rules that exclude them, and time-zone ranges outside `timezone_overlap`.
- **Seniority and stack really match:** read the requirements, not just the title.
- **Not excluded:** company not in `exclude_companies`, domain not in `domains_avoid`, no `deal_breakers`.
- Note sign-in walls on the apply link (Workday, JOIN, Himalayas…) under **Gaps / risks**.

### 6. Score (0–100)

| Factor | Weight |
|---|---|
| Stack match (core stack first, then databases, queues, cloud) | 35 |
| Domain match (`domains_preferred` highest; then domains in the user's career history) | 20 |
| Seniority fit | 15 |
| Location / remote / right-to-work eligibility | 15 |
| Company signal (funding, size, credible product, salary transparency) | 10 |
| Freshness (≤7 days full, ≤30 days half) | 5 |

Save roles scoring **≥ 60**; mark **≥ 80** with ⭐. A published salary top below `salary.minimum` caps the score at 60 and goes in Gaps / risks.

### 7. Pick the CV

Follow the **Selection Decision Tree** in `CV/summary.md` and give the filename exactly as it is in `CV/`. Add a one-line tweak note when the summary's tweak guidance applies.

### 8. Write to `found-jobs.md`

Dedupe against the seen set (by normalised URL, and by company + title). Add a new run section directly under `# Found Jobs`:

```markdown
## Run — YYYY-MM-DD HH:MM (N new, M ⭐)

### ⭐ 87 — Senior Backend Engineer (Payments) · Acme Pay
- **Link:** https://jobs.ashbyhq.com/acme/…
- **Source:** Ashby (slug sweep) · **Posted:** 2026-10-05
- **Location:** Remote — EMEA · **Salary:** €85–100k (or "not listed")
- **Stack:** Node.js, TypeScript, PostgreSQL, Kafka, AWS
- **Why it fits:** 1–2 sentences tied to specific experience from `my_profile.md`
- **Gaps / risks:** e.g. wants Go, German preferred, Workday account needed
- **CV:** `<file>.pdf`
- **Apply:** `/apply https://jobs.ashbyhq.com/acme/…`
- **Status:** new
```

Leave existing entries untouched, except updating `Status` when told (`new` → `applied` / `skipped` / `closed`). Keep the `## Watchlist` table (company · ATS · board API URL) at the bottom, and add good companies to it.

### 9. Report

In chat: roles checked and added; the top 3 by score with links and chosen CV; new watchlist companies; sources that failed; and one combined command for the ⭐ roles, ready to paste: `/apply <url1>,<url2>,…`.

## Rules

- Don't invent salaries, dates or requirements: write "not listed".
- Don't create application folders (`/apply` does).
- If an API fails or changes shape, note it, fall back to Search mode for that source, and carry on.
- Respect rate limits: one request at a time, and don't hammer a single host.
