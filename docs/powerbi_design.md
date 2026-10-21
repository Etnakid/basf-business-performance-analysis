# Power BI report design

## Status

This is an approved **design prototype**, not a native Power BI dashboard.
`powerbi/design/preview.html` opens in a browser and contains its own data and
image bytes. No PBIX dashboard, DAX measures or Power BI interactions have been
implemented as part of this design milestone. The earlier local
`BASF_Data_Preparation.pbix` contains the Power Query preparation only and is not
included in this repository.

## Approved direction

- A single landscape page, targeting a 16:9 desktop canvas.
- Dark green background with bright green accents and readable pale text.
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

## Next implementation step

Build the native Power BI report from the approved layout, add and validate the
required DAX measures, reproduce the intended year-selection behaviour and
review the exported report before treating the dashboard as complete. Confirm
font support and legibility in Power BI during implementation.
