# BASF Business Performance Analysis

[English](README.md) | **Deutsch**

Ich lebe in Ludwigshafen am Rhein, wo BASF die größte industrielle Präsenz der Stadt ist. Deshalb wollte ich mir das Unternehmen, das mein direktes Umfeld so stark prägt, genauer ansehen und verstehen, wie sich seine finanzielle Entwicklung im Laufe der Jahre verändert hat.

Für dieses Projekt habe ich mich bewusst auf Finanzdaten konzentriert. Umsatz, Profitabilität, Cashflow, Investitionen und Kapitalrendite waren die passenden Kennzahlen für die Analyse, die ich durchführen wollte. Mit diesem klaren Schwerpunkt konnte ich das Projekt überschaubar halten und mich gezielt mit den wirtschaftlichen Ergebnissen beschäftigen.

Das Projekt umfasst die Jahre **2016–2025** und verbindet **Power Query, PostgreSQL und Power BI**. Die Datenaufbereitung und die SQL-Analyse sind abgeschlossen. Als Nächstes erstelle ich den Power-BI-Bericht.

## Was ich herausfinden wollte

Meine Analyse orientiert sich an acht Fragen:

1. Wie hat sich der Umsatz von BASF zwischen 2016 und 2025 verändert?
2. Wie haben sich EBITDA, EBIT und Jahresüberschuss entwickelt?
3. In welchen Jahren war die EBITDA-Marge vor Sondereinflüssen am höchsten bzw. am niedrigsten?
4. Wie haben sich der operative Cashflow und der Free Cashflow verändert?
5. Wie haben sich Investitionen und ROCE entwickelt?
6. In welchen Jahren gab es die größten jährlichen Umsatzsteigerungen und Umsatzrückgänge?
7. In welchen Jahren hat BASF einen Jahresfehlbetrag ausgewiesen?
8. Wie schneidet das Jahr 2025 bei den neun ausgewählten Kennzahlen im Vergleich zu 2024 ab?

## Datenquellen

Ich habe zwei offizielle Excel-Dateien aus dem **BASF-Bericht 2025** verwendet:

- [Zehnjahresübersicht / Ten-Year Summary](https://report.basf.com/2025/en/overviews/ten-year-summary.html): `10y-overview-basf-ar25.xlsx` mit den historischen Datenreihen für die Analyse.
- [Download-Center](https://report.basf.com/2025/en/services/downloads.html): `all-tables-basf-ar25.xlsx` zum Abgleich der Übersicht und zur Klärung ausgewählter Kennzahlendefinitionen.

Die unveränderten Originaldateien bewahre ich lokal unter `data/raw/` auf. Sie sind von GitHub ausgeschlossen. Im Repository liegen der aufbereitete Datensatz, das Transformationsskript, die SQL-Abfragen und die Dokumentation.

## Meine neun ausgewählten Kennzahlen

| Kennzahl | Einheit |
| --- | --- |
| Umsatz (Sales) | Millionen EUR |
| EBITDA | Millionen EUR |
| EBIT | Millionen EUR |
| Jahresüberschuss/-fehlbetrag (Net Income) | Millionen EUR |
| EBITDA-Marge vor Sondereinflüssen | % |
| Operativer Cashflow (Operating Cash Flow) | Millionen EUR |
| Free Cashflow | Millionen EUR |
| Investitionen: Zugänge zu Sachanlagen und immateriellen Vermögenswerten | Millionen EUR |
| ROCE | % |

Ich habe die ursprünglichen Einheiten und Definitionen von BASF beibehalten. Die veröffentlichte EBITDA-Marge wird **vor Sondereinflüssen** ausgewiesen, während die ausgewählte EBITDA-Reihe unbereinigt ist. Deshalb lässt sich diese Marge nicht einfach durch Division des ausgewählten EBITDA durch den Umsatz nachvollziehen.

Die Investitionsreihe erfasst **Anlagenzugänge**. Sie unterscheidet sich von den Auszahlungen, die BASF zur Berechnung des Free Cashflows verwendet.

## Wie ich die Daten aufbereitet habe

Ich habe KI-Unterstützung eingesetzt, um die Quelldateien zu prüfen, den Datensatz aufzubereiten, das Power-Query-M-Skript zu erstellen und die SQL-Abfragen sowie die Dokumentation auszuarbeiten. Anschließend habe ich die Power-Query-Transformation in Power BI Desktop und die SQL-Abfragen in meiner lokalen PostgreSQL-Datenbank ausgeführt und die Ergebnisse schrittweise geprüft.

Das Power-Query-Skript:

- Liest die unveränderte Excel-Datei mit der Zehnjahresübersicht ein.
- Wählt ausschließlich die neun Finanzkennzahlen aus.
- Entfernt Überschriften, Hinweise und nicht benötigte Zeilen.
- Wandelt die Jahresspalten in Zeilen um.
- Entfernt bekannte Fußnotenbuchstaben an Zahlen, ohne deren Wert zu verändern.
- Behält fehlende Werte bei, ohne sie durch Schätzungen zu ersetzen.

Der aufbereitete Datensatz hat diese Struktur:

```text
year | kpi | value | unit
```

Er enthält **90 Zeilen: zehn Jahre × neun Kennzahlen**.

Für ROCE im Jahr 2016 weist BASF in der Quelltabelle keinen Wert aus. Ich habe diese Angabe als fehlend beibehalten: als leeres Feld in der CSV-Datei und als `NULL` in PostgreSQL.

Zur Transparenz: Die im Repository gespeicherte CSV-Datei wurde mit KI-Unterstützung direkt aus der Quelldatei erstellt und mit den entsprechenden Zellen abgeglichen. Das Power-Query-Skript wurde anschließend erfolgreich ausgeführt und seine Vorschau geprüft. Einen vollständigen automatisierten Vergleich zwischen einem exportierten Power-Query-Ergebnis und der gespeicherten CSV-Datei habe ich nicht durchgeführt.

Die genauen Quellzeilen, Kennzahlendefinitionen und Prüfungen sind in den [Hinweisen zur Datenaufbereitung](docs/data_preparation.md) dokumentiert.

## SQL-Analyse

Ich habe die aufbereitete CSV-Datei in die Datenbank `basf_business_performance` importiert und in der Tabelle `public.basf_kpis` gespeichert.

Vor der Analyse habe ich geprüft, ob der Import Folgendes enthält:

- 90 Zeilen.
- Zehn Jahre von 2016 bis 2025.
- Neun unterschiedliche Kennzahlen.
- Genau einen fehlenden Wert: ROCE für 2016.

Zur Beantwortung der acht Fragen nutze ich Filter, bedingte Aggregationen, Common Table Expressions, Fensterfunktionen und einen Self-Join.

Alle acht Abfragen wurden erfolgreich in **PostgreSQL 17 über pgAdmin** ausgeführt. Die Zeilenanzahl und die angezeigten Ergebnisse wurden mit den erwarteten Ausgaben abgeglichen. Zusätzlich wurden die Skripte mit derselben CSV-Datei separat in PGlite auf Basis von PostgreSQL 18.6 getestet.

Die SQL-Dateien:

- [Tabelle anlegen](sql/01_create_table.sql)
- [Importierte Daten prüfen](sql/02_data_checks.sql)
- [Die acht Analysefragen beantworten](sql/03_business_analysis.sql)

## Was die Analyse zeigt

In den veröffentlichten Daten sind mir besonders diese Ergebnisse aufgefallen:

- Der Umsatz stieg von **57.550 Millionen EUR im Jahr 2016 auf 59.657 Millionen EUR im Jahr 2025**. Das entspricht einem Anstieg von **3,66 %**, wobei es innerhalb dieses Zeitraums deutliche Schwankungen gab.
- Der größte jährliche Umsatzanstieg entfiel auf **2021 (+32,88 %)**, der stärkste Rückgang auf **2023 (−21,10 %)**.
- Die EBITDA-Marge vor Sondereinflüssen war **2016 mit 17,9 % am höchsten** und **2025 mit 11,0 % am niedrigsten**.
- BASF wies **2020 und 2022 Jahresfehlbeträge** aus. Im Jahr 2022 blieb das EBIT trotz des Jahresfehlbetrags positiv.
- Im Vergleich **2025 zu 2024** sank der Umsatz um **2,91 %** und der operative Cashflow um **19,23 %**. Gleichzeitig stiegen der Jahresüberschuss um **24,73 %** und der Free Cashflow um **79,41 %**.

Diese Ergebnisse haben mir gezeigt, warum mehrere Finanzkennzahlen gemeinsam betrachtet werden sollten: Umsatz, Ergebnis und Cashflow können sich in unterschiedliche Richtungen entwickeln.

Die vollständigen Ergebnisse und Interpretationsregeln stehen in den [Hinweisen zur SQL-Analyse](docs/sql_analysis.md).

## Wichtige Einschränkungen

BASF kennzeichnet ausgewählte historische Zahlen als angepasst oder neu dargestellt. Dazu gehören Werte für **2017, 2018 und 2024** im Zusammenhang mit nicht fortgeführten Aktivitäten. Ich habe die Zahlen so übernommen, wie sie in der Zehnjahresübersicht 2025 veröffentlicht wurden, und die zugehörigen Hinweise dokumentiert.

Die berechneten Veränderungen beschreiben deshalb die **veröffentlichten Datenreihen**. Sie sollten nicht automatisch als Wachstum auf vergleichbarer Basis interpretiert werden.

Außerdem unterscheide ich zwischen **prozentualen Veränderungen** und Veränderungen in **Prozentpunkten**. Steigt beispielsweise der ROCE von 5,1 % auf 5,8 %, entspricht das einem Anstieg um **0,7 Prozentpunkte**.

Der Datensatz ermöglicht beschreibende Vergleiche. Allein daraus lassen sich weder die Ursachen eines Verlusts noch der Erfolg einer Investitionsentscheidung ableiten. Ebenso lässt sich damit nicht nachweisen, dass Veränderungen der Investitionen Veränderungen des ROCE verursacht haben.

## Aufbau des Repositorys

```text
data/
  processed/     Aufbereiteter Finanzdatensatz

power_query/     Reproduzierbares Power-Query-M-Skript
sql/             Tabellendefinition, Datenprüfungen und Analyseabfragen
docs/            Quellen, Methodik, Ergebnisse und Einschränkungen
powerbi/         Freigegebener Entwurf und native PBIP-Umsetzung
tools/           Projekterstellung und Strukturprüfungen
```

Die Originaldateien liegen lokal unter `data/raw/`. Dieser Ordner ist von Git ausgeschlossen.

## Das Projekt nachvollziehen

1. Die beiden offiziellen BASF-Excel-Dateien herunterladen und unter `data/raw/` ablegen.
2. In Power BI Desktop oder Excel eine leere Abfrage erstellen.
3. Den erweiterten Editor öffnen und den Inhalt von `power_query/basf_kpis.m` einfügen.
4. `RawFile` auf den lokalen Pfad der Zehnjahresdatei setzen und die Abfrage aktualisieren.
5. Die erwarteten 90 Zeilen und den fehlenden ROCE-Wert für 2016 prüfen.
6. Der [PostgreSQL-Anleitung](docs/postgresql_setup.md) folgen, um die Tabelle anzulegen und die aufbereitete CSV-Datei zu importieren.
7. Die Datenprüfungen und anschließend die acht Analyseabfragen einzeln ausführen.

Die technischen Detaildokumente und die Kommentare in den SQL-Dateien sind auf Englisch verfasst.

## Entwurf für den Bericht

Ich habe ein einseitiges Layout im Querformat mit dunkelgrünem Hintergrund,
abgerundeten Kennzahlenkarten, weich eingeblendeten Fotos aus Ludwigshafen und
dem offiziellen BASF-Logo entworfen. Die Vorschau verwendet denselben Datensatz
und bietet eine Jahresauswahl für 2024/2025. Sie ist ein **interaktiver
Designentwurf und noch kein fertiger Power-BI-Bericht**.

Die [Vorschau](powerbi/design/preview.html) herunterladen und im Browser öffnen;
GitHub zeigt ihren Quelltext an, führt sie aber nicht aus. Die
[Designhinweise und Bildnachweise](docs/powerbi_design.md) dokumentieren den
Entwurf.

## Natives Power-BI-Projekt — Desktop-Prüfung steht aus

Ich habe [das PBIP-Projekt](powerbi/BASF/BASF.pbip) mit neun Kennzahlenkarten,
vier historischen Diagrammen und einer Jahresauswahl vorbereitet. Es enthält
einen portablen Stand der aufbereiteten CSV-Datei und benötigt dafür keine
Datenbank-Zugangsdaten oder lokalen Quelldateipfade. Das separate Power-Query-M-Skript
bleibt der dokumentierte Weg zur Bereinigung der Originaldateien.

Die Projektdefinitionen haben Strukturprüfungen und die Validierung anhand der
Microsoft-JSON-Schemata bestanden. **Aktualisierung, DAX-Ausführung und Darstellung
in Power BI Desktop sind noch nicht geprüft.** Der Bericht ist daher noch kein
fertig validiertes Dashboard. Die [Anleitung und Prüfschritte](docs/powerbi_implementation.md)
dokumentieren den aktuellen Stand.

## Nächster Schritt

Ich werde den nativen Bericht in Power BI Desktop öffnen und prüfen, die
Interaktionen und Finanzwerte kontrollieren und anschließend die endgültigen
Screenshots für mein Portfolio erstellen.
