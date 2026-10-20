# PostgreSQL setup and import

The local database is named `basf_business_performance`. The CSV keeps its tidy
structure in `public.basf_kpis`: `year`, `kpi`, `value`, `unit`.

## First-time setup

1. Create `basf_business_performance` in pgAdmin with the appropriate local owner.
2. Open its Query Tool and run `sql/01_create_table.sql` once.
3. Right-click `Schemas > public > Tables > basf_kpis` and choose Import/Export Data.
4. Select **Import** and `data/processed/basf_kpis_2016_2025.csv` from the local clone.
5. Set format CSV, encoding UTF8, Header on, delimiter comma, Quote and Escape double
   quote, and the NULL string empty. Import columns in this order: year, kpi, value, unit.
6. Run the statements in `sql/02_data_checks.sql` independently.

The first check must return 90 rows, 10 years, 9 KPIs, 2016–2025 and one missing
value. The missing-value query must return only `2016 | ROCE | NULL | %`.
Each year must have nine rows, and the duplicate check must return none.

The table definition permits the missing value and prevents duplicate year/KPI
pairs. Monetary and percentage values use `NUMERIC`; no missing value is imputed.
Do not rerun the table creation or import on an already populated table.

## Optional psql import

For a fresh, empty table, launch psql from the repository root, connected to the
BASF database, and run this client-side command on one line:

```text
\copy public.basf_kpis (year,kpi,value,unit) FROM 'data/processed/basf_kpis_2016_2025.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '', ENCODING 'UTF8')
```

`\copy` runs in psql, not in the pgAdmin Query Tool. Never include passwords or
machine-specific authentication configuration in this repository.

## Execution evidence

On October 20, 2026, the table was created and the CSV imported in PostgreSQL 17
using pgAdmin on the project owner's Windows computer. Screenshots confirmed the
expected totals, and the owner confirmed that the sole missing row was 2016 ROCE.
The full check file was also executed against the same CSV in the isolated
PostgreSQL-compatible validation environment described in `sql_analysis.md`.
