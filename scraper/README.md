# Fall 2026 Internship Tracker

A daily scraper that monitors 8 job sources, filters for roles starting after
**August 6 2026**, deduplicates across runs, and serves everything through a
clean static dashboard hosted for free on GitHub Pages.

---

## How it works

```
GitHub Actions (8 AM EST daily)
    │
    ├── Layer 1: APIs          Adzuna · USAJobs · RemoteOK
    ├── Layer 2: ATS           Greenhouse (~65 companies) · Lever (~40 companies)
    ├── Layer 3: Universities  Ivy League + NYC-area schools + national labs
    ├── Layer 4: Workday       ~90 large enterprises (JPMorgan, Amazon, Google…)
    └── Layer 4b: iCIMS        Banks + Big 4 consulting (SMBC, Citi, Deloitte…)
            │
            ▼
    normalize → filter → deduplicate → docs/jobs.json
            │
            ▼
    GitHub Pages → your dashboard
```

**Target roles:** Data Engineering · Data Analyst / BI · Data Science ·
Research Engineering · Research Assistant / REU · Software Engineering

**Date filter:** Only internships starting on or after Aug 6 2026.
Jobs with no stated start date are kept but flagged as "date unconfirmed"
— you can hide them with the toggle on the dashboard.

---

## Repo structure

```
├── scraper.py                  Main orchestrator
├── config.py                   ← Edit this to add companies / keywords
├── requirements.txt
├── test_sources.py             Test any source locally before deploying
├── setup.sh                    One-command local setup
├── .env.example                Copy to .env, fill in API keys
├── .gitignore
│
├── sources/
│   ├── adzuna.py               Adzuna Jobs API
│   ├── usajobs.py              USAJobs API (federal / research roles)
│   ├── remoteok.py             RemoteOK (no key needed)
│   ├── greenhouse.py           Greenhouse ATS public JSON API
│   ├── lever.py                Lever ATS public JSON API
│   ├── universities.py         Ivy League + NYC research pages
│   ├── workday.py              Workday CXS API
│   └── icims.py                iCIMS career pages
│
├── utils/
│   ├── normalize.py            Title / location / type cleanup
│   ├── filter.py               Role classifier + date filter
│   ├── dedup.py                Deduplication across daily runs
│   └── http.py                 Async HTTP with retry + backoff
│
├── docs/                       Served by GitHub Pages
│   ├── index.html              Dashboard (the website)
│   ├── jobs.json               Auto-written by scraper daily
│   └── run_log.json            Scraper health log (shown in dashboard)
│
└── .github/workflows/
    └── scrape.yml              GitHub Actions — runs daily at 8 AM EST
```

---

## Setup (15–20 minutes total)

### Step 1 — Create a private GitHub repo

```bash
# On github.com: New repo → name it "internship-tracker" → Private → Create
git clone https://github.com/YOUR_USERNAME/internship-tracker.git
cd internship-tracker
```

### Step 2 — Copy files into the repo

Unzip the downloaded archive and copy everything into your cloned repo,
keeping the folder structure intact. Then:

```bash
git add .
git commit -m "initial setup"
git push
```

### Step 3 — Get free API keys

**Adzuna** (best free coverage — takes 2 minutes)
1. Go to https://developer.adzuna.com/
2. Sign up → My Apps → Create App
3. Copy your **App ID** and **App Key**

**USAJobs** (federal + research roles — instant approval)
1. Go to https://developer.usajobs.gov/
2. Fill out the form → check your email
3. Copy your **API Key** (your email is used as the User-Agent)

**RemoteOK** — no key needed, works out of the box.

### Step 4 — Add secrets to GitHub

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret name       | Value                   |
|-------------------|-------------------------|
| `ADZUNA_APP_ID`   | Your Adzuna App ID      |
| `ADZUNA_APP_KEY`  | Your Adzuna App Key     |
| `USAJOBS_API_KEY` | Your USAJobs API key    |
| `USAJOBS_EMAIL`   | Your email address      |

### Step 5 — Enable GitHub Pages

In your repo: **Settings → Pages**
- Source: **Deploy from a branch**
- Branch: `main` · Folder: `/docs`
- Save

Your dashboard will be live at:
`https://YOUR_USERNAME.github.io/internship-tracker/`

### Step 6 — Trigger the first run

1. Go to your repo → **Actions** tab
2. Click **Daily Internship Scraper** → **Run workflow** → **Run workflow**
3. Wait ~5–10 minutes
4. Refresh your GitHub Pages URL — jobs appear

After the first run, everything is automatic. The scraper runs every morning
at 8 AM EST, pushes updated `jobs.json`, and your dashboard refreshes on load.

---

## Local development

```bash
# One-command setup:
bash setup.sh

# Then fill in your keys:
cp .env.example .env
# edit .env with your Adzuna + USAJobs credentials

# Test individual sources before a full run:
python test_sources.py remoteok          # test one source (no key needed)
python test_sources.py greenhouse lever  # test multiple
python test_sources.py                   # test all

# Full run:
python scraper.py
# Results written to docs/jobs.json — open docs/index.html in your browser
```

---

## Customization

### Add a Greenhouse company

In `config.py`, add to `GREENHOUSE_COMPANIES`:
```python
("company-slug", "Display Name"),
```
Find the slug from their URL: `boards.greenhouse.io/SLUG`

### Add a Lever company

In `config.py`, add to `LEVER_COMPANIES`:
```python
("company-slug", "Display Name"),
```
Find the slug from: `jobs.lever.co/SLUG`

### Add a Workday company

In `config.py`, add to `WORKDAY_COMPANIES`:
```python
("tenant-slug", "Display Name"),
```
Find the tenant from their careers URL: `TENANT.wd5.myworkdayjobs.com`

### Add a university

In `config.py`, add to `UNIVERSITIES`:
```python
{
    "name": "MIT",
    "urls": [
        "https://www.eecs.mit.edu/research/undergraduate-research/",
    ],
},
```

### Change the start date cutoff

```python
# config.py
START_AFTER = "2026-08-06"   # change this
```

### Add role keywords

In `config.py`, edit `ROLE_KEYWORDS`. First match wins — keep specific phrases first.

---

## Dashboard features

- **Stats bar** — total jobs, new today, saved, applied
- **Role filters** — Data Eng · Data Analyst · Data Science · SWE · Research Eng · Research / REU
- **Status filters** — All · New · Saved · Applied
- **Hide unconfirmed** — hides jobs with no stated start date
- **Sort** — newest first · oldest first · company A–Z
- **Search** — by title, company, or location
- **Per-card actions** — Save · Applied · Skip (toggleable, stored in browser localStorage)
- **"Date unconfirmed" badge** — amber badge on jobs where start date isn't stated
- **Source health panel** — shows each scraper source's status from the last run

---

## Troubleshooting

**No jobs appearing after first run**
- Check Actions → the run log for errors
- Make sure your 4 secrets are set correctly
- Try running locally: `python test_sources.py remoteok` (no key needed)

**Too many summer roles showing up**
- Add phrases to `EXCLUDE_SIGNALS` in `config.py`
- Use the "Hide unconfirmed" toggle to filter ambiguous postings

**A company returns 0 results**
- Their Greenhouse/Lever/Workday slug may be wrong
- Check their actual careers URL to find the correct slug
- Workday tenants sometimes use `wd1`/`wd3` instead of `wd5` — the scraper tries all three

**Workday companies all failing**
- Some large companies use custom Workday domains — check their careers page URL directly

**University pages returning nothing**
- University pages change structure frequently — update the URL in `config.py`
- The heuristic extractor works best on pages with clear `<a>` or `<h3>` tags around job titles
