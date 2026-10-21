# Native Power BI implementation

## Status

The one-page native report is implemented in `powerbi/BASF.pbip` and has
been opened and refreshed in Power BI Desktop. The project owner approved its
final appearance. Screenshots were reviewed for the 2025 default, selection of
2024 while retaining the full chart history, and missing ROCE in 2016.

The project owner ran `powerbi/verify_in_desktop.dax` in Desktop DAX Query
View and reported **all 22 checks as PASS** on 21 October 2026. This result was
reported in chat; no result-table screenshot or machine-readable export was
provided for independent inspection. This distinction is retained in the
validation record below.

The first supplied native PDF had misaligned charts and values and was rejected.
A subsequent native PDF supplied on 21 October 2026 was rendered and visually
reviewed: its cards and four charts align with the background, all nine 2025
values match the CSV, and labels and footer remain readable. This accepted
[PDF](../powerbi/preview/report-2025.pdf) and its
[directly rendered image](../powerbi/preview/report-2025.png) are now included.
The export uses Italian numeric formatting; values remain in the original units.
No generated mockup is presented as an exported Power BI report. The PBIP/PBIR
source is the repository deliverable; a compiled PBIX is not included.

## Implementation decisions

The semantic model explicitly sets `defaultPowerBIDataSourceVersion` to
`powerBI_V3` and uses semantic-model definition version 4.0. The earlier package
omitted that enhanced-metadata setting and failed during Desktop conversion.
The final package opened and refreshed successfully.

The registered page background uses Power BI's nested `image.image` structure,
with expression-wrapped name and scaling. A flat image object passed the
open-ended JSON schema but did not render. See Microsoft's
[page-formatting reference](https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/powerbi-report-cli/references/authoring/page-formatting.md).

The decorative layer includes emerald/teal gradients, diagonal facets, perimeter
traces, the original BASF logo, genuine Ludwigshafen photographs, bold card
headings and original units. Its caption placement and card spacing were revised
against Desktop screenshots. Plot backgrounds use subdued gradients rather than
decorative data marks. Values, comparisons, charts and the year selector remain
native Power BI visuals.

## Opening the project on Windows

1. Extract the complete package with **Extract all**. Do not open files inside
   the ZIP or move the PBIP away from its two companion folders.
2. Optionally, in `powerbi/assets`, open `SpaceGrotesk-Medium.ttf` and click **Install**. Close
   and reopen Power BI Desktop if it was already running. This font is supplied
   under the accompanying SIL Open Font License. Desktop and service font
   behaviour still need checking; native text has a Segoe UI/sans-serif fallback.
   The title and decorative labels are rendered in Space Grotesk in the background
   and do not require installing the font.
3. Open `powerbi/BASF.pbip` in a recent Power BI Desktop. The file
   `powerbi/BASF.Report/definition.pbir` is an alternative entry point. If project
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
value. Card measures explicitly apply the selected year. The report opens with
2025 saved as the slicer selection. If the selection is cleared, card measures
fall back to the latest year, 2025.
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

## Validation record

Completed outside Desktop:

- 30 PBIP/PBIR JSON definitions validated against their declared Microsoft JSON
  schemas, including semantic query references.
- The V3 theme independently validated against Microsoft's theme schema 2.159.
- Embedded CSV bytes checked against the repository CSV, including all 90 pairs,
  original units and the null observation.
- Native measure/column references, canvas bounds, image nesting, resource
  filenames and theme registration checked.
- Decorative background rendered and visually inspected separately.

Completed in Desktop, based on screenshots reviewed on 21 October 2026:

- The report opened and refreshed, with nine 2025 values matching the source CSV.
- The approved geometric background, photo captions and separated card typography
  rendered without the earlier overlaps.
- Selecting 2024 changed Sales to 61,444 and the other visible values to their
  2024 observations. All four history charts retained 2016–2025. The dropdown
  obscured the ROCE card in that particular screenshot, so it is not counted as
  a visually inspected 2024 value.
- Selecting 2016 left ROCE blank, displayed `Not reported`, and displayed
  `No prior-year value` for comparisons outside the available period.
- The owner reported all 22 supplied DAX checks as PASS. Those checks cover row
  count, missingness, all nine 2025 values, selected 2024 Sales, percentage-point
  changes, loss/negative-base guards and retained chart history. The DAX result
  table itself was not independently inspected.

A subsequent native PDF and its rendered portfolio image were reviewed and
accepted on 21 October 2026, resolving the earlier presentation blocker. This
static review does not independently rerun Desktop interactions or DAX.
Keyboard-only accessibility, Power BI Service font rendering and a full automatic
comparison of every visual cell across every year have not been tested.

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

## Repository layout

The PBIP entry point is directly in `powerbi/`; an extra `BASF/` wrapper was
removed. `BASF.Report` and `BASF.SemanticModel` are required companion folders.
The deeper `definition/pages/.../visuals/...` directories belong to the PBIR
format and are preserved. `assets/` contains the originals needed to regenerate
the background; `tools/` contains the reproducible build and checking scripts.
The superseded HTML prototype was removed; Git history preserves it.

The first export's scaling issue was not reproduced in the subsequently supplied
PDF. No data, background or visual positions were changed for this documentation
review. The accepted PDF records the 2025 view; year interactions remain available
in the editable PBIP.

## Repeatable structural checks

From the repository root, using Python 3.12 (the tested version):

```text
python tools/check_powerbi_project.py
python -m pip install jsonschema==4.26.0
python tools/check_powerbi_project.py --schemas
```

The first command uses only the standard library. Schema validation additionally
needs `jsonschema` and internet access to fetch Microsoft's declared schemas.
Both checks passed again on 21 October 2026: exact CSV bytes and checksum,
90 unique observations, missing 2016 ROCE, 23 visual bindings/canvas bounds,
46 measures and 30 declared-schema definitions. These are structural checks,
not execution of DAX or the Power BI rendering engine.
