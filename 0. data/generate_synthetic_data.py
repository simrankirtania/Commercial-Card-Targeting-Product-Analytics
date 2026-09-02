"""
generate_synthetic_data.py
---------------------------
Generates a synthetic B2B commercial-card dataset representing:
    1. prospects.csv     - un-acquired businesses in the target-marketing funnel
    2. customers.csv      - acquired commercial cardmembers (with enrichment gaps, by design)
    3. transactions.csv   - card spend transactions for acquired customers
    4. feature_rollout.csv- A/B test assignment + engagement log for a new
                             "Smart Spend Alerts" product feature

The data is entirely synthetic (no real company/person data) and is built to
mirror the kind of commercial-card / GCS data used for prospect targeting,
data-quality enrichment, and product analytics.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RNG = np.random.default_rng(42)
N_PROSPECTS = 6000
N_CUSTOMERS = 2200          # subset of prospects that converted
N_DAYS_TXN = 180
OUT_DIR = "/home/claude/amex-project/data"

INDUSTRIES = ["Manufacturing", "Retail Trade", "Professional Services",
              "Construction", "Healthcare", "Transportation & Logistics",
              "Technology", "Hospitality", "Wholesale Distribution", "Education"]

REGIONS = ["North", "South", "East", "West", "Central"]

COMPANY_SIZE_BANDS = ["1-9 employees", "10-49 employees",
                       "50-249 employees", "250-999 employees", "1000+ employees"]

SPEND_CATEGORIES = ["Travel", "Meetings & Events", "Office Supplies",
                     "Raw Materials", "Software & SaaS", "Fuel & Fleet",
                     "Utilities", "Professional Fees"]


def gen_prospects():
    ids = [f"PROS-{100000+i}" for i in range(N_PROSPECTS)]
    industry = RNG.choice(INDUSTRIES, N_PROSPECTS)
    region = RNG.choice(REGIONS, N_PROSPECTS)
    size_band = RNG.choice(COMPANY_SIZE_BANDS, N_PROSPECTS,
                            p=[0.35, 0.30, 0.20, 0.10, 0.05])
    est_annual_revenue = RNG.lognormal(mean=13.5, sigma=1.1, size=N_PROSPECTS).round(-3)
    digital_engagement_score = RNG.beta(2, 3, N_PROSPECTS) * 100  # 0-100 intent score
    years_in_business = RNG.integers(1, 40, N_PROSPECTS)
    existing_bank_relationship = RNG.choice(["Yes", "No"], N_PROSPECTS, p=[0.55, 0.45])

    # deliberately introduce data-quality issues to enrich later
    df = pd.DataFrame({
        "prospect_id": ids,
        "industry": industry,
        "region": region,
        "company_size_band": size_band,
        "est_annual_revenue": est_annual_revenue,
        "digital_engagement_score": digital_engagement_score.round(1),
        "years_in_business": years_in_business,
        "existing_bank_relationship": existing_bank_relationship,
    })

    # inject missingness / inconsistent casing to simulate raw source data
    missing_idx = RNG.choice(df.index, size=int(0.08 * len(df)), replace=False)
    df.loc[missing_idx, "digital_engagement_score"] = np.nan
    dup_idx = RNG.choice(df.index, size=int(0.03 * len(df)), replace=False)
    df.loc[dup_idx, "industry"] = df.loc[dup_idx, "industry"].str.upper()
    rev_missing = RNG.choice(df.index, size=int(0.05 * len(df)), replace=False)
    df.loc[rev_missing, "est_annual_revenue"] = np.nan

    df.to_csv(f"{OUT_DIR}/prospects_raw.csv", index=False)
    return df


def gen_customers(prospects_df):
    # conversion probability driven by engagement score + existing relationship
    p = prospects_df["digital_engagement_score"].fillna(20) / 400 + \
        (prospects_df["existing_bank_relationship"] == "Yes") * 0.08
    p = (p - p.min()) / (p.max() - p.min())
    converted_idx = prospects_df.sample(
        n=N_CUSTOMERS, weights=p + 0.01, random_state=42
    ).index

    cust = prospects_df.loc[converted_idx].copy()
    cust = cust.rename(columns={"prospect_id": "source_prospect_id"})
    cust.insert(0, "customer_id", [f"CUST-{200000+i}" for i in range(len(cust))])
    signup_start = datetime(2025, 1, 1)
    cust["acquisition_date"] = [
        signup_start + timedelta(days=int(d))
        for d in RNG.integers(0, 400, len(cust))
    ]
    cust["credit_line"] = (RNG.lognormal(9.5, 0.6, len(cust)) // 1000 * 1000)
    cust.to_csv(f"{OUT_DIR}/customers.csv", index=False)
    return cust


def gen_transactions(customers_df):
    rows = []
    start_date = datetime(2026, 3, 1)
    for _, row in customers_df.iterrows():
        n_txn = RNG.poisson(lam=18)
        for _ in range(n_txn):
            day_offset = RNG.integers(0, N_DAYS_TXN)
            txn_date = start_date + timedelta(days=int(day_offset))
            category = RNG.choice(SPEND_CATEGORIES)
            amount = round(float(RNG.gamma(2.2, 180)), 2)
            rows.append((row["customer_id"], txn_date.date().isoformat(),
                         category, amount))
    txn = pd.DataFrame(rows, columns=["customer_id", "txn_date",
                                       "spend_category", "amount"])
    txn.to_csv(f"{OUT_DIR}/transactions.csv", index=False)
    return txn


def gen_feature_rollout(customers_df):
    """Simulates an A/B test for a new 'Smart Spend Alerts' feature and
    30-day post-exposure engagement (product health metric)."""
    df = customers_df[["customer_id", "acquisition_date"]].copy()
    df["variant"] = RNG.choice(["control", "treatment"], len(df), p=[0.5, 0.5])

    base_login_rate = RNG.normal(0.42, 0.08, len(df)).clip(0.05, 0.95)
    treatment_lift = np.where(df["variant"] == "treatment",
                               RNG.normal(0.09, 0.03, len(df)), 0)
    df["week4_active_rate"] = (base_login_rate + treatment_lift).clip(0, 1).round(3)

    base_dispute_rate = RNG.normal(0.06, 0.02, len(df)).clip(0.0, 0.3)
    treatment_effect_disputes = np.where(df["variant"] == "treatment",
                                          -RNG.normal(0.012, 0.006, len(df)), 0)
    df["dispute_rate_30d"] = (base_dispute_rate + treatment_effect_disputes).clip(0, 1).round(3)

    df["cohort_month"] = pd.to_datetime(df["acquisition_date"]).dt.to_period("M").astype(str)
    df.to_csv(f"{OUT_DIR}/feature_rollout.csv", index=False)
    return df


if __name__ == "__main__":
    prospects = gen_prospects()
    customers = gen_customers(prospects)
    transactions = gen_transactions(customers)
    rollout = gen_feature_rollout(customers)
    print(f"prospects_raw.csv:   {len(prospects):,} rows")
    print(f"customers.csv:       {len(customers):,} rows")
    print(f"transactions.csv:    {len(transactions):,} rows")
    print(f"feature_rollout.csv: {len(rollout):,} rows")
