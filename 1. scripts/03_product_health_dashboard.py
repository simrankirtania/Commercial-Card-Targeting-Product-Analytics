"""
03_product_health_dashboard.py
---------------------------------
Builds a 4-panel product/portfolio health dashboard (saved as a PNG) covering:
    A. Targeting funnel — prospect tiers by industry
    B. Monthly commercial-card spend trend
    C. A/B test lift — Smart Spend Alerts (activation vs dispute rate)
    D. Cohort heatmap — week-4 activation rate by acquisition month x variant

Mirrors JD requirement: "Oversee product documentation, performance
dashboards ... Monitor product health metrics and user analytics."
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=0.9)
DATA_DIR = "/home/claude/amex-project/data"
OUT_DIR = "/home/claude/amex-project/outputs"

prospects = pd.read_csv(f"{DATA_DIR}/prospects_enriched.csv")
transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv", parse_dates=["txn_date"])
ab_summary = pd.read_csv(f"{OUT_DIR}/ab_test_results.csv")
cohort = pd.read_csv(f"{OUT_DIR}/cohort_activation_table.csv")

fig, axes = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle("Commercial Card Product & Targeting Health Dashboard",
             fontsize=15, fontweight="bold")

# A. Targeting funnel by industry
tier_industry = prospects.groupby(["industry", "targeting_tier"], observed=True).size().unstack(fill_value=0)
tier_industry = tier_industry[["Tier 1 - Priority", "Tier 2 - Warm", "Tier 3 - Nurture"]]
tier_industry.plot(kind="barh", stacked=True, ax=axes[0, 0],
                    color=["#2E7D32", "#FBC02D", "#B0BEC5"])
axes[0, 0].set_title("A. Prospect Targeting Funnel by Industry")
axes[0, 0].set_xlabel("Number of Prospects")
axes[0, 0].set_ylabel("")
axes[0, 0].legend(title="Tier", fontsize=8)

# B. Monthly spend trend
monthly = transactions.set_index("txn_date").resample("ME")["amount"].sum() / 1000
axes[0, 1].plot(monthly.index, monthly.values, marker="o", color="#1565C0")
axes[0, 1].set_title("B. Monthly Commercial Card Spend ($000s)")
axes[0, 1].set_ylabel("Total Spend ($000s)")
axes[0, 1].tick_params(axis="x", rotation=30)

# C. A/B test lift
metrics = ab_summary["metric"]
control_vals = ab_summary["control_mean"]
treatment_vals = ab_summary["treatment_mean"]
x = range(len(metrics))
width = 0.35
axes[1, 0].bar([i - width / 2 for i in x], control_vals, width, label="Control", color="#90A4AE")
axes[1, 0].bar([i + width / 2 for i in x], treatment_vals, width, label="Treatment", color="#1E88E5")
axes[1, 0].set_xticks(list(x))
axes[1, 0].set_xticklabels(["Week-4\nActivation Rate", "30-Day\nDispute Rate"])
axes[1, 0].set_title("C. Smart Spend Alerts — A/B Test Result\n(both deltas significant at p < 0.05)")
axes[1, 0].legend()

# D. Cohort heatmap
cohort_plot = cohort.set_index("cohort_month")
sns.heatmap(cohort_plot, annot=True, fmt=".2f", cmap="YlGnBu", ax=axes[1, 1],
            cbar_kws={"label": "Week-4 Activation Rate"})
axes[1, 1].set_title("D. Cohort Activation Rate by Acquisition Month")
axes[1, 1].set_xlabel("Variant")
axes[1, 1].set_ylabel("Acquisition Month")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f"{OUT_DIR}/product_health_dashboard.png", dpi=160)
print(f"Dashboard saved to {OUT_DIR}/product_health_dashboard.png")
