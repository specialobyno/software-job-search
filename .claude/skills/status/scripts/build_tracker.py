#!/usr/bin/env python3
"""Build applications.md: one table of every application, read from each job folder.

An application is jobs/<company>-<role>/forms.md with a **Stage:** line. Run from anywhere:

    python3 .claude/skills/status/scripts/build_tracker.py [--today YYYY-MM-DD]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
JOBS = os.path.join(ROOT, "jobs")
STAGES = ["interviewing", "offer", "filled", "blocked", "drafted", "unknown",
          "submitted", "rejected", "withdrawn", "closed"]
FOLLOW_UP_DAYS = 10   # first nudge
GO_COLD_DAYS = 21     # suggest marking closed

def header_field(text, name):
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""

def parse_date(s):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s or "")
    return dt.date.fromisoformat(m.group(1)) if m else None

def cv_prefix():
    try:
        cfg = json.load(open(os.path.join(ROOT, "profile.json"), encoding="utf-8"))
    except Exception:
        return ""
    return cfg.get("cv_rules", {}).get("file_prefix", "")

def read_app(d):
    p = os.path.join(JOBS, d, "forms.md")
    if not os.path.exists(p):
        return None
    text = open(p, encoding="utf-8").read()
    if "**Stage:**" not in text:
        return None
    head = text.split("\n---", 1)[0]
    title = re.sub(r"^#\s*(Application:\s*)?", "", head.splitlines()[0]).strip()
    role, _, company = title.partition(" — ")
    stage_line = header_field(head, "Stage")
    stage = (stage_line.split() or [""])[0].lower()
    m = re.search(r"\*\*Applied:\*\*\s*(~?\d{4}-\d{2}-\d{2})", stage_line)
    applied = m.group(1) if m else ""
    m = re.search(r"https?://[^\s)>`]+", header_field(head, "URL") or head)
    url = m.group(0).rstrip(".,") if m else ""
    m = re.search(r"`(?:CV/)?([^`/]+\.pdf)`", head)
    interview = ""
    ip = os.path.join(JOBS, d, "interview-process.md")
    if os.path.exists(ip):
        interview = header_field(open(ip, encoding="utf-8").read(), "Current stage")
    return {
        "dir": d, "role": role.strip(), "company": company.strip() or d, "stage": stage,
        "applied": applied, "date": header_field(head, "Date"), "url": url,
        "source": urlparse(url).netloc.replace("www.", "") if url else "",
        "cv": m.group(1) if m else "", "interview": interview, "file": f"jobs/{d}/forms.md",
    }

def next_action(a, today):
    s = a["stage"]
    if s == "interviewing":
        return a["interview"] or "update interview-process.md (/interview)"
    if s == "offer":
        return "review the offer"
    if s == "filled":
        return "review the filled form and say \"yes, submit\" (or submit yourself)"
    if s == "blocked":
        return "submit manually (see Status in forms.md)"
    if s == "drafted":
        return "finish and submit (/apply Step 9)"
    if s == "unknown":
        return "confirm whether it was sent, then set Stage"
    if s == "submitted":
        d = parse_date(a["applied"]) or parse_date(a["date"])
        if d:
            age = (today - d).days
            if age >= GO_COLD_DAYS:
                return f"no reply after {age} days: mark closed, or one last follow-up"
            if age >= FOLLOW_UP_DAYS:
                return f"follow-up due ({age} days since applying)"
        return "wait for a reply"
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.today)
    prefix = cv_prefix()
    short = lambda cv: (cv[len(prefix):] if prefix and cv.startswith(prefix) else cv).replace(".pdf", "").strip("_")

    apps = []
    if os.path.isdir(JOBS):
        for d in sorted(os.listdir(JOBS)):
            if os.path.isdir(os.path.join(JOBS, d)):
                a = read_app(d)
                if a:
                    a["next"] = next_action(a, today)
                    apps.append(a)

    unknown_stages = [a for a in apps if a["stage"] not in STAGES]
    order = {s: i for i, s in enumerate(STAGES)}
    apps.sort(key=lambda a: (order.get(a["stage"], 99), -(parse_date(a["applied"]) or parse_date(a["date"]) or dt.date.min).toordinal()))
    counts = Counter(a["stage"] for a in apps)
    sent = [a for a in apps if a["stage"] in ("submitted", "interviewing", "offer", "rejected", "closed")]
    attention = [a for a in apps if a["stage"] in ("interviewing", "offer", "filled", "blocked", "drafted", "unknown")
                 or "follow-up" in a["next"] or "no reply" in a["next"]]
    week_ago = today - dt.timedelta(days=7)
    sent_week = sum(1 for a in apps if (parse_date(a["applied"]) or dt.date.min) >= week_ago)

    out = [
        "# Applications", "",
        f"_Generated {today.isoformat()} by `/status` from each `jobs/*/forms.md` **Stage:** line. Don't edit this file; edit the Stage line and re-run `/status`._", "",
        "**Totals:** " + (" · ".join(f"{s} {counts[s]}" for s in STAGES if counts[s]) or "none yet")
        + f" · **{len(apps)} in all** · sent in the last 7 days: {sent_week}", "",
        "## Needs your attention", "",
    ]
    if attention:
        out += ["| Company | Role | Stage | Next action |", "|---|---|---|---|"]
        out += [f"| {a['company']} | [{a['role']}]({a['file']}) | {a['stage']} | {a['next']} |" for a in attention]
    else:
        out.append("Nothing waiting on you.")
    out += ["", "## All applications", "",
            "| Company | Role | Stage | Applied | CV | Source | Next action |", "|---|---|---|---|---|---|---|"]
    out += [f"| {a['company']} | [{a['role']}]({a['file']}) | {a['stage']} | {a['applied'] or '–'} | {short(a['cv'])} | {a['source']} | {a['next']} |" for a in apps]

    # What converts: interviews by CV and by source, among applications actually sent.
    def conv(key):
        tally = defaultdict(lambda: [0, 0])
        for a in sent:
            k = a[key] or "unknown"
            tally[k][0] += 1
            tally[k][1] += a["stage"] in ("interviewing", "offer")
        return sorted(tally.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))
    if sent:
        for label, key in (("CV", "cv"), ("Source", "source")):
            out += ["", f"## Interviews by {label}", "", f"| {label} | Sent | Interviews |", "|---|---|---|"]
            out += [f"| {short(k) if key == 'cv' else k} | {n} | {i} |" for k, (n, i) in conv(key)]

    if unknown_stages:
        out += ["", "## Unrecognised Stage values", ""]
        out += [f"- `{a['file']}`: \"{a['stage']}\" (use one of: {', '.join(STAGES)})" for a in unknown_stages]

    open(os.path.join(ROOT, "applications.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"applications.md: {len(apps)} applications" + ("; " + ", ".join(f"{s} {counts[s]}" for s in STAGES if counts[s]) if apps else ""))
    print(f"needs attention: {len(attention)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
