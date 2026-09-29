// Create a blank query in Excel or Power BI, open Advanced Editor, and paste this script.
// Change RawFile to the local path of the unchanged BASF ten-year workbook.
let
    RawFile = "C:\\path\\to\\data\\raw\\10y-overview-basf-ar25.xlsx",
    Source = Excel.Workbook(File.Contents(RawFile), null, true),
    Sheet = Source{[Item="10y-overview", Kind="Sheet"]}[Data],
    Header = Table.PromoteHeaders(Table.Skip(Sheet, 3), [PromoteAllScalars=true]),
    LabelColumn = Table.ColumnNames(Header){0},
    Mappings = #table({"source_label", "kpi", "unit"}, {
        {"Sales", "Sales", "million EUR"},
        {"EBITDA", "EBITDA", "million EUR"},
        {"EBIT", "EBIT", "million EUR"},
        {"Net income", "Net Income", "million EUR"},
        {"EBITDA margin before special items", "EBITDA Margin before special items", "%"},
        {"Cash flows from operating activities", "Operating Cash Flow", "million EUR"},
        {"Free cash flow", "Free Cash Flow", "million EUR"},
        {"Additions to property, plant and equipment and intangible assets", "Investments / CapEx (additions to PPE and intangible assets)", "million EUR"},
        {"ROCE", "ROCE", "%"}
    }),
    Selected = Table.SelectRows(Header, each List.Contains(Mappings[source_label], Record.Field(_, LabelColumn))),
    Named = Table.RenameColumns(Selected, {{LabelColumn, "source_label"}}),
    Years = List.Transform({2016..2025}, each Text.From(_)),
    Narrow = Table.SelectColumns(Named, List.Combine({{"source_label"}, Years})),
    Matched = Table.NestedJoin(Narrow, {"source_label"}, Mappings, {"source_label"}, "mapping", JoinKind.Inner),
    Expanded = Table.ExpandTableColumn(Matched, "mapping", {"kpi", "unit"}),
    Long = Table.Unpivot(Expanded, Years, "year", "source_value"),
    // Footnote markers are a single trailing lowercase letter (a, b or e in these rows).
    // Remove only that marker; a dash represents a source missing value.
    ParseNumber = (v as any) as nullable number =>
        let
            t = if v = null then null else Text.Trim(Text.From(v, "en-US")),
            last = if t = null or Text.Length(t) = 0 then "" else Text.End(t, 1),
            clean = if List.Contains({"a", "b", "e"}, last) then Text.Start(t, Text.Length(t)-1) else t,
            number = if clean = null or List.Contains({"", "–", "—"}, clean) then null
                     else Number.FromText(Text.Replace(clean, ",", ""), "en-US")
        in number,
    Values = Table.AddColumn(Long, "value", each ParseNumber([source_value]), type nullable number),
    Typed = Table.TransformColumnTypes(Values, {{"year", Int64.Type}}),
    Output = Table.SelectColumns(Typed, {"year", "kpi", "value", "unit"}),
    // Unpivot can omit null source cells; explicitly preserve the source dash for 2016 ROCE.
    WithMissing = if Table.RowCount(Table.SelectRows(Output, each [year] = 2016 and [kpi] = "ROCE")) = 0
        then Table.InsertRows(Output, Table.RowCount(Output), {[year=2016, kpi="ROCE", value=null, unit="%"]})
        else Output,
    Sorted = Table.Sort(WithMissing, {{"year", Order.Ascending}, {"kpi", Order.Ascending}})
in
    Sorted
