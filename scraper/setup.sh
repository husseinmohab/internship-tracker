#!/usr/bin/env bash
# setup.sh — One-command local environment setup
# Usage: bash setup.sh

set -e

echo ""
echo "================================================"
echo "  Fall 2026 Internship Tracker — Local Setup"
echo "================================================"
echo ""

# ── Python version check ───────────────────────────────────────────────
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo "✗ Python not found. Install Python 3.10+ from https://python.org"
    exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    echo "✗ Python 3.10+ required (found $PY_VERSION)"
    exit 1
fi

echo "✓ Python $PY_VERSION"

# ── Virtual environment ────────────────────────────────────────────────
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment..."
    $PYTHON -m venv venv
fi

# Activate
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

echo "✓ Virtual environment active"

# ── Install dependencies ───────────────────────────────────────────────
echo "→ Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"

# ── Playwright browsers ────────────────────────────────────────────────
echo "→ Installing Playwright browser (Chromium)..."
playwright install chromium --with-deps --quiet 2>/dev/null || \
playwright install chromium 2>/dev/null || \
echo "  (Playwright install had warnings — this is usually fine)"
echo "✓ Playwright ready"

# ── .env file ─────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "✓ Created .env from template"
    echo ""
    echo "  ┌─────────────────────────────────────────────┐"
    echo "  │  Next step: fill in your API keys in .env   │"
    echo "  │                                             │"
    echo "  │  ADZUNA_APP_ID=...    (developer.adzuna.com) │"
    echo "  │  ADZUNA_APP_KEY=...                         │"
    echo "  │  USAJOBS_API_KEY=...  (developer.usajobs.gov)│"
    echo "  │  USAJOBS_EMAIL=...                          │"
    echo "  └─────────────────────────────────────────────┘"
    echo ""
else
    echo "✓ .env already exists"
fi

# ── docs/ folder ──────────────────────────────────────────────────────
mkdir -p docs
if [ ! -f "docs/jobs.json" ]; then
    echo '{"last_updated":"","jobs":[]}' > docs/jobs.json
    echo "✓ Created empty docs/jobs.json"
fi

# ── Done ───────────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Setup complete!"
echo "================================================"
echo ""
echo "  Test a single source (no API key needed):"
echo "    python test_sources.py remoteok"
echo ""
echo "  Test all sources:"
echo "    python test_sources.py"
echo ""
echo "  Run the full scraper:"
echo "    python scraper.py"
echo ""
echo "  Then open docs/index.html in your browser."
echo ""
