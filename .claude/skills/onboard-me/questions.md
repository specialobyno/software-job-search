# Onboarding Question Bank

Used by `/onboard-me`. For each section: the questions, which are multiple choice (**MC**, ask with `AskUserQuestion`), and where each answer is stored. **Pre-fill from the uploads and ask the user to confirm**; only ask outright for what the uploads don't answer. Five or six questions per message at most.

---

## identity

1. Full name exactly as it should appear on CVs and forms (accents included). Then confirm the split: first, middle (if any), last. → `names.first_name`, `middle_name`, `last_name`, `full_name`
2. A name they prefer to be called, if different. → `names.preferred_name`
3. **MC** Pronouns: he/him · she/her · they/them · prefer not to say (Other for anything else). → `pronouns`
4. Nationality (some forms ask; leave empty to skip). → `nationality`
5. Email for applications (one they check daily) and phone with country code. → `contact.email`, `contact.phone`
6. City, region and country they live in; postcode. → `contact.city`, `region`, `country`, `postcode`
7. Street address: **optional**, only used for the rare form that requires it ("for NDA purposes", Rippling). → `contact.street_address`
8. LinkedIn, GitHub, portfolio or personal site (as `linkedin.com/in/…`, `github.com/…`). → `contact.linkedin`, `github`, `website`
9. Date of birth: **only if** they want forms that require it filled for them; otherwise skip. → `date_of_birth` (YYYY-MM-DD)

## work-rights

1. Citizenships, and the countries where they can legally work today (citizen, permanent resident, or visa with type and expiry). → `right_to_work.citizenships`, `authorised_in`
2. Countries where they'd need visa sponsorship. → `right_to_work.needs_sponsorship_for`
3. **MC** Open to relocating? No · Yes, within my region · Yes, anywhere for the right role. If yes, where to. → `willing_to_relocate`, `relocation_countries`
4. Write the **right-to-work sentence** forms will use, and confirm it, e.g. "I'm an EU citizen living in Portugal and don't need sponsorship for roles in the EU or remote roles in the UK." → `right_to_work.statement`
5. **MC** Availability: immediately · 2 weeks · 1 month · 2–3 months · a specific date. Plus their notice period if employed. → `availability.notice_period`, `earliest_start`, `statement` (one sentence, e.g. "I am available to start immediately.")
6. Anything never to write about availability (e.g. "a notice period" when they're free now). → `availability.never_say`

## targets

1. Job titles they'd apply for, most important first (3–6), e.g. Senior Backend Engineer, Full Stack Engineer, Platform Engineer. → `targets.titles`
2. **MC (multi)** Seniority: Mid · Senior · Staff/Principal · Lead/Manager. → `targets.seniority`
3. **MC (multi)** Role types: Backend · Full stack · Frontend · Platform/DevOps/SRE · Mobile · Data · AI/ML engineering. Note "frontend-heavy full stack" preference. → `targets.role_types`
4. Core stack they want to work in (languages, frameworks, databases, cloud), and what they can also do but don't want as the core. → `targets.core_stack`, `also_capable`
5. Domains they'd love, and domains to avoid (e.g. gambling, defence, ad tech). → `targets.domains_preferred`, `domains_avoid`
6. **MC (multi)** Work modes: Remote · Hybrid · On-site. Then: cities for hybrid/on-site, and remote regions (EU, EMEA, worldwide, US time zones…). → `targets.work_modes`, `locations`, `remote_regions`
7. Time-zone limits ("at least 4 hours overlap with CET"; "US Eastern hours are fine"). → `targets.timezone_overlap`
8. **MC (multi)** Employment types: Full-time employee · Contract/B2B · Freelance · Part-time. → `targets.employment_types`
9. **Companies never to apply to**: current employer first, plus anywhere applied to in the last 6 months. → `targets.exclude_companies`
10. Deal-breakers (on-site abroad, heavy on-call, a required language they don't speak, take-homes over N hours…), and situations where Claude should ask first rather than decide. → `targets.deal_breakers`, `ask_before`
11. **MC** Applications per week: 5 · 10 · 15 · 20+. → `targets.applications_per_week`

## salary

1. Currency and period (per year or per month; gross). → `salary.currency`, `period`
2. The figure to ask for by default. → `salary.default`
3. The lowest they'd accept (used to flag roles, never written on a form). → `salary.minimum`
4. Anything else: day rate for contracts, equity views, different figures per country. → `salary.notes`

Explain the rule once: no published range or the default inside it → the default; range top below the default → the top (flagged if below the minimum); range bottom above the default → the middle of the range.

## career

Show the career history drafted from the uploads as a table (company, title, start, end, location) and confirm **row by row**:

1. Is each title exactly how they want it shown? Alternative titles they're happy to use for the same job, depending on the role applied for. → `title`, `title_options`
2. Exact start and end months ("Month YYYY"). Is the latest one current? → `start`, `end`, `current`
3. Company renames, acquisitions or roles merged ("X was rebranded as Y: show only Y"). → `organisation`, plus a `never_say` entry for the old name and a `facts.md` Section 1 rule
4. Roles to leave off CVs entirely (very short, irrelevant). Record in `facts.md` Section 1 so no CV adds them back.
5. Conflicts found between files (different dates or titles) and gaps over 6 months: what's true, and how to explain a gap. → `my_profile.md` → "Gaps and changes"
6. When did their professional software career start, and how should years of experience be stated ("8+ years")? → `experience.since`, `experience.years_statement`

## roles-deep (one round per role, most recent first)

1. What the company does, in one line; company size and stage if relevant. → `what_they_do`
2. Team: size, who they worked with, what they owned versus what others owned. → `my_profile.md`
3. Stack used there (languages, frameworks, databases, queues, cloud, CI/CD, observability, testing). → `stack`
4. Two or three things they built or led there that they're proud of: the problem, what they did, the result. → `highlights` (one line each) and `my_profile.md` (the full version)
5. Numbers they're happy to use (users, traffic, latency, revenue, team size, cost saved). Only what they give. → in the highlight text
6. **Scope limits**: anything used but owned by someone else ("used AWS, the platform team provisioned it"; "contributed to, didn't lead"). → `scope_notes`, and a `facts.md` Section 1 rule if it's easy to get wrong
7. Anything never to say about this role. → `never_say`

## projects-education

1. Side projects, freelance clients, open source: name, type, what it does, stack, link, dates. Confirm these are **never attributed to an employer**. → `side_projects`
2. Degrees: qualification, institution, years, status (completed / in progress, with the expected date). How to show it if in progress. → `education`
3. Certifications: name, issuer, year, expiry. → `certifications`
4. Languages and levels (native, fluent, professional, basic, or A1–C2). → `languages`

## standard-answers

1. **MC** Gender · Ethnicity · Disability · Veteran status: each "Prefer not to say" (default) or their own answer. → `standard_answers.*`
2. **MC** "How did you hear about us?" default: Company careers page · Job board · LinkedIn · Other. → `how_did_you_hear`
3. References: available on request, or names to give later? → `references`
4. Willing to travel? Security clearance? → `willing_to_travel`, `security_clearance`
5. Their **biggest strength**, in a sentence, backed by an example. → `biggest_strength`
6. The **default "challenging problem" story** for forms that ask (point at a story or a role highlight). → `default_challenging_problem`

## writing

1. **MC** Tone: Warm and direct · Formal · Concise and technical · Other. → `writing.tone`
2. Words or phrases they never want in their applications ("passionate", "rockstar", "leveraged"). → `writing.avoid` (warnings)
3. Things that must never be claimed (a tool they only touched, a title they never held). → `facts.md` Section 4, one bullet per term (errors)
4. If they uploaded old cover letters: confirm the voice you read in them ("You write short paragraphs and lead with the product; keep that?"). → `writing.notes`

## stories

Ask for one at a time; aim for 3 on the first run, 5–8 over later runs:
1. The hardest bug or production incident they solved.
2. A project they're proudest of.
3. A disagreement with a colleague or manager, and how it was resolved.
4. Leading or influencing without formal authority (or mentoring).
5. A failure or mistake, and what changed afterwards.
6. A trade-off under deadline pressure.

For each: situation, task, action, result. Write it in `interview-stories.md`, mark missing details **[fill in]**, and say which questions it answers ("Good for").

## job-sources

1. **MC (multi)** Regions to search (from `job-sites.md` Tier 4): Europe-wide · UK & Ireland · DACH · Portugal/Spain · Nigeria/West Africa · Other Africa · Middle East · US/Canada · LATAM · APAC. → `job_search.regions`
2. Companies they already know they'd love to work at (added to the slug sweep).
3. **MC** Is the Gmail connector set up in Claude (needed for `/inbox`)? Yes · Not yet · I don't use Gmail. → `job_search.gmail_connected`

---

## profile.json shapes

```json
"career_history": [{
  "organisation": "Acme Pay", "title": "Senior Backend Engineer", "title_options": ["Backend Engineer", "Software Engineer"],
  "start": "March 2022", "end": "", "current": true, "location": "London, UK (remote)", "employment_type": "full-time",
  "what_they_do": "Payment orchestration platform for online merchants",
  "stack": ["Node.js", "NestJS", "PostgreSQL", "Kafka", "AWS"],
  "highlights": ["Led the network tokenisation integration for Visa and Mastercard", "..."],
  "scope_notes": "Deployed services on AWS; the platform team provisioned it",
  "never_say": ["AcmeOld"]
}],
"side_projects": [{ "name": "", "type": "personal | freelance | open source", "description": "", "stack": [], "link": "", "dates": "", "attribution": "never attributed to an employer" }],
"education": [{ "qualification": "BSc Computer Science", "institution": "", "start": "2014", "end": "2018", "status": "completed | in progress", "show_as": "2014 – 2018", "notes": "" }],
"certifications": [{ "name": "", "issuer": "", "year": "", "expires": "" }],
"languages": [{ "language": "English", "level": "Native" }]
```

Dates in `career_history` are always "Month YYYY" (`profile_check.py` rejects anything else). The current job has `"end": ""` and `"current": true`.
