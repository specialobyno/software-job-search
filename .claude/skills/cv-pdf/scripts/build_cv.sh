#!/usr/bin/env bash
# Build an ATS-friendly CV PDF from HTML and verify it against profile.json.
# Usage: build_cv.sh <source.html> <output.pdf> [preview_dir]
#   e.g. build_cv.sh CV/source/Ada_Obi_Backend_Engineer_Nodejs.html CV/Ada_Obi_Backend_Engineer_Nodejs.pdf
set -uo pipefail

SRC="${1:?usage: build_cv.sh <source.html> <output.pdf> [preview_dir]}"
OUT="${2:?usage: build_cv.sh <source.html> <output.pdf> [preview_dir]}"
PREVIEW_DIR="${3:-${TMPDIR:-/tmp}/cv-preview/$(basename "${OUT%.pdf}")}"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
CONFIG="$ROOT/profile.json"

for bin in weasyprint pdftotext pdfinfo pdffonts pdftoppm python3; do
  command -v "$bin" >/dev/null || { echo "FAIL: $bin not installed (see dependencies.md)"; exit 1; }
done
[ -f "$SRC" ] || { echo "FAIL: source not found: $SRC"; exit 1; }
[ -f "$CONFIG" ] || { echo "FAIL: $CONFIG not found"; exit 1; }
grep -q '{{' "$SRC" && { echo "FAIL: the source still has {{PLACEHOLDERS}}:"; grep -o '{{[^}]*}}' "$SRC" | sort -u | head -20; exit 1; }

fail=0
pass() { echo "  ok    $1"; }
bad()  { echo "  FAIL  $1"; fail=1; }
warn() { echo "  warn  $1"; }

echo "== Rendering"
weasyprint --pdf-variant pdf/ua-1 "$SRC" "$OUT" 2>&1 | grep -v -e '^$' || true
[ -s "$OUT" ] || { echo "FAIL: no PDF produced"; exit 1; }
echo "  -> $OUT"

echo "== Structure"
info="$(pdfinfo "$OUT")"
pages="$(awk '/^Pages:/{print $2}' <<<"$info")"
grep -q '^Tagged:[[:space:]]*yes' <<<"$info" && pass "tagged PDF (PDF/UA)" || bad "PDF is not tagged"
grep -q 'A4' <<<"$info" && pass "A4 page size" || warn "page size is not A4 (fine if profile.json cv_rules.page_size is Letter)"
if [ "$pages" -ge 1 ] && [ "$pages" -le 2 ]; then pass "$pages page(s)"; else warn "$pages pages (target 1–2)"; fi
if pdffonts "$OUT" | awk 'NR>2 && $(NF-4)!="yes"{exit 1}'; then pass "all fonts embedded"; else bad "a font is not embedded"; fi

echo "== Text extraction and profile.json rules (what an ATS sees)"
text="$(pdftotext -layout "$OUT" -)"
if ! printf '%s' "$text" | python3 -I -c '
import json, re, sys
sys.stdin.reconfigure(encoding="utf-8", errors="replace")
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
t = sys.stdin.read()
low = t.lower()
flat = re.sub(r"\s+", " ", low)
fail = False
def ok(m): print("  ok    " + m)
def bad(m):
    global fail; fail = True; print("  FAIL  " + m)
def warn(m): print("  warn  " + m)

n = len(t.split())
ok(f"text layer present ({n} words)") if n > 150 else bad("little or no extractable text")
rules = cfg.get("cv_rules", {})
c = cfg.get("contact", {})
must = [x for x in rules.get("must_contain", []) if x] or [c.get("email", ""), c.get("phone", ""), c.get("linkedin", "")]
for m in [x for x in must if x]:
    ok("found: " + m) if m.lower() in low else bad("missing from extracted text: " + m)
name = cfg.get("names", {}).get("full_name", "")
if name:
    ok("name: " + name) if name.lower() in flat else bad("full name missing: " + name)
for h in rules.get("required_headings", ["Experience", "Education"]):
    ok("heading containing: " + h) if h.lower() in low else bad("no heading containing: " + h)
bad("garbled characters (mojibake): add <meta charset=\"utf-8\"> to the HTML head") if re.search("â€|Ã[\u0080-¿]|�", t) else ok("no garbled characters")
bad("ligature glyphs found (fi/fl): keywords may not match") if re.search("[ﬀ-ﬆ]", t) else ok("no ligature glyphs")
banned = list(rules.get("banned_terms", []))
for job in cfg.get("career_history", []):
    banned += job.get("never_say", [])
for term in [b for b in banned if b]:
    bad("banned term present: " + term) if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", t, re.I) else ok("no " + term)
for term in rules.get("warn_terms", []):
    if term and re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", t, re.I): warn("check this term: " + term)
current = [j for j in cfg.get("career_history", []) if j.get("current")]
present = re.findall(r"[–—-]\s*present\b", t, re.I)
if present and not current:
    bad("\"– Present\" found, but profile.json has no current job")
elif len(present) > len(current) + sum(1 for e in cfg.get("education", []) if e.get("status") == "in progress"):
    warn("more \"– Present\" dates than current roles/studies in profile.json")
for job in cfg.get("career_history", []):
    org = job.get("organisation", "")
    if org and org.lower() in flat:
        titles = [x for x in [job.get("title", "")] + job.get("title_options", []) if x]
        if not any(x.lower() in flat for x in titles):
            warn(org + ": none of the allowed titles found (" + ", ".join(titles) + ")")
        end = "Present" if job.get("current") else job.get("end", "")
        dates = job.get("start", "") + " – " + end
        if job.get("start") and dates.lower() not in flat:
            warn(org + ": dates not found as " + dates)
    elif org:
        warn(f"{org} (career_history) is not on this CV: fine only if it was left out on purpose")
sys.exit(1 if fail else 0)
' "$CONFIG"; then fail=1; fi

echo "== Previews"
mkdir -p "$PREVIEW_DIR"
rm -f "$PREVIEW_DIR"/page-*.png
pdftoppm -r 80 -png "$OUT" "$PREVIEW_DIR/page"
ls "$PREVIEW_DIR"/page-*.png | sed 's/^/  /'

echo "== Extracted text"
echo "$text"

echo
[ $fail -eq 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL — fix the source (or profile.json) and rebuild"
exit $fail
