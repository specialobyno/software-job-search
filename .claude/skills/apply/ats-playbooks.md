# ATS Playbooks: filling real application forms

Read the general rules and the section for the ATS (applicant tracking system) you're on before Step 9 of `/apply`. **After every application, add what you learned** (a field that wouldn't register, a validation surprise, a sign-in wall) to the right section, with the date.

---

## General rules (all ATSs)

1. Open the posting in a **new tab** (`tabs_context_mcp`, then `navigate`), open the form, and locate fields with `find`/`read_page`.
   - **Don't close tabs while other filled forms are waiting.** Closing a tab group's first tab can drop the whole group, and every filled form in it becomes unreachable and has to be refilled. Close tabs only after every submission, or reuse one tab per form.
2. **Text fields:** click the field, then `type`.
   - If clicking by element `ref` doesn't focus the input (common on React forms), **click by on-screen coordinates from a fresh screenshot**, in the screenshot's coordinate frame, then type. This is the most reliable method (Greenhouse, Ashby, custom agency portals).
   - Fallback: focus with `javascript_tool` (`el.focus(); el.select()`) and type. **Not on Ashby**: there it fails (see the Ashby section's first rule).
   - **Never set `.value` through JavaScript.** React forms ignore it, and the field looks filled but submits empty.
   - **Keystrokes go to the tab in front, not the tab you name.** With several forms open, `type` after a `left_click` on a background tab types into nothing, or into the tab in front. Take a `screenshot` of the tab first, which brings it to the front, then click and type, and check `document.activeElement.name` after the click.
3. **Read values back after each batch** with `javascript_tool` (`document.getElementById(...).value`, or `querySelectorAll('input,textarea')` → name/value). Screenshots can be stale or scrolled.
4. **Name:** first, middle and last exactly as in `profile.json` → `names`; the middle name goes only in a Middle Name field, never in Last Name.
5. **Phone:** type `profile.json` → `contact.phone` with its country code; country pickers usually set themselves (but see Recruitee below).
6. **CV upload:** never click "Attach" (it opens a native file picker). Use `file_upload` with the file input's `ref` and the absolute path of the CV named in `forms.md`. Confirm the file name appears on the page.
7. **Cover letter:** prefer "Enter manually" and type the letter exactly as in `forms.md`, without the notes to the user (lines starting with ">"). Check the length and the first and last lines.
8. **Consent / privacy / terms:** tick only as part of the approved submission, never while filling. Optional marketing, talent-pool or future-contact consents stay unticked unless the user says otherwise.
9. **CAPTCHA:** stop and ask the user to complete it in the open tab. Never solve one.
10. **Validation errors after Submit:** report the exact message, fix it with the user, and don't retry silently.

---

## Ashby (`jobs.ashbyhq.com`)

- **Board API:** `https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true` lists every role with its location and pay.
- The form is on the `/application` tab of the posting.
- **Rule: a filled-looking field doesn't prove Ashby registered it.** Ashby keeps its own form state, and a field whose DOM `.value` (or screenshot) reads back correctly can still fail at Submit with "Missing entry for required field: …". This has hit email fields, Yes/No pairs and full-name fields (even after JS focus + `type`). So, on every Ashby form:
  1. **Upload the Resume first**, then wait a few seconds before typing (uploads can reset text fields, and Submit during an upload fails with "We're updating your application (e.g. uploading files), please try again").
  2. **Enter every required text field the same way:** a real click by on-screen coordinates from a fresh screenshot, `cmd+a`, `Delete`, `type`, then `Tab`. Never JS focus alone.
  3. **Toggle every Yes/No pair once** (click the other option, then the intended one) and check the selected state.
  4. **Expect one validation round.** If Submit reports a missing field, re-enter that field with step 2 and submit again; report anything else (General rule 10).
- **Location** is a search box: type your city (`contact.city`), wait for suggestions, then pick the "City, Region, Country" entry. "Which location are you applying for?" fields are often fixed lists that look like plain text inputs: type the first letters and pick the option, or they read back empty.
- Confirmation text: "Success. Your application was successfully submitted" or a company-specific thank-you.
- On some boards typing by `ref` click doesn't register at all, and after the uploads every text field reads back empty (the reason for step 1 of the rule above).
- **Pronouns, nationality and similar free-text fields** can be required: use `profile.json`, and if it's empty, ask the user; never guess. A "US state" combobox for non-US applicants: type N/A and pick it.
- Some companies limit applications (e.g. one per 90 days across all engineering roles): check the posting before applying to a second role there.
- `javascript_tool` read-backs can be blocked on a page ("Cookie/query string data"); verify with screenshots instead.
- **Conditional questions appear only after an answer:** "Yes" to "residing in Europe?" can reveal required fields (current city/country, visa sponsorship) that weren't in the form when it was read, so the first Submit fails. After every Yes/No click, re-read the form text before calling it filled. Picking "Another job board" as the source can also open a required "Which one?" box.
- **Location questions can carry a hint below the label** ("Or within a commutable distance, e.g. …"). Read the hint before answering Yes/No, and take a screenshot when drafting.
- **Address fields may say "For NDA purposes"**, which means a full street address is expected. Use `contact.street_address`, or ask the user rather than leave only the city.
- "What platform encouraged you to apply?" can be a fixed-option combobox (Article, Friend, LinkedIn, Other, Twitter…). List the options with `[role=option]` and pick the true one ("Other" when the source was your own search).
- **Autofill from resume:** uploading the CV to the "Autofill from resume" box also attaches it as the Resume and fills Name, Email and LinkedIn. Read the values back.

## JazzHR (`<company>.applytojob.com`)

- Plain HTML form. **Clicking by `ref` doesn't register typing.** Use coordinate clicks from a screenshot, then type. `file_upload` on the resume input works, though the page still shows "Attach resume" afterwards; check `input.files[0].name`.
- Address has extra City / State / Postal boxes. Yes/No questions are checkbox pairs.
- Ends with a **reCAPTCHA "Human Check"**: the user ticks it before submitting.
- The cookie banner covers the lower form. Reject it by coordinate click first.

## Factorial (`<company>.factorial.com`, was `factorialhr.com`)

- Careers home `https://<company>.factorial.com/`; posting `/job_posting/<slug>`; form `/apply/<slug>`.
- Phone prefix is a native `<select>` (`form_input` works). Text fields take coordinate click + type. Questions are radios.
- "I have read and acknowledge the Privacy Policy" is required; the talent-pool checkbox is optional and stays unticked.

## Claude desktop built-in browser (instead of Chrome)

- The pane has no file-upload tool, so the user must attach the Resume. Coordinate click + `cmd+a`/`Delete`/`type`/`Tab` registers text fields. When the upload comes last, re-read every text field after it before Submit. A CV the user attached in the pane may never show up in Claude's page reads (and a consent box can flip state between turns), so read-backs can't confirm an upload there: let the user submit, and check the Success page afterwards.

## Greenhouse (`boards.greenhouse.io`, `job-boards.greenhouse.io`, `job-boards.eu.greenhouse.io`)

- **Board API:** `https://boards-api.greenhouse.io/v1/boards/<token>/jobs?questions=true` returns every question with its type and options, which is useful for drafting `forms.md` before opening Chrome. It serves EU boards too (`boards-api.eu.greenhouse.io` sometimes doesn't answer at all).
- **Embedded forms** (careers pages that wrap Greenhouse in an iframe) are easier to fill at `https://job-boards.greenhouse.io/embed/job_app?for=<board>&token=<job id>`.
- React-select dropdowns: click the control, type the option text, and press Enter (Return doesn't submit the form). Then read back the chosen label: the react-select `input` reads back empty after selecting, so check the label on a screenshot.
- Some boards add fields the API doesn't list: **Country (phone) + Location (City)** autocomplete (type "City, Country" and pick it), a separate "Country" + "City" pair, and an optional Education/Degree block.
- `el.focus()` via `javascript_tool` + `type` registers text fields on many boards. Typing the full international phone number sets the country picker correctly.
- Consent is sometimes just a sentence in the job description, with no checkbox. A reCAPTCHA badge doesn't always mean a challenge at Submit. The confirmation page is `/jobs/<id>/confirmation` ("Thank you for applying.").

## API applications (no form)

- Some postings ask for an application by API, e.g. `POST https://<company>/api/hiring/apply` with JSON (role slug, name, email, link, cover note…). Draft the JSON in `forms.md`, save it as `request.json`, and send it with curl only after the user's "yes". Follow redirects to the final host and post there directly (a 308 from the bare host to `www.` is common). An HTTP 500 for a complete body, when `{}` returns a proper 400 validation error, means the failure is on their side: report it, don't retry in a loop.

## Lever (`jobs.lever.co`, `jobs.eu.lever.co`)

- **API:** `https://api.lever.co/v0/postings/<company>?mode=json` (EU: `api.eu.lever.co`).
- The form is a plain HTML page at `/apply`. Typing usually registers on the first try. "Additional information" is the cover-letter box.
- **Wait for the resume parser before typing.** After the upload it says "Analyzing resume…" then "Success!", and it then overwrites name, phone, current location, current company (it may put a past employer as current: clear it), LinkedIn and "Other URL", and **wipes custom question answers typed before it finished**. Upload, wait for "Success!", then type, and read back.
- Some boards end with an **hCaptcha**: the user ticks it (often no challenge appears at Submit). Confirmation page `/thanks`: "Application submitted!".
- CV-only forms exist (resume, name, email, phone, location, company; no questions or cover letter). Location suggestions may use "City, ISO3" (e.g. "Paris, FRA"). Some agencies post on behalf of unnamed partner companies.

## Teamtailor (`<company>.teamtailor.com`, or a custom careers domain)

- The form opens in a modal after "Apply for this job". It offers "Apply with LinkedIn"; fill it manually instead, so every answer comes from `forms.md`.
- Screening questions appear after the contact details. Scroll the modal, not the page.
- Some sites use a full page at `/jobs/<id>/applications/new` instead of a modal, with two cookie banners (decline both) and a required office checkbox even for remote roles. The CV upload lands in `candidate[resume_remote_url]`, so `input.files` reads empty afterwards; check that field instead. Consent can be a sentence above Submit with no checkbox. The thanks page shows an "Applied: N" count (earlier applications to the same company) and an optional "Connect" sign-up: skip it.
- The first `file_upload` right after `navigate` can hang the tab for good ("Page still loading", screenshots time out); a fresh tab works. Run one `javascript_tool` call first to make sure the page is ready, then upload.
- A cookie modal can swallow the first clicks after it closes: decline cookies ("No, adjust" → "Deny") before filling, then click fields by coordinates. Address is often a location search: type your city and pick the suggestion. Skip optional endorser requests and profile sign-ups on the thanks page.

## Workable (`apply.workable.com`)

- The form is on the posting's `/apply` page. Some companies add an "Apply with LinkedIn/Indeed" step first; skip it.
- LinkedIn Easy Apply postings often mirror a Workable posting. Apply on Workable so the answers can be read back.
- **Free-text answers can be single-line inputs with a hidden `maxLength`** (one allowed 127 characters and silently cut the text). Read every answer's length back.
- The Resume `ref` from `find` can point at the `<label>`; ask `find` for the hidden `input type=file` that accepts .pdf.
- **The resume parser fills Address with a wrong city** more often than not: fix it and read back. Phone has a country picker, so type the number without the prefix.
- Notice period and "applied on your own or via a recruiter" can be searchable dropdowns ("Available immediately", "Applied directly"). A "Notice Period" custom field may accept only digits and "." (typed text vanishes): enter the number of weeks, or "0". "Job location" can be a searchable dropdown of countries. Required free-text "Nationality" fields: use `profile.json`, or ask.
- Screening questions are `QA_<id>` fields; Yes/No are radios.
- `jobs.workable.com` view pages: "Apply now" opens the form in a modal whose inputs `javascript_tool` can't see (it reads 0 forms), but `find` refs and ref clicks work. Requirement checks are YES/NO button pairs. After Submit, a "Save your profile" sign-up appears: skip it.

## Recruitee (`<company>.recruitee.com`, or a custom domain)

- **API:** `https://<company>.recruitee.com/api/offers/` lists every offer with its description and location flags (it works on custom domains too).
- **Phone country picker defaults to the job's country**, so typing the number with its own prefix can become "+40 <your number>". Open the "Select country calling code" button, pick your country, then clear and retype the number and read it back. Alternatively, clear the field and type the full international number with no spaces in one go (typing only the national number can pick a random country).
- Single-option skill ratings are checkboxes. Yes/No radios may not register by `ref` click; coordinate clicks do.
- The cover letter has a "Write it here instead" text box. There's often no consent checkbox before "Send".
- A required **video answer** (Record Video / Upload Video) can't be filled by Claude: the user records it (Stage `blocked` until then).
- Aggregator listings (e.g. Himalayas) sometimes open a Recruitee form in a new tab with no sign-in, so check the aggregator's Apply button before treating it as a wall.

## Personio (`<company>.jobs.personio.de`)

- **XML feed:** `https://<company>.jobs.personio.de/xml`.
- Forms are plain: `el.focus()` + `type` works for text, `form_input` for the `<select>`s; CV and "Other" (cover letter) via `file_upload`. Watch for German-only required fields.
- **Job checks:** the job page embeds a "We couldn't find any jobs" translation string, so text-based dead-link checks give false positives. Check the `/xml` feed for `<id><job id></id>` instead.
- Confirmation: "Thank you very much for your application!"

## Agency and custom job portals

- Clicking by `ref` often doesn't register typing. **Use coordinate clicks from a screenshot, then type.**
- Agency roles for a client may ask about work permits for the client's country. Ask the user rather than guessing.

## Eightfold (`*.eightfold.ai`)

- Enterprise ATS that parses the CV and auto-fills the work history. **Check every auto-filled job against `profile.json` → `career_history`** before continuing (titles, dates, names to never use).

---

## Walls: hand these over to the user (never create accounts or sign in)

| Site | What happens | What to do |
|---|---|---|
| **JOIN** (`join.com`) | "Jetzt bewerben" leads to e-mail or Google sign-in before the form. When the user is already signed in, step 1 "Bestätigen Sie Ihren CV" pre-loads an **old CV** from the JOIN profile, and the only way to swap it is "Datei entfernen" (no file input until then) | Draft `forms.md` with the usual JOIN fields; the user signs in and submits, or approves removing the stored CV first. Never send the stored one. Once approved: "Datei entfernen" → upload the CV to the dropzone file input → "Weiter"; the next step wants the **cover letter as a file** (build a one-page PDF with weasyprint from `forms.md`); the review page has a **pre-ticked "Diesen CV standardmäßig für künftige Bewerbungen verwenden"** (a profile setting): untick it unless the user asks; then "Bestätigen & bewerben" |
| **Talent marketplaces** (e.g. Proxify) | Step 1 creates an applicant account | Draft answers; the user submits |
| **Himalayas** | "Apply" needs a Himalayas account. Location tags can be wrong or restrictive (a role shown as "United States only" that isn't, or the reverse). Many listings are Himalayas-only (`directApply: false`) | Find the company's own ATS posting (its careers page often links to JazzHR, Ashby, etc.); otherwise hand over |
| **Workday** (`*.myworkdayjobs.com`) | Requires an account per company: "Apply Manually" goes straight to a "Create Account/Sign In" step. The JD is readable through `/wday/cxs/<tenant>/<site>/job/<path>` (JSON), which WebFetch can't render | Hand over: draft the Workday steps (My Information, My Experience, Application Questions, Voluntary Disclosures) in `forms.md`, leave the tab open for the user to sign in, then fill |
| **Arc.dev, Remote Rocketship, Working Nomads, LinkedIn** | Aggregators with sign-up walls | Search "<company> <title> ashby/greenhouse/lever" for the real posting |
| **MeetFrank** (`meetfrank.com`) | Apply goes to `/login` (email, then a code) | The user signs in themselves in the open tab; never enter credentials (form notes below) |
| A job site that's down | — | Email the recruiter instead (below) |

### Sending an application email (Gmail in Chrome)

Attachments through the Gmail API need the PDF inlined as base64, which is error-prone. Instead open `https://mail.google.com/mail/?view=cm&fs=1&to=<addr>&su=<subject>`, type the body, attach with `file_upload` on the compose window's file input, and send with **Cmd+Enter** (a click on Send may not register). Check `in:sent to:<addr>` before retrying, so nothing is sent twice. Only with the user's explicit OK to send.

## Rippling (`ats.rippling.com/<company>/jobs`)

- **Board API:** `https://api.rippling.com/platform/api/ats/v1/board/<company>/jobs` lists every role with its `workLocation`. The form is at `/<locale>/<company>/jobs/<uuid>/apply`.
- Uploading the CV runs a parser ("CV parsing was successful") that fills first/last name, email, phone (country picker) and LinkedIn, and **sets Location from the CV**. Once Location is set, **Address, City, State/Territory, ZIP and Country all become required**, so a street address and postal code are needed (use `contact.street_address` in `profile.json`; ask if it is empty). The SMS opt-in is a Yes/No radio pair; pick No. The terms consent is a sentence above "Apply", with no checkbox. Coordinate clicks + typing work; `input[type=file]` reads empty afterwards but the file chip shows.

## Homerun (`<careers domain>/<job>/en/apply`)

- Three steps: basic info + resume → Questions → Preview → "Submit your application". The form fields are in the HTML, so curl can read every question while drafting.
- `javascript_tool` is blocked once the URL has `?&step=` ("Cookie/query string data"); use `find` refs: ref click + `type` registers every textarea, and `get_page_text` reads the values back. `file_upload` on the resume input works (the file chip shows).
- No consent checkbox; the cookie notice may only have an ×. After Submit the page says "Your application has been submitted!", and the hidden preview resets to "no answer" for every question, which is normal and not lost data.

## Company WordPress forms

- Often a single form on the posting page: Name (one field), Email, Phone, LinkedIn (sometimes required), CV file, a "How did you find this job?" select, a required privacy checkbox, Apply. Ref clicks + typing usually work; read values back from the inputs. If an aggregator's Apply button for the same role leads to a sign-up, apply on the company's form instead. Cookie banners: "Reject All".

## MeetFrank form

- After the user signs in: several steps on one page, revealed one by one with Continue: (1) CV upload / LinkedIn autofill, (2) full name, current or last job title, speciality (dropdown: type "Software" → "Software Engineering"), city search, phone with a country picker, (3) monthly gross salary dropdown in fixed steps, (4) the company's optional questions, then "Submit your application".
- `get_page_text` can return a stale step-1 view; use screenshots or `javascript_tool` on `main`. The city search may only offer neighbourhood-level entries: pick the closest. No cover-letter field: put a short intro in the first optional question.

## CVWarehouse (`jobpage.cvwarehouse.com/ApplicationForm/AppForm?job=<id>…`)

- Often reached from a job board that hides the form behind a login: curl the board's posting page and grep `cvwarehouse` for the form link. No account needed: reject cookies, then click "Fill in the form below" to reveal the inputs.
- Selects (`TitleSingleSelect`, `Country`, `EducationLevelSingleSelect`, `Nationality`, `Level`) take `form_input`; ref click + `type` registers text fields, and `emailConfirm` copies the email by itself. Typically required: title, names, email, country, city, education level, degree, school, one language with a level, mobile phone, CV, two consent boxes.
- **The Claude extension may refuse screenshots on this domain** ("Permission denied for this action on this domain"), and the tab can freeze (CDP timeouts, `get_page_text` stuck "loading") right after `file_upload`. Ask the user to allow the site in the extension before filling, and upload the CV first so a freeze costs nothing.
- **The CV slot is a Dropzone, not the first file input:** input 0 is the photo cropper (`myCroppic_imgUploadField`; uploading a PDF there froze the tab), and of the two `input.dz-hidden-input`s the CV one belongs to the `Dropzone.instances` entry whose element is `documentUploadZone`; the other (`#fileUpload`) is "Upload additional files". Tag them with `setAttribute('aria-label', …)`, get the ref with `find`, then check the PDF name appears right under "CV *". Submit otherwise fails with "The document field is required".
- **Some countries also need Region** (a `<select name=Region>`); it isn't marked required until Submit fails. Consent checkboxes register with coordinate clicks, not `ref` clicks. The confirmation can take ~10 s to replace the form (URL gets `&successful=true`).

## Comeet / Spark Hire Recruit (`www.comeet.co/jobs/<org>/<pos>/apply`)

- Careers pages often embed the form in a cross-origin iframe; clicks and typing on the embed don't register, and `find`/`javascript_tool` can't see inside it. Read the iframe `src` (origin + path only, since query strings get the JS output blocked) and open `https://www.comeet.co/jobs/<org>/<pos>/apply` directly: a plain form (firstName, lastName, email, phone, cv file, linkedin, coverLetter/portfolio files, comment, optional `gdprConsent` extended-retention box). Coordinate clicks + typing register every field; `file_upload` on the "Resume" ref works. Cookie banners may have a "Cookies settings" → "Save settings" path with everything off.
