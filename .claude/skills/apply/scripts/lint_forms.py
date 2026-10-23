#!/usr/bin/env python3
"""Lint an application's forms.md against profile.json and facts.md.

    python3 .claude/skills/apply/scripts/lint_forms.py jobs/<job>/forms.md [...]
    python3 .claude/skills/apply/scripts/lint_forms.py --hook     # PostToolUse hook (tool-call JSON on stdin)

Checks only what gets sent: the Application Form Fields and Cover Letter sections,
skipping notes to the user (lines starting with ">"). Errors break a hard rule; warnings need a look.
Exit 1 (2 in --hook mode) on errors.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
STAGES = {"drafted", "filled", "blocked", "unknown", "submitted", "interviewing", "offer", "rejected", "withdrawn", "closed"}
SENT = {"submitted", "interviewing", "offer", "rejected", "withdrawn", "closed"}

def profile():
    p = os.path.join(ROOT, "profile.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

def answer_lines(text):
    out, on = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            t = line[3:].lower()
            on = t.startswith(("application form fields", "cover letter", "form fields", "answers"))
            continue
        if on and not line.lstrip().startswith((">", "###", "**Type:**", "**Required:**")):
            out.append((n, line))
    return out

def never_claim():
    """Bullets in facts.md "## 4. Never claim" (text before any parenthesis)."""
    p = os.path.join(ROOT, "facts.md")
    if not os.path.exists(p):
        return []
    m = re.search(r"^## 4\. Never claim\s*$(.*?)(?=^## |\Z)", open(p, encoding="utf-8").read(), re.M | re.S)
    if not m:
        return []
    items = [re.sub(r"\(.*?\)", "", l.lstrip("-* ").strip()).strip(" \"'`") for l in m.group(1).splitlines()
             if l.strip().startswith(("-", "*"))]
    return [i for i in items if i and "{{" not in i and len(i) < 60]

def lint(path, cfg):
    text = open(path, encoding="utf-8").read()
    errors, warnings = [], []
    head = text.split("\n---", 1)[0]
    sm = re.search(r"^\*\*Stage:\*\*\s*(\S+)", head, re.M)
    stage = sm.group(1).lower() if sm else ""
    if not sm:
        errors.append("header has no **Stage:** line (values in /status)")
    elif stage not in STAGES:
        errors.append(f"unknown Stage \"{stage}\" (use one of: {', '.join(sorted(STAGES))})")

    for label in ("CV to use for this application", "Recommended CV"):
        m = re.search(rf"{re.escape(label)}:?\**:?\s*`(?:[^`]*/)?([^`/]+\.pdf)`", text)
        if m:
            if not os.path.exists(os.path.join(ROOT, "CV", m.group(1))):
                errors.append(f"{label}: `{m.group(1)}` isn't in CV/")
            break
    else:
        if stage not in SENT:
            warnings.append("no \"**CV to use for this application:**\" line naming a PDF in CV/")

    names = cfg.get("names", {})
    middle, last = names.get("middle_name", ""), names.get("last_name", "")
    for m in re.finditer(r"^###\s*(Last name|Surname|Family name)[^\n]*\n(.*?)(?=^###|\Z)", text, re.I | re.M | re.S):
        if middle and re.search(rf"\b{re.escape(middle)}\b", m.group(2)):
            errors.append(f"Last Name field contains the middle name \"{middle}\" (Last = {last}; middle only in a Middle Name field)")

    rules = cfg.get("cv_rules", {})
    banned = list(rules.get("banned_terms", [])) + never_claim() + list(cfg.get("availability", {}).get("never_say", []))
    for job in cfg.get("career_history", []):
        banned += job.get("never_say", [])
    warn = list(rules.get("warn_terms", [])) + list(cfg.get("writing", {}).get("avoid", []))
    for n, line in answer_lines(text):
        for term in banned:
            if term and re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", line, re.I):
                errors.append(f"line {n}: \"{term}\" must never be used (profile.json never_say / banned_terms, or facts.md Section 4)")
        for term in warn:
            if term and re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", line, re.I):
                warnings.append(f"line {n}: check \"{term}\" (profile.json writing.avoid / warn_terms)")
        if re.search(r"\{\{[^}]*\}\}", line):
            errors.append(f"line {n}: unfilled {{{{placeholder}}}}")
        for job in cfg.get("career_history", []):
            if not job.get("current") and job.get("organisation") and re.search(
                    rf"\b(I|currently) (work|am working|am) (at|for) {re.escape(job['organisation'])}\b", line, re.I):
                warnings.append(f"line {n}: {job['organisation']} in the present tense, but it ended {job.get('end')}")

    # Salary: when the header gives an annual range and a salary field exists
    sal = cfg.get("salary", {})
    default = sal.get("default") or 0
    m = re.search(r"\*\*Salary:\*\*\s*(.+)$", head, re.M)
    has_field = re.search(r"^###[^\n]*(salary|compensation|pay expectation|expected pay|remuneration)", text, re.I | re.M)
    if default and m and has_field and not re.search(r"month|/mo|hour|day|net", m.group(1), re.I):
        nums = [float(x.replace(",", "")) * (1000 if k else 1) for x, k in re.findall(r"[€£$]\s*([\d,.]+)\s*([kK])?", m.group(1))]
        if len(nums) >= 2 and all(x > 1000 for x in nums[:2]):
            lo, hi = sorted(nums[:2])
            want = hi if hi < default else (round((lo + hi) / 2 / 1000) * 1000 if lo > default else default)
            if f"{int(want):,}" not in text and f"{int(want / 1000)}k" not in text.lower():
                warnings.append(f"salary range {lo:,.0f}–{hi:,.0f} → the salary rule gives {int(want):,}, which isn't in the answers")

    if stage in SENT and errors:  # already sent: nothing to fix in the form, but stay consistent with it
        warnings = [f"{e} (already sent: stay consistent, or note it in facts.md)" for e in errors] + warnings
        errors = []
    return errors, warnings

def report(path, errors, warnings):
    lines = [f"{os.path.relpath(path, ROOT)}: {len(errors)} error(s), {len(warnings)} warning(s)"]
    return "\n".join(lines + [f"  ERROR   {e}" for e in errors] + [f"  warning {w}" for w in warnings])

def main():
    cfg = profile()
    if "--hook" in sys.argv:
        try:
            data = json.load(sys.stdin)
        except Exception:
            return 0
        path = (data.get("tool_input") or {}).get("file_path", "")
        if not path.endswith("/forms.md") or not os.path.exists(path):
            return 0
        errors, warnings = lint(path, cfg)
        if errors:
            print(report(path, errors, warnings) + "\nFix these in forms.md (rules: profile.json, facts.md, .claude/CLAUDE.md).", file=sys.stderr)
            return 2
        if warnings:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": report(path, errors, warnings)}}))
        return 0
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 1
    failed = False
    for p in paths:
        errors, warnings = lint(p, cfg)
        print(report(p, errors, warnings))
        failed |= bool(errors)
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
