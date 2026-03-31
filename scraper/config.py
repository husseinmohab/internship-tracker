"""
config.py — Central configuration for all scrapers.
Edit this file to add/remove companies, keywords, or universities.
"""

# ── Cutoff date ────────────────────────────────────────────────────────────────
# Only include internships starting ON or AFTER this date
START_AFTER = "2026-08-06"

# ── Role keywords → internal role code ────────────────────────────────────────
# Order matters: first match wins. Keep more specific phrases first.
ROLE_KEYWORDS = [
    ("de", [
        "data engineer", "data engineering", "data pipeline", "etl intern",
        "data infrastructure", "data platform", "analytics engineer",
        "data integration", "data warehouse", "lakehouse",
    ]),
    ("da", [
        "data analyst", "business intelligence", "bi analyst", "bi intern",
        "supply chain analyst", "analytics intern", "business analyst",
        "operations analyst", "reporting analyst", "insights analyst",
        "marketing analyst", "financial analyst intern", "quantitative analyst",
        "revenue analyst", "growth analyst",
    ]),
    ("ds", [
        "data scientist", "data science", "machine learning intern",
        "ml intern", "ai intern", "applied scientist", "applied ml",
        "deep learning intern", "nlp intern", "computer vision intern",
        "generative ai", "llm intern",
    ]),
    ("re", [
        "research engineer", "research engineering", "applied research intern",
        "research scientist intern", "research swe", "ai research intern",
        "ml research intern", "research fellow",
    ]),
    ("ra", [
        "research assistant", "research intern", "reu",
        "undergraduate researcher", "undergraduate research",
        "lab assistant", "computational research", "research associate intern",
        "student researcher",
    ]),
    ("swe", [
        "software engineer", "software engineering", "software developer",
        "swe intern", "backend intern", "fullstack intern",
        "full stack intern", "full-stack intern", "frontend intern",
        "platform intern", "infrastructure intern", "systems intern",
        "devops intern", "cloud intern",
    ]),
]

# ── Search query strings sent to APIs ─────────────────────────────────────────
API_QUERIES = [
    "data engineer intern fall 2026",
    "data engineering co-op fall 2026",
    "data scientist intern fall 2026",
    "data analyst intern fall 2026",
    "business intelligence intern fall 2026",
    "supply chain analyst intern fall 2026",
    "software engineer intern fall 2026",
    "research engineer intern fall 2026",
    "research assistant intern fall 2026",
    "machine learning intern fall 2026",
    "analytics engineer intern fall 2026",
    "data engineer co-op",
    "data science co-op fall",
    "software engineer co-op fall 2026",
    "ml engineer intern fall 2026",
    "ai intern fall 2026",
]

# ── Greenhouse companies ───────────────────────────────────────────────────────
# Verify slug at: https://boards.greenhouse.io/{slug}/jobs
GREENHOUSE_COMPANIES = [
    # Finance & Trading
    ("twosigma",              "Two Sigma"),
    ("citadel",               "Citadel"),
    ("hudsonrivertrading",    "Hudson River Trading"),
    ("iexcloud",              "IEX Cloud"),
    ("bloomberg",             "Bloomberg LP"),
    ("robinhood",             "Robinhood"),
    ("stripe",                "Stripe"),
    ("squareup",              "Block (Square)"),
    ("brex",                  "Brex"),
    ("ramp",                  "Ramp"),
    ("plaid",                 "Plaid"),
    ("coinbase",              "Coinbase"),
    ("kraken",                "Kraken"),
    ("chime",                 "Chime"),
    ("affirm",                "Affirm"),
    ("klarna",                "Klarna"),
    ("marqeta",               "Marqeta"),
    # Data / Analytics Platforms
    ("databricks",            "Databricks"),
    ("snowflake",             "Snowflake"),
    ("datadog",               "Datadog"),
    ("amplitude",             "Amplitude"),
    ("dbtlabs",               "dbt Labs"),
    ("fivetran",              "Fivetran"),
    ("airbyte",               "Airbyte"),
    ("starburst",             "Starburst Data"),
    ("dremio",                "Dremio"),
    ("monte-carlo",           "Monte Carlo"),
    ("atlan",                 "Atlan"),
    ("anomalo",               "Anomalo"),
    ("lightdash",             "Lightdash"),
    ("metabase",              "Metabase"),
    ("preset",                "Preset"),
    ("rudderstack",           "RudderStack"),
    ("meltano",               "Meltano"),
    ("greatexpectations",     "Great Expectations"),
    ("datafold",              "Datafold"),
    # AI / ML
    ("cohere",                "Cohere"),
    ("huggingface",           "Hugging Face"),
    ("scaleai",               "Scale AI"),
    ("weights-biases",        "Weights & Biases"),
    ("modal-labs",            "Modal"),
    ("together-ai",           "Together AI"),
    ("mistral",               "Mistral AI"),
    ("perplexity",            "Perplexity AI"),
    ("cursor",                "Cursor"),
    ("anyscale",              "Anyscale"),
    ("determined-ai",         "Determined AI"),
    ("labelbox",              "Labelbox"),
    ("snorkelai",             "Snorkel AI"),
    # Product / SaaS
    ("palantir",              "Palantir"),
    ("figma",                 "Figma"),
    ("notion",                "Notion"),
    ("airtable",              "Airtable"),
    ("asana",                 "Asana"),
    ("lattice",               "Lattice"),
    ("rippling",              "Rippling"),
    ("gusto",                 "Gusto"),
    ("benchling",             "Benchling"),
    ("retool",                "Retool"),
    ("hex",                   "Hex"),
    ("linear",                "Linear"),
    ("loom",                  "Loom"),
    ("miro",                  "Miro"),
    ("zapier",                "Zapier"),
    ("webflow",               "Webflow"),
    # Supply Chain / Logistics
    ("flexport",              "Flexport"),
    ("project44",             "Project44"),
    ("nuvocargo",             "Nuvocargo"),
    ("loadsmart",             "Loadsmart"),
    ("stord",                 "Stord"),
    ("shipbob",               "ShipBob"),
    ("leaf-logistics",        "Leaf Logistics"),
    # Healthcare / Bio
    ("flatiron",              "Flatiron Health"),
    ("tempus",                "Tempus"),
    ("ro",                    "Ro Health"),
    ("turquoise-health",      "Turquoise Health"),
    ("komodo-health",         "Komodo Health"),
    ("arcus",                 "Arcus Biosciences"),
    # Other tech
    ("cloudflare",            "Cloudflare"),
    ("hashicorp",             "HashiCorp"),
    ("fastly",                "Fastly"),
    ("supabase",              "Supabase"),
    ("vercel",                "Vercel"),
    ("netlify",               "Netlify"),
    ("render",                "Render"),
    ("fly",                   "Fly.io"),
    ("clickhouse",            "ClickHouse"),
    ("timescale",             "Timescale"),
    ("neon",                  "Neon"),
]

# ── Lever companies ────────────────────────────────────────────────────────────
# Verify slug at: https://jobs.lever.co/{slug}
LEVER_COMPANIES = [
    # Streaming / Media
    ("netflix",               "Netflix"),
    ("spotify",               "Spotify"),
    ("twitch",                "Twitch"),
    # Ride-share / Mobility
    ("lyft",                  "Lyft"),
    ("lime",                  "Lime"),
    ("bird",                  "Bird"),
    # Infrastructure / DevTools
    ("confluent",             "Confluent"),
    ("prefect",               "Prefect"),
    ("astronomer",            "Astronomer"),
    ("aiflow",                "Airflow / Apache"),
    ("census",                "Census"),
    ("hightouch",             "Hightouch"),
    ("segment",               "Segment"),
    ("statsig",               "Statsig"),
    ("split",                 "Split"),
    ("launchdarkly",          "LaunchDarkly"),
    ("mixpanel",              "Mixpanel"),
    ("heap",                  "Heap"),
    ("fullstory",             "FullStory"),
    ("contentsquare",         "ContentSquare"),
    # AI / Research adjacent
    ("deepmind",              "Google DeepMind"),
    ("inflection",            "Inflection AI"),
    ("adept",                 "Adept AI"),
    ("generally-intelligent", "Generally Intelligent"),
    ("covariant",             "Covariant"),
    ("wayve",                 "Wayve"),
    ("nuro",                  "Nuro"),
    # Finance
    ("carta",                 "Carta"),
    ("mercury",               "Mercury"),
    ("pilot",                 "Pilot"),
    ("mosaic",                "Mosaic"),
    ("alchemy",               "Alchemy"),
    # Other
    ("samsara",               "Samsara"),
    ("verkada",               "Verkada"),
    ("joby-aviation",         "Joby Aviation"),
    ("relativity-space",      "Relativity Space"),
    ("astranis",              "Astranis"),
    ("varda",                 "Varda Space"),
    ("shield-ai",             "Shield AI"),
    ("sarcos",                "Sarcos Technology"),
    ("osaro",                 "Osaro"),
    ("machina-labs",          "Machina Labs"),
]

# ── Workday companies ──────────────────────────────────────────────────────────
# Workday tenant slugs — verify at https://{tenant}.wd5.myworkdayjobs.com/
WORKDAY_COMPANIES = [
    # Big Tech
    ("amazon",                "Amazon"),
    ("google",                "Google"),
    ("microsoft",             "Microsoft"),
    ("apple",                 "Apple"),
    ("meta",                  "Meta"),
    ("ibm",                   "IBM"),
    ("oracle",                "Oracle"),
    ("sap",                   "SAP"),
    ("salesforce",            "Salesforce"),
    ("servicenow",            "ServiceNow"),
    ("workday",               "Workday"),
    ("adobe",                 "Adobe"),
    ("intuit",                "Intuit"),
    ("qualcomm",              "Qualcomm"),
    ("nvidia",                "NVIDIA"),
    ("intel",                 "Intel"),
    ("amd",                   "AMD"),
    ("broadcom",              "Broadcom"),
    ("cisco",                 "Cisco"),
    ("vmware",                "VMware"),
    # Finance
    ("jpmorgan",              "JPMorgan Chase"),
    ("goldmansachs",          "Goldman Sachs"),
    ("morganstanley",         "Morgan Stanley"),
    ("blackrock",             "BlackRock"),
    ("bofa",                  "Bank of America"),
    ("citigroup",             "Citigroup"),
    ("wellsfargo",            "Wells Fargo"),
    ("americanexpress",       "American Express"),
    ("visa",                  "Visa"),
    ("mastercard",            "Mastercard"),
    ("fidelity",              "Fidelity Investments"),
    ("vanguard",              "Vanguard"),
    ("statestreet",           "State Street"),
    ("bnymellon",             "BNY Mellon"),
    ("usbank",                "US Bank"),
    ("pnc",                   "PNC Financial"),
    ("capitalone",            "Capital One"),
    ("discover",              "Discover Financial"),
    ("schwab",                "Charles Schwab"),
    ("td",                    "TD Bank"),
    # Consulting
    ("mckinsey",              "McKinsey & Company"),
    ("bcg",                   "Boston Consulting Group"),
    ("bain",                  "Bain & Company"),
    ("deloitte",              "Deloitte"),
    ("accenture",             "Accenture"),
    ("ey",                    "EY"),
    ("kpmg",                  "KPMG"),
    ("pwc",                   "PwC"),
    ("boozallen",             "Booz Allen Hamilton"),
    ("leidos",                "Leidos"),
    ("saic",                  "SAIC"),
    # Healthcare / Pharma
    ("johnson-johnson",       "Johnson & Johnson"),
    ("pfizer",                "Pfizer"),
    ("merck",                 "Merck"),
    ("abbvie",                "AbbVie"),
    ("lilly",                 "Eli Lilly"),
    ("bristolmyerssquibb",    "Bristol Myers Squibb"),
    ("astrazeneca",           "AstraZeneca"),
    ("novartis",              "Novartis"),
    ("roche",                 "Roche"),
    ("unitedhealth",          "UnitedHealth Group"),
    ("cigna",                 "Cigna"),
    ("cvs",                   "CVS Health"),
    ("anthem",                "Anthem"),
    # Supply Chain / Retail / Logistics
    ("walmart",               "Walmart"),
    ("target",                "Target"),
    ("amazon-logistics",      "Amazon Logistics"),
    ("fedex",                 "FedEx"),
    ("ups",                   "UPS"),
    ("dhl",                   "DHL"),
    ("xpo",                   "XPO Logistics"),
    ("cargill",               "Cargill"),
    ("caterpillar",           "Caterpillar"),
    ("deere",                 "John Deere"),
    ("boeing",                "Boeing"),
    ("lockheedmartin",        "Lockheed Martin"),
    ("generaldynamics",       "General Dynamics"),
    ("raytheon",              "Raytheon"),
    ("northropgrumman",       "Northrop Grumman"),
    # Telecom / Media
    ("verizon",               "Verizon"),
    ("att",                   "AT&T"),
    ("tmobile",               "T-Mobile"),
    ("comcast",               "Comcast"),
    ("nbc",                   "NBCUniversal"),
    ("warnerbros",            "Warner Bros. Discovery"),
    ("disney",                "Disney"),
    ("fox",                   "Fox Corporation"),
    ("nytimes",               "The New York Times"),
    # Energy / Utilities
    ("exxonmobil",            "ExxonMobil"),
    ("chevron",               "Chevron"),
    ("shell",                 "Shell"),
    ("bp",                    "BP"),
    ("ge",                    "GE"),
    ("siemens",               "Siemens"),
    ("honeywell",             "Honeywell"),
    ("3m",                    "3M"),
]

# ── Universities ───────────────────────────────────────────────────────────────
UNIVERSITIES = [
    # Ivy League
    {
        "name": "Columbia University",
        "urls": [
            "https://datascience.columbia.edu/research/opportunities/",
            "https://engineering.columbia.edu/student-opportunities",
            "https://stat.columbia.edu/opportunities/",
        ],
    },
    {
        "name": "Cornell University",
        "urls": [
            "https://tech.cornell.edu/about/jobs/",
            "https://www.cs.cornell.edu/undergrad/uresbigs",
        ],
    },
    {
        "name": "Princeton University",
        "urls": [
            "https://reu.cs.princeton.edu/",
            "https://csml.princeton.edu/opportunities",
            "https://orfe.princeton.edu/about/jobs",
        ],
    },
    {
        "name": "Yale University",
        "urls": [
            "https://seas.yale.edu/research/student-research",
            "https://cpsc.yale.edu/research/undergraduate-research",
            "https://statistics.yale.edu/",
        ],
    },
    {
        "name": "Harvard University",
        "urls": [
            "https://seas.harvard.edu/research/undergraduate-research",
            "https://iacs.seas.harvard.edu/positions",
            "https://datascience.harvard.edu/research",
        ],
    },
    {
        "name": "University of Pennsylvania",
        "urls": [
            "https://www.cis.upenn.edu/research/undergraduate-research/",
            "https://dsl.cis.upenn.edu/",
            "https://statistics.wharton.upenn.edu/research/",
        ],
    },
    {
        "name": "Dartmouth College",
        "urls": [
            "https://web.cs.dartmouth.edu/undergraduate/research-opportunities",
        ],
    },
    {
        "name": "Brown University",
        "urls": [
            "https://cs.brown.edu/research/",
            "https://dsi.brown.edu/research",
        ],
    },
    # NYC & Metro Area
    {
        "name": "NYU",
        "urls": [
            "https://cds.nyu.edu/phd-program/current-openings/",
            "https://engineering.nyu.edu/research/student-research-opportunities",
            "https://courant.nyu.edu/research/",
        ],
    },
    {
        "name": "Columbia Engineering",
        "urls": [
            "https://www.engineering.columbia.edu/research/undergraduate-research",
        ],
    },
    {
        "name": "Fordham University",
        "urls": [
            "https://www.fordham.edu/info/25135/research_opportunities",
        ],
    },
    {
        "name": "Rockefeller University",
        "urls": [
            "https://www.rockefeller.edu/research/summer-undergraduate/",
        ],
    },
    {
        "name": "Stony Brook University",
        "urls": [
            "https://www.cs.stonybrook.edu/research/undergraduate",
        ],
    },
    {
        "name": "Rutgers University",
        "urls": [
            "https://www.cs.rutgers.edu/research/undergraduate-research",
            "https://reu.dimacs.rutgers.edu/",
        ],
    },
    {
        "name": "Stevens Institute of Technology",
        "urls": [
            "https://www.stevens.edu/school-engineering-science/departments/computer-science/research",
        ],
    },
    {
        "name": "NJIT",
        "urls": [
            "https://cs.njit.edu/research/undergraduate-research",
        ],
    },
    # National Labs
    {
        "name": "Brookhaven National Laboratory",
        "urls": [
            "https://www.bnl.gov/education/programs/program.php?q=181",
        ],
    },
    {
        "name": "MIT Lincoln Laboratory",
        "urls": [
            "https://www.ll.mit.edu/careers/student-opportunities",
        ],
    },
    {
        "name": "Argonne National Laboratory",
        "urls": [
            "https://www.anl.gov/education/undergraduates",
        ],
    },
    # AI Research Labs
    {
        "name": "Allen Institute for AI",
        "urls": [
            "https://allenai.org/careers",
        ],
    },
    {
        "name": "Simons Institute (Berkeley)",
        "urls": [
            "https://simons.berkeley.edu/programs",
        ],
    },
    {
        "name": "Flatiron Institute",
        "urls": [
            "https://www.simonsfoundation.org/flatiron/",
        ],
    },
]

# ── Start date inclusion signals ───────────────────────────────────────────────
START_DATE_SIGNALS = [
    "fall 2026", "fall '26", "fall2026",
    "co-op", "coop", "co op",
    "september 2026", "october 2026", "november 2026",
    "august 2026", "aug 2026", "sept 2026", "sep 2026",
    "starting august", "starting september", "starting fall",
    "fall semester", "autumn 2026",
    "2026 fall", "'26 fall",
]

# ── Exclusion signals (summer-only roles) ──────────────────────────────────────
EXCLUDE_SIGNALS = [
    "summer 2026", "summer '26", "summer2026",
    "summer only", "10 weeks", "12 weeks",
    "may 2026", "june 2026", "july 2026",
    "spring 2026", "spring '26",   # too early
    "spring 2027",                  # too late to be relevant
    "new grad", "new graduate", "full time offer", "full-time offer",
]
