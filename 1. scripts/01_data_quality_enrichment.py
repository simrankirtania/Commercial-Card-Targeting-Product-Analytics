"""
01_data_quality_enrichment.py
------------------------------
Cleans and enriches the raw prospect file so it is usable for targeting and
modeling. Mirrors the JD requirement: "Create and implement analytical
solutions on enriching data quality for usage across analytics and targeting."

Steps:
    1. Standardize categorical text (casing, whitespace)
    2. Impute missing engagement scores using industry + region medians
    3. Impute missing revenue using a size-band-based estimate
    4. Flag and quantify data-quality issues found (for a QA log)
    5. Engineer a firmographic "targeting readiness" feature set
    6. Output prospects_enriched.csv + a data_quality_report.csv
"""

import pandas as pd
import numpy as np

IN_PATH = "/home/claude/amex-project/data/prospects_raw.csv"
OUT_PATH = "/home/claude/amex-project/data/prospects_enriched.csv"
REPORT_PATH = "/home/claude/amex-project/outputs/data_quality_report.csv"

df = pd.read_csv(IN_PATH)
issues = {}

# 1. Standardize text fields
issues["inconsistent_industry_casing"] = int((df["industry"] != df["industry"].str.title()).sum())
df["industry"] = df["industry"].str.strip().str.title()
df["region"] = df["region"].str.strip().str.title()

# 2. Impute missing engagement score with industry+region median
issues["missing_engagement_score"] = int(df["digital_engagement_score"].isna().sum())
df["digital_engagement_score"] = df.groupby(["industry", "region"])["digital_engagement_score"] \
    .transform(lambda s: s.fillna(s.median()))
df["digital_engagement_score"] = df["digital_engagement_score"].fillna(
    df["digital_engagement_score"].median()
)

# 3. Impute missing revenue using median revenue per size band
issues["missing_revenue"] = int(df["est_annual_revenue"].isna().sum())
df["est_annual_revenue"] = df.groupby("company_size_band")["est_annual_revenue"] \
    .transform(lambda s: s.fillna(s.median()))

# 4. Duplicate ID check
issues["duplicate_prospect_ids"] = int(df["prospect_id"].duplicated().sum())

# 5. Feature engineering — targeting readiness score (0-100)
#    Weighted blend: engagement (40%), company scale (30%), tenure stability (30%)
size_map = {b: i + 1 for i, b in enumerate(
    ["1-9 employees", "10-49 employees", "50-249 employees",
     "250-999 employees", "1000+ employees"])}
df["size_rank"] = df["company_size_band"].map(size_map)

df["engagement_norm"] = (df["digital_engagement_score"] - df["digital_engagement_score"].min()) / \
    (df["digital_engagement_score"].max() - df["digital_engagement_score"].min())
df["scale_norm"] = (df["size_rank"] - df["size_rank"].min()) / \
    (df["size_rank"].max() - df["size_rank"].min())
df["tenure_norm"] = (df["years_in_business"] - df["years_in_business"].min()) / \
    (df["years_in_business"].max() - df["years_in_business"].min())

df["targeting_readiness_score"] = (
    0.40 * df["engagement_norm"] + 0.30 * df["scale_norm"] + 0.30 * df["tenure_norm"]
) * 100
df["targeting_readiness_score"] = df["targeting_readiness_score"].round(1)

df["targeting_tier"] = pd.cut(
    df["targeting_readiness_score"],
    bins=[-1, 33, 66, 100],
    labels=["Tier 3 - Nurture", "Tier 2 - Warm", "Tier 1 - Priority"]
)

df = df.drop(columns=["size_rank", "engagement_norm", "scale_norm", "tenure_norm"])
df.to_csv(OUT_PATH, index=False)

report = pd.DataFrame(list(issues.items()), columns=["issue", "records_affected"])
report["pct_of_total"] = (report["records_affected"] / len(df) * 100).round(2)
report.to_csv(REPORT_PATH, index=False)

print("Data quality issues found & resolved:")
print(report.to_string(index=False))
print(f"\nEnriched file written to {OUT_PATH}")
print(f"\nTargeting tier distribution:\n{df['targeting_tier'].value_counts()}")
