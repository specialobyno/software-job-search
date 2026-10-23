# CV Summary & Selection Guide

The reference for choosing which CV to send for any job. Read it before every application (`/apply` Step 4, `/hunt` step 7). **Base CVs** come from onboarding, one per positioning; **tailored CVs** are built from a base CV for a specific job (by `/apply` Step 8) and are reused for similar jobs.

All CVs are built from HTML in `CV/source/` with `.claude/skills/cv-pdf/scripts/build_cv.sh <source.html> <output.pdf>`. Never send the original files in `intake/`; they are source material only.

---

## CV Index

| # | File | Type | Positioning | Best for |
|---|------|------|-------------|----------|

## Detailed CV Summaries

<!-- One entry per CV:

### CV N — `<file>.pdf`
- **Headline:**
- **Source:** `CV/source/<file>.html` (built from: …)
- **Summary:**
- **Best for:**
- **Key differentiators:**
- **When to tweak:**
-->

## Selection Decision Tree

```
(written by /onboard-me once there are 2+ CVs, e.g.)
Is the role mainly backend?
├── Yes → CV 1
└── No → full stack → CV 2
```

## Content Source Index (where to borrow from)

For each theme a job description might raise (payments, event-driven, cloud, leadership, a framework…), the CV(s) holding the best wording. `/apply` assembles tweaks from these before writing anything new.

| Theme | Best wording in |
|---|---|

**Never copy:** {{wording known to be wrong in the old CVs in intake/, e.g. an old title or a wrong date}}

## CV Tweak Guidance

When no CV is a perfect fit, recommend a tweak rather than building from scratch. Template for the rebuild:

```
Rebuild my CV from the base CV below to fit this job description.
Keep all factual content accurate: do not invent experience or skills.

- [ADD]: <bullet, skill or section, with its source>
- [REMOVE]: <section or bullet that is irrelevant>
- [EMPHASISE]: <existing bullet to move higher>
- [REFRAME]: <existing bullet to rephrase in the JD's language>
- [HEADLINE]: <new headline>

Career history exactly as in profile.json. 1–2 pages, ATS-friendly: one column, no tables, no graphics.

Base CV: [text]
Job description: [text]
```
