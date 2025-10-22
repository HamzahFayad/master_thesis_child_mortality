# Aktueller Fortschritt - Plan


### Aktuelle Aufgaben
- Schritt A für Pipeline > rohe Daten laden, non-countries entfernen, filtern auf 6 year period, mergen für main df
- Explorative Datenanalyse, Zusammenhänge Features + Label analysieren
- Feature vs. Label & Feature vs. Feature

### Geplant
- erstes Data-Handling: fehlende Werte, 

### Abgeschlossen
- rohe Daten geladen (10 CSV Dateien) - Label + 9 Features
- Continents etc. entfernen
- Datenintegration: Dateien mergen (eindeutige ID: Entity/Code/Jahr), Outer Join um alle Infos zu behalten
- Datentypen checken
-- Anforderung Betreuung: begrenzten Analysezeitraum auswählen + DF darauf filtern
 --> den Zeitraum (6 Jahre) mit höchster Datenvollständigkeit bzw. geringsten NaNs

### Notizen
- Datensätze, die ausgeschlossen wurden (da viele Länder "No Data"):
Alphabetisierungsrate, Armutsrate