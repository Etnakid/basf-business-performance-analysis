# BASF Business Performance Analysis

A focused Junior Data Analyst / BI Analyst portfolio project using nine annual financial KPI series for 2016–2025. This repository currently contains **data preparation only**; analysis and reporting are later phases.

## Sources and files

- [BASF Report 2025, Ten-Year Summary](https://report.basf.com/2025/en/overviews/ten-year-summary.html), workbook `10y-overview-basf-ar25.xlsx`, sheet `10y-overview`.
- [BASF Report 2025, Download Center](https://report.basf.com/2025/en/services/downloads.html), workbook `all-tables-basf-ar25.xlsx`; its `10y-overview` sheet duplicates the summary and its 2024–2025 detail sheets provide definition checks.

Place the unchanged downloaded workbooks in `data/raw/`. This directory is excluded from Git. The two source copies inspected for this preparation have SHA-256 hashes `b3ae575749ca0740e837174169786c6c6ab10e0440a021e841ff488a1281ef11` and `3c51b713e17a113d0dd03128eea3eae6974395ba6f4775e3c014e52dcd0d8512`, respectively.

`data/processed/basf_kpis_2016_2025.csv` has columns `year,kpi,value,unit`. It contains 90 year/KPI combinations and one empty `value`: ROCE in 2016, shown as a dash by BASF. Monetary figures retain BASF's **million euros**; margins and ROCE retain **percent units** (for example 11.8 means 11.8%, not 0.118). Values are never imputed.

## Reproduce the Power Query transformation

1. Download the two official Excel files and put them unchanged in `data/raw/`.
2. In Excel or Power BI Desktop, create a blank Power Query, open Advanced Editor and paste `power_query/basf_kpis.m`.
3. Change only `RawFile` at the top to the full local path of `10y-overview-basf-ar25.xlsx`, then refresh.
4. Verify 90 rows, ten years, nine KPIs per year and only the 2016 ROCE null. Export the resulting table as UTF-8 CSV with header `year,kpi,value,unit` for the processed file.

The M query reads the ten-year sheet, skips the title rows, promotes the year header, selects exactly nine named source rows, removes all other content, unpivots 2016–2025, strips only the known trailing footnote letters `a`, `b`, `e`, parses numbers without altering their magnitude, and explicitly retains the 2016 ROCE null. Unexpected nonnumeric text fails refresh rather than silently changing a value. Its output is sorted by year and KPI.

The committed CSV was transcribed directly from the supplied source workbook and independently checked against those source cells. The M query was subsequently run in Power BI Desktop against the unchanged local BASF workbook: its preview showed four columns, 90 rows, the 2016 ROCE null, and the expected displayed values for 2016–2018. See [source mapping and limitations](docs/data_preparation.md). The Power BI preview check does not constitute a separate full export-and-compare of all 90 query results.

## Next milestone

SQL analysis and Power BI work are outside this data-preparation phase.
