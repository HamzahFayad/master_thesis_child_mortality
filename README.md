# Github Repository zur Masterarbeit

> _Einsatz von Machine Learning zur Prädiktion der Kindersterblichkeitsrate und Identifikation 
relevanter Einflussfaktoren: Eine simulationsbasierte Analyse auf Länderebene_

### Ziel der Arbeit:
Einsatz von Machine Learning Modellen zur retrospektiven Prädiktion des globalen Gesundheitsindikators ‚Kindersterblichkeitsrate‘ auf Länderebene in einem begrenzten Zeitraum.

Es sollen spezifische Determinanten aus sozioökonomischen und gesundheitsbezogenen Bereichen identifiziert werden, die als Einflussfaktoren der Zielvariable dienen.

Eine Simulation in Form einer webbasierten Demo ergänzt die Arbeit damit, wie sich hypothetische Änderungen einzelner Einflussfaktoren auf die Zielvariable auswirken könnten.

[Projekt Workflow](https://miro.com/app/board/uXjVJyJRsyM=/?share_link_id=203735676385)

### Projektstruktur:
- `00_data/`    
Original Rohdaten, merged, filtered, imputed, splitted Datensätze 
(Zwischenschritte für Nachvollziehbarkeit)
- `01_notebooks/`  
Jupyter Notebooks
Zweck: gesamter Workflow in einzelne Notebooks und prototypisch Logik austesten für finale Pipeline
(Datenüberblick, Qualitätsanalyse, EDA, Datenvisualisierungen, Preprocessing und co.)
- `02_src/`  
wiederverwendbare Funktionen, Refactorings aus notebooks und finale Pipeline
- `03_visualizations/`  
wichtige Diagramme aus allen notebooks
- `04_models/`
Model gespeichert zur Weiterverwendung  
- `05_reports/`
Thesis und weitere Dokumentationen 

### Simulationstool:
[Tool Git Repository](https://github.com/HamzahFayad/master_thesis_streamlit_demo)

### Setup:

Prerequisites: Python 3.11+

1. Umgebung erstellen:
python3.11 -m venv masterthesis_venv
source masterthesis_venv/bin/activate  # Mac/Linux
oder: masterthesis_venv\Scripts\activate  # Windows

2. Abhängigkeiten installieren:
`pip install -r requirements.txt`

3. Pipeline ausführen:
`cd 02_src`
`python3 model_pipeline.py`