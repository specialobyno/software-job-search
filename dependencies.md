# Setup prompt: install everything this repo needs

**How to use this file:** open a terminal in this folder, start Claude Code (`claude`), and type:

> Follow dependencies.md

Claude then checks your machine, installs only what's missing (asking before anything that needs your password), tells you the few things you have to click yourself, and verifies that everything works. You can run it again at any time; it skips what's already installed.

---

## Instructions for Claude

You are setting up this machine for this job-search repo. Work through the steps below **in order**. For every item: **check first** (`command -v`, `--version`), and install only if it's missing or too old. Before any command that needs `sudo`, installs a package manager, or changes system settings, say what it does and ask for a yes. Show progress as a short checklist, and finish with the summary table in step 7. Never ask for or type the user's passwords: when `sudo` or an installer prompts for one, tell the user to type it into the terminal themselves (suggest running the command with the `!` prefix so it runs in this session).

### 1. Detect the system

`uname -s`, `uname -m`, and on Linux `cat /etc/os-release`. Then use the matching column below.

- **macOS:** Homebrew (`brew`).
- **Linux:** `apt` (Debian/Ubuntu) or `dnf` (Fedora/RHEL).
- **Windows:** this repo's scripts need a Unix shell. If Claude Code is running in PowerShell or CMD, stop and recommend WSL (Windows Subsystem for Linux): `wsl --install` in an admin PowerShell, restart, then clone the repo inside WSL (Ubuntu) and run this prompt again there. Chrome on Windows still works for form filling.

### 2. Package manager

- **macOS:** if `brew` is missing, ask, then install it with the official command from https://brew.sh (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`). The user types their password when prompted. Afterwards add it to the PATH as the installer says (`eval "$(/opt/homebrew/bin/brew shellenv)"` on Apple Silicon).
- **Linux:** `sudo apt update` (or nothing for `dnf`).

### 3. Command-line tools

| Tool | Why | macOS | Debian/Ubuntu | Fedora | Check |
|---|---|---|---|---|---|
| git | version history, commits | `brew install git` (or Xcode tools: `xcode-select --install`) | `sudo apt install -y git` | `sudo dnf install -y git` | `git --version` |
| Python 3.9+ | all repo scripts | `brew install python` | `sudo apt install -y python3` | `sudo dnf install -y python3` | `python3 --version` |
| Node.js LTS (20+) and npm | Claude Code itself, and handy for JS tooling | `brew install node` | NodeSource or `sudo apt install -y nodejs npm` (check the version is 20+; if not, use `nvm`: https://github.com/nvm-sh/nvm) | `sudo dnf install -y nodejs` | `node --version` |
| WeasyPrint | builds the CV PDFs | `brew install weasyprint` | `sudo apt install -y weasyprint` (or `python3 -m pip install --user weasyprint` if the package is old: need 60+) | `sudo dnf install -y weasyprint` | `weasyprint --version` |
| Poppler (`pdftotext`, `pdfinfo`, `pdffonts`, `pdftoppm`) | reads CVs, verifies PDFs, makes previews | `brew install poppler` | `sudo apt install -y poppler-utils` | `sudo dnf install -y poppler-utils` | `pdftotext -v` |
| Fonts (Arial-compatible) | the CV template uses Arial/Helvetica | built in | `sudo apt install -y fonts-liberation` | `sudo dnf install -y liberation-sans-fonts` | `fc-list \| grep -i -E 'arial\|liberation'` |
| GitHub CLI (`gh`) | creates the user's **private** repo | `brew install gh` | `sudo apt install -y gh` (or the official repo: https://github.com/cli/cli/blob/trunk/docs/install_linux.md) | `sudo dnf install -y gh` | `gh --version` |
| curl | job board APIs | built in | `sudo apt install -y curl` | built in | `curl --version` |

No Python packages are needed beyond the standard library (WeasyPrint aside).

### 4. Claude Code side

1. **Claude Code version:** `claude --version`. If it's old, suggest `claude update` (or `npm install -g @anthropic-ai/claude-code`).
2. **Skills:** this repo's skills live in `.claude/skills/` and load automatically; nothing to install. Check they're found: `ls .claude/skills`.
3. **No plugins are required.** Don't install extra plugins or MCP servers unless the user asks (they add noise and cost tokens).
4. **Claude in Chrome** (needed by `/apply` to fill forms) — **the user does this part:**
   - Install Google Chrome if it's missing (https://www.google.com/chrome/).
   - Install the "Claude" extension by Anthropic from the Chrome Web Store (search "Claude in Chrome"), sign in with the same Claude account, and pin it.
   - In Claude Code, run `/chrome` and enable it (or start Claude Code with `claude --chrome`).
   - Then test it yourself: load the `claude-in-chrome` skill and call `tabs_context_mcp`. If it answers, it works. If not, tell the user what to check (extension signed in, Chrome open, `/chrome` enabled) and move on; it's only needed at Step 9 of `/apply`.
5. **Gmail connector** (optional, used by `/inbox` and for follow-up drafts) — **the user does this part:** on claude.ai → Settings → Connectors → Gmail → Connect, with the inbox they use for applications. Restart Claude Code afterwards. Check with a ToolSearch for `Gmail`; if the tools appear, set `profile.json` → `job_search.gmail_connected` to `true`.

### 5. Make the user's copy private

This folder will hold personal data (CVs, contact details, applications). Run `git remote -v`:

- If `origin` points to the shared public template, explain why that's a problem and offer (on a yes): `git remote rename origin template`, then `gh auth login` (the user completes it in the browser), then `gh repo create <their-name>-job-search --private --source . --remote origin --push`.
- If there's no remote, offer the same `gh repo create … --private` step, or leave it local-only.
- If `origin` is already a private repo of theirs (`gh repo view --json visibility`), say so and move on.

### 6. Verify

1. `python3 .claude/skills/onboard-me/scripts/profile_check.py` runs (it will list missing sections; that's expected before onboarding).
2. `python3 .claude/skills/status/scripts/build_tracker.py` runs.
3. **CV build smoke test:** write a minimal HTML file to the scratchpad (`<!doctype html><html><head><meta charset="utf-8"><style>body{font-family:Arial,Helvetica,sans-serif}</style></head><body><h1>Test CV</h1><p>Hello</p></body></html>`), render it with `weasyprint --pdf-variant pdf/ua-1 <in.html> <out.pdf>`, then `pdfinfo <out.pdf> | grep Tagged` (should say yes) and `pdffonts <out.pdf>` (fonts embedded = yes). Delete the test files.
4. `echo '{}' | python3 .claude/skills/apply/scripts/lint_forms.py --hook; echo $?` prints `0` (the forms hook is wired up).

### 7. Summary

Finish with a table: each item, ✅ installed / already there, ⚠️ needs the user (with the exact next action), or ❌ failed (with the error). Then the next step: **`/onboard-me`** (and `/help-me` for an overview).
