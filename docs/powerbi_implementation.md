# Native Power BI implementation

## Status

The native project is prepared in `powerbi/BASF/BASF.pbip`. It contains a semantic
model, DAX measures and a one-page PBIR report definition. The V2 package has
opened and refreshed in the user's Desktop: its screenshot shows all nine 2025
card values matching the CSV and all four native history charts, without the
earlier field errors. Full DAX acceptance tests and interaction checks remain
pending. No final PBIX or finished portfolio export is claimed at this stage.

First Desktop attempt: the project opened, but requested an enhanced-metadata
upgrade; after that upgrade its tables disappeared and visuals reported
`Missing_References`. The decorative background/theme were also absent.
The corrected package explicitly sets `defaultPowerBIDataSourceVersion` to
`powerBI_V3`, uses semantic-model definition version 4.0 and matches image/theme
resource identifiers to their filenames. The corrected package still requires
a fresh Desktop opening and refresh; its success is not yet established.
Microsoft's [semantic model definition example](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/semantic-model-definition)
shows the enhanced-metadata model property.

V2 Desktop review then confirmed that data and chart bindings worked, but the
page background was still absent. V3 corrects the background's required nested
`image.image` structure, including expression-wrapped name and scaling. The
previous flat structure passed the open-ended JSON property schema but was not
rendered. This nesting is documented in Microsoft's
[page-formatting reference](https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/powerbi-report-cli/references/authoring/page-formatting.md).
V3 also refreshes the theme resource identifier, corrects the bundled static font's
family/style metadata, adds a Segoe UI/sans-serif fallback and increases card and
axis text sizes. The title, photos, logo, rounded surfaces, labels and units are
already in the registered background. V3 visual rendering still needs confirmation
in Desktop; no user reconstruction of these elements is intended.

## Opening the project on Windows

1. Extract the complete package with **Extract all**. Do not open files inside
   the ZIP or move the PBIP away from its two companion folders.
2. Optionally, in `BASF/assets`, open `SpaceGrotesk-Medium.ttf` and click **Install**. Close
   and reopen Power BI Desktop if it was already running. This font is supplied
   under the accompanying SIL Open Font License. Desktop and service font
   behaviour still need checking; native text has a Segoe UI/sans-serif fallback.
   The title and decorative labels are rendered in Space Grotesk in the background
   and do not require installing the font.
3. Open `BASF/BASF.pbip` in a recent Power BI Desktop. The file
   `BASF/BASF.Report/definition.pbir` is an alternative entry point. If project
   support is disabled, enable the relevant Power BI Project option under
   **File > Options and settings > Options > Preview features** and restart.
4. Click **Home > Refresh** to load the model. No PostgreSQL connection, password
   or source-file path is required for this portable snapshot.
5. Review the report and run the checks below. Save as a PBIX locally if desired;
   the PBIP remains the source-controlled implementation.

## Model and Power Query

- `basf_kpis`: the same 90 observations as the processed CSV, with the single
  missing 2016 ROCE observation preserved as null.
- `Report Year`: ten years used by a **disconnected** slicer. It does not filter
  history charts. No relationship is needed for this deliberately small model.
- The import partition embeds the exact CSV bytes as Base64 and loads them using
  Power Query `Csv.Document`. It promotes headers, maps the empty value to null
  and sets explicit types using `en-US` numeric parsing.
- This is a portable snapshot, **not another workbook-cleaning implementation**.
  The original Power Query cleaning workflow remains in `power_query/basf_kpis.m`.
  Python assembles project definitions and decorative assets; it does not clean
  or calculate the BASF source observations.
- Refresh loads the embedded snapshot. To use a revised CSV, update the processed
  file through the documented preparation workflow and run
  `python tools/build_powerbi_project.py` from the repository. Reopen and refresh
  Desktop. This command regenerates the authored report definitions, so preserve
  any manual Desktop edits before rebuilding.

`model.bim` records the CSV SHA256 annotation. The initial snapshot SHA256 is
`393023daf578f8c38c509c5873b8ed177566a02711e502cb4cbdd6c725d08822`.

## Measures and interactions

The model has 46 measures: selected year and five reusable measures per KPI
(history, selected value, previous value, change and change label). These are
display helpers for the existing nine KPIs, not additional financial indicators.
`measures.dax` provides a readable generated reference; the executable definitions
are in `BASF.SemanticModel/model.bim`.

History measures use `SELECTEDVALUE` after filtering to a single KPI. This avoids
summing unlike units or accidentally showing a multi-year total as an annual
value. Card measures explicitly apply the selected year. With no year selection,
cards use the latest year, 2025; this default is labelled beside the selector.
The dropdown permits 2016–2025, extending the prototype's 2024/2025 selection.

Margin and ROCE are stored in percentage points: the format appends a literal
percent sign, so 11 becomes 11.0%, not 1,100%. Their changes are percentage-point
differences. Monetary percentage changes appear only when the previous value is
positive and the current value is nonnegative. Loss transitions and zero bases
receive a text label rather than a misleading growth rate. Missing observations
remain blank; comparison labels explain missing prior-year values.

Selecting a year updates the cards; all four history charts retain 2016–2025.
Chart clicks do not cross-filter other visuals. Native history highlighting of
the selected year is not implemented. Deltas use neutral colours, including for
investments. These are explicit adaptations of the HTML design, not claims of
pixel-identical reproduction. The background contains decorative panels, labels,
logo and photographs; values, comparisons, chart marks and the slicer are native
Power BI visuals. No custom visual or HTML visual is required.

See [design notes and credits](powerbi_design.md) for all image/logo sources.
The title uses Space Grotesk rendered in the background; native text requests
Space Grotesk/Space Grotesk Medium with Segoe UI and sans-serif fallbacks.

## Validation and pending acceptance

Completed outside Desktop:

- 30 PBIP/PBIR JSON definitions validated against their declared Microsoft JSON
  schemas, including semantic query references.
- The V3 theme independently validated against Microsoft's theme schema 2.159.
- Embedded CSV bytes checked against the repository CSV, including all 90 pairs,
  original units and the null observation.
- Native measure/column references, canvas bounds, image nesting, resource
  filenames and theme registration checked.
- Decorative background rendered and visually inspected separately.

**Pending in Desktop for V3:** reopen/refresh, full DAX acceptance tests, font rendering, chart
colours, negative profitability values, legends, label clipping, slicer operation,
blank display, keyboard readability and final PDF/screenshot export. Run
`BASF/verify_in_desktop.dax` in DAX Query View; it must return PASS on every row.
Then select 2024 and 2016 manually to check interaction and missing-value display.
These DAX checks are provided but have not yet been executed.

Expected 2025 card values in source units:

| KPI | Value | Change vs 2024 |
| --- | ---: | ---: |
| Sales | 59,657 | −2.91% |
| EBITDA | 5,618 | −9.55% |
| EBIT | 1,634 | −9.72% |
| Net income | 1,619 | +24.73% |
| EBITDA margin before special items | 11.0% | −0.8 pp |
| Operating cash flow | 5,610 | −19.23% |
| Free cash flow | 1,342 | +79.41% |
| Investments / asset additions | 4,787 | −29.87% |
| ROCE | 5.8% | +0.7 pp |

Restatements and discontinued operations limit comparability. The EBITDA margin
is before special items; EBITDA is unadjusted. Investment additions are not cash
CapEx and cannot be subtracted from OCF to reproduce FCF.

## Format references

- [Microsoft: report project folder and PBIR](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
- [Microsoft: semantic model project folder and model.bim](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
- The `$schema` properties in the project files identify the exact schema versions.

The background can be regenerated with `python tools/render_powerbi_background.py`
(Pillow and Inkscape required). It contains no data values and is not a screenshot
of a running Power BI report. Local caches and PBIX files are excluded from Git.
