# Job Sites for Software Engineers

Ranked for a software engineer searching remote, hybrid or local roles. `/onboard-me` picks the regional rows that fit the user (`profile.json` → `job_search.regions`) and seeds the ATS slug sweep with companies in their domains. `/hunt` searches these and always obeys the **Automation** column:

- **API / RSS**: fetch structured data directly (preferred)
- **Search**: discover listings with web search (`site:` queries), then fetch the individual public job pages
- **Alerts only**: never scrape (terms of service forbid it, or bots are blocked). The user sets up the site's own email alerts; `/inbox` or a paste brings the listings in
- **Manual**: profile-based or login-gated; the user maintains it by hand

---

## Tier 0 — Company ATS boards (the main source)

Most companies post here first, often days before (or instead of) job boards.

| # | ATS | Public job pages | Public API (per company) | Automation |
|---|-----|------------------|--------------------------|------------|
| 0.1 | Ashby | https://jobs.ashbyhq.com | `https://api.ashbyhq.com/posting-api/job-board/{company}?includeCompensation=true` | API / Search |
| 0.2 | Greenhouse | https://boards.greenhouse.io · https://job-boards.greenhouse.io · https://job-boards.eu.greenhouse.io | `https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true` (serves EU boards too) | API / Search |
| 0.3 | Lever | https://jobs.lever.co · https://jobs.eu.lever.co | `https://api.lever.co/v0/postings/{company}?mode=json` | API / Search |
| 0.4 | Workable | https://apply.workable.com | `https://apply.workable.com/api/v1/widget/accounts/{company}` | Search |
| 0.5 | Personio | https://{company}.jobs.personio.de | `https://{company}.jobs.personio.de/xml` | Search |
| 0.6 | Teamtailor | https://{company}.teamtailor.com | — | Search |
| 0.7 | Recruitee | https://{company}.recruitee.com | `https://{company}.recruitee.com/api/offers/` | Search |
| 0.8 | SmartRecruiters | https://jobs.smartrecruiters.com | `https://api.smartrecruiters.com/v1/companies/{company}/postings` | Search |
| 0.9 | Rippling | https://ats.rippling.com | `https://api.rippling.com/platform/api/ats/v1/board/{company}/jobs` | Search |
| 0.10 | BambooHR · Breezy HR | https://{company}.bamboohr.com/careers · https://{company}.breezy.hr | — | Search |
| 0.11 | Workday | https://{company}.wd*.myworkdayjobs.com | — | Search (applying needs an account: the user submits) |

### ATS slug sweep

`/hunt` step 2 curls every slug below (and every `found-jobs.md` watchlist company) on every run. `/onboard-me` replaces the seed list with 15–30 companies that hire for the user's stack, domains and regions, checking each slug answers HTTP 200. Add companies as they turn up; move slugs that start returning 404 to "Dead slugs" with the date.

- **Ashby:** (seed) ramp, mercury, deel, posthog, supabase
- **Greenhouse:** (seed) gitlab, remote, stripe, cloudflare, datadog, wise
- **Lever:** (seed) palantir
- **Dead slugs:** (none yet)

---

## Tier 1 — Biggest volume

| # | Site | Link | Automation |
|---|------|------|------------|
| 1 | LinkedIn Jobs | https://www.linkedin.com/jobs/ | Alerts only |
| 2 | Indeed | https://www.indeed.com (country sites) | Alerts only |
| 3 | Glassdoor | https://www.glassdoor.com/Job/ | Alerts only |
| 4 | Wellfound (ex-AngelList Talent) | https://wellfound.com/jobs | Alerts only / Manual |
| 5 | Welcome to the Jungle (incl. Otta) | https://www.welcometothejungle.com/en/jobs | Search |
| 6 | Hacker News "Who's Hiring" | https://news.ycombinator.com/submitted?id=whoishiring | API — `https://hn.algolia.com/api/v1/search_by_date?tags=comment,story_{threadId}&query={term}` |
| 7 | Y Combinator — Work at a Startup | https://www.workatastartup.com | Manual |

## Tier 2 — Remote-first boards

| # | Site | Link | Automation |
|---|------|------|------------|
| 8 | We Work Remotely | https://weworkremotely.com | RSS — `https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss`, `.../remote-full-stack-programming-jobs.rss`, `.../remote-front-end-programming-jobs.rss`, `.../remote-devops-sysadmin-jobs.rss` |
| 9 | Remote OK | https://remoteok.com | API — `https://remoteok.com/api` (credit Remote OK if you republish) |
| 10 | Himalayas | https://himalayas.app/jobs | API — `https://himalayas.app/jobs/api?limit=100`, country search `https://himalayas.app/jobs/api/search?country={ISO2}` (applying needs an account) |
| 11 | Remotive | https://remotive.com | API — `https://remotive.com/api/remote-jobs?category=software-dev&search={term}` |
| 12 | freehire (aggregates company ATS boards) | https://freehire.me | API, no key — `https://freehire.me/api/v1/jobs/search?q={term}&regions={region}&work_mode=remote&sort=posted_at&order=desc&limit=100` (also `countries={ISO2}`; honour `Retry-After`) |
| 13 | Arbeitnow (EU / remote) | https://www.arbeitnow.com | API, no key — `https://www.arbeitnow.com/api/job-board-api?page={n}` (filter `remote: true` and titles locally) |
| 14 | Working Nomads | https://www.workingnomads.com/jobs | Search |
| 15 | EU Remote Jobs | https://euremotejobs.com | Search |
| 16 | Remote Rocketship | https://www.remoterocketship.com | Search |
| 17 | JustRemote · NoDesk · Jobspresso · Dynamite Jobs | various | Search |
| 18 | FlexJobs (paid) | https://www.flexjobs.com | Manual |

## Tier 3 — Vetted talent marketplaces (companies apply to you)

| # | Site | Link | Automation |
|---|------|------|------------|
| 19 | Arc.dev | https://arc.dev | Manual |
| 20 | Turing | https://www.turing.com/jobs | Manual |
| 21 | Toptal (contract) | https://www.toptal.com/developers | Manual |
| 22 | Andela | https://www.andela.com | Manual |
| 23 | Braintrust | https://www.usebraintrust.com | Manual |
| 24 | Levels.fyi Jobs | https://www.levels.fyi/jobs | Search |

## Tier 4 — Regional boards (keep the rows in `job_search.regions`)

| Region | Sites | Automation |
|---|---|---|
| Europe-wide | Landing.jobs · Relocate.me · EuroTechJobs · EURES | Search |
| Portugal | ITJobs.pt · Landing.jobs · Net-Empregos | Search |
| Spain | InfoJobs · Tecnoempleo · Manfred | Search |
| UK & Ireland | CWJobs · Totaljobs · Reed · Otta · IrishJobs.ie | Search |
| Germany / Austria / Switzerland | GermanTechJobs · Berlin Startup Jobs · Swiss Dev Jobs · StepStone · XING | Search (StepStone and XING: Alerts only) |
| Netherlands / Nordics | Werkzoeken · The Hub (Nordic startups) | Search |
| France | Welcome to the Jungle · Free-Work | Search |
| Poland / Eastern Europe | Just Join IT · No Fluff Jobs · Djinni (Ukraine) | Search |
| Nigeria / West Africa | Jobberman · MyJobMag · HotNigerianJobs · local tech companies' own ATS boards (add them to the sweep list) | Search |
| Kenya / East Africa · South Africa | BrighterMonday · Fuzu · OfferZen · PNet · CareerJunction | Search |
| Middle East | Bayt · GulfTalent · Naukrigulf | Search |
| US / Canada | Built In · Dice · Job Bank (Canada) | Search (Dice: Alerts only) |
| India / APAC | Instahyre · Cutshort · Tech in Asia Jobs | Search |
| LATAM (US-time-zone remote) | Get on Board · Torre | Search |

## Tier 5 — Domain niches

| Domain | Sites | Automation |
|---|---|---|
| Fintech, banking | eFinancialCareers | Search |
| Crypto, Web3 | Web3.career · CryptoJobsList · Cryptocurrency Jobs | Search |
| AI / ML | aijobs.net · Hugging Face job board | Search |
| Climate | Climatebase · Work on Climate | Search |
| Open source | GitHub Careers of OSS companies (via their ATS) | Search |
| Health tech | Health tech companies' ATS boards (sweep list) | API |
| Gaming | Hitmarker · Work With Indies | Search |
