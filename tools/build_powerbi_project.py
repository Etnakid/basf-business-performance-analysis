"""Build the portable PBIP report definition from the checked-in processed CSV.

Standard library only. The approved background/theme/font are maintained assets;
this script does not clean the BASF workbooks or render Power BI visuals.
"""
import base64
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'powerbi' / 'BASF'
REPORT = OUT / 'BASF.Report'
MODEL = OUT / 'BASF.SemanticModel'
PAGE = REPORT / 'definition/pages/Performance'
SCHEMA = 'https://developer.microsoft.com/json-schemas/fabric/'
FONT = "'Space Grotesk', 'Space Grotesk Medium', 'Segoe UI', sans-serif"
THEME_NAME = 'BASFGreen-7c3e41a2.json'
KPIS = [
    ('Sales', 'Sales', False),
    ('EBITDA', 'EBITDA', False),
    ('EBIT', 'EBIT', False),
    ('Net Income', 'Net Income', False),
    ('EBITDA Margin before special items', 'EBITDA Margin', True),
    ('Operating Cash Flow', 'Operating Cash Flow', False),
    ('Free Cash Flow', 'Free Cash Flow', False),
    ('Investments / CapEx (additions to PPE and intangible assets)', 'Investments', False),
    ('ROCE', 'ROCE', True),
]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def lit(value):
    if isinstance(value, bool):
        text = str(value).lower()
    elif isinstance(value, (int, float)):
        text = str(value) + 'D'
    else:
        text = "'" + value.replace("'", "''") + "'"
    return {'expr': {'Literal': {'Value': text}}}


def color(value):
    return {'solid': {'color': lit(value)}}


def obj(**props):
    return [{'properties': props}]


def field(name, table='basf_kpis', column=False):
    return {('Column' if column else 'Measure'): {
        'Expression': {'SourceRef': {'Entity': table}}, 'Property': name}}


def projection(name, table='basf_kpis', column=False):
    return {'field': field(name, table, column), 'queryRef': table + '.' + name,
            'nativeQueryRef': name}


def visual(name, kind, x, y, w, h, roles, objects=None, title=None, alt=None):
    container = {
        'background': obj(show=lit(False)),
        'border': obj(show=lit(False)),
        'visualHeader': obj(show=lit(False)),
        'title': obj(show=lit(bool(title)), text=lit(title or ''),
                     fontColor=color('#EAF5E2'), fontSize=lit(13),
                     fontFamily=lit(FONT)),
        'padding': obj(top=lit(0), bottom=lit(0), left=lit(0), right=lit(0)),
        'general': obj(altText=lit(alt or title or name)),
    }
    config = {'visualType': kind, 'query': {'queryState': {
        role: {'projections': projections} for role, projections in roles.items()}},
        'objects': objects or {}, 'visualContainerObjects': container,
        'drillFilterOtherVisuals': False}
    if kind in ('lineChart', 'clusteredColumnChart'):
        config['query']['sortDefinition'] = {'sort': [
            {'field': field('year', column=True), 'direction': 'Ascending'}],
            'isDefaultSort': False}
    write(PAGE / 'visuals' / name / 'visual.json', {
        '$schema': SCHEMA + 'item/report/definition/visualContainer/2.1.0/schema.json',
        'name': name, 'position': {'x': x, 'y': y, 'width': w, 'height': h,
                                  'z': 10, 'tabOrder': len(VISUALS)},
        'visual': config})
    VISUALS.append(name)


def build():
    csv_path = ROOT / 'data/processed/basf_kpis_2016_2025.csv'
    raw = csv_path.read_bytes()
    rows = list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
    if len(rows) != 90 or len({(r['year'], r['kpi']) for r in rows}) != 90:
        raise ValueError('Expected exactly 90 unique year/KPI pairs')
    if [(r['year'], r['kpi']) for r in rows if not r['value']] != [('2016', 'ROCE')]:
        raise ValueError('Unexpected missing observations')
    write(OUT / 'BASF.pbip', {
        '$schema': SCHEMA + 'pbip/pbipProperties/1.0.0/schema.json',
        'version': '1.0', 'artifacts': [{'report': {'path': 'BASF.Report'}}],
        'settings': {'enableAutoRecovery': True}})
    write(REPORT / 'definition.pbir', {
        '$schema': SCHEMA + 'item/report/definitionProperties/2.0.0/schema.json',
        'version': '4.0', 'datasetReference': {'byPath': {'path': '../BASF.SemanticModel'}}})
    write(MODEL / 'definition.pbism', {
        '$schema': SCHEMA + 'item/semanticModel/definitionProperties/1.0.0/schema.json',
        'version': '4.0', 'settings': {}})

    m_query = [
        'let',
        '    // Portable snapshot of the repository CSV; not the workbook cleaning query.',
        '    // Rebuild this project after updating the processed CSV.',
        '    Source = Csv.Document(Binary.FromText("' + base64.b64encode(raw).decode() +
        '", BinaryEncoding.Base64), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        '    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '    MissingAsNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, {"value"}),',
        '    Typed = Table.TransformColumnTypes(MissingAsNull, {{"year", Int64.Type}, {"kpi", type text}, {"value", type number}, {"unit", type text}}, "en-US")',
        'in', '    Typed']
    measures = [{'name': 'Selected Year', 'expression':
                 "SELECTEDVALUE('Report Year'[year], MAXX(ALL('Report Year'), 'Report Year'[year]))",
                 'formatString': '0', 'displayFolder': 'Selection'}]
    dax_doc = ['// Generated from tools/build_powerbi_project.py. Run verification in Desktop.']
    for key, name, percentage in KPIS:
        fmt = '0.0"%"' if percentage else '#,0;(#,0);0'
        base = 'CALCULATE(SELECTEDVALUE(basf_kpis[value]), basf_kpis[kpi] = "' + key + '")'
        selected = f'VAR Y = [Selected Year]\nRETURN CALCULATE([{name}], REMOVEFILTERS(basf_kpis[year]), basf_kpis[year] = Y)'
        previous = f'VAR Y = [Selected Year] - 1\nRETURN CALCULATE([{name}], REMOVEFILTERS(basf_kpis[year]), basf_kpis[year] = Y)'
        delta = (f'VAR C = [{name} Selected]\nVAR P = [{name} Previous]\n'
                 'RETURN IF(ISBLANK(C) || ISBLANK(P), BLANK(), ' +
                 ('C - P)' if percentage else 'IF(P > 0 && C >= 0, DIVIDE(C - P, P), BLANK()))'))
        # No misleading percentage growth across a loss/profit transition or zero base.
        label = (f'VAR D = [{name} Change]\nVAR C = [{name} Selected]\nVAR P = [{name} Previous]\n'
                 'RETURN SWITCH(TRUE(), ISBLANK(C), "Not reported", '
                 'ISBLANK(P), "No prior-year value", ISBLANK(D), "Not comparable", '
                 'FORMAT(D, ' + ('"+0.0;-0.0;0.0") & " pp vs PY")' if percentage else
                                 '"+0.0%;-0.0%;0.0%") & " vs PY")'))
        for suffix, expr, form, folder in [('', base, fmt, 'History'),
                (' Selected', selected, fmt, 'Cards'), (' Previous', previous, fmt, 'Comparison'),
                (' Change', delta, '0.0' if percentage else '0.0%', 'Comparison'),
                (' Change Label', label, None, 'Comparison')]:
            item = {'name': name + suffix, 'expression': expr.splitlines(), 'displayFolder': folder}
            if form: item['formatString'] = form
            measures.append(item)
            dax_doc.extend(['', f'// {name + suffix}', expr])
    model = {'name': 'BASF', 'compatibilityLevel': 1601, 'model': {
        'culture': 'en-US', 'sourceQueryCulture': 'en-US',
        'defaultPowerBIDataSourceVersion': 'powerBI_V3',
        'dataAccessOptions': {'legacyRedirects': True, 'returnErrorValuesAsNull': True},
        'annotations': [{'name': 'PBI_QueryOrder', 'value': '["basf_kpis","Report Year"]'},
                        {'name': 'ProcessedCsvSHA256', 'value': hashlib.sha256(raw).hexdigest()}],
        'tables': [
            {'name': 'basf_kpis', 'columns': [
                {'name': n, 'dataType': typ, 'sourceColumn': n,
                 'summarizeBy': 'none', **({'formatString': '0'} if n == 'year' else {})}
                for n, typ in [('year', 'int64'), ('kpi', 'string'), ('value', 'double'), ('unit', 'string')]],
             'measures': measures,
             'partitions': [{'name': 'basf_kpis', 'mode': 'import',
                             'source': {'type': 'm', 'expression': m_query}}]},
            {'name': 'Report Year', 'description': 'Disconnected year selector; does not shorten history charts.',
             'columns': [{'name': 'year', 'dataType': 'int64', 'sourceColumn': 'year',
                          'formatString': '0', 'summarizeBy': 'none'}],
             'partitions': [{'name': 'Report Year', 'mode': 'import', 'source': {'type': 'm',
                 'expression': ['let', '    Source = Table.FromList({2016..2025}, Splitter.SplitByNothing(), {"year"}),',
                                '    Typed = Table.TransformColumnTypes(Source, {{"year", Int64.Type}})',
                                'in', '    Typed']}}]}]}}
    write(MODEL / 'model.bim', model)
    (OUT / 'measures.dax').write_text('\n'.join(dax_doc) + '\n', encoding='utf-8')
    write(REPORT / 'definition/version.json', {
        '$schema': SCHEMA + 'item/report/definition/versionMetadata/1.0.0/schema.json', 'version': '2.0.0'})
    write(REPORT / 'definition/report.json', {
        '$schema': SCHEMA + 'item/report/definition/report/2.0.0/schema.json',
        'themeCollection': {'customTheme': {'name': THEME_NAME, 'reportVersionAtImport': '5.59',
                                          'type': 'RegisteredResources'}},
        'resourcePackages': [{'name': 'RegisteredResources', 'type': 'RegisteredResources', 'items': [
            {'name': THEME_NAME, 'path': THEME_NAME, 'type': 'CustomTheme'},
            {'name': 'background.png', 'path': 'background.png', 'type': 'Image'}]}]})
    write(REPORT / 'definition/pages/pages.json', {
        '$schema': SCHEMA + 'item/report/definition/pagesMetadata/1.0.0/schema.json',
        'pageOrder': ['Performance'], 'activePageName': 'Performance'})

    for i, (_, name, percentage) in enumerate(KPIS):
        x = 32 + i * 172
        card_projection = projection(name + ' Selected')
        if percentage:
            # The decorative card already labels the original unit below the value.
            card_projection['format'] = '0.0'
        visual('KPI%02d' % i, 'card', x + 3, 254, 156, 51,
               {'Values': [card_projection]},
               {'labels': obj(color=color('#F3FAEC'), fontSize=lit(26), fontFamily=lit(FONT),
                              labelDisplayUnits=lit(1), labelPrecision=lit(1 if percentage else 0)),
                'categoryLabels': obj(show=lit(False))},
               alt=f'{name}: selected year. ' + ('Percent.' if percentage else 'Million EUR.'))
        visual('Delta%02d' % i, 'card', x + 3, 316, 156, 24,
               {'Values': [projection(name + ' Change Label')]},
               {'labels': obj(color=color('#B8CCB7'), fontSize=lit(9), fontFamily=lit(FONT)),
                'categoryLabels': obj(show=lit(False))}, alt=f'{name}: comparison with previous year')

    visual('YearSelector', 'slicer', 1370, 138, 192, 55,
           {'Values': [projection('year', 'Report Year', True)]},
           {'data': obj(mode=lit('Dropdown')),
            'selection': obj(singleSelect=lit(True), selectAllCheckboxEnabled=lit(False)),
            'header': obj(show=lit(False)),
            'items': obj(fontColor=color('#EAF5E2'), background=color('#102818'),
                         textSize=lit(12), fontFamily=lit(FONT))},
           alt='Choose report year. With no selection the cards show 2025, the latest year.')
    for name, kind, x, y, w, h, ms in [
        ('SalesHistory', 'lineChart', 44, 409, 802, 187, ['Sales']),
        ('ProfitabilityHistory', 'lineChart', 884, 409, 672, 187, ['EBITDA', 'EBIT', 'Net Income']),
        ('CashFlowHistory', 'lineChart', 44, 664, 802, 176, ['Operating Cash Flow', 'Free Cash Flow']),
        ('InvestmentHistory', 'clusteredColumnChart', 884, 664, 672, 176, ['Investments'])]:
        visual(name, kind, x, y, w, h,
               {'Category': [projection('year', column=True)], 'Y': [projection(m) for m in ms]},
               {'categoryAxis': obj(show=lit(True), axisType=lit('Categorical'),
                                    showAxisTitle=lit(False), labelColor=color('#A4B9AA'), fontSize=lit(10), fontFamily=lit(FONT)),
                'valueAxis': obj(show=lit(True), showAxisTitle=lit(False),
                                 labelColor=color('#A4B9AA'), fontSize=lit(10), fontFamily=lit(FONT),
                                 labelDisplayUnits=lit(1), gridlineColor=color('#24402B')),
                'legend': obj(show=lit(len(ms) > 1), position=lit('Top'), labelColor=color('#B8CCB7'), fontSize=lit(10), fontFamily=lit(FONT)),
                'labels': obj(show=lit(False))},
               alt='2016–2025 annual ' + ', '.join(ms) + '; million EUR; as published, not like-for-like.')

    write(PAGE / 'page.json', {
        '$schema': SCHEMA + 'item/report/definition/page/2.0.0/schema.json',
        'name': 'Performance', 'displayName': 'Business performance',
        'displayOption': 'FitToPage', 'width': 1600, 'height': 900,
        'objects': {'background': obj(color=color('#06120C'), transparency=lit(0), image={'image': {
            'name': lit('background.png'), 'url': {'expr': {'ResourcePackageItem': {
                'PackageName': 'RegisteredResources', 'PackageType': 1, 'ItemName': 'background.png'}}},
            'scaling': lit('Fit')}})},
        'visualInteractions': [
            {'source': a, 'target': b, 'type': 'NoFilter'} for a in VISUALS if a.endswith('History')
            for b in VISUALS if b != a]})
    print(f'Built {len(VISUALS)} native visuals, {len(measures)} measures; CSV SHA256 {hashlib.sha256(raw).hexdigest()}')


VISUALS = []
if __name__ == '__main__':
    build()
