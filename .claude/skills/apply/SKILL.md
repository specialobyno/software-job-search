---
name: apply
description: "Apply to one or more jobs. Given a URL or comma-separated list of URLs, checks eligibility, researches each company, selects the best CV, produces a forms.md with every application field pre-answered in the user's voice, builds a tailored ATS-friendly CV PDF via the cv-pdf skill when it helps, then fills the real application form in Chrome and submits it only after the user reviews it and explicitly says yes."
metadata:
  version: 1.0.0
---

# /apply Skill

```
/apply <url>
/apply <url1>,<url2>,<url3>
```

Run the steps for **each URL** in turn, with a separate folder for each. Everything about the user comes from `profile.json`, `my_profile.md`, `facts.md`, `CV/summary.md` and `.claude/CLAUDE.md`.

**Before anything:** if `profile.json` → `onboarding.completed` is empty, stop and suggest `/onboard-me` (offer to draft only if the user insists; no filling or submitting).

---

### Step 1 — Read the job and the real form

Open the URL in Chrome (`claude-in-chrome` skill) and capture: exact title, company, location and remote policy, salary range, the full description, and **every form field** (labels, types, required flags, dropdown options, character limits). ATS forms are rendered by JavaScript, often in a modal behind "Apply", so WebFetch only sees "Loading application form": click Apply (it only opens the form) and read the fields. Don't fill anything yet; that's Step 9. When the URL is an aggregator (Himalayas, Remote Rocketship, LinkedIn…) whose Apply leads to a sign-up wall, find the company's own ATS posting (search `"<company>" "<title>" ashby OR greenhouse OR lever`) and read that form instead.

If the page is gone (404, "no longer accepting applications"), log it and skip.

### Step 1b — Eligibility gate (stop early)

Before any research, check, quoting the posting:

1. **Location / work authorisation** against `profile.json` → `right_to_work` and `targets` (work modes, locations, remote regions, time-zone overlap). Read the location on the company's own ATS posting, not the aggregator's tags (they often drop "US only" or a single-country restriction).
2. **Excluded:** the company is in `targets.exclude_companies` or a `domains_avoid` domain → stop.
3. **Sign-in walls** (JOIN, Workday, Himalayas, Proxify…; see `ats-playbooks.md` → Walls): drafting is fine, but the user submits.
4. **Hard mismatches:** a required language, clearance or licence the user lacks; seniority far off; a core-stack gap; anything in `targets.deal_breakers` or `targets.ask_before`; salary clearly below `salary.minimum`.

If any applies, **stop and ask** (one `AskUserQuestion`): "Apply anyway (honest answers)", "Draft only, I'll submit", "Skip", or "Look for an eligible sibling role on the same board" (board APIs in `.claude/skills/hunt/job-sites.md`). Record the answer on the `forms.md` Eligibility line; `**Stage:** blocked` when the user submits. If nothing applies, say "Eligibility: OK" in one line and carry on. When the user's answer is a new general rule ("B2B is fine from now on"), offer to add it to `profile.json` → `targets` (or run `/onboard-me targets`).

### Step 2 — Research the company

Web search: what the company does (product, customers, market), size and stage, engineering culture (blog, open source, notable challenges), recent news and funding, values, anything on the team or stack. Save a brief `jobs/<folder>/research.md`.

### Step 3 — Analyse the description

Must-haves, nice-to-haves, domain, stack signals, role type, seniority, company type, and the 5–8 keywords an ATS will look for.

### Step 4 — Select the best CV

Read `CV/summary.md` in parts when it's long (`grep -n '^## \|^### CV' CV/summary.md`): the **CV Index**, the **Selection Decision Tree**, the **Content Source Index**, then the **Detailed CV Summaries** of the 2–3 shortlisted CVs. Never pick from the index alone.

```
Recommended CV: <filename>
Reason: <1–2 sentences>
```

**If tweaks would meaningfully improve the fit**, write a **CV Tweak Recommendation**: the base CV, bullets to ADD / REMOVE / EMPHASISE / REFRAME, the headline, and the rebuild prompt (template in `CV/summary.md`). **Build it from existing material, not from scratch:**

1. List the job's main themes from Step 3.
2. Look each theme up in the Content Source Index and extract the CVs it names (`CV/source/<name>.html`, or `pdftotext -layout "CV/<file>.pdf" -`).
3. Take the strongest wording for each bullet, skill row or project and adapt it to the job's language. Write new text only for gaps no CV covers, grounded in `my_profile.md` and `profile.json`.
4. Filter everything through `profile.json` → `career_history` (titles, `title_options`, dates, `scope_notes`, `never_say`) and `facts.md` (Section 4 never; Section 3 not until confirmed). Side-project work stays under projects, never under an employer.
5. Label each borrowed item with its source ("[ADD] from CV 2: …") and note what you deliberately left out.

If the job asks for something the user doesn't have, say so honestly in the recommendation; never add it.

### Step 5 — Create the job folder

`jobs/<company-slug>-<role-slug>/`, e.g. `jobs/stripe-senior-backend-engineer/`.

### Step 6 — Draft every answer

Sources: `profile.json` (facts and standing answers), `facts.md` (Section 1 usable; Section 2 = what was already told to employers, stay consistent; Section 3 unconfirmed, don't reuse as fact; Section 4 never), `my_profile.md` (narrative and depth), `interview-stories.md`, `CV/summary.md`, `research.md`.

**Salary rule** (`profile.json` → `salary`, in its currency and period):

1. No published range, or `default` falls inside it → **`default`**.
2. The range's top is below `default` → **the top** (flag it if it's below `minimum`).
3. The range's bottom is above `default` → **the middle of the range, rounded to the nearest thousand**.

Compare like with like: annualise monthly or daily ranges first (×12, or ×14 where the posting says so), then answer in the posting's own units. Convert other currencies at the current rate for the comparison, answer in the posting's currency, and note the conversion. Under the salary answer in `forms.md`, add a one-line note with the case that applied.

| Field | Answer |
|---|---|
| Names | `names`: first, middle (Middle Name field only), last; full-name fields use `full_name` |
| Pronouns, nationality | `pronouns`, `nationality` (ask if empty and required; never guess) |
| Email, phone, location, LinkedIn, GitHub, website | `contact` (street address only when the form requires it) |
| Date of birth | `date_of_birth`, only when the form requires it; ask if empty |
| Right to work / sponsorship | `right_to_work.statement` |
| Availability / start date / notice | `availability.statement`; never anything in `availability.never_say` |
| Salary | the rule above: a figure in a short field, or "<figure> per year, and I'm happy to discuss the full package." in free text |
| Diversity, disability, veteran, criminal record, references, travel, clearance | `standard_answers` |
| How did you hear | `standard_answers.how_did_you_hear`, unless the source was clearly different (e.g. a referral) |
| Years of experience | from `experience.years_statement` / `since` |
| Cover letter | see below |
| Why this company | something specific from `research.md`: product, mission, an engineering challenge |
| Why this role | the role's responsibilities tied to the user's demonstrated experience |
| Biggest strength | `standard_answers.biggest_strength` |
| Experience with [tech] | from the CVs and `my_profile.md`, honest about depth; respect `scope_notes` |
| A challenging problem | `standard_answers.default_challenging_problem`, or the story in `interview-stories.md` closest to the job's focus |
| Any other open-ended field | first person, grounded in real experience, 2–4 sentences |
| Experience question with no documented example | **Don't leave it blank.** Craft a realistic, specific answer set in the user's most fitting real role, with techniques consistent with their stack there; never invent employers, products, titles or metrics beyond qualitative ones ("from seconds to well under a second"). Label it in `forms.md`: "crafted from <role>: check it matches what you did", and **add a row to `facts.md` Section 3** |
| Government ID, tax, social-security or bank numbers | **Never.** Leave for the user (Stage `blocked` if required) |

**Cover letter** (3–4 paragraphs): (1) an opening that names the role and company and says what genuinely interests the user, from the research; never "I am writing to apply for…". (2) one or two paragraphs connecting 2–3 specific achievements from their real roles to the job's core requirements, with concrete technical detail, mirroring the job's language naturally. No over-precise counts that read as AI-written (say "microservices", "several", "a wide range of"), and don't fixate on figures from one CV. (3) a short close: interest in a conversation and availability; no begging or over-thanking. Tone from `writing.tone`: confident, direct, warm. Signed with `full_name`.

### Step 7 — Write `forms.md`

```markdown
# Application: <Job Title> — <Company>

**URL:** <job url>
**Date:** <today>
**Stage:** drafted
**Status:** Drafted
**Location:** <…> · **Salary:** <published range or "not listed">
**CV to use for this application:** `CV/<filename>.pdf`

---

## Eligibility
<"OK", or the issue and the user's decision>

## CV Recommendation
<recommended CV + reason; the tweak recommendation if any>

---

## Application Form Fields

### <Field label>
**Type:** <text / textarea / dropdown / checkbox / file upload> · **Required:** Yes/No

<answer>

> <notes to the user, e.g. "crafted from Acme: check it matches what you did", salary case>

---

## Cover Letter

<letter>

---

## Research Notes Summary
<3–5 bullets>
```

**Stage values:** `drafted`, `filled`, `blocked`, `unknown`, `submitted` (add ` · **Applied:** <date>`), `interviewing`, `offer`, `rejected`, `withdrawn`, `closed`. `**Status:**` stays free text.

A hook runs `lint_forms.py` after every write to a `forms.md`. It **blocks** terms that must never appear (`cv_rules.banned_terms`, each role's `never_say`, `availability.never_say`, `facts.md` Section 4), the middle name in a Last Name field, unfilled `{{placeholders}}`, a CV that isn't in `CV/`, and a missing Stage. It **warns** about `writing.avoid` / `warn_terms`, a past job in the present tense, and a salary that doesn't follow the rule. Fix every error; check each warning.

### Step 8 — Build the tailored CV (uses the `cv-pdf` skill)

**Skip it** when Step 4 recommended no tweaks; say so in the final report.

Otherwise:
1. **Reuse first.** If an existing CV in `CV/summary.md` already applies essentially the same tweaks, recommend it instead of building a near-duplicate; update `forms.md` and stop.
2. Invoke the `cv-pdf` skill (`Skill(cv-pdf, "<job folder>")`). The tweak recommendation is the spec. Follow that skill end to end: HTML source in `CV/source/`, `build_cv.sh` passing, previews checked, registered in `CV/summary.md`.
3. **Name it by positioning, not company**, so it can be reused: `<cv_rules.file_prefix><Role>_<Focus>.pdf`. Never overwrite an existing CV.
4. Point every CV reference in `forms.md` at the new PDF by full path: the **CV to use** header line, the `Recommended CV:` line (noting it was built from the base CV), every resume upload field. The base CV may appear only as "Base CV" inside the tweak record. Retitle the tweak section "CV Tweak Recommendation (done: built as CV N)" with the date.
5. Report anything left generic that the user should personalise.

With several URLs, build each job's CV right after its `forms.md`, and reuse a CV built earlier in the run when a later job's tweaks match it.

### Step 9 — Fill the form in Chrome, then ask before submitting

Fill in the **real** form completely from `forms.md`, then **stop before the final Submit**. Submitting is irreversible and sends personal data, so it always needs the user's explicit approval in chat, every time, for every job.

**Blockers → hand over** (Stage `blocked`, reason in **Status**): an account or sign-in is needed (never create accounts or enter passwords), the form asks for ID, tax or bank numbers, a required video answer, or `forms.md` has an unresolved decision (ask first, or fill the rest and raise it in the review).

**Filling:** read `.claude/skills/apply/ats-playbooks.md` first, in parts (`grep -n '^## ' .claude/skills/apply/ats-playbooks.md`): the **General rules**, the section(s) for this ATS, and **Walls** when a sign-in or email is involved. They cover clicking by coordinates when refs don't register, never setting `.value` by JavaScript, reading values back, `file_upload` for the CV, and consent boxes only at submission. Fill every field, then **read all values back**.

**Review, don't submit.** Leave the tab open and post:
- a table of every field and the exact value entered (as read back), including the uploaded CV file name and how the cover letter was entered;
- the consent fields still to accept, quoting what each agrees to;
- every open risk from `forms.md` (location wording, gaps, salary, crafted answers);
- the question: reply **"yes, submit"** to accept the consent fields and submit, or say what to change.

Set Stage `filled`, Status "Filled, awaiting review".

**On an explicit yes for this job:**
1. Make any requested corrections and read them back. If the user corrects a standing fact (a name, the phone), update `profile.json` too and re-render (`profile_check.py --render`).
2. Tick the consent field(s), read every value back once more, take a screenshot, then click Submit.
3. CAPTCHA → stop; the user completes it in the open tab. Never solve one.
4. Confirm success from the confirmation page and quote it. On validation errors, report them and fix them with the user; never retry silently.
5. Close the tab (only once no other filled form is waiting in the same tab group). Stage `submitted · **Applied:** <date>`; Status "✅ Submitted <date>" with what was sent (CV, cover letter, key values) and any next steps shown. Set the role's `Status` in `found-jobs.md` to `applied`. Rebuild the tracker: `python3 .claude/skills/status/scripts/build_tracker.py`.
6. Add anything new learned about this ATS to `ats-playbooks.md`, with the company and date.

If the user says no or wants changes, leave it unsubmitted and update `forms.md` to match.

---

## Quality checks before finishing

- [ ] Onboarding complete; eligibility gate passed, or the user chose how to proceed
- [ ] `lint_forms.py` reports no errors for this `forms.md`
- [ ] Crafted answers are labelled and listed in `facts.md` Section 3
- [ ] Every visible required field has an answer
- [ ] The cover letter names the company and something specific about it
- [ ] Nothing claims experience outside the user's files; career history, titles and dates match `profile.json`
- [ ] Salary follows the rule; right to work, availability and standard answers come from `profile.json`
- [ ] `forms.md` names one CV, by full path, everywhere (search it for `.pdf`)
- [ ] A tailored CV was built via `cv-pdf` (build passed, previews checked, registered) or an existing one reused, if tweaks were recommended
- [ ] Submitted **only after an explicit "yes" in chat** for this job, with the confirmation recorded; or `blocked` with the reason
