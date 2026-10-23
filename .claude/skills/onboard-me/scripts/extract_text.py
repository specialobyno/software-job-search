#!/usr/bin/env python3
"""Print the text of uploaded files so /onboard-me can read them.

    python3 -I .claude/skills/onboard-me/scripts/extract_text.py <file> [<file> ...]

PDF → pdftotext -layout (poppler); DOCX → the document XML (no extra packages);
TXT/MD → as is; RTF/DOC/ODT/Pages → textutil (macOS) or pandoc when installed.
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile

def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'")):
        text = text.replace(a, b)
    return text

def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        if not shutil.which("pdftotext"):
            return "[pdftotext missing: install poppler (see dependencies.md)]"
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    if ext == ".docx":
        return docx_text(path)
    if ext in (".txt", ".md", ".csv", ".json", ".html"):
        return open(path, encoding="utf-8", errors="replace").read()
    if shutil.which("textutil"):
        return subprocess.run(["textutil", "-convert", "txt", "-stdout", path], capture_output=True, text=True).stdout
    if shutil.which("pandoc"):
        return subprocess.run(["pandoc", "-t", "plain", path], capture_output=True, text=True).stdout
    return f"[can't read {ext} files here: export it as PDF or DOCX]"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    for path in sys.argv[1:]:
        print(f"===== {path}")
        try:
            text = extract(path)
        except Exception as e:  # a corrupt or password-protected file
            text = f"[could not read: {e}]"
        words = len(text.split())
        print(text.strip())
        if words < 50:
            print(f"[only {words} words extracted: it may be a scanned image. Ask for a text-based PDF or DOCX]")
    return 0

if __name__ == "__main__":
    sys.exit(main())
