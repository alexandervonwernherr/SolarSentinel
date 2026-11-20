# Vergleich: project_template ↔ SolarSentinel

Stand 2026-11-19. Template: `4month/my_ds-capstone-project-template` (neuefische, 1 Commit).
SolarSentinel: Gruppenrepo, Branch `kb-branch5`.

## 1. Was wo liegt

| Bereich | Template | SolarSentinel | Lücke? |
|---|---|---|---|
| README | Setup, MLflow, Usage, nbdime-Tipps | 2 Zeilen ("Predicting Solar Events") | **ja, groß** |
| Ordnerstruktur | `data/` `models/` `modeling/` `notebooks/` `images/` | flach + Personenordner `Alex/ Karl/ Nooshin/` | ja |
| Daten laden | in `train.py` (`__get_data`) | `update_data.py` (OMNI-Download → `omni_all.csv`) | nein, SolarSentinel ist weiter |
| Feature Engineering | `modeling/feature_engineering.py` | noch keins | später |
| Training + Predict | `modeling/train.py`, `modeling/predict.py` | noch keins | später |
| Experiment-Tracking | MLflow (`config.py`, `.mlflow_uri`) | keins | ja |
| Abhängigkeiten | `requirements.txt` (Deploy) + `requirements_dev.txt` (Dev) | keine Datei; Notebook installiert per `subprocess` | **ja** |
| Setup-Befehl | `Makefile` → `make setup` (pyenv 3.11.3 + .venv) | keiner | ja |
| Python-Version | 3.11.3 fest | nicht festgelegt | ja |
| .gitignore | Standard + `data/*.csv`, `models/*`, `mlruns`, `.mlflow_uri` | Standard (neuere Version), **ohne** Daten-/Modell-Regeln | **ja: `omni_raw/` und `omni_all.csv` würden mitcommittet** |
| Notebook-Merge | nbdime (`nbdime config-git --enable`) | nichts | ja, bei 3 Leuten wichtig |
| GitHub Actions | 4 Workflows: Issue/PR → neuefische Project-Board (Todo / In Progress / Done) | keine | optional |
| Tests | `pytest`, `testbook` in Dev-Requirements | keine | später |
| Formatierung | `black` | keine | optional |
| Doku / Planung | – | PDF-Plan, `solarsentinel.qea` (Enterprise Architect), `Karl/kp_index_erklaert.md` | SolarSentinel ist weiter |

## 2. Was SolarSentinel hat und das Template nicht

- Echte Datenquelle (NASA OMNI, stündlich + minütlich) mit Download-Skript
- Fachliche Erklärung des Kp-Index (`Karl/kp_index_erklaert.md`)
- Rollen: Alex = GitHub/Code, Karl = Doku, Nooshin = Wissenschaft
- Streamlit-Skizze (`Karl/kp_dashboard.py`, noch fehlerhaft: `request.get`, `pd = pd.DataFrame(...)`)

## 3. Was ich aus dem Template übernehmen würde (Priorität)

| # | Was | Warum | Aufwand |
|---|---|---|---|
| 1 | `.gitignore`-Zeilen: `omni_raw/`, `*.csv`, `models/`, `mlruns`, `.mlflow_uri` | OMNI-Rohdaten sind hunderte MB, dürfen nicht ins Repo | 1 Min |
| 2 | `requirements_dev.txt` (pandas, numpy, scikit-learn, matplotlib, requests, streamlit, jupyterlab, nbdime, mlflow) | alle drei gleiche Umgebung; ersetzt `subprocess`-Install im Notebook | 5 Min |
| 3 | nbdime aktivieren | Notebook-Konflikte zu dritt | 1 Min |
| 4 | README nach Template-Gliederung: Ziel, Daten, Setup, Usage, Team | Abgabe + Onboarding | Doku-Rolle = Karl |
| 5 | Ordner `data/` `models/` `notebooks/` + `.gitkeep` | gemeinsame Pfade statt Personenordner | Teamabsprache |
| 6 | `modeling/` (train/predict/config) + MLflow | sobald es ein Modell gibt | später |
| 7 | GitHub-Actions fürs Project-Board | nur wenn ihr das neuefische-Board nutzt; braucht Secrets `DS_PROJECT_BOARD_APP_ID/PEM` | Alex |

Nicht übernehmen: `environment.yml` (veraltet, Python 3.8, passt nicht zu `requirements*.txt`), die MLflow-Erklärbilder in `images/`, Coffee-Dataset-Code.

## 3b. Update nach Pull (2026-11-19, Commit `f1906c7`)

Alex hat nur `SolarSentinel.ipynb` geändert:
- lädt `omni_all.csv` in Chunks → speichert `omni_1995.parquet`
- Feature `b_sum` (Betrag des Magnetfelds), Plots Mai-Sturm 2024
- **Baseline-Modell:** DummyRegressor vs. LightGBM, Metriken R2 / MAE / RMSE

Folgen für die Liste oben:
- Punkt 1: `.gitignore` braucht zusätzlich `*.parquet`
- Punkt 2: neue Pakete `seaborn`, `lightgbm`, `pyarrow` (in `requirements_dev.txt` ergänzt)
- Punkt 6 rückt näher: es gibt jetzt ein Modell → MLflow / `modeling/train.py` lohnt sich, sobald mehrere Modelle verglichen werden
- Keine Konflikte mit README, `.gitignore` oder Ordnerstruktur → Kopieren ins Root ist jetzt gefahrlos

## 4. Was davon in `Karl/` passt

Nur Punkte 2 und 4 lassen sich in `Karl/` vorbereiten (Entwurf `requirements_dev.txt`, README-Entwurf).
Punkte 1, 3, 5–7 betreffen das ganze Repo → mit Alex absprechen, er pusht.
