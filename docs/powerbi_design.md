# Report design and asset credits

## Current design

The native entry point is `powerbi/BASF.pbip`. Its appearance was approved after
review in Power BI Desktop. The superseded HTML mockup was removed from current
files and remains available in Git history.

- One 16:9 landscape page with nine rounded KPI cards and four history charts.
- Emerald/teal gradients, diagonal facets and perimeter traces outside data areas;
  quiet plot backgrounds preserve contrast and do not add decorative data marks.
- The original white BASF logo and claim at top left; genuine Ludwigshafen photos
  fade into the top-right edge without separate frames.
- A Ludwigshafen caption accompanies the photos; Report Year sits above the slicer.
- Bold Space Grotesk headings in the decorative background. Native values request
  Space Grotesk with Segoe UI/sans-serif fallbacks.
- A 2016–2025 selector, initially set to 2025, updates card values and comparisons.
  The history charts retain the entire period. Native selected-year highlighting
  is not implemented.
- Sales, profitability, operating/free cash flow and investment additions have
  native charts. Margin/ROCE histories and rankings remain available in SQL.
- Comparisons use percentage points for margin/ROCE and percentages for eligible
  monetary values. Investment changes have neutral colours.
- Source/comparability notes and an independent portfolio notice appear at the foot.

The background includes decorative surfaces, labels, units, photographs and logo.
Values, comparison text, chart marks and the selector are native Power BI visuals.
The 90 observations and original units match the processed CSV; 2016 ROCE stays
missing. The report uses a portable snapshot rather than a live database connection.
See [implementation and validation](powerbi_implementation.md) for details.

## Export status

The first supplied PDF was rendered and inspected: foreground values and charts
were displaced relative to the background. It is not accepted for the portfolio
and has not been published. The approved Desktop view is the reference while
export alignment is resolved. No recreated image is presented as a native export.

## Asset credits

All company marks and photos remain the property of their respective owners.
Their use identifies the company analysed and does not imply BASF sponsorship.
The original white logo retains its proportions and its “We create chemistry” claim.

- Official logo: [BASF Report 2025](https://report.basf.com/2025/en/),
  [original SVG](https://report.basf.com/2025/en/_assets/images/logo.svg?h=ukb0Fg6R).
- Logo reference: [BASF Brand Portal](https://brandportal.basf.com/global/en/create/corporate-design/logo).
- Dusk photo: © BASF, [annual press conference press photos](https://www.presseportal.de/pm/16344/5980793).
- Aerial photo: © BASF, [Ludwigshafen Verbund site press release](https://www.basf.com/no/en/media/news-releases/2018/04/p-18-183).
- Typeface: [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk).
  Bundled font files are accompanied by the SIL Open Font License in `powerbi/assets/OFL.txt`.
