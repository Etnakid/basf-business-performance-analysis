-- Run once in the basf_business_performance database.
-- Existing tables are not dropped or replaced.
CREATE TABLE public.basf_kpis (
    year SMALLINT NOT NULL CHECK (year BETWEEN 2016 AND 2025),
    kpi TEXT NOT NULL,
    value NUMERIC,
    unit TEXT NOT NULL CHECK (unit IN ('million EUR', '%')),
    PRIMARY KEY (year, kpi)
);
