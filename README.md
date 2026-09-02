# Commercial Card Targeting & Product Analytics

An end-to-end analytics project that simulates how a B2B commercial-card business can turn messy prospect and customer data into better acquisition, product, and portfolio decisions.

The project combines **data generation, data cleaning, feature engineering, SQL analysis, A/B testing, cohort analysis, and stakeholder reporting** into one reproducible workflow.

> **Note:** All data used in this project is synthetic and was created specifically for this portfolio project. No real customer, company, or transaction data is used.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [Key Results](#key-results)
- [Analytics Workflow](#analytics-workflow)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Data Cleaning & Enrichment](#data-cleaning--enrichment)
- [SQL Analysis](#sql-analysis)
- [A/B Testing & Cohort Analysis](#ab-testing--cohort-analysis)
- [Product Health Dashboard](#product-health-dashboard)
- [Business Recommendations](#business-recommendations)
- [Tools & Technologies](#tools--technologies)
- [How to Run the Project](#how-to-run-the-project)
- [Limitations](#limitations)
- [Author](#author)
- [License](#license)

---

## Project Overview

Commercial-card businesses manage large volumes of prospect, customer, transaction, and product-engagement data. The challenge is turning that data into decisions that improve acquisition efficiency, customer engagement, and portfolio performance.

This project simulates that workflow through five connected stages:

1. **Generate and ingest synthetic commercial-card data**
2. **Clean and enrich messy prospect records**
3. **Prioritize prospects and analyze spend using SQL**
4. **Evaluate a new product feature using A/B testing**
5. **Visualize results in a stakeholder-facing dashboard**

The result is a repeatable analytics loop:

**Enrich data → Target the right prospects → Analyze customer behavior → Test product changes → Report the impact → Repeat**

---

## Business Problem

The project addresses three common problems faced by B2B commercial-card and lending businesses:

### 1. Messy and incomplete prospect data
Missing values and inconsistent formatting can lead to unreliable targeting decisions.

### 2. No clear prospect prioritization
Without a scoring framework, sales and marketing teams may spend equal effort on both high-value and low-propensity accounts.

### 3. Product decisions based on guesswork
New features should be evaluated with statistical evidence before being scaled across the customer base.

---

## Project Objectives

The analysis was designed to:

- Build a realistic synthetic commercial-card dataset for analysis.
- Clean inconsistent and incomplete prospect data.
- Create a **Targeting Readiness Score** to prioritize acquisition opportunities.
- Segment prospects into actionable targeting tiers.
- Use SQL to answer targeting and portfolio-spend questions.
- Identify high-value customers for retention and cross-sell opportunities.
- Measure the impact of a new **Smart Spend Alerts** feature using an A/B test.
- Validate product performance across acquisition cohorts.
- Consolidate acquisition, spend, and product metrics into one dashboard.

---

## Key Results

| Area | Result | Business Value |
|---|---:|---|
| Priority prospects | **251 of 6,000** prospects identified | Focus high-touch outreach on the strongest acquisition opportunities |
| Priority prospects without an existing bank relationship | **111** prospects | Creates an immediately actionable outbound target list |
| Data quality | Approximately **65%** of records touched by cleaning or imputation | Improves the reliability of downstream targeting |
| Week-4 activation | **+8.82 percentage points** | Stronger early customer engagement |
| 30-day dispute rate | **-1.23 percentage points** | Potential reduction in servicing and dispute-related costs |
| Statistical significance | **p < 0.001** for both A/B test metrics | Provides strong evidence that the observed differences are unlikely to be random |
| Cohort validation | Treatment outperformed control in **all 14 acquisition cohorts** | Confirms that the activation lift was consistent across cohorts |
| Portfolio spend | **39,797 transactions** and approximately **$15.74M** in observed spend | Supports portfolio monitoring and customer segmentation |

---

## Analytics Workflow

```text
┌─────────────────────────────┐
│  1. Data Generation         │
│  Prospects • Customers      │
│  Transactions • A/B Logs    │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  2. Data Quality &          │
│     Enrichment              │
│  Clean • Impute • Score     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  3. SQL Analysis            │
│  Targeting • Spend • Value  │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  4. Product Experimentation │
│  A/B Test • Cohort Analysis │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  5. Dashboard & Reporting   │
│  Business Recommendations   │
└─────────────────────────────┘
```

---

## Dataset

The project uses a synthetic dataset designed to resemble a commercial-card business environment.

### Data Sources

| File | Description |
|---|---|
| `prospects_raw.csv` | 6,000 un-acquired businesses in the prospect funnel, including deliberately introduced data-quality issues |
| `prospects_enriched.csv` | Cleaned and enriched prospect dataset with targeting scores and tiers |
| `customers.csv` | 2,200 acquired commercial-card customers |
| `transactions.csv` | 39,797 commercial-card transactions across a 180-day period |
| `feature_rollout.csv` | Control/treatment assignments and product engagement outcomes |
| `generate_synthetic_data.py` | Script used to reproducibly generate the synthetic datasets |

### Synthetic Data Design

The generated data includes:

- **10 industries**
- **5 regions**
- **Multiple company-size bands**
- Estimated annual revenue
- Digital engagement scores
- Years in business
- Existing banking relationship indicators
- Commercial-card spend categories
- Customer acquisition cohorts
- A/B test assignments and product-health metrics

Deliberate data-quality issues were introduced into the raw prospect data, including missing values and inconsistent industry casing, so the project could demonstrate a realistic enrichment workflow.

---

## Repository Structure

```text
Commercial-Card-Analytics/
│
├── 0. data/
│   ├── customers.csv
│   ├── feature_rollout.csv
│   ├── generate_synthetic_data.py
│   ├── prospects_enriched.csv
│   ├── prospects_raw.csv
│   └── transactions.csv
│
├── 1. Notebook/
│   └── commercial_card_analytics.ipynb
│
├── 2. Report/
│   └── Commercial Card Targeting & Product Analytics.pdf
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Data Cleaning & Enrichment

## Data Quality Issues Addressed

The raw prospect dataset intentionally contains common data-quality problems.

The enrichment process includes:

- Standardizing inconsistent text formatting and casing
- Handling missing digital engagement scores
- Imputing engagement values using **industry + region medians**
- Imputing missing revenue values using **company-size medians**
- Checking for duplicate prospect IDs

This step ensures that incomplete or inconsistent source data does not directly distort prospect-targeting decisions.

---

## Targeting Readiness Score

A **0–100 Targeting Readiness Score** was engineered using three business signals:

| Component | Weight |
|---|---:|
| Digital Engagement | **40%** |
| Company Scale | **30%** |
| Business Tenure | **30%** |

Prospects were then segmented into three targeting tiers:

| Tier | Purpose |
|---|---|
| **Tier 1 – Priority** | Highest-priority prospects for focused outbound activity |
| **Tier 2 – Warm** | Prospects suitable for continued sales and marketing engagement |
| **Tier 3 – Nurture** | Lower-priority prospects suitable for lower-cost campaigns and long-term nurturing |

### Targeting Outcome

- **251 Priority prospects**
- **3,774 Warm prospects**
- **1,975 Nurture prospects**

A further filter identified **111 Priority prospects with no existing bank relationship**, creating a practical outreach list for acquisition teams.

---

# SQL Analysis

The enriched datasets are loaded into an **in-memory SQLite database** inside the notebook.

The SQL analysis demonstrates practical business queries for sales, marketing, and portfolio teams.

### Key SQL Analyses

#### 1. Priority Prospect List
Identifies Tier 1 prospects without an existing bank relationship and ranks them by Targeting Readiness Score.

**Business use:** Creates a ready-to-use outbound targeting list.

#### 2. Industry Targeting Funnel
Summarizes:

- Total prospects
- Tier 1 prospect counts
- Average readiness scores
- Average estimated revenue

**Business use:** Helps identify industries with stronger acquisition opportunities.

#### 3. Spend by Category
Analyzes active customers, total spend, and average transaction values by spend category.

**Business use:** Helps understand category behavior and commercial-card usage.

#### 4. Monthly Spend Trend
Tracks portfolio-level spend over time.

**Business use:** Helps identify changes in customer activity, seasonality, or portfolio health.

#### 5. Top Spend-Decile Customers
Uses the SQL `NTILE()` window function to identify the highest-spending customer segment.

**Business use:** Supports retention, relationship management, and cross-sell targeting.

---

# A/B Testing & Cohort Analysis

## Feature Tested: Smart Spend Alerts

The project evaluates whether a new **Smart Spend Alerts** feature improves customer behavior.

Customers were divided into:

- **Control group**
- **Treatment group**

Two product-health metrics were evaluated:

### Week-4 Activation Rate

| Variant | Activation Rate |
|---|---:|
| Control | **41.99%** |
| Treatment | **50.81%** |
| Difference | **+8.82 percentage points** |

### 30-Day Dispute Rate

| Variant | Dispute Rate |
|---|---:|
| Control | **6.04%** |
| Treatment | **4.81%** |
| Difference | **-1.23 percentage points** |

### Statistical Method

The analysis uses **Welch's independent two-sample t-test** (`equal_var=False`) to compare control and treatment groups.

Both results were statistically significant at **p < 0.001**.

### Cohort Validation

The activation results were also evaluated by acquisition month.

The treatment group outperformed the control group across **all 14 acquisition cohorts**, with treatment advantages ranging from approximately **+5.5 to +12.1 percentage points**.

This additional analysis helps verify that the overall result was not driven by one unusually strong acquisition period.

---

# Product Health Dashboard

The project concludes with a four-panel dashboard designed for stakeholder reporting.

### Dashboard Views

**A. Prospect Targeting Funnel by Industry**  
Shows the distribution of Priority, Warm, and Nurture prospects across industries.

**B. Monthly Commercial Card Spend**  
Tracks portfolio spend trends over time.

**C. Smart Spend Alerts A/B Test Result**  
Compares control and treatment performance for activation and dispute rate.

**D. Cohort Activation Rate by Acquisition Month**  
Shows how the treatment effect performs across customer acquisition cohorts.

The dashboard connects the full business story, from acquisition opportunity to customer behavior and product performance.

---

## Business Recommendations

Based on the analysis, the recommended actions are:

### 1. Prioritize Tier 1 outreach
Start acquisition efforts with the **111 Priority prospects without an existing bank relationship**, then expand based on score and industry.

### 2. Scale Smart Spend Alerts carefully
The experiment shows higher activation and lower dispute rates. A broader rollout is supported, while continuing to monitor:

- Long-term retention
- Support volume
- Operational cost
- Customer experience

### 3. Keep cohort reporting in the monitoring process
Overall averages can hide differences between customer groups. Cohort-level reporting should remain part of product performance monitoring.

### 4. Investigate major spend movements
Monthly and category-level trends should be used to determine whether changes are driven by:

- Seasonality
- Customer attrition
- Changes in customer behavior
- Category mix

### 5. Maintain the data-quality pipeline
The cleaning and enrichment process should run whenever new prospect data is received so that data-quality issues do not silently affect targeting decisions.

---

# Tools & Technologies

| Category | Tools |
|---|---|
| Programming | Python |
| Data Manipulation | pandas, NumPy |
| Database & SQL | SQLite, SQL |
| Statistical Analysis | SciPy |
| Data Visualization | Matplotlib, Seaborn |
| Analysis Environment | Jupyter Notebook |
| Reporting | Dashboard and analytical report |

### Skills Demonstrated

- Data cleaning and imputation
- Exploratory data analysis
- Feature engineering
- Composite scoring
- Customer and prospect segmentation
- SQL query design
- Joins and aggregations
- SQL window functions
- A/B testing
- Welch's t-test
- Hypothesis testing
- Cohort analysis
- Data visualization
- Dashboard design
- Business storytelling
- Translating analytical findings into recommendations

---

# How to Run the Project

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository-name>.git
cd <your-repository-name>
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Launch Jupyter Notebook

```bash
jupyter notebook
```

## 4. Open the analysis notebook

Navigate to:

```text
1. Notebook/commercial_card_analytics.ipynb
```

Run the notebook from top to bottom to reproduce the workflow:

1. Load and generate the data
2. Clean and enrich prospect records
3. Create targeting scores and tiers
4. Run SQL analyses
5. Perform A/B testing
6. Validate results across cohorts
7. Generate the product-health dashboard

### Optional: Regenerate the Synthetic Data

The project also includes:

```text
0. data/generate_synthetic_data.py
```

This script can be used to regenerate the synthetic datasets. If running it in a new environment, make sure the output directory in the script points to your local `0. data/` folder.

---

# Limitations

This project is a **portfolio simulation built entirely on synthetic data**.

The numerical results demonstrate the analytical workflow and methods, but they should **not** be interpreted as real customer behavior or business performance for American Express or any other company.

In a production environment, the analysis would additionally require:

- Data governance and privacy controls
- Clearly defined business metrics
- Production-grade data pipelines
- Experiment-design review
- Monitoring and alerting
- Stakeholder validation
- Long-term impact measurement

---

# Author

**Simran Kirtania**

Data Analytics Portfolio Project focused on applying analytics techniques to real-world business problems involving customer acquisition, product performance, and portfolio management.

---

# License

This project is available under the license included in the repository.

---

## Final Takeaway

This project demonstrates a complete analytics loop that can be applied to commercial-card, lending, fintech, and other B2B businesses:

> **Clean the data → identify the right opportunities → understand customer behavior → test product changes → measure the impact → make better decisions.**
