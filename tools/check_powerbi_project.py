"""Check data integrity, semantic bindings and layout bounds (not DAX execution).

Optional --schemas validates against Microsoft's declared JSON schemas and
requires jsonschema plus internet access. Downloaded schemas stay outside Git.
"""
import argparse
import base64
import concurrent.futures
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'powerbi/BASF'


def run(schemas=False):
    model = json.loads((PROJECT/'BASF.SemanticModel/model.bim').read_text())['model']
    tables = {t['name']: t for t in model['tables']}
    assert model.get('defaultPowerBIDataSourceVersion') == 'powerBI_V3', 'Enhanced model metadata must be explicit'
    fact = tables['basf_kpis']
    query = '\n'.join(fact['partitions'][0]['source']['expression'])
    encoded = re.search(r'Binary.FromText\("([^"]+)"', query).group(1)
    actual = base64.b64decode(encoded, validate=True)
    expected = (ROOT/'data/processed/basf_kpis_2016_2025.csv').read_bytes()
    assert actual == expected, 'Embedded snapshot differs from repository CSV'
    rows = list(csv.DictReader(io.StringIO(actual.decode())))
    assert len(rows) == 90 and len({(r['year'], r['kpi']) for r in rows}) == 90
    assert {int(r['year']) for r in rows} == set(range(2016,2026))
    assert [(r['year'],r['kpi']) for r in rows if not r['value']] == [('2016','ROCE')]
    assert {r['unit'] for r in rows} == {'million EUR','%'}
    assert {r['kpi'] for r in rows if r['unit']=='%'} == {'ROCE','EBITDA Margin before special items'}
    annotations = {a['name']: a['value'] for a in model['annotations']}
    assert annotations['ProcessedCsvSHA256'] == hashlib.sha256(expected).hexdigest()
    pagepath = PROJECT/'BASF.Report/definition/pages/Performance'
    page = json.loads((pagepath/'page.json').read_text())
    report = json.loads((PROJECT/'BASF.Report/definition/report.json').read_text())
    resources = report['resourcePackages'][0]['items']
    for item in resources:
        assert item['name'] == item['path'], 'Use the actual resource filename as its identifier'
        assert (PROJECT/'BASF.Report/StaticResources/RegisteredResources'/item['path']).is_file()
    assert report['themeCollection']['customTheme']['name'] in {i['name'] for i in resources}
    background = page['objects']['background'][0]['properties']['image']
    assert set(background) == {'image'}, 'Power BI requires a nested image.image object'
    image = background['image']['url']['expr']['ResourcePackageItem']
    assert background['image']['scaling']['expr']['Literal']['Value'] == "'Fit'"
    assert image['ItemName'] in {i['name'] for i in resources}
    theme_name = report['themeCollection']['customTheme']['name']
    theme = json.loads((PROJECT/'BASF.Report/StaticResources/RegisteredResources'/theme_name).read_text())
    assert theme['name'] == theme_name
    definitions=[]
    for path in PROJECT.rglob('*'):
        if path.suffix not in {'.json','.pbip','.pbir','.pbism'}: continue
        d=json.loads(path.read_text())
        if '$schema' in d: definitions.append((path,d))
    visuals=[]
    for path in pagepath.glob('visuals/*/visual.json'):
        d=json.loads(path.read_text());visuals.append(d)
        p=d['position']
        assert 0<=p['x'] and 0<=p['y'] and p['x']+p['width']<=page['width'] and p['y']+p['height']<=page['height'], path
        for role in d['visual']['query']['queryState'].values():
            for item in role['projections']:
                f=item['field'];kind=next(iter(f));binding=f[kind]
                table=tables[binding['Expression']['SourceRef']['Entity']]
                assert binding['Property'] in {x['name'] for x in table['measures' if kind=='Measure' else 'columns']}, path
    assert len(visuals)==23
    assert {d['name'] for d in visuals} == {p.name for p in (pagepath/'visuals').iterdir()}
    assert len(fact['measures'])==46
    if schemas:
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT7
        from jsonschema import Draft7Validator
        store={}
        pending={d['$schema'] for _,d in definitions}
        def get(u):
            return u,json.load(urllib.request.urlopen(u,timeout=45))
        def refs(d):
            if isinstance(d,dict):
                for k,v in d.items():
                    if k=='$ref':yield v
                    else:yield from refs(v)
            elif isinstance(d,list):
                for v in d:yield from refs(v)
        while pending:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
                for u,d in ex.map(get,pending):store[u]=d
            pending={urllib.parse.urljoin(u,r).split('#')[0]
                     for u,d in store.items() for r in refs(d)}-store.keys()
        registry=Registry().with_resources((u,Resource.from_contents(d,default_specification=DRAFT7)) for u,d in store.items())
        for path,d in definitions:
            errors=list(Draft7Validator(store[d['$schema']],registry=registry).iter_errors(d))
            assert not errors, (path,[e.message for e in errors])
        print(f'PASS: {len(definitions)} definitions validated against Microsoft schemas')
    print('PASS: exact CSV snapshot, 90 unique observations, original units, 2016 ROCE null')
    print('PASS: 23 visual bindings and canvas bounds, 46 measure definitions')
    print('NOT RUN: Desktop refresh, DAX execution and native visual rendering')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--schemas',action='store_true')
    run(parser.parse_args().schemas)
