# Commercial Card Targeting & Product Analytics

**A synthetic end-to-end analytics project simulating a commercial-card business's prospect-targeting and product-health workflow.**

> All data is synthetically generated (`data/generate_synthetic_data.py`). No real company, customer, or transaction data is used.

## Project Overview

A B2B commercial-card issuer needs to (1) find and prioritize the right prospects to acquire, and (2) track whether a newly launched product feature is actually improving customer engagement and risk. This project builds both halves of that workflow:

| Business Need | What's Built |
|---|---|
| Enrich messy prospect data for targeting | `scripts/01_data_quality_enrichment.py` |
| Score & tier prospects for outbound targeting | Targeting Readiness Score + SQL targeting queries |
| Evaluate a new product feature (A/B test) | `scripts/02_ab_testing_cohort_analysis.py` |
| Track product health & funnel performance | `scripts/03_product_health_dashboard.py` |

## Dataset (synthetic, ~48K rows)
- **6,000 prospects** — firmographics (industry, region, size, revenue, engagement, relationship status) with realistic data-quality issues injected (missing values, inconsistent casing)
- **2,200 customers** — converted prospects with acquisition date & credit line
- **~40,000 transactions** — commercial card spend across 8 categories over 180 days
- **2,200 feature-rollout records** — A/B test assignment for a "Smart Spend Alerts" feature, with week-4 activation rate and 30-day dispute rate

## Pipeline

```
data/generate_synthetic_data.py          → prospects_raw.csv, customers.csv, transactions.csv, feature_rollout.csv
scripts/01_data_quality_enrichment.py    → prospects_enriched.csv, data_quality_report.csv
scripts/02_ab_testing_cohort_analysis.py → ab_test_results.csv, cohort_activation_table.csv
scripts/03_product_health_dashboard.py   → product_health_dashboard.png
sql/targeting_and_spend_queries.sql      → SQL used for the same targeting/spend/AB logic (SQLite-compatible)
```

Run in order:
```bash
pip install -r requirements.txt
python data/generate_synthetic_data.py
python scripts/01_data_quality_enrichment.py
python scripts/02_ab_testing_cohort_analysis.py
python scripts/03_product_health_dashboard.py
```

## Key Results

**Data quality & enrichment**
- Identified and resolved missingness/inconsistency across ~3,900 of 6,000 prospect records (casing, missing engagement scores, missing revenue) using industry/region-level imputation
- Engineered a 0–100 **Targeting Readiness Score** (engagement 40% / company scale 30% / tenure 30%) and tiered prospects into Priority / Warm / Nurture segments for outbound targeting

**A/B test — Smart Spend Alerts feature**
- Week-4 activation rate: **42.0% (control) → 50.8% (treatment)**, +8.8pp lift, Welch's t-test p < 0.001
- 30-day dispute rate: **6.0% (control) → 4.8% (treatment)**, −1.2pp, p < 0.001
- Lift held consistently across every monthly acquisition cohort (see cohort heatmap), suggesting the effect isn't driven by a single seasonal cohort

**Product health dashboard**
- Single-view dashboard combining targeting funnel, spend trend, A/B lift, and cohort retention — the kind of artifact used to brief stakeholders on product/portfolio performance

<img width="2400" height="1760" alt="product_health_dashboard" src="https://github.com/user-attachments/assets/c95fc3a4-1a4e-4639-a3c8-4c1864193214" />


## How This Maps to the Role

| JD Responsibility | Project Component |
|---|---|
| "Create innovative data products encompassing commercial prospect and customer targeting use-cases" | Targeting Readiness Score + tiered SQL targeting list |
| "Create and implement analytical solutions on enriching data quality" | Data quality/enrichment pipeline with a QA log |
| "Support growth through experimentation (A/B testing, cohort analysis, funnel performance)" | Welch's t-test A/B evaluation + cohort activation table |
| "Monitor product health metrics and user analytics" | 4-panel product health dashboard |
| "HIVE, SAS, SQL, Excel (Python)" | SQL queries (Hive/SQLite-compatible syntax) + Python/pandas pipeline |

## Tech Stack
Python (pandas, numpy, scipy, matplotlib, seaborn) · SQL (SQLite/Hive-syntax compatible)

## Repository Structure
```
├── data/
│   └── generate_synthetic_data.py
├── scripts/
│   ├── 01_data_quality_enrichment.py
│   ├── 02_ab_testing_cohort_analysis.py
│   └── 03_product_health_dashboard.py
├── sql/
│   └── targeting_and_spend_queries.sql
├── outputs/
│   ├── data_quality_report.csv
│   ├── ab_test_results.csv
│   ├── cohort_activation_table.csv
│   └── product_health_dashboard.png
├── requirements.txt
└── README.md
```

---
*Built by Simran Kirtania · [Portfolio](https://simrankirtaniaportfolio.netlify.app) · [GitHub](https://github.com/simrankirtania)*
