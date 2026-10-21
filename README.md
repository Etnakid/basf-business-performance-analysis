# BASF Business Performance Analysis

**English** | [Deutsch](README.de.md)

I live in Ludwigshafen am Rhein, where BASF is the city’s largest industrial presence. I wanted to take a closer look at the company behind such a prominent part of my surroundings and understand how its financial performance has changed over time.

For this project, I chose to focus exclusively on financial data. Sales, profitability, cash flow, investments and returns were the most relevant measures for the analysis I wanted to carry out. Keeping this focus also helped me build a manageable project without spreading the analysis across too many topics.

The project covers **2016–2025** and combines **Power Query, PostgreSQL and Power BI**. Data preparation and SQL analysis are complete; the Power BI report is the next step.

## What I wanted to understand

I organised the analysis around eight questions:

1. How did BASF’s sales change between 2016 and 2025?
2. How did EBITDA, EBIT and net income evolve?
3. Which years recorded the highest and lowest EBITDA margin before special items?
4. How did operating cash flow and free cash flow change?
5. How did investments and ROCE evolve?
6. Which years recorded the largest annual sales increases and declines?
7. In which years did BASF report a net loss?
8. How did 2025 compare with 2024 across the nine selected KPIs?

## Data sources

I used two official Excel workbooks from the **BASF Report 2025**:

- [Ten-Year Summary](https://report.basf.com/2025/en/overviews/ten-year-summary.html): `10y-overview-basf-ar25.xlsx`, containing the historical series used in the analysis.
- [Download Center](https://report.basf.com/2025/en/services/downloads.html): `all-tables-basf-ar25.xlsx`, used to cross-check the summary and clarify selected financial definitions.

The original workbooks are preserved locally in `data/raw/` and excluded from GitHub. The repository contains the processed dataset, transformation script, SQL queries and documentation.

## The nine KPIs I selected

| KPI | Unit |
| --- | --- |
| Sales | Million EUR |
| EBITDA | Million EUR |
| EBIT | Million EUR |
| Net Income | Million EUR |
| EBITDA Margin before special items | % |
| Operating Cash Flow | Million EUR |
| Free Cash Flow | Million EUR |
| Investments: additions to property, plant and equipment and intangible assets | Million EUR |
| ROCE | % |

I kept BASF’s original units and definitions. In particular, the reported EBITDA margin is **before special items**, while the EBITDA series is unadjusted. These two measures should not be assumed to reconcile through a simple division.

The investment series represents **additions to assets**. It differs from the cash payments used in BASF’s free cash flow calculation.

## How I prepared the data

I used an AI-assisted workflow to help inspect the source files, prepare the dataset, write the Power Query M script and develop the SQL queries and documentation. I then executed the Power Query transformation in Power BI Desktop and the SQL queries in my local PostgreSQL database, reviewing the results along the way.

The Power Query script:

- Reads the original ten-year workbook.
- Selects only the nine financial KPIs.
- Removes headings, notes and unrelated rows.
- Converts the year columns into a long table.
- Removes known footnote letters attached to numbers while preserving their values.
- Retains missing data without replacing it with estimates.

The processed dataset has this structure:

```text
year | kpi | value | unit
```

It contains **90 rows: ten years × nine KPIs**.

BASF does not provide a ROCE value for 2016 in the source table. I kept that observation as a missing value, represented by an empty field in the CSV and `NULL` in PostgreSQL.

For transparency, the committed CSV was prepared directly from the source workbook with AI assistance and checked against its cells. The Power Query script was subsequently executed successfully and its preview reviewed. I did not perform a full automated comparison between an exported Power Query result and the committed CSV.

The exact source rows, KPI definitions and validation details are documented in [Data preparation notes](docs/data_preparation.md).

## SQL analysis

I imported the processed CSV into the `basf_business_performance` database and stored it in `public.basf_kpis`.

Before analysing the data, I checked that the import contained:

- 90 rows.
- Ten years, from 2016 to 2025.
- Nine distinct KPIs.
- Exactly one missing value: ROCE in 2016.

The SQL analysis uses filtering, conditional aggregation, common table expressions, window functions and a self-join to answer the eight questions.

All eight queries were executed successfully in **PostgreSQL 17 through pgAdmin**. Their row counts and displayed results were reviewed against the expected outputs. The scripts were also tested separately using the same CSV in PGlite, based on PostgreSQL 18.6.

The SQL files are available here:

- [Create the table](sql/01_create_table.sql)
- [Check the imported data](sql/02_data_checks.sql)
- [Answer the eight business questions](sql/03_business_analysis.sql)

## What the analysis shows

A few findings stood out in the published data:

- Sales rose from **€57,550 million in 2016 to €59,657 million in 2025**, an increase of **3.66%**, with substantial fluctuations between those years.
- The largest annual sales increase occurred in **2021 (+32.88%)**, while the largest decline occurred in **2023 (−21.10%)**.
- The EBITDA margin before special items was highest in **2016 (17.9%)** and lowest in **2025 (11.0%)**.
- BASF reported net losses in **2020 and 2022**. In 2022, EBIT remained positive despite the net loss.
- In **2025 versus 2024**, sales fell **2.91%** and operating cash flow fell **19.23%**, while net income rose **24.73%** and free cash flow rose **79.41%**.

These results helped me see why several financial measures need to be considered together: sales, profit and cash flow can move in different directions.

The complete findings and interpretation rules are available in [SQL analysis notes](docs/sql_analysis.md).

## Important limitations

BASF marks selected historical figures as restated or adjusted, including figures for **2017, 2018 and 2024** associated with discontinued operations. I used the values as published in the 2025 ten-year summary and documented these notes.

The changes calculated here therefore describe the **published series**. They should not automatically be interpreted as like-for-like growth.

I also distinguish between **percent changes** and **percentage-point changes**. For example, ROCE moving from 5.1% to 5.8% is an increase of **0.7 percentage points**.

This dataset supports descriptive comparisons. By itself, it cannot explain the causes of a loss, establish whether an investment decision was successful or demonstrate that changes in investment caused changes in ROCE.

## Repository structure

```text
data/
  processed/     Clean financial dataset

power_query/     Reproducible Power Query M script
sql/             Table definition, data checks and analysis queries
docs/            Sources, methodology, findings and limitations
powerbi/         Approved design and native PBIP implementation
tools/           Project assembly and structural validation
```

The original Excel workbooks are kept locally in `data/raw/`, which is excluded from Git.

## Reproducing the project

1. Download the two official BASF workbooks and place them in `data/raw/`.
2. Create a blank query in Power BI Desktop or Excel.
3. Open Advanced Editor and paste `power_query/basf_kpis.m`.
4. Set `RawFile` to the local path of the ten-year workbook and refresh.
5. Verify the expected 90 rows and the missing ROCE value for 2016.
6. Follow the [PostgreSQL setup instructions](docs/postgresql_setup.md) to create the table and import the processed CSV.
7. Run the data checks, then execute the eight analysis queries individually.

## Report design preview

I designed a single-page, landscape layout with a dark green background,
rounded KPI cards, faded Ludwigshafen photographs and the official BASF logo.
The preview uses the same financial dataset, with a 2024/2025 reporting-year
selector. It is an **interactive design prototype, not a completed Power BI report**.

Download [the preview](powerbi/design/preview.html) and open it in a browser;
GitHub displays its source rather than running it. See the [design notes and asset
credits](docs/powerbi_design.md).

## Native Power BI project — awaiting Desktop verification

I have prepared [the PBIP project](powerbi/BASF/BASF.pbip), with nine KPI cards,
four history charts and a reporting-year selector. It includes a portable
snapshot of the processed CSV, so opening it does not require database credentials
or machine-specific source paths. The original workbook-cleaning workflow remains
the separate Power Query M script.

The project definitions passed structural and Microsoft JSON schema checks.
**Desktop refresh, DAX execution and native visual rendering are still unverified**;
this is not yet a completed or validated dashboard. See the
[opening instructions, measures and acceptance checks](docs/powerbi_implementation.md).

## Next step

I will open and validate the native report in Power BI Desktop, check its
interactions and financial results, then capture the final portfolio screenshots.
