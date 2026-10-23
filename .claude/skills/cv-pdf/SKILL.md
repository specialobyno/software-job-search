---
name: cv-pdf
description: "Build an ATS-friendly CV as a polished PDF from an HTML source with WeasyPrint (tagged PDF/UA, embedded fonts, single column), verify it against profile.json, check the page previews, and register it in CV/summary.md. Use for the base CVs at onboarding, to turn a 'CV Tweak Recommendation' from an application's forms.md into a real CV, or to edit or rebuild a CV in CV/source/. Not for cover letters or general documents."
metadata:
  version: 1.0.0
---

# /cv-pdf Skill

```
/cv-pdf <job folder>            # build the tailored CV from that forms.md's CV Tweak Recommendation
/cv-pdf base: <positioning>     # a base CV (called by /onboard-me)
/cv-pdf CV/source/<name>.html   # edit and rebuild an existing CV
```

The source of truth for every CV is an HTML file in `CV/source/`; the PDF in `CV/` is a build output. **Why HTML + WeasyPrint:** exact layout control without hacks, a *tagged* PDF (PDF/UA) with embedded fonts and a clean reading order (what ATS text extractors and screen readers rely on), no ligature or hyphenation artefacts mangling keywords, and every edit is a text diff. Requires `weasyprint` and `poppler` (see `dependencies.md`).

## 1. Gather the content

- **Tailored CV:** the job's "CV Tweak Recommendation" in `forms.md` is the spec. Start from the base CV's HTML in `CV/source/` (far better than re-extracting the PDF).
- **Base CV:** `profile.json` (career history, education, projects, skills), `my_profile.md` (achievements in depth), the matching group in `intake/sample-jobs.md` (keywords), and the user's original CV text (`python3 -I .claude/skills/onboard-me/scripts/extract_text.py intake/cvs/<file>`) for wording they already like.
- **Borrowed items:** text from the other CVs the recommendation names, and the **Content Source Index** in `CV/summary.md` before writing anything new; respect its "never copy" list.
- **Facts:** `facts.md`: Section 1 rules apply; Section 2 (said in interviews) must stay consistent; Section 3 (unconfirmed) and Section 4 (never claim) stay out.

## 2. Content rules (these override anything in an old CV)

- Titles, companies and dates exactly as in `profile.json` → `career_history`, "Month YYYY – Month YYYY"; a role's title may be one of its `title_options` when it fits the job better. "– Present" only for a role with `current: true`.
- Respect each role's `scope_notes` (e.g. "deployed on AWS, didn't provision it") and never use its `never_say` terms or `cv_rules.banned_terms`.
- Side projects and freelance work go under **Notable Projects**, never under an employer.
- Use the job's wording only for skills the user really has. Nothing invented: no roles, qualifications, numbers or tools they didn't give.
- Education as in `profile.json` (`show_as`); never "Present" for a finished degree.
- No photo, date of birth or marital status unless the target country expects it and the user agreed.

## 3. Write the HTML

Save to `CV/source/<pdf-basename>.html`, starting from the closest existing source or `assets/cv-template.html` (its `{{PLACEHOLDERS}}` must all be replaced). Keep the template's CSS; change content only, unless the user asks for a design change.

**ATS layout rules:**
- `<meta charset="utf-8">` in the head.
- One column. No `<table>`, no multi-column CSS, no text in images or SVG, no icons for contact details.
- Name in `<h1>`; standard `<h2>` titles: Professional Summary, Core Skills, Professional Experience, Notable Projects, Education, Certifications, Languages (keep headings containing each word in `cv_rules.required_headings`).
- Role line = "Title — Company", then the dates (right-aligned with flexbox, but after the title in the DOM).
- Skills as labelled single-line rows (`<p><strong>Databases:</strong> …</p>`), not tag clouds or bars.
- Real `<ul><li>` bullets; links as visible text (`linkedin.com/in/…`).
- One date format throughout.
- Don't put `break-inside: avoid` on whole roles (a long role then jumps a page and leaves a big gap); the template keeps each role's title with its first bullet.
- Target **2 A4 pages** (1 is fine early in a career; `cv_rules.page_size` may say Letter). Trim weaker bullets before shrinking fonts below 9.2pt.

## 4. Build and verify

```bash
.claude/skills/cv-pdf/scripts/build_cv.sh CV/source/<name>.html CV/<name>.pdf <scratchpad>/cv-preview/<name>
```

It **fails** on: leftover `{{placeholders}}`, an untagged PDF, unembedded fonts, little extractable text, a missing name/email/phone/LinkedIn (or other `cv_rules.must_contain`), missing required headings, garbled characters, ligature glyphs, any banned or `never_say` term, and "– Present" when no job is current. It **warns** on the page count, page size, and titles or dates that don't match `career_history`. It prints the extracted text (what an ATS sees) and writes PNG previews.

Then **look at every preview** (`Read` each PNG): no heading stranded at a page bottom, no role split awkwardly, balanced whitespace, page 2 not nearly empty. Fix the HTML and rebuild until clean.

## 5. Register

- `CV/summary.md`: an index row (next free number), a detailed entry (headline, source, summary, best for, key differentiators, when to tweak), a **Selection Decision Tree** branch if it's the best pick for a role type, and the **Content Source Index** rows for themes where it now holds the best wording. Add newly found mistakes in older CVs to "never copy".
- The originating `forms.md` (tailored CVs): point **CV to use**, **Recommended CV** and every upload field at the new file; mark the tweak section "done: built as CV N" with the date.

## 6. Report

The PDF path, what changed versus the base, the verification results (pages, tagged, fonts), the preview check, and anything left generic for the user to fill in.

## Files

- `assets/cv-template.html`: the reference design (A4, Arial, navy accent, ATS-safe).
- `scripts/build_cv.sh`: render, verify against `profile.json`, preview.
