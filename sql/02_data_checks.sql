-- Run after importing data/processed/basf_kpis_2016_2025.csv.
-- Expected: 90 | 10 | 9 | 2016 | 2025 | 1.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT year) AS total_years,
    COUNT(DISTINCT kpi) AS total_kpis,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(*) FILTER (WHERE value IS NULL) AS missing_values
FROM public.basf_kpis;

-- Expected: one row, 2016 | ROCE | NULL | %.
SELECT year, kpi, value, unit
FROM public.basf_kpis
WHERE value IS NULL;

-- Expected: ten rows, each with nine KPIs.
SELECT year, COUNT(*) AS kpi_count
FROM public.basf_kpis
GROUP BY year
ORDER BY year;

-- Expected: no rows. The primary key also prevents duplicates.
SELECT year, kpi, COUNT(*) AS occurrences
FROM public.basf_kpis
GROUP BY year, kpi
HAVING COUNT(*) > 1;
