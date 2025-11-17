# Aktueller Fortschritt - Plan


### Todos Aktuell
- weitere Explorative Datenanalyse, Zusammenhänge Features + Label analysieren
- Verteilungen visualisieren, evtl. zeitliche Trends, 'Top 10' Countries Vergleich etc.
- Feature vs. Label & Feature vs. Feature, Correlations

- Split Datensatz mit GroupShuffleSplit (nach country gruppiert)
- Cross Validation (GroupKFold) definieren


### Geplant
- EDA abschließen
- Split, GroupKFold

- Data Preprocessing: Missing Indicators, Data Cleaning/ Imputation, Transformation (Skewness, Scaling/Normalize)?
- Länderbasiertes Cluster (One-Hot-Encoded) als zusätzl. Feature? (Vergleich Clustering vs OWID)
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

- Train Test Split mit GroupShuffleSplit #1: gruppiert nach Ländern splitten für nächste Schritte (+Experimente) - (grad nur im Notebook als Test)

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

### Schritte Pipeline grob:
Vorschritte:
- CSV Files laden
- nur countries behalten & files mergen, 
- auf Zeitraum begrenzen (6 Jahre), also pro Country 6 Zeilen
- countries mit >= 50% missing values ausschließen

Pipeline:
- Train-Test Split (grouped nach country)
- GroupKFold definieren
- Imputation (restl. missing values), Transformation, Normalisieren/Skalieren (nur für Linear Regr) (später Rücskalieren, eig wichtig für XAI) ??
Country als kateg. Variable wie behandeln? Cluster mit KMeans (basierend auf numer. Features) & One HotEncoding

- Training (Cross-Validation zb k=5 mit GroupKFold & validieren)
- Evaluation mit Testset
------
- XAI mit SHAP...

### Notizen / offene Fragen
- Datensätze, die ausgeschlossen wurden (da viele Länder "No Data"):
Alphabetisierungsrate, Armutsrate und weitere
- wie mit Country als kateg. Variable umgehen?
- wenn numer. Features skaliert werden -> muss für SHAP rückskaliert werden (?) 
- Herausforderung SHAP Interpretierbarkeit & Multikollinearität (evtl. Features clustern ?)
- missing not at random, wie imputieren? (missing_indicator columns pro feature, iterative imp?)