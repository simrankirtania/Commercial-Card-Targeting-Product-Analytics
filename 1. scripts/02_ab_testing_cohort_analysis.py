"""
02_ab_testing_cohort_analysis.py
----------------------------------
Statistical evaluation of the "Smart Spend Alerts" product feature A/B test,
plus a cohort-retention view — mirrors the JD requirement:
"Utilize analytics to inform business and customer strategy, optimize user
journeys, and support growth through experimentation (A/B testing, cohort
analysis, funnel performance)."

Outputs:
    - Welch's t-test on week-4 activation rate (treatment vs control)
    - Welch's t-test on 30-day dispute rate (treatment vs control)
    - Cohort table: week-4 activation rate by acquisition month x variant
    - ab_test_results.csv summary for the dashboard
"""

import pandas as pd
from scipy import stats

DATA_PATH = "/home/claude/amex-project/data/feature_rollout.csv"
OUT_PATH = "/home/claude/amex-project/outputs/ab_test_results.csv"

df = pd.read_csv(DATA_PATH)

control = df[df["variant"] == "control"]
treatment = df[df["variant"] == "treatment"]

# Welch's t-test (unequal variance assumption — safer default for real-world data)
t_active, p_active = stats.ttest_ind(
    treatment["week4_active_rate"], control["week4_active_rate"], equal_var=False
)
t_disp, p_disp = stats.ttest_ind(
    treatment["dispute_rate_30d"], control["dispute_rate_30d"], equal_var=False
)

lift_active = treatment["week4_active_rate"].mean() - control["week4_active_rate"].mean()
lift_disp = treatment["dispute_rate_30d"].mean() - control["dispute_rate_30d"].mean()

summary = pd.DataFrame([
    {
        "metric": "week4_active_rate",
        "control_mean": round(control["week4_active_rate"].mean(), 4),
        "treatment_mean": round(treatment["week4_active_rate"].mean(), 4),
        "abs_lift": round(lift_active, 4),
        "t_stat": round(t_active, 3),
        "p_value": round(p_active, 5),
        "significant_at_5pct": p_active < 0.05,
    },
    {
        "metric": "dispute_rate_30d",
        "control_mean": round(control["dispute_rate_30d"].mean(), 4),
        "treatment_mean": round(treatment["dispute_rate_30d"].mean(), 4),
        "abs_lift": round(lift_disp, 4),
        "t_stat": round(t_disp, 3),
        "p_value": round(p_disp, 5),
        "significant_at_5pct": p_disp < 0.05,
    },
])
summary.to_csv(OUT_PATH, index=False)

# Cohort table
cohort = (
    df.groupby(["cohort_month", "variant"])["week4_active_rate"]
    .mean()
    .round(3)
    .reset_index()
    .pivot(index="cohort_month", columns="variant", values="week4_active_rate")
)
cohort.to_csv("/home/claude/amex-project/outputs/cohort_activation_table.csv")

print("=== A/B Test Summary: Smart Spend Alerts ===")
print(summary.to_string(index=False))
print("\n=== Cohort Table: Week-4 Activation Rate by Acquisition Month ===")
print(cohort.to_string())
