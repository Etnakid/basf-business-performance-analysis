# SQL analysis

Eight questions use the existing nine KPI series. The analysis file is
`sql/03_business_analysis.sql`; all statements are read-only.

## Run in pgAdmin

The table has already been imported and checked on the project owner's computer.
Open Query Tool connected to **basf_business_performance**, then use the folder
icon (Open File) to open `sql/03_business_analysis.sql` from the local repository.
Select one complete numbered query, from its WITH/SELECT through its semicolon,
and press F5. Repeat for Q1–Q8. Executing all at once can leave only the final
result visible, so selecting one query is the simplest way to review each answer.

## Questions and outputs

| Query | Business question | Output |
| --- | --- | --- |
| Q1 | How did sales change from 2016 to 2025? | Annual sales and absolute/percentage change from 2016 |
| Q2 | How did EBITDA, EBIT and net income evolve? | Ten annual rows with the three financial series |
| Q3 | Which years had the highest and lowest EBITDA margin before special items? | Maximum and minimum years, including ties |
| Q4 | How did operating cash flow and free cash flow evolve? | Ten annual rows with both cash flow series |
| Q5 | How did investments and ROCE evolve? | Annual additions to PPE/intangibles and ROCE; 2016 ROCE remains null |
| Q6 | Which years had the largest annual sales growth and decline? | Nine consecutive-year comparisons with growth and decline ranks |
| Q7 | Which years recorded a net loss? | Loss years with sales and EBIT for context |
| Q8 | How did 2025 compare with 2024 for all nine KPIs? | Prior/current values, absolute deltas, monetary percentage changes |

## Findings from the supplied dataset

These are descriptive findings from the published series, not like-for-like
organic growth estimates or explanations of business causes.

| Query | Finding |
| --- | --- |
| Q1 | Sales moved from 57,550 to 59,657 million EUR between 2016 and 2025, a 3.66% increase; the series peaked at 87,327 in 2022. |
| Q2 | EBITDA peaked at 11,355 and EBIT at 7,677 million EUR in 2021. Net income peaked at 8,421 in 2019. The respective 2025 values were 5,618, 1,634 and 1,619. |
| Q3 | The reported margin before special items was highest in 2016 (17.9%) and lowest in 2025 (11.0%). |
| Q4 | Operating cash flow and FCF peaked in 2017 at 8,785 and 4,789 million EUR. In 2025 they were 5,610 and 1,342, versus 6,946 and 748 in 2024: opposite directions in the latest year. |
| Q5 | Additions peaked at 10,735 million EUR in 2018 and were 4,787 in 2025. Available ROCE values range from 1.7% in 2020 to 15.4% in 2017; 2025 was 5.8%. No causal relationship is inferred. |
| Q6 | The largest sales increase was 2021 (+32.88%); the largest decline was 2023 (-21.10%). |
| Q7 | Net losses occurred in 2020 (-1,060 million EUR) and 2022 (-627). EBIT in 2022 was nevertheless positive (6,548). |
| Q8 | In 2025 sales fell 2.91%, EBITDA 9.55%, EBIT 9.72%, operating cash flow 19.23% and additions 29.87%. Net income rose 24.73% and FCF 79.41%. The margin fell 0.8 percentage points; ROCE rose 0.7 percentage points. |

## Interpretation rules

- Amounts remain in **million EUR**. Percent series retain BASF's original
  percent units: 11 means 11%, not 0.11.
- Margin and ROCE differences are **percentage points**, e.g. 5.8 - 5.1 = 0.7 pp.
- The reported EBITDA margin is **before special items**. It is not calculated
  from the unadjusted EBITDA series in Q2.
- Investments mean **additions to PPE and intangible assets**, not cash payments.
  Do not reconstruct FCF by subtracting this series from operating cash flow.
- Year-on-year sales calculations require consecutive years. Zero denominators
  yield null. Q8 suppresses monetary growth percentages for nonpositive prior
  values or negative current values; absolute differences remain available.
- No null is converted to zero. Extremum queries retain tied years.
- Read [data preparation notes](data_preparation.md) for BASF's 2017, 2018 and 2024
  restatements/discontinued-operation adjustments. These affect comparability;
  rankings and changes here describe the as-published series.
- An increase is not automatically an improvement: lower investment, for example,
  requires context. The dataset cannot establish causes of profit or cash changes.

## Validation and limits

All three SQL files were executed using the supplied 90-row CSV in **PGlite
0.5.10 (PostgreSQL 18.6 compiled to WebAssembly)** on October 20, 2026. The data
checks passed. Q1–Q8 returned 10, 10, 2, 10, 10, 9, 2 and 9 rows respectively.
Checks also covered tied margin extrema, zero and negative prior values, a
missing prior calendar year and a current null. Synthetic changes were rolled
back and never written to the project CSV.

On October 20, 2026, all eight analysis queries were also executed successfully
in pgAdmin on the owner's local PostgreSQL 17 instance. Screenshots confirmed
the same row counts (10, 10, 2, 10, 10, 9, 2, 9) and the displayed results,
including 2016 ROCE null, margin extrema, the 2021 sales growth rank, loss years
and the visible 2024–2025 comparisons. This manual review was not a full
automated comparison of every local output cell. The local table creation,
import and initial count/null checks were verified earlier in the same session.
The native Power BI report is now implemented; see [implementation and validation](powerbi_implementation.md).

On 21 October 2026, all three committed SQL files were rerun in a fresh, isolated
PostgreSQL 17 database using the committed CSV. Import checks passed and Q1–Q8
again returned 10, 10, 2, 10, 10, 9, 2 and 9 rows. The principal findings above
matched the returned results. The owner's existing database was not modified.

## SQL references

- [PostgreSQL 17 window functions](https://www.postgresql.org/docs/17/functions-window.html)
- [PostgreSQL 17 psql and client-side copy](https://www.postgresql.org/docs/17/app-psql.html)
