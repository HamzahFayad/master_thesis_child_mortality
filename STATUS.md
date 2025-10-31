# Aktueller Fortschritt - Plan


### Todos Aktuell
- Explorative Datenanalyse, Zusammenhänge Features + Label analysieren
- Verteilungen visualisieren, evtl. zeitliche Trends, 'Top 10' Countries Vergleich etc.
- Feature vs. Label & Feature vs. Feature, Correlations
- Skewness: Transformation (zb logn) für rechtsschiefe testweise, Normalisierung/Standardisierung testen (visualisieren) - nur für LR ?
- Train-Test Split (GroupShuppfleSplit)
- Preprocessing B02: restl. Missing Values Imputation (testen)
                     evtl grouped nach countries per column 
                     (missing values: SimpleImputer)

### Geplant
- EDA abschließen
- Data Preprocessing: Data Cleaning/ Imputation, evtl. Outlier, Transformation (Scaling/Normalize)?
- evtl. Länderbasiertes Cluster (One-Hot-Encoded) als zusätzl. Feature? (Vergleich Clustering vs OWID basiert)
- Feature-Engineering, Feature Selection oder Feature-Cluster?
- Datensplittung für Modelltraining und -test
- Modelltraining (LR, RF, XGB) und Evaluation

### Abgeschlossen
- rohe Daten geladen (10 CSV Dateien) - Label + 9 Features
- Continents etc. entfernen
- Datenintegration: Dateien mergen (eindeutige ID: Entity/Code/Jahr), Outer Join um alle Infos zu behalten
- Datentypen checken
- describe() für erste Erkentnisse
- Anforderung Betreuung: begrenzten Analysezeitraum auswählen + DF darauf filtern
    --> Zeitraum (6 Jahre) mit höchster Datenvollständigkeit bzw. geringsten NaNs
- Schritt A für Pipeline (Vorarbeit): rohe Daten laden, non-countries entfernen, filtern auf 6 year period, mergen für main df

- Schritt B01 für Pipeline (Vorarbeit), erstes Data-Handling: Länder mit >=50% missing values entfernt als custom preprocessing function 01 für ersten gefilterten Datensatz (vorallem sind Inseln, Überseegebiete betroffen; filtered_data_01.csv als 1. interim Datensatz)
- Schritt B02 für Pipeline (Vorarbeit): füg missing indicators für alle 9 Features

- Train Test Split mit GroupShuffleSplit #1: gruppiert nach Ländern splitten für nächste Schritte (+Experimente)

### Erkentnisse
Daten:
- Zeitraum begrenzen auf 6 Jahre -> 2013-2018 am wenigsten null Werte insg.
- 1200 Rows im main DF 2013-2018, 200 Länder (Schritt A)

Explorative Analyse:
- insg. 1273 Null Values, am höchsten bei: physicians_per_1000_people: 447 (37.25%), nurses_and_midwives_per_1000_people: 338 (28.17%), prevalence_of_undernourishment: 198 (16.50%)
- höchste U5MR im DF: 278 per 1000 Lebendgeburten, geringste U5MR: 1,7 per 1000 Geburten
- Label + 6 features sind rechtsschief verteilt (Histogramme)
- Scatterplots: einige Feature-Label Beziehungen haben logarithmisches/exponentielles Verhalten 
  (zB. gdp_per_capita, physicians_per_1000); ähnliche Werte clustern sich oft zusammen, trotzdem auch vereinzelte Outlier
- höchste Anzahl an Missing Values haben meist Entwicklungsländer/Länder mit schwierigen Situationen/Umständen (Nordkorea,Südsudan, Guinea...), vereinzelt auch kleine Länder (Monaco oder Andorra zB) - oft schwieriger zuverlässige Daten aus Niedrigeinkommensländern zu erhalten

- starke bis mittelstarke Korrelationen zw. allen Features & Label
- aber auch: Viele Features korrelieren stark

Preprocessing:
- Missing Values: 7 Länder haben über 50% missing values und daher entfernt >> 1. gefiltertes DF (Schritt B01) --> von 1273 missing values nur noch 967 missing values

### Schritte Pipeline:
Vorschritte:
- CSV Files laden
- nur countries behalten & files mergen, 
- auf Zeitraum begrenzen (6 Jahre), also pro Country 6 Zeilen
- countries mit >= 50% missing values ausschließen
- Missing Values Spalten (0 oder 1 wenn column fehlt) (oder nach dem Train-Test Split ?)
Modelltraining:
- Train-Test Split (grouped nach country? am besten randomized/shuffeld? - random countries für test und trainset statt nach Reihenfolge zu gehen), Jahr entfernen (Fokus ist ja nur Faktoren, sonst wird Trend mitgelernt)?
- Imputation (restl. missing values), Log-Transf, Normalisieren/Skalieren (nur für Linear Regr) (später Rücskalieren, eig wichtig für XAI)
Country als kateg. Variable wie behandeln? Encoding (aber zu viel?)
- (Multikolineraität)
- Training
- Evaluation
- XAI mit SHAP zb.

### Notizen / offene Fragen
- Datensätze, die ausgeschlossen wurden (da viele Länder "No Data"):
Alphabetisierungsrate, Armutsrate
- Worldbank Groups als Feature behalten oder erstmal ohne? (x)
- wie mit Country als kateg. Variable umgehen?
- wenn Features skaliert werden -> muss für SHAP rückskaliert werden (?) 
- Herausforderung SHAP Interpretierbarkeit & Multikollinearität (evtl. Features clustern ?)