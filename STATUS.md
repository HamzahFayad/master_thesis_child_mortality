# Aktueller Fortschritt - Plan


### Aktuelle Aufgaben
- describe() für erste Erkentnisse
- Explorative Datenanalyse, einzelne Features, Zusammenhänge Features + Label analysieren
- Verteilungen visualisieren, evtl. zeitliche Trends, 'Top 10' Countries Vergleich etc.
- Feature vs. Label & Feature vs. Feature, Correlations

### Geplant
- Data Preprocessing:
    > Data-Handling, 

### Abgeschlossen
- rohe Daten geladen (10 CSV Dateien) - Label + 9 Features
- Continents etc. entfernen
- Datenintegration: Dateien mergen (eindeutige ID: Entity/Code/Jahr), Outer Join um alle Infos zu behalten
- Datentypen checken
- Anforderung Betreuung: begrenzten Analysezeitraum auswählen + DF darauf filtern
    --> Zeitraum (6 Jahre) mit höchster Datenvollständigkeit bzw. geringsten NaNs
- Schritt A für Pipeline: rohe Daten laden, non-countries entfernen, filtern auf 6 year period, mergen für main df
- erstes Data-Handling: Länder mit >=50% missing values entfernt
- Schritt B01 für Pipeline: custom preprocessing function 01 für ersten gefilterten Datensatz

### Erkentnisse
Daten:
- Zeitraum begrenzen auf 6 Jahre -> 2013-2018 am wenigsten null Werte insg.
- 1200 Rows im main DF 2013-2018 (Schritt A)

Explorative Analyse:
- insg. 1273 Null Values, am höchsten bei: physicians_per_1000_people: 447 (37.25%), nurses_and_midwives_per_1000_people: 338 (28.17%), prevalence_of_undernourishment: 198 (16.50%)
- höchste U5MR im DF: 278 per 1000 Lebendgeburten, geringste U5MR: 1,7 per 1000 Geburten
- Label + 6 features sind rechtsschief verteilt (Histogramme)

- starke bis mittelstarke Korrelationen zw. allen Features & Label
- aber auch: Viele Features korrelieren stark

Preprocessing:
>
> Missing Values:
- Schritt B01: 7 Länder haben über 50% missing values und daher entfernt >> 1. gefiltertes DF
    --> von 1273 missing values nur noch 967 missing values

### Notizen
- Datensätze, die ausgeschlossen wurden (da viele Länder "No Data"):
Alphabetisierungsrate, Armutsrate