-- BASF Business Performance Analysis | PostgreSQL 17
-- Run each numbered query independently in pgAdmin (select it, then F5).
-- Source: the BASF Report 2025 ten-year summary, as published.
-- Read docs/data_preparation.md for 2017, 2018 and 2024 restatements.
-- Monetary values: million EUR. Margins/ROCE: percent units, not fractions.
-- No missing values are replaced with zero.

-- Q1: How did sales change between 2016 and 2025?
-- The first query returns the annual trend with 2016 as a comparison base.
WITH sales AS (
    SELECT year, value, unit,
           FIRST_VALUE(value) OVER (ORDER BY year) AS sales_2016
    FROM public.basf_kpis
    WHERE kpi = 'Sales'
)
SELECT year, value AS sales_million_eur, unit,
       value - sales_2016 AS change_since_2016_million_eur,
       ROUND(100.0 * (value - sales_2016) / NULLIF(sales_2016, 0), 2)
           AS change_since_2016_pct
FROM sales
ORDER BY year;

-- Q2: How did EBITDA, EBIT and net income evolve?
-- One row per year; all three columns are in million EUR.
-- Do not reconcile unadjusted EBITDA with the adjusted margin in Q3.
SELECT year,
       MAX(value) FILTER (WHERE kpi = 'EBITDA') AS ebitda_million_eur,
       MAX(value) FILTER (WHERE kpi = 'EBIT') AS ebit_million_eur,
       MAX(value) FILTER (WHERE kpi = 'Net Income') AS net_income_million_eur
FROM public.basf_kpis
WHERE kpi IN ('EBITDA', 'EBIT', 'Net Income')
GROUP BY year
ORDER BY year;

-- Q3: Which years had the highest and lowest EBITDA margin before special items?
-- Return every tied maximum/minimum, if present.
WITH ranked_margins AS (
    SELECT year, value,
           DENSE_RANK() OVER (ORDER BY value DESC) AS highest_rank,
           DENSE_RANK() OVER (ORDER BY value ASC) AS lowest_rank
    FROM public.basf_kpis
    WHERE kpi = 'EBITDA Margin before special items' AND value IS NOT NULL
)
SELECT year, value AS ebitda_margin_before_special_items_pct,
       CASE WHEN highest_rank = 1 AND lowest_rank = 1 THEN 'Highest and lowest'
            WHEN highest_rank = 1 THEN 'Highest'
            ELSE 'Lowest' END AS position
FROM ranked_margins
WHERE highest_rank = 1 OR lowest_rank = 1
ORDER BY value DESC, year;

-- Q4: How did operating cash flow and free cash flow evolve?
-- Both source series are in million EUR.
SELECT year,
       MAX(value) FILTER (WHERE kpi = 'Operating Cash Flow')
           AS operating_cash_flow_million_eur,
       MAX(value) FILTER (WHERE kpi = 'Free Cash Flow') AS free_cash_flow_million_eur
FROM public.basf_kpis
WHERE kpi IN ('Operating Cash Flow', 'Free Cash Flow')
GROUP BY year
ORDER BY year;

-- Q5: How did investments and ROCE evolve?
-- Investments are additions to PPE and intangible assets, not cash CapEx.
-- Do not subtract them from operating cash flow to reconstruct FCF.
-- Side-by-side trends do not establish causation; 2016 ROCE remains NULL.
SELECT year,
       MAX(value) FILTER (
           WHERE kpi = 'Investments / CapEx (additions to PPE and intangible assets)'
       ) AS investments_additions_million_eur,
       MAX(value) FILTER (WHERE kpi = 'ROCE') AS roce_pct
FROM public.basf_kpis
WHERE kpi IN ('Investments / CapEx (additions to PPE and intangible assets)', 'ROCE')
GROUP BY year
ORDER BY year;

-- Q6: Which years had the largest annual sales growth and decline?
-- Return all nine year-on-year changes ranked in both directions.
-- Rankings describe changes in the published series, including scope changes.
WITH previous_sales AS (
    SELECT year, value,
           LAG(year) OVER (ORDER BY year) AS previous_year,
           LAG(value) OVER (ORDER BY year) AS previous_value
    FROM public.basf_kpis
    WHERE kpi = 'Sales'
), changes AS (
    SELECT year, previous_year, value AS sales_million_eur,
           previous_value AS previous_sales_million_eur,
           value - previous_value AS yoy_change_million_eur,
           100.0 * (value - previous_value) / NULLIF(previous_value, 0)
               AS yoy_change_pct
    FROM previous_sales
    WHERE previous_year = year - 1 AND previous_value IS NOT NULL
)
SELECT year, previous_year, sales_million_eur, previous_sales_million_eur,
       yoy_change_million_eur, ROUND(yoy_change_pct, 2) AS yoy_change_pct,
       DENSE_RANK() OVER (ORDER BY yoy_change_pct DESC NULLS LAST) AS growth_rank,
       DENSE_RANK() OVER (ORDER BY yoy_change_pct ASC NULLS LAST) AS decline_rank
FROM changes
ORDER BY yoy_change_pct DESC NULLS LAST, year;

-- Q7: In which years was net income negative?
-- Sales and EBIT provide context; they do not explain the cause of a loss.
WITH annual_results AS (
    SELECT year,
           MAX(value) FILTER (WHERE kpi = 'Sales') AS sales_million_eur,
           MAX(value) FILTER (WHERE kpi = 'EBIT') AS ebit_million_eur,
           MAX(value) FILTER (WHERE kpi = 'Net Income') AS net_income_million_eur
    FROM public.basf_kpis
    WHERE kpi IN ('Sales', 'EBIT', 'Net Income')
    GROUP BY year
)
SELECT year, sales_million_eur, ebit_million_eur, net_income_million_eur
FROM annual_results
WHERE net_income_million_eur < 0
ORDER BY year;

-- Q8: How does 2025 compare with 2024 across all nine KPIs?
-- Monetary deltas: million EUR. Margin/ROCE deltas: percentage points (pp).
-- Monetary % changes are shown only for a positive base and nonnegative current
-- value. This avoids misleading growth percentages across losses/zero bases.
-- The delta is a numerical increase/decrease, not automatically good/bad.
SELECT current_kpi.kpi,
       previous_kpi.value AS value_2024,
       current_kpi.value AS value_2025,
       current_kpi.unit,
       current_kpi.value - previous_kpi.value AS absolute_change,
       CASE WHEN current_kpi.unit = '%' THEN 'pp'
            ELSE current_kpi.unit END AS change_unit,
       CASE WHEN current_kpi.unit = 'million EUR'
                  AND previous_kpi.value > 0 AND current_kpi.value >= 0
            THEN ROUND(100.0 * (current_kpi.value - previous_kpi.value)
                       / NULLIF(previous_kpi.value, 0), 2)
       END AS monetary_change_pct
FROM public.basf_kpis AS current_kpi
LEFT JOIN public.basf_kpis AS previous_kpi
    ON previous_kpi.kpi = current_kpi.kpi
   AND previous_kpi.year = current_kpi.year - 1
   AND previous_kpi.unit = current_kpi.unit
WHERE current_kpi.year = 2025
ORDER BY current_kpi.kpi;
