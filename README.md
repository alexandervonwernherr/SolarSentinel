# SolarSentinel

Live-Vorhersage geomagnetischer Stürme (Kp-Index) aus Sonnenwind-Daten.

## Ziel

| | |
|---|---|
| Problem | Der offizielle Kp-Index wird nur alle **3 Stunden** aktualisiert. |
| Ziel | Eine Vorhersage alle **paar Minuten** aus Echtzeit-Daten. |
| Zielgröße | **Kp-Index** (0–9): wie stark das Erdmagnetfeld gestört ist. Ab Kp 5 spricht man von einem Sturm (G1–G5). |
| Idee | Satelliten am L1-Punkt messen den Sonnenwind 30–90 Minuten, bevor er die Erde erreicht. Vor allem Bz < 0 (Magnetfeld zeigt nach Süden) treibt Stürme an. |

Hintergrund: [Karl/kp_index_erklaert.md](Karl/kp_index_erklaert.md)

## Daten

Quelle: NASA OMNI ([spdf.gsfc.nasa.gov/pub/data/omni](https://spdf.gsfc.nasa.gov/pub/data/omni))

| Datensatz | Auflösung | Zeitraum | Wichtige Spalten |
|---|---|---|---|
| OMNI2 | stündlich | ab 1963 | `kp`, `dst`, `ap`, `f107`, `sunspot` |
| OMNI high-res | 1 Minute | ab 1981 | `bz_gsm`, `by_gsm`, `b_mag`, `speed`, `density`, `pressure`, `e_field`, `sym_h`, `ae` |

Füllwerte von NASA (z. B. `9999.99`) werden beim Laden zu `NaN`.

## Setup

Voraussetzung: [uv](https://docs.astral.sh/uv/getting-started/installation/). Python 3.14 lädt uv selbst, falls es fehlt.

```bash
git clone https://github.com/alexandervonwernherr/SolarSentinel.git
cd SolarSentinel
uv sync                              # baut .venv exakt nach uv.lock
uv run nbdime config-git --enable    # einmalig: Notebook-Merges lesbar machen
```

Im Notebook als Kernel `.venv` auswählen.

| Datei | Inhalt | Ins Repo? |
|---|---|---|
| `.python-version` | Python-Version (3.14) | ja |
| `pyproject.toml` | Pakete: `dependencies` = Modell + Dashboard, `dev` = Notebooks/Plots | ja |
| `uv.lock` | exakte Versionen aller Pakete | ja |
| `.venv/` | die installierte Umgebung | **nein**, baut jeder selbst |

Regeln:
- Neues Paket: `uv add paket` (nur fürs Entwickeln: `uv add --dev paket`), **nie** `pip install`
- `uv.lock` immer mit committen
- Nach jedem `git pull`: `uv sync`

## Usage

1. Daten herunterladen und zusammenführen (mehrere GB, läuft lange; bereits geladene Dateien werden übersprungen):

   ```bash
   uv run python update_data.py
   ```

   Ergebnis: `omni_raw/` (Rohdateien von NASA) und `omni_all.csv` (zusammengeführte Tabelle).

2. `SolarSentinel.ipynb` öffnen: wandelt `omni_all.csv` in `omni_1995.parquet` um, baut Features (z. B. `b_sum`) und trainiert eine Baseline (DummyRegressor vs. LightGBM).

Daten (`omni_raw/`, `*.csv`, `*.parquet`, `_data/`) und Modelle (`_models/`) gehören **nicht** ins Repo (siehe `.gitignore`).

## Projektstruktur

```
SolarSentinel/
├── update_data.py            # OMNI-Download + Zusammenführen
├── SolarSentinel.ipynb       # gemeinsames Notebook: EDA + Baseline
├── _data/                    # lokale Daten (nicht im Repo)
├── _models/                  # gespeicherte Modelle (nicht im Repo)
├── pyproject.toml, uv.lock   # Pakete (uv)
├── .python-version           # Python 3.14
├── Alex/  Karl/  Nooshin/    # persönliche Arbeitsordner
└── *.pdf, solarsentinel.qea  # Plan und Architektur
```

## Team

| Name | Rolle |
|---|---|
| Alex | GitHub, Code |
| Karl | Projektdokumentation |
| Nooshin | Wissenschaftlicher Hintergrund |

## Notebook-Merge-Konflikte

```bash
nbdime mergetool
git add <notebook>.ipynb
git commit -m "Resolve notebook merge conflict"
```
