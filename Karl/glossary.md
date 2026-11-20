# SolarSentinel Glossary

Every technical term in the project, explained simply. As of 2026-11-20.
The big picture: [project_sketch.png](project_sketch.png) · Full explanation: [00_project_explained.ipynb](00_project_explained.ipynb)

---

## 1. Sun and space

| Term | Simply explained |
|---|---|
| **Solar wind** | Constant stream of charged particles from the Sun. Normally 300–500 km/s, during storms 800+ km/s. |
| **Plasma** | Gas so hot that its atoms break into charged particles. The solar wind is made of it. |
| **Flare** | Bright flash of light on the Sun. The light (incl. X-rays) reaches Earth after ~8 minutes. Classes A, B, C, M, X (X = strongest). |
| **CME** (Coronal Mass Ejection) | A huge plasma cloud thrown out by the Sun. Takes 1–3 days to Earth. Main cause of big storms. |
| **Coronal hole** | Dark area on the Sun that releases fast solar wind. Causes mostly moderate, recurring storms (every ~27 days = one solar rotation). |
| **Solar cycle** | The Sun gets more active and calmer again every ~11 years. Near the maximum there are more storms. |
| **Sunspots** (`sunspot`) | Dark spots on the Sun. Their number shows how active the Sun currently is. |
| **F10.7** (`f107`) | Radio emission of the Sun at 10.7 cm wavelength. A second measure of solar activity. |
| **IMF** (Interplanetary Magnetic Field) | The magnetic field carried along by the solar wind. |
| **L1** (Lagrange point 1) | Point ~1.5 million km in front of Earth towards the Sun. Gravity of Sun and Earth balance so a satellite can travel along. It sees the solar wind 30–90 minutes before it arrives. |
| **DSCOVR, ACE, IMAP** | Satellites at L1 that measure the solar wind. |

## 2. Earth

| Term | Simply explained |
|---|---|
| **Magnetosphere** | Earth's "magnetic bubble" that protects us from the solar wind. |
| **Geomagnetic storm** | The magnetosphere gets shaken hard because a lot of solar wind energy gets in. This is what Kp measures. |
| **Magnetometer** | Instrument that measures strength and direction of a magnetic field. On the ground and on satellites. |
| **Aurora** | Light in the sky when particles hit the atmosphere. The stronger the storm, the further south it is visible. |
| **GIC** (Geomagnetically Induced Currents) | Currents a storm creates in long conductors (power grid, pipelines). Can overheat transformers. |

## 3. Measurements = columns in `omni_all.csv` / the Parquet files

| Column | Meaning | Unit |
|---|---|---|
| `bx_gsm`, `by_gsm`, `bz_gsm` | The three directions of the solar wind magnetic field. **Bz < 0** (pointing south) = the door to Earth opens → storm risk. | nT |
| `b_mag` / `b_sum` | Total strength of the magnetic field. Alex computes `b_sum` himself: √(Bx² + By² + Bz²). | nT |
| `speed` | Speed of the solar wind | km/s |
| `density` | Number of particles per cubic centimetre | n/cm³ |
| `temp` | Temperature of the plasma | Kelvin |
| `pressure` | How hard the solar wind pushes on the magnetosphere | nPa |
| `e_field` | Electric field (≈ speed × Bz). A good single hint for storm strength. | mV/m |
| `timeshift_s` | How long the solar wind took from L1 to Earth. OMNI has already shifted the data by this. | seconds |
| `sym_h` | One-minute version of Dst (see below) | nT |
| `asy_h` | How uneven the disturbance is around Earth | nT |
| `ae`, `al`, `au` | Disturbance near the poles (aurora zone) | nT |
| `pc_n` | Polar cap index north | – |

**Units:** **nT** = nanotesla (magnetic field; Earth's field is ~50,000 nT). **GSM** = coordinate system aligned with Earth's magnetic field, hence `_gsm`.

## 4. Indices (storm numbers)

| Index | Simply explained |
|---|---|
| **K** | Disturbance at **one** station, 0–9, per 3 hours |
| **Kp** (`kp`) | Average of many stations = **planetary** K. 0–9 in thirds (5-, 5o, 5+). **Our target.** Published by GFZ Potsdam. |
| **ap** (`ap`) | Kp converted to a linear scale (0–400). Good for calculating and averaging. |
| **Hp30 / Hp60** | Like Kp, but every 30 or 60 minutes and open-ended (no cap at 9). |
| **Dst** (`dst`) | How much the magnetic field at the equator **drops**. The more negative, the stronger the storm (−100 nT = strong, −400 nT = extreme). Hourly. |
| **G-scale** | NOAA storm classes G1–G5. Kp 5 = G1 … Kp 9 = G5. |
| **R-scale / S-scale** | NOAA classes for radio blackouts from flares (R) and radiation storms (S). Not what our Kp measures. |

## 5. Data

| Term | Simply explained |
|---|---|
| **OMNI** | NASA dataset that merges measurements of several L1 satellites into one time series, shifted to Earth. |
| **OMNI2 / high-res** | OMNI2 = hourly since 1963 (incl. Kp, Dst). High-res = every minute since 1981 (solar wind). |
| **Fill value** | Placeholder for "no measurement", e.g. `9999.99`. Becomes `NaN` when loading. |
| **NaN** | "Not a Number" = missing value |
| **DOY** (`doy`) | Day of year: day 1–366 |
| **CSV** | Text file with comma-separated columns. Simple, but large and slow. |
| **Parquet** | Column-based file format. Much smaller and faster than CSV (`omni_1995.parquet`). |
| **Chunk** | A piece of a big file. Alex reads `omni_all.csv` in chunks of 2 million rows so the RAM is enough. |

## 6. Model

| Term | Simply explained |
|---|---|
| **Feature** | Input column for the model (e.g. `bz_gsm`, `speed`) |
| **Target** | What we want to predict (for us: `kp`) |
| **Feature engineering** | Building new, more useful columns, e.g. `b_sum` or slopes |
| **Slope** | How fast a value is changing right now |
| **Regression** | Predicting a number (Kp = 6.3). Opposite: **classification** = predicting a class (storm yes/no). |
| **Baseline** | Simplest comparison model. The real model has to beat it, otherwise it is useless. |
| **DummyRegressor** | Baseline that always predicts the average |
| **LightGBM** | Fast model made of many small decision trees that improve each other (gradient boosting) |
| **Chronos / PatchTST** | Pretrained models for time series (Alex' new notebooks) |
| **Train / validation / test** | Data to learn from / to tune / for the final check. The model never sees the test data while learning. |
| **R²** | How much of the variation the model explains. 1 = perfect, 0 = as good as the average, < 0 = worse. |
| **MAE** | Mean absolute error: on average this many Kp points off |
| **RMSE** | Like MAE, but punishes big errors more |
| **Imbalanced data** | 90 %+ of the time Kp < 5. Without countermeasures the model mostly learns "calm". |
| **Forecast horizon / lead time** | How far into the future we predict. For us limited by L1 → Earth (30–90 min). |
| **MLflow** | Tool that stores every model run with its settings and results so you can compare them |

## 7. Tools and repo

| Term | Simply explained |
|---|---|
| **uv** | Tool that installs Python and packages. Replaces `pip` + `venv`. |
| **venv / `.venv`** | Separate Python environment for the project. Everyone builds it with `uv sync`. |
| **`pyproject.toml`** | Recipe: which packages the project needs |
| **`uv.lock`** | Shopping list: exact version of every package, so everyone has the same |
| **`.python-version`** | Which Python version (for us 3.14) |
| **dev packages** | Only needed for development (Jupyter, plots), not for the finished dashboard |
| **Kernel** | The Python a notebook runs with. Choose `.venv`. |
| **`.gitignore`** | List of what Git should **not** upload (data, `.venv`, models) |
| **`.gitkeep`** | Empty file so Git keeps an empty folder (`_data/`, `_models/`) |
| **nbdime** | Shows differences in notebooks readably and helps with merge conflicts |
| **Merge conflict** | Two people changed the same spot. Git doesn't know which version is right. |
| **Streamlit** | Python package for simple web dashboards (`Karl/tools/kp_dashboard.py`) |
| **API / JSON** | Interface on the web that delivers data, usually in the text format JSON (e.g. NOAA live data) |
