# Aktueller Fortschritt - Plan


### Aktuelle Aufgaben
- describe() für erste Erkentnisse
- Explorative Datenanalyse, einzelne Features, Zusammenhänge Features + Label analysieren
- Verteilungen visualisieren, evtl. zeitliche Trends, 'Top 10' Countries Vergleich
- Feature vs. Label & Feature vs. Feature

### Geplant
- Data Preprocessing:
    erstes Data-Handling: fehlende Werte

### Abgeschlossen
- rohe Daten geladen (10 CSV Dateien) - Label + 9 Features
- Continents etc. entfernen
- Datenintegration: Dateien mergen (eindeutige ID: Entity/Code/Jahr), Outer Join um alle Infos zu behalten
- Datentypen checken
- Anforderung Betreuung: begrenzten Analysezeitraum auswählen + DF darauf filtern
 --> den Zeitraum (6 Jahre) mit höchster Datenvollständigkeit bzw. geringsten NaNs
- Schritt A für Pipeline > rohe Daten laden, non-countries entfernen, filtern auf 6 year period, mergen für main df

### Erkentnisse
- Zeitraum begrenzen auf 6 Jahre -> 2013-2018 am wenigsten null Werte insg.
- 1200 Rows im main DF 2013-2018
- insg. 1273 Null Values, am höchsten diese (physicians_per_1000_people: 447, nurses_and_midwives_per_1000_people: 338, prevalence_of_undernourishment: 198)
- starke bis mittelstarke Korrelationen zw. allen Features & Label
- aber: Viele Features korrelieren stark

### Notizen
- Datensätze, die ausgeschlossen wurden (da viele Länder "No Data"):
Alphabetisierungsrate, Armutsrate