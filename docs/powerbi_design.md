# Power BI report design

## Status

This is an approved **design prototype**, not a native Power BI dashboard.
`powerbi/design/preview.html` opens in a browser and contains its own data and
image bytes. No PBIX dashboard, DAX measures or Power BI interactions have been
implemented as part of this design milestone. The earlier local
`BASF_Data_Preparation.pbix` contains the Power Query preparation only and is not
included in this repository.

The native PBIP report is now implemented in `powerbi/BASF/` and its final
appearance was approved after review in Power BI Desktop. Year selection and
missing-value handling were checked in screenshots; the owner reported 22 PASS
results for the DAX acceptance query. See the [implementation and validation
record](powerbi_implementation.md). The browser preview remains a separate early
design reference; native PDF and final portfolio image exports are still pending.

## Approved direction

- A single landscape page, targeting a 16:9 desktop canvas.
- Dark green background with bright green accents and readable pale text.
- Native V6 refinement: emerald/teal gradients, diagonal facets and perimeter
  traces outside the data areas; subdued gradient plot surfaces.
- Space Grotesk for the title, values and labels; the browser preview loads the
  font from Google Fonts and falls back to Segoe UI if unavailable.
- The original white BASF logo and its “We create chemistry” claim at top left.
- Two genuine BASF Ludwigshafen photographs, blended into the top-right edge
  without separate frames or gaps.
- Nine rounded KPI cards with subtle gradient borders and restrained highlights.
- Four history charts: sales; EBITDA/EBIT/net income; operating/free cash flow;
  and investments (asset additions).
- A 2024/2025 selector updates card values and year-on-year deltas; chart histories
  retain the full 2016–2025 period and highlight the selected year.
- Percentage-point deltas for margin and ROCE, percentage deltas for monetary
  measures. Investment decreases are displayed neutrally rather than labelled
  automatically favourable or unfavourable.
- An explicit independent portfolio notice; this is not an official BASF report.

The four charts are a compact overview of the SQL questions. Margin/ROCE trends,
full rankings and loss-year details remain available in the SQL analysis; the
prototype does not yet provide a separate visual answer to every question.

The narrow-screen layout stacks the content for readability. The intended
Power BI canvas remains landscape; the responsive browser behaviour is not a
claim about a native Power BI mobile layout.

## Dataset and validation

The embedded observations come from
`data/processed/basf_kpis_2016_2025.csv`: 90 year/KPI pairs and a single missing
value (2016 ROCE). Monetary figures remain in million EUR. No new financial
metrics or imputed observations were introduced. The preview is a snapshot;
it does not connect to PostgreSQL or refresh the source workbook.

As with the SQL analysis, published BASF restatements affect comparability.
The EBITDA margin is before special items, whereas EBITDA is unadjusted.
Investment additions must not be used to reconstruct FCF from operating cash
flow. See `data_preparation.md` and `sql_analysis.md`.

## Asset credits

All company marks and photos remain the property of their respective owners.
Assets identify the company being analysed; they do not imply BASF sponsorship
or endorsement. The logo file is used as supplied, without redrawing, recolouring,
changing its proportions or removing its claim.

- Official white logo: [BASF Report 2025](https://report.basf.com/2025/en/),
  [original SVG](https://report.basf.com/2025/en/_assets/images/logo.svg?h=ukb0Fg6R).
- Logo reference: [BASF Brand Portal](https://brandportal.basf.com/global/en/create/corporate-design/logo).
- Dusk photograph: © BASF, [2025 annual press conference press photos](https://www.presseportal.de/pm/16344/5980793).
- Daytime aerial photograph: © BASF, [Ludwigshafen Verbund site, 2018 press release](https://www.basf.com/no/en/media/news-releases/2018/04/p-18-183).
- Typeface: [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk).

## Remaining presentation step

Export the implemented native report to PDF and capture clean screenshots before
adding static portfolio previews. Refer to `powerbi_implementation.md` for the
completed checks and their evidence limits.
