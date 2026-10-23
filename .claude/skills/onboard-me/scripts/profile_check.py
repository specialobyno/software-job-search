#!/usr/bin/env python3
"""Check profile.json and the onboarding files; report what is still missing.

    python3 .claude/skills/onboard-me/scripts/profile_check.py            # validate + section status
    python3 .claude/skills/onboard-me/scripts/profile_check.py --render   # also rewrite the Candidate block in .claude/CLAUDE.md
    python3 .claude/skills/onboard-me/scripts/profile_check.py --mark <section> [...]   # record sections finished this run
    python3 .claude/skills/onboard-me/scripts/profile_check.py --finish   # stamp onboarding.completed (only when nothing required is missing)

/onboard-me runs this at the start of every run (to pick what to ask) and after every section it saves.
Exit code 1 when profile.json has validation errors.
"""
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PROFILE = os.path.join(ROOT, "profile.json")
CLAUDE_MD = os.path.join(ROOT, ".claude", "CLAUDE.md")
START, END = "<!-- candidate:start -->", "<!-- candidate:end -->"
MONTH = r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}"

# (key, title, required for "onboarded")
SECTIONS = [
    ("files", "CVs and documents in intake/", True),
    ("identity", "Name, pronouns, contact details", True),
    ("work-rights", "Right to work, location, availability", True),
    ("targets", "Target roles, stack, domains, work modes, exclusions", True),
    ("salary", "Salary expectation", True),
    ("career", "Career history (exact titles and dates)", True),
    ("roles-deep", "Each role in depth (stack, achievements, scope)", True),
    ("projects-education", "Side projects, education, certifications, languages", True),
    ("standard-answers", "Standard form answers (diversity, how you heard, references)", True),
    ("writing", "Writing voice, words to avoid, things never to claim", False),
    ("stories", "Interview stories (STAR)", False),
    ("job-sources", "Job sources and the company watchlist", True),
    ("cvs", "Base CVs built and registered", True),
]

def load():
    return json.load(open(PROFILE, encoding="utf-8"))

def read(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def validate(p):
    errors, warnings = [], []
    n = p.get("names", {})
    if n.get("first_name") and n.get("last_name") and n.get("full_name"):
        for part in ("first_name", "last_name"):
            if n[part] not in n["full_name"]:
                errors.append(f"names.full_name \"{n['full_name']}\" doesn't contain names.{part} \"{n[part]}\"")
    email = p.get("contact", {}).get("email", "")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", email, re.I):
        errors.append(f"contact.email doesn't look like an email: {email}")
    phone = p.get("contact", {}).get("phone", "")
    if phone and not phone.startswith("+"):
        warnings.append("contact.phone has no +country code (forms and ATS phone pickers need it)")
    for i, job in enumerate(p.get("career_history", [])):
        where = f"career_history[{i}] ({job.get('organisation') or '?'})"
        for k in ("organisation", "title", "start"):
            if not job.get(k):
                errors.append(f"{where}: missing {k}")
        for k in ("start", "end"):
            v = job.get(k, "")
            if v and not re.fullmatch(MONTH, v):
                errors.append(f"{where}: {k} \"{v}\" must be \"Month YYYY\" (e.g. \"March 2024\")")
        if not job.get("end") and not job.get("current"):
            errors.append(f"{where}: no end date; set \"current\": true if it's the present job")
        if job.get("current") and job.get("end"):
            errors.append(f"{where}: has an end date but \"current\": true")
    s = p.get("salary", {})
    if s.get("default") and s.get("minimum") and s["minimum"] > s["default"]:
        errors.append("salary.minimum is above salary.default")
    return errors, warnings

def filled(v):
    if isinstance(v, (list, dict)):
        return bool(v) and any(filled(x) for x in (v.values() if isinstance(v, dict) else v))
    return v not in ("", 0, None, False)

def status(p):
    """{section: (state, [missing])} with state done / partial / missing."""
    out = {}
    def put(key, need):
        missing = [label for label, ok in need if not ok]
        state = "done" if not missing else ("missing" if len(missing) == len(need) else "partial")
        out[key] = (state, missing)

    intake = [f for f in os.listdir(os.path.join(ROOT, "intake", "cvs")) if not f.startswith(".")] \
        if os.path.isdir(os.path.join(ROOT, "intake", "cvs")) else []
    put("files", [("at least one CV in intake/cvs/", bool(intake))])

    n, c = p.get("names", {}), p.get("contact", {})
    put("identity", [("first/last/full name", all(n.get(k) for k in ("first_name", "last_name", "full_name"))),
                     ("email", filled(c.get("email"))), ("phone", filled(c.get("phone"))),
                     ("city and country", filled(c.get("city")) and filled(c.get("country"))),
                     ("LinkedIn or GitHub", filled(c.get("linkedin")) or filled(c.get("github"))),
                     ("pronouns (or \"prefer not to say\")", filled(p.get("pronouns")))])

    r, a = p.get("right_to_work", {}), p.get("availability", {})
    put("work-rights", [("right-to-work statement", filled(r.get("statement"))),
                        ("countries authorised in", filled(r.get("authorised_in"))),
                        ("availability statement", filled(a.get("statement")))])

    t = p.get("targets", {})
    put("targets", [("target titles", filled(t.get("titles"))), ("seniority", filled(t.get("seniority"))),
                    ("core stack", filled(t.get("core_stack"))), ("work modes", filled(t.get("work_modes"))),
                    ("locations or remote regions", filled(t.get("locations")) or filled(t.get("remote_regions")))])

    s = p.get("salary", {})
    put("salary", [("default figure", filled(s.get("default"))), ("currency", filled(s.get("currency")))])

    jobs = p.get("career_history", [])
    put("career", [("at least one role", bool(jobs)), ("experience.since", filled(p.get("experience", {}).get("since")))])

    deep = [(f"{j.get('organisation', '?')}: stack + 3 highlights + what the company does",
             filled(j.get("stack")) and len(j.get("highlights", [])) >= 3 and filled(j.get("what_they_do"))) for j in jobs]
    put("roles-deep", deep or [("career history first", False)])

    put("projects-education", [("education (or \"none\" noted)", filled(p.get("education")) or "projects-education" in p.get("onboarding", {}).get("sections_done", [])),
                               ("languages", filled(p.get("languages")))])

    sa = p.get("standard_answers", {})
    put("standard-answers", [("how did you hear", filled(sa.get("how_did_you_hear"))),
                             ("biggest strength", filled(sa.get("biggest_strength"))),
                             ("default challenging problem", filled(sa.get("default_challenging_problem")))])

    w = p.get("writing", {})
    put("writing", [("tone", filled(w.get("tone")))])

    stories = len(re.findall(r"^## \d+\.", read("interview-stories.md"), re.M))
    put("stories", [(f"at least 3 stories (have {stories})", stories >= 3)])

    sites = read(".claude/skills/hunt/job-sites.md")
    m = re.search(r"^## ATS slug sweep(.*?)(?=^## |\Z)", sites, re.M | re.S)
    slugs = 0
    for line in (m.group(1).splitlines() if m else []):
        lm = re.match(r"^- \*\*(?!Dead)[^*]+:\*\*(.*)$", line)
        if lm and "(seed)" not in lm.group(1):  # the shipped seed list doesn't count
            slugs += len([s for s in lm.group(1).split(",") if s.strip()])
    put("job-sources", [("job_search.regions", filled(p.get("job_search", {}).get("regions"))),
                        (f"10+ companies in the ATS slug sweep (have {slugs})", slugs >= 10)])

    summary = read("CV/summary.md")
    cvs = [f for f in os.listdir(os.path.join(ROOT, "CV")) if f.endswith(".pdf")] if os.path.isdir(os.path.join(ROOT, "CV")) else []
    put("cvs", [("a base CV PDF in CV/", bool(cvs)),
                ("every CV registered in CV/summary.md", bool(cvs) and all(f in summary for f in cvs))])
    return out

def render(p):
    n, c, r, a, s, t = (p.get(k, {}) for k in ("names", "contact", "right_to_work", "availability", "salary", "targets"))
    if not n.get("full_name"):
        block = "_Not onboarded yet. Run `/onboard-me`._"
    else:
        jobs = p.get("career_history", [])
        hist = "; ".join(f"{j.get('organisation')} — {j.get('title')}, {j.get('start')} – {'present' if j.get('current') else j.get('end')}" for j in jobs)
        langs = ", ".join(f"{l.get('language')} ({l.get('level')})" for l in p.get("languages", []))
        sal = f"{s.get('currency', '')} {s.get('default', 0):,} per {s.get('period', 'year')}" if s.get("default") else "not set"
        links = " · ".join(x for x in (c.get("linkedin"), c.get("github"), c.get("website")) if x)
        lines = [
            f"- **Name:** {n['full_name']}. First **{n.get('first_name')}**" + (f", middle **{n['middle_name']}** (Middle Name fields only, never in Last Name)" if n.get("middle_name") else "") + f", last **{n.get('last_name')}**." + (f" Goes by {n['preferred_name']}." if n.get("preferred_name") else ""),
            f"- **Pronouns:** {p.get('pronouns') or 'not given (ask)'} · **Nationality:** {p.get('nationality') or 'not given'}",
            f"- **Email:** {c.get('email')} · **Phone:** {c.get('phone')}",
            f"- **Location:** {', '.join(x for x in (c.get('city'), c.get('country')) if x)}" + (" (street address in profile.json, only for forms that require it)" if c.get("street_address") else ""),
            f"- **Links:** {links or 'none'}",
            f"- **Right to work:** {r.get('statement') or 'not set'}",
            f"- **Availability:** {a.get('statement') or 'not set'}" + (f" Never write: {', '.join(repr(x) for x in a.get('never_say', []))}." if a.get("never_say") else ""),
            f"- **Salary default:** {sal} (rule in `.claude/skills/apply/SKILL.md`, Step 6)",
            f"- **Targets:** {', '.join(t.get('titles', [])) or 'not set'} · {', '.join(t.get('work_modes', []))}",
            f"- **Career history (canonical, overrides any CV PDF):** {hist or 'not set'}",
            f"- **Languages:** {langs or 'not set'}",
        ]
        block = "\n".join(lines)
    text = read(".claude/CLAUDE.md")
    if START not in text or END not in text:
        sys.exit("CLAUDE.md has no candidate markers")
    text = text[:text.index(START) + len(START)] + "\n" + block + "\n" + text[text.index(END):]
    open(CLAUDE_MD, "w", encoding="utf-8").write(text)

def main():
    args = sys.argv[1:]
    p = load()
    today = dt.date.today().isoformat()
    if "--mark" in args:
        ob = p.setdefault("onboarding", {})
        for sec in args[args.index("--mark") + 1:]:
            if sec.startswith("--"):
                break
            if sec not in [k for k, _, _ in SECTIONS]:
                sys.exit(f"unknown section {sec}; use one of: {', '.join(k for k, _, _ in SECTIONS)}")
            if sec not in ob.setdefault("sections_done", []):
                ob["sections_done"].append(sec)
        ob["started"] = ob.get("started") or today
        ob["last_run"] = today
        json.dump(p, open(PROFILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(PROFILE, "a").write("\n")

    errors, warnings = validate(p)
    st = status(p)
    done = set(p.get("onboarding", {}).get("sections_done", []))
    print("Section                       State     Missing")
    for key, title, required in SECTIONS:
        state, missing = st[key]
        mark = state if state != "done" or key in done else "done*"
        print(f"{key:<29} {mark:<9} {'; '.join(missing)}{'' if required else '  (optional)'}")
    print("(done* = the data is there but the section wasn't confirmed with the user in a run yet)")
    for e in errors:
        print("ERROR   " + e)
    for w in warnings:
        print("warning " + w)
    oq = p.get("onboarding", {}).get("open_questions", [])
    if oq:
        print(f"Open questions saved for later: {len(oq)}")
        for q in oq:
            print("  - " + q)
    req_missing = [k for k, _, req in SECTIONS if req and st[k][0] != "done"]
    print("Required sections still incomplete: " + (", ".join(req_missing) or "none"))

    if "--render" in args or "--finish" in args:
        render(p)
        print("CLAUDE.md candidate block rewritten")
    if "--finish" in args:
        ob = p.setdefault("onboarding", {})
        ob["runs"] = ob.get("runs", 0) + 1
        ob["last_run"] = today
        if not errors and not req_missing:
            ob["completed"] = ob.get("completed") or today
        json.dump(p, open(PROFILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(PROFILE, "a").write("\n")
        print(f"run {ob['runs']} recorded; onboarding.completed = {ob.get('completed') or 'not yet (required sections missing)'}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
