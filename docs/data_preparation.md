# Data preparation notes

## Source mapping

All year values are in columns **C:L** (2016–2025) of the separate `10y-overview-basf-ar25.xlsx`, sheet `10y-overview`; header row **4**. The corresponding rows of `all-tables-basf-ar25.xlsx`, sheet `10y-overview`, are one row lower because that sheet starts with a “Back to index” row.

| Output KPI | BASF source label | Separate workbook row | Unit |
| --- | --- | ---: | --- |
| Sales | Sales | 31 | million EUR |
| EBITDA | EBITDA | 32 | million EUR |
| EBIT | EBIT | 33 | million EUR |
| Net Income | Net income | 38 | million EUR |
| EBITDA Margin before special items | EBITDA margin before special items | 7 | % |
| Operating Cash Flow | Cash flows from operating activities | 8 | million EUR |
| Free Cash Flow | Free cash flow | 9 | million EUR |
| Investments / CapEx (additions to PPE and intangible assets) | Additions to property, plant and equipment and intangible assets | 19 | million EUR |
| ROCE | ROCE | 11 | % |

**Definitions matter.** BASF's reported margin is *before special items*, whereas the selected EBITDA series is unadjusted. The two must not be assumed to reconcile by division. “Investments / CapEx” here means BASF's additions to property, plant and equipment and intangible assets; it is **not** the cash payments for these assets used in BASF's free cash flow reconciliation. For 2025, additions are 4,787 million EUR in the ten-year summary, while cash payments are 4,267 million EUR in `gby-free-cash-flow` row 7 and `gby-cash-flow-statement` row 13 of the all-tables workbook. Do not subtract this additions series from operating cash flow to recreate free cash flow.

## Missing data and comparability

- BASF prints a dash for **2016 ROCE** (`C11`). The tidy row remains present with an empty value, representing SQL/Power BI null.
- Source footnote **a** (row 63) says 2017 figures marked `a` were restated when oil and gas activities were presented as discontinued operations.
- Source footnote **b** (row 64) says 2018 figures marked `b` were restated when construction chemicals activities were presented as discontinued operations.
- Source footnote **e** (row 67) says 2024 figures marked `e` were adjusted to present the Coatings business as a discontinued operation.
- The selected financial rows carrying these markers are Sales, EBITDA, EBIT and the reported EBITDA margin for 2017, 2018 and 2024; ROCE is marked for 2018 and 2024. Other selected figures, including the cash flow rows and Net income, are taken exactly as published in the same ten-year summary. The presence or absence of a marker is retained here as documentation, not a numerical adjustment.
- Differences across years can reflect these presentation changes, so apparent year-to-year movements should be interpreted with the BASF footnotes in mind.

Source values such as `61,223a` become `61223`; `12.0b` becomes `12.0`; negative values retain the minus sign. The source dash becomes null. No other rows or metrics are imported.

## Validation

The committed CSV was checked against the exact named rows and year columns in the untouched ten-year workbook: **90 records**, years 2016–2025, nine distinct KPIs per year, no duplicate year/KPI pair, and exactly one missing value (2016 ROCE). Representative cross-checks: 2016 Sales 57,550; 2024 Sales 61,444 after footnote removal; 2025 Sales 59,657; 2025 EBITDA 5,618; 2025 free cash flow 1,342; 2025 ROCE 5.8.

The Power Query script was executed in Power BI Desktop on September 29, 2026 against the unchanged ten-year workbook. The resulting preview displayed four columns and **90 rows**, including null for 2016 ROCE. The visible 2016–2018 values matched the committed CSV, including the footnote-marked 2017 and 2018 figures. A full export-and-compare of every Power Query result against the CSV was not performed; the CSV itself was checked cell by cell against the source workbook independently.
