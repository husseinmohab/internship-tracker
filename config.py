"""
config.py — Central configuration for all scrapers.
Edit this file to add/remove companies, keywords, or universities.
"""

# ── Cutoff date ────────────────────────────────────────────────────────────────
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

# ── Search queries for APIs ────────────────────────────────────────────────────
API_QUERIES = [
    "data engineer intern fall 2026 new york",
    "data engineering co-op fall 2026 new york",
    "data scientist intern fall 2026 new york",
    "data analyst intern fall 2026 new york",
    "business intelligence intern fall 2026",
    "supply chain analyst intern fall 2026",
    "software engineer intern fall 2026 new york",
    "research engineer intern fall 2026",
    "research assistant intern fall 2026",
    "machine learning intern fall 2026 new york",
    "analytics engineer intern fall 2026",
    "data engineer co-op new york",
    "software engineer co-op fall 2026",
    "ml engineer intern fall 2026",
    "fintech data intern fall 2026 new york",
]

# ── Greenhouse companies ───────────────────────────────────────────────────────
GREENHOUSE_COMPANIES = [
    # FinTech — NYC-heavy
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
    ("carta",                 "Carta"),
    ("mercury",               "Mercury"),
    ("alphapoint",            "AlphaPoint"),
    ("betterment",            "Betterment"),
    ("wealthfront",           "Wealthfront"),
    ("sofi",                  "SoFi"),
    ("nerdwallet",            "NerdWallet"),
    ("blend",                 "Blend"),
    ("commonbond",            "CommonBond"),
    ("greenlight",            "Greenlight"),
    ("dave",                  "Dave"),
    ("paxos",                 "Paxos"),
    ("anchorage",             "Anchorage Digital"),
    ("chainalysis",           "Chainalysis"),
    ("fireblocks",            "Fireblocks"),
    ("alchemy",               "Alchemy"),
    ("opensea",               "OpenSea"),
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
    ("metabase",              "Metabase"),
    ("rudderstack",           "RudderStack"),
    ("meltano",               "Meltano"),
    ("datafold",              "Datafold"),
    # AI / ML
    ("cohere",                "Cohere"),
    ("huggingface",           "Hugging Face"),
    ("scaleai",               "Scale AI"),
    ("weights-biases",        "Weights & Biases"),
    ("modal-labs",            "Modal"),
    ("together-ai",           "Together AI"),
    ("perplexity",            "Perplexity AI"),
    ("anyscale",              "Anyscale"),
    ("labelbox",              "Labelbox"),
    ("snorkelai",             "Snorkel AI"),
    # Infrastructure / Security
    ("cloudflare",            "Cloudflare"),
    ("hashicorp",             "HashiCorp"),
    ("fastly",                "Fastly"),
    ("supabase",              "Supabase"),
    ("vercel",                "Vercel"),
    ("clickhouse",            "ClickHouse"),
    ("timescale",             "Timescale"),
    ("neon",                  "Neon"),
    # Product / SaaS
    ("palantir",              "Palantir"),
    ("figma",                 "Figma"),
    ("notion",                "Notion"),
    ("airtable",              "Airtable"),
    ("asana",                 "Asana"),
    ("rippling",              "Rippling"),
    ("gusto",                 "Gusto"),
    ("retool",                "Retool"),
    ("hex",                   "Hex"),
    ("zapier",                "Zapier"),
    # Supply Chain / Logistics
    ("flexport",              "Flexport"),
    ("project44",             "Project44"),
    ("loadsmart",             "Loadsmart"),
    ("shipbob",               "ShipBob"),
    # Healthcare / Bio
    ("flatiron",              "Flatiron Health"),
    ("tempus",                "Tempus"),
    ("komodo-health",         "Komodo Health"),
]

# ── Lever companies ────────────────────────────────────────────────────────────
LEVER_COMPANIES = [
    # FinTech
    ("robinhood",             "Robinhood"),
    ("mosaic",                "Mosaic"),
    ("pilot",                 "Pilot"),
    ("lob",                   "Lob"),
    ("column",                "Column"),
    ("increase",              "Increase"),
    ("lithic",                "Lithic"),
    ("unit",                  "Unit"),
    ("synctera",              "Synctera"),
    ("treasury-prime",        "Treasury Prime"),
    ("modern-treasury",       "Modern Treasury"),
    ("dwolla",                "Dwolla"),
    ("finix",                 "Finix"),
    ("tabapay",               "TabaPay"),
    # Infrastructure / DevTools
    ("confluent",             "Confluent"),
    ("prefect",               "Prefect"),
    ("astronomer",            "Astronomer"),
    ("census",                "Census"),
    ("hightouch",             "Hightouch"),
    ("statsig",               "Statsig"),
    ("launchdarkly",          "LaunchDarkly"),
    ("mixpanel",              "Mixpanel"),
    ("heap",                  "Heap"),
    ("fullstory",             "FullStory"),
    # AI / Research
    ("deepmind",              "Google DeepMind"),
    ("adept",                 "Adept AI"),
    ("covariant",             "Covariant"),
    # Streaming / Media
    ("netflix",               "Netflix"),
    ("spotify",               "Spotify"),
    # Mobility
    ("lyft",                  "Lyft"),
    ("samsara",               "Samsara"),
    ("verkada",               "Verkada"),
]

# ── Workday companies ──────────────────────────────────────────────────────────
WORKDAY_COMPANIES = [
    # Big Tech
    ("amazon",                "Amazon"),
    ("google",                "Google"),
    ("microsoft",             "Microsoft"),
    ("apple",                 "Apple"),
    ("meta",                  "Meta"),
    ("ibm",                   "IBM"),
    ("oracle",                "Oracle"),
    ("salesforce",            "Salesforce"),
    ("servicenow",            "ServiceNow"),
    ("adobe",                 "Adobe"),
    ("intuit",                "Intuit"),
    ("nvidia",                "NVIDIA"),
    ("cisco",                 "Cisco"),
    # Finance — NYC HQ or major presence
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
    ("capitalone",            "Capital One"),
    ("discover",              "Discover Financial"),
    ("schwab",                "Charles Schwab"),
    ("td",                    "TD Bank"),
    ("pnc",                   "PNC Financial"),
    # FinTech on Workday
    ("paypal",                "PayPal"),
    ("intuit",                "Intuit"),
    ("adyen",                 "Adyen"),
    ("fiserv",                "Fiserv"),
    ("fis",                   "FIS Global"),
    ("ncr",                   "NCR Atleos"),
    ("broadridge",            "Broadridge Financial"),
    ("ss-c",                  "SS&C Technologies"),
    ("ihs-markit",            "S&P Global / IHS Markit"),
    ("msci",                  "MSCI"),
    ("factset",               "FactSet"),
    ("intercontinentalexchange", "ICE / NYSE"),
    ("nasdaq",                "Nasdaq"),
    ("dtcc",                  "DTCC"),
    ("refinitiv",             "LSEG / Refinitiv"),
    # Consulting
    ("mckinsey",              "McKinsey & Company"),
    ("bcg",                   "Boston Consulting Group"),
    ("deloitte",              "Deloitte"),
    ("accenture",             "Accenture"),
    ("boozallen",             "Booz Allen Hamilton"),
    ("leidos",                "Leidos"),
    # Supply Chain / Retail
    ("walmart",               "Walmart"),
    ("target",                "Target"),
    ("fedex",                 "FedEx"),
    ("ups",                   "UPS"),
    ("xpo",                   "XPO Logistics"),
    ("cargill",               "Cargill"),
    # Healthcare
    ("johnson-johnson",       "Johnson & Johnson"),
    ("pfizer",                "Pfizer"),
    ("merck",                 "Merck"),
    ("unitedhealth",          "UnitedHealth Group"),
    ("cigna",                 "Cigna"),
    # Media / Telecom — NYC
    ("verizon",               "Verizon"),
    ("att",                   "AT&T"),
    ("comcast",               "Comcast"),
    ("nbc",                   "NBCUniversal"),
    ("warnerbros",            "Warner Bros. Discovery"),
    ("nytimes",               "The New York Times"),
    ("bloomberg",             "Bloomberg"),
]

# ── Universities ───────────────────────────────────────────────────────────────
UNIVERSITIES = [
    {
        "name": "Columbia University",
        "urls": [
            "https://datascience.columbia.edu/research/opportunities/",
            "https://engineering.columbia.edu/student-opportunities",
        ],
    },
    {
        "name": "Cornell Tech",
        "urls": [
            "https://tech.cornell.edu/about/jobs/",
        ],
    },
    {
        "name": "Princeton University",
        "urls": [
            "https://reu.cs.princeton.edu/",
            "https://csml.princeton.edu/opportunities",
        ],
    },
    {
        "name": "Yale University",
        "urls": [
            "https://seas.yale.edu/research/student-research",
            "https://cpsc.yale.edu/research/undergraduate-research",
        ],
    },
    {
        "name": "Harvard University",
        "urls": [
            "https://iacs.seas.harvard.edu/positions",
            "https://datascience.harvard.edu/research",
        ],
    },
    {
        "name": "University of Pennsylvania",
        "urls": [
            "https://www.cis.upenn.edu/research/undergraduate-research/",
        ],
    },
    {
        "name": "Brown University",
        "urls": [
            "https://dsi.brown.edu/research",
        ],
    },
    {
        "name": "NYU",
        "urls": [
            "https://cds.nyu.edu/phd-program/current-openings/",
            "https://engineering.nyu.edu/research/student-research-opportunities",
        ],
    },
    {
        "name": "Rutgers University",
        "urls": [
            "https://reu.dimacs.rutgers.edu/",
        ],
    },
    {
        "name": "Stony Brook University",
        "urls": [
            "https://www.cs.stonybrook.edu/research/undergraduate",
        ],
    },
    {
        "name": "Brookhaven National Laboratory",
        "urls": [
            "https://www.bnl.gov/education/programs/program.php?q=181",
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
    "fall semester", "autumn 2026", "2026 fall",
]

# ── Exclusion signals ──────────────────────────────────────────────────────────
EXCLUDE_SIGNALS = [
    # Wrong season
    "summer 2026", "summer '26", "summer2026", "summer only",
    "may 2026", "june 2026", "july 2026",
    "spring 2026", "spring '26", "spring 2027",
    # Full-time / senior signals
    "new grad", "new graduate",
    "full time offer", "full-time offer",
    "senior ", "staff ", "principal ", "lead ",
    "director", "manager", "vp of", "vice president",
    "5+ years", "3+ years", "7+ years",
    # Clearly not student roles
    "executive", "c-suite", "partner role",
]
