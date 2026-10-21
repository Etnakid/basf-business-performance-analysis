# BASF Business Performance Analysis

[English](README.md) | **Deutsch**

Ein unabhängiges Portfolio-Projekt zur Analyse von **neun Finanzkennzahlen für 2016–2025** mit **Power Query, PostgreSQL und Power BI**.

Ich lebe in Ludwigshafen am Rhein, wo BASF mein Umfeld stark prägt. Deshalb wollte ich verstehen, wie sich Umsatz, Profitabilität, Cashflow, Investitionen und Kapitalrendite über die Jahre entwickelt haben. Der klare Fokus auf Finanzdaten hält das Projekt überschaubar.

[![Power-BI-Bericht: Übersicht 2025](powerbi/preview/report-2025.png)](powerbi/preview/report-2025.pdf)

**[PDF ansehen](powerbi/preview/report-2025.pdf)** · [Editierbares Power-BI-Projekt](powerbi/BASF.pbip) · [SQL-Analyse](sql/03_business_analysis.sql)

## Wichtigste Ergebnisse

- Der Umsatz stieg von **57.550 Millionen EUR (2016) auf 59.657 Millionen EUR (2025), um 3,66 %**, mit dem Höchststand 2022.
- Der größte jährliche Umsatzanstieg entfiel auf **2021 (+32,88 %)**, der stärkste Rückgang auf **2023 (−21,10 %)**.
- Die EBITDA-Marge vor Sondereinflüssen war **2016 am höchsten (17,9 %)** und **2025 am niedrigsten (11,0 %)**.
- Jahresfehlbeträge traten **2020 und 2022** auf; 2022 blieb das EBIT positiv.
- **2025 gegenüber 2024** sanken Umsatz (**−2,91 %**) und operativer Cashflow (**−19,23 %**), während Jahresüberschuss (**+24,73 %**) und Free Cashflow (**+79,41 %**) stiegen.

Die Ergebnisse beschreiben die veröffentlichten Datenreihen. Anpassungen und nicht fortgeführte Aktivitäten schränken die Vergleichbarkeit ein; die Veränderungen sind nicht automatisch Wachstum auf vergleichbarer Basis. Siehe [Ergebnisse und Interpretationsregeln](docs/sql_analysis.md).

## Analyse und eingesetzte Fähigkeiten

Die acht SQL-Fragen behandeln Umsatztrends; EBITDA, EBIT und Jahresüberschuss; Margenextrema; Cashflow; Anlagenzugänge und ROCE; jährliche Umsatzranglisten; Verlustjahre sowie den Vergleich aller neun Kennzahlen zwischen 2025 und 2024.

| Schritt | Enthaltene Arbeit |
| --- | --- |
| Power Query | Quellzeilen auswählen, Jahre entpivotieren, bekannte Fußnoten entfernen, Datentypen setzen und fehlende Werte erhalten |
| PostgreSQL | Importprüfungen, bedingte Aggregation, CTEs, Fensterfunktionen und Self-Join |
| Power BI | Eine Seite mit neun Kennzahlenkarten, vier Verlaufsdiagrammen, DAX-Vergleichen und einer nicht verknüpften Jahresauswahl |

Ich habe die Power-Query-Transformation und SQL-Abfragen lokal ausgeführt und den Bericht in Power BI Desktop geprüft. Das Projekt wurde mit KI-Unterstützung entwickelt. Ausführung und Validierung sind im [Prüfprotokoll](docs/powerbi_implementation.md) dokumentiert, das automatisierte Prüfungen, visuelle Kontrollen und vom Eigentümer gemeldete DAX-Ergebnisse unterscheidet.

## Daten und Definitionen

Die Quelle ist der offizielle **BASF-Bericht 2025**:

- [Zehnjahresübersicht](https://report.basf.com/2025/en/overviews/ten-year-summary.html): [Excel-Datei](https://report.basf.com/2025/en/_assets/downloads/10-year-summary-basf-ar25.xlsx).
- [Download-Center](https://report.basf.com/2025/en/services/downloads.html): [Alle Tabellen](https://report.basf.com/2025/en/_assets/downloads/all-tables-basf-ar25.xlsx), für Abgleich und Definitionen.

Die [aufbereitete CSV-Datei](data/processed/basf_kpis_2016_2025.csv) enthält **90 Beobachtungen: zehn Jahre × neun Kennzahlen**, mit `year | kpi | value | unit`. Die Kennzahlen sind Sales, EBITDA, EBIT, Net Income, EBITDA Margin before special items, Operating Cash Flow, Free Cash Flow, Anlagenzugänge und ROCE.

- Geldbeträge bleiben in **Millionen EUR**; Marge und ROCE in Prozenteinheiten.
- **ROCE 2016 fehlt** und bleibt ein leeres CSV-Feld bzw. SQL-/Power-BI-null.
- Die Marge wird **vor Sondereinflüssen** ausgewiesen; die EBITDA-Reihe ist unbereinigt. Aus EBITDA geteilt durch Umsatz ergibt sich diese Marge daher nicht.
- Investitionen bedeuten **Zugänge zu Sachanlagen und immateriellen Vermögenswerten**, keine Auszahlungen. Die Reihe eignet sich nicht zur Rekonstruktion des Free Cashflows durch Abzug vom operativen Cashflow.
- Margen- und ROCE-Veränderungen werden in **Prozentpunkten** angegeben.

Alle 90 Beobachtungen wurden am 21. Oktober 2026 erneut mit beiden offiziellen Excel-Dateien abgeglichen. Quellzeilen, fehlende Werte und Anpassungen stehen in den [Hinweisen zur Datenaufbereitung](docs/data_preparation.md). Originaldateien sind von Git ausgeschlossen und werden für die Rekonstruktion separat heruntergeladen.

## Nachvollziehen oder prüfen

### Bericht ansehen

Für einen schnellen Überblick genügt das PDF oben. Für Interaktionen das **gesamte Repository** herunterladen oder klonen, die Begleitordner zusammenlassen und `powerbi/BASF.pbip` in Power BI Desktop öffnen. **Aktualisieren** lädt den exakt eingebetteten CSV-Datenstand. Datenbank-Zugangsdaten, Originaldateien und Python sind dafür nicht erforderlich. Es werden keine neuen BASF-Daten heruntergeladen.

2025 ist vorausgewählt. Eine andere Jahresauswahl ändert die Karten; alle vier Diagramme behalten 2016–2025. ROCE bleibt für 2016 leer. Siehe [Power-BI-Einrichtung und Prüfung](docs/powerbi_implementation.md) oder die [italienische Kurzanleitung](powerbi/START_HERE.it.md).

### SQL-Analyse ausführen

Der [PostgreSQL-Anleitung](docs/postgresql_setup.md) folgen, eine leere Tabelle anlegen und die gespeicherte CSV importieren. Zuerst `sql/02_data_checks.sql`, danach die acht nummerierten Abfragen in `sql/03_business_analysis.sql` ausführen. Dafür sind weder Originaldateien noch Power BI nötig. Die Skripte wurden am 21. Oktober 2026 erfolgreich in einer isolierten **PostgreSQL-17**-Datenbank erneut ausgeführt.

### Transformation aus der Quelle wiederholen

1. Beide Excel-Dateien oben in einen lokalen Ordner `data/raw/` herunterladen.
2. In Power BI Desktop oder Excel eine leere Abfrage erstellen und [power_query/basf_kpis.m](power_query/basf_kpis.m) in den erweiterten Editor einfügen.
3. `RawFile` auf den lokalen Pfad zu `10-year-summary-basf-ar25.xlsx` setzen und aktualisieren.
4. 90 Zeilen, neun Kennzahlen und den einzigen fehlenden Wert ROCE 2016 prüfen.

Die ursprüngliche Power-Query-Vorschau wurde geprüft. Ein vollständiger exportierter Power-Query-Datensatz wurde nicht automatisiert mit der CSV verglichen. Der unabhängige Excel-CSV-Abgleich umfasst sämtliche Quellbeobachtungen.

### Optionale Projektpflege

Python ist nur zum Erstellen oder Prüfen der Definitionen erforderlich. Vom Repository-Hauptordner aus (mit Python 3.12 getestet):

```text
python tools/check_powerbi_project.py
python -m pip install jsonschema==4.26.0
python tools/check_powerbi_project.py --schemas
```

Die Schemaprüfung benötigt Internetzugang. Sie prüft Struktur und eingebettete Daten, führt aber weder DAX aus noch rendert sie Power BI. Zum Neuerstellen nach CSV-Änderungen die [Pflegehinweise](docs/powerbi_implementation.md) beachten; der Builder überschreibt die Berichtsdefinitionen.

## Aufbau des Repositorys

```text
data/processed/   Geprüfter Datensatz mit 90 Zeilen
power_query/     Transformation der Originaldatei
sql/             Tabelle, Importprüfungen und acht Analysefragen
docs/            Quellen, Methodik, Ergebnisse und Prüfprotokolle
powerbi/         PBIP, Bericht/Modell, DAX, Assets und Vorschau
tools/           Builder, Strukturprüfung und Hintergrund-Renderer
```

Das native PDF und sein gerendertes Bild zeigen die Ansicht 2025. Das editierbare PBIP ist enthalten; eine kompilierte PBIX-Datei nicht. Bildquellen und Schriftlizenz stehen in den [Designnachweisen](docs/powerbi_design.md). Das unabhängige Portfolio-Projekt wird nicht von BASF gesponsert. Technische Detaildokumente und SQL-Kommentare sind auf Englisch.
