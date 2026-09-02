-- ============================================================================
-- targeting_and_spend_queries.sql
-- Prospect targeting + commercial-card spend analysis queries.
-- Tables assumed loaded (e.g., via SQLite/Hive) from the CSVs in /data:
--   prospects_enriched(prospect_id, industry, region, company_size_band,
--                       est_annual_revenue, digital_engagement_score,
--                       years_in_business, existing_bank_relationship,
--                       targeting_readiness_score, targeting_tier)
--   customers(customer_id, source_prospect_id, industry, region, ...,
--             acquisition_date, credit_line)
--   transactions(customer_id, txn_date, spend_category, amount)
--   feature_rollout(customer_id, acquisition_date, variant,
--                    week4_active_rate, dispute_rate_30d, cohort_month)
-- ============================================================================

-- 1. PRIORITY PROSPECT LIST FOR OUTBOUND TARGETING
-- Highest-readiness prospects, by industry, that don't yet have a competing
-- banking relationship (best conversion economics).
SELECT
    industry,
    region,
    company_size_band,
    prospect_id,
    targeting_readiness_score,
    targeting_tier
FROM prospects_enriched
WHERE targeting_tier = 'Tier 1 - Priority'
  AND existing_bank_relationship = 'No'
ORDER BY targeting_readiness_score DESC
LIMIT 200;

-- 2. INDUSTRY-LEVEL TARGETING FUNNEL SUMMARY
SELECT
    industry,
    COUNT(*)                                                   AS total_prospects,
    SUM(CASE WHEN targeting_tier = 'Tier 1 - Priority' THEN 1 ELSE 0 END) AS tier1_count,
    ROUND(AVG(targeting_readiness_score), 1)                  AS avg_readiness_score,
    ROUND(AVG(est_annual_revenue), 0)                          AS avg_est_revenue
FROM prospects_enriched
GROUP BY industry
ORDER BY tier1_count DESC;

-- 3. CUSTOMER SPEND BY CATEGORY (last 90 days) — product/portfolio health input
SELECT
    spend_category,
    COUNT(DISTINCT customer_id)                AS active_customers,
    ROUND(SUM(amount), 2)                       AS total_spend,
    ROUND(AVG(amount), 2)                       AS avg_txn_amount
FROM transactions
WHERE txn_date >= date('now', '-90 day')
GROUP BY spend_category
ORDER BY total_spend DESC;

-- 4. MONTHLY SPEND TREND (funnel/engagement performance)
SELECT
    strftime('%Y-%m', txn_date)  AS spend_month,
    COUNT(DISTINCT customer_id)  AS active_customers,
    ROUND(SUM(amount), 2)        AS total_spend
FROM transactions
GROUP BY spend_month
ORDER BY spend_month;

-- 5. TOP-DECILE CUSTOMERS BY SPEND (for retention / cross-sell targeting)
WITH customer_spend AS (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
),
ranked AS (
    SELECT customer_id, total_spend,
           NTILE(10) OVER (ORDER BY total_spend DESC) AS spend_decile
    FROM customer_spend
)
SELECT c.customer_id, c.industry, c.region, r.total_spend
FROM ranked r
JOIN customers c ON c.customer_id = r.customer_id
WHERE r.spend_decile = 1
ORDER BY r.total_spend DESC;

-- 6. A/B TEST — SMART SPEND ALERTS FEATURE (product health metrics)
SELECT
    variant,
    COUNT(*)                             AS customers,
    ROUND(AVG(week4_active_rate), 3)     AS avg_week4_active_rate,
    ROUND(AVG(dispute_rate_30d), 3)      AS avg_dispute_rate_30d
FROM feature_rollout
GROUP BY variant;

-- 7. COHORT ANALYSIS — WEEK-4 ACTIVATION RATE BY ACQUISITION MONTH & VARIANT
SELECT
    cohort_month,
    variant,
    COUNT(*)                          AS cohort_size,
    ROUND(AVG(week4_active_rate), 3)  AS avg_week4_active_rate
FROM feature_rollout
GROUP BY cohort_month, variant
ORDER BY cohort_month, variant;
