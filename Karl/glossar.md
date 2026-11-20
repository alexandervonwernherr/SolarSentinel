# Glossar SolarSentinel

Alle Fachwörter aus dem Projekt, einfach erklärt. Stand 2026-11-19.
Zusammenhang als Bild: [sonnensturm_skizze.md](sonnensturm_skizze.md) · Kp im Detail: [kp_index_erklaert.md](kp_index_erklaert.md)

---

## 1. Sonne und Weltraum

| Begriff | Einfach erklärt |
|---|---|
| **Sonnenwind** | Ständiger Strom geladener Teilchen von der Sonne. Normal 300–500 km/s, bei Stürmen 800+ km/s. |
| **Plasma** | Gas, das so heiß ist, dass die Atome in geladene Teilchen zerfallen. Daraus besteht der Sonnenwind. |
| **Flare (Sonneneruption)** | Heller Lichtblitz auf der Sonne. Das Licht (auch Röntgen) ist nach ~8 Minuten an der Erde. Klassen A, B, C, M, X (X = am stärksten). |
| **CME** (Coronal Mass Ejection) | Koronaler Massenauswurf: eine riesige Plasmawolke, die die Sonne wegschleudert. Braucht 1–3 Tage zur Erde. Hauptursache großer Stürme. |
| **Koronales Loch** | Dunkle Stelle auf der Sonne, aus der schneller Sonnenwind strömt. Macht eher mittlere, wiederkehrende Stürme (alle ~27 Tage, eine Sonnenumdrehung). |
| **Sonnenzyklus** | Die Sonne wird alle ~11 Jahre aktiver und wieder ruhiger. Im Maximum gibt es mehr Stürme. |
| **Sonnenflecken** (`sunspot`) | Dunkle Flecken auf der Sonne. Ihre Anzahl zeigt, wie aktiv die Sonne gerade ist. |
| **F10.7** (`f107`) | Radiostrahlung der Sonne bei 10,7 cm Wellenlänge. Zweites Maß für die Sonnenaktivität. |
| **IMF** (Interplanetary Magnetic Field) | Das Magnetfeld, das der Sonnenwind mitschleppt. |
| **L1** (Lagrange-Punkt 1) | Punkt ~1,5 Mio km vor der Erde Richtung Sonne. Dort heben sich die Anziehung von Sonne und Erde so auf, dass ein Satellit mitfliegen kann. Er sieht den Sonnenwind 30–90 Minuten, bevor er ankommt. |
| **DSCOVR, ACE, IMAP** | Satelliten am L1-Punkt, die den Sonnenwind messen. |

## 2. Erde

| Begriff | Einfach erklärt |
|---|---|
| **Magnetosphäre** | Die "Magnetblase" der Erde, die uns vor dem Sonnenwind schützt. |
| **Geomagnetischer Sturm** | Die Magnetosphäre wird stark durchgeschüttelt, weil viel Sonnenwind-Energie hineinkommt. Das misst der Kp. |
| **Magnetometer** | Messgerät für Stärke und Richtung eines Magnetfelds. Am Boden und auf den Satelliten. |
| **Polarlicht** | Leuchten am Himmel, wenn Teilchen in die Atmosphäre krachen. Je stärker der Sturm, desto weiter südlich sichtbar. |
| **GIC** (Geomagnetically Induced Currents) | Ströme, die ein Sturm in langen Leitungen (Stromnetz, Pipelines) erzeugt. Können Transformatoren überhitzen. |

## 3. Messgrößen = Spalten in `omni_all.csv`

| Spalte | Bedeutung | Einheit |
|---|---|---|
| `bx_gsm`, `by_gsm`, `bz_gsm` | Die drei Richtungen des Sonnenwind-Magnetfelds. **Bz < 0** (zeigt nach Süden) = die Tür zur Erde geht auf → Sturmgefahr. | nT |
| `b_mag` / `b_sum` | Gesamtstärke des Magnetfelds. `b_sum` rechnet Alex selbst: √(Bx² + By² + Bz²). | nT |
| `speed` | Tempo des Sonnenwinds | km/s |
| `density` | Wie viele Teilchen pro Kubikzentimeter | n/cm³ |
| `temp` | Temperatur des Plasmas | Kelvin |
| `pressure` | Druck, mit dem der Sonnenwind auf die Magnetosphäre drückt | nPa |
| `e_field` | Elektrisches Feld (≈ Tempo × Bz). Guter Einzel-Hinweis auf Sturmstärke. | mV/m |
| `timeshift_s` | Wie lange der Sonnenwind von L1 zur Erde gebraucht hat. OMNI hat die Daten schon darauf verschoben. | Sekunden |
| `sym_h` | Minuten-Version des Dst (siehe unten) | nT |
| `asy_h` | Wie ungleich die Störung rund um die Erde ist | nT |
| `ae`, `al`, `au` | Störung in der Nähe der Pole (Polarlicht-Zone) | nT |
| `pc_n` | Polarkappen-Index Nord | – |

**Einheiten:** **nT** = Nanotesla (Magnetfeld; das Erdfeld hat ~50.000 nT). **GSM** = Koordinatensystem, das sich am Erdmagnetfeld ausrichtet, deshalb `_gsm`.

## 4. Indizes (Sturm-Zahlen)

| Index | Einfach erklärt |
|---|---|
| **K** | Störung an **einer** Messstation, 0–9, pro 3 Stunden |
| **Kp** (`kp`) | Mittelwert vieler Stationen = **planetarer** K. 0–9 in Dritteln (5-, 5o, 5+). **Unser Ziel.** Herausgeber: GFZ Potsdam. |
| **ap** (`ap`) | Kp in eine lineare Skala umgerechnet (0–400). Gut zum Rechnen und Mitteln. |
| **Hp30 / Hp60** | Wie Kp, aber alle 30 bzw. 60 Minuten und nach oben offen (kein Deckel bei 9). |
| **Dst** (`dst`) | Wie stark das Magnetfeld am Äquator **sinkt**. Je negativer, desto stärker der Sturm (−100 nT = stark, −400 nT = extrem). Stündlich. |
| **G-Skala** | NOAA-Sturmklassen G1–G5. Kp 5 = G1 … Kp 9 = G5. |
| **R-Skala / S-Skala** | NOAA-Klassen für Funkstörungen durch Flares (R) und Strahlungsstürme (S). Andere Baustelle als unser Kp. |

## 5. Daten

| Begriff | Einfach erklärt |
|---|---|
| **OMNI** | NASA-Datensatz, der Messungen mehrerer L1-Satelliten zu einer Zeitreihe zusammenfügt und auf die Erde verschiebt. |
| **OMNI2 / high-res** | OMNI2 = stündlich ab 1963 (mit Kp, Dst). High-res = minütlich ab 1981 (Sonnenwind). |
| **Füllwert** | Platzhalter für "keine Messung", z. B. `9999.99`. Wird beim Laden zu `NaN`. |
| **NaN** | "Not a Number" = fehlender Wert |
| **DOY** (`doy`) | Day of Year: Tag 1–366 im Jahr |
| **CSV** | Textdatei mit Komma-getrennten Spalten. Einfach, aber groß und langsam. |
| **Parquet** | Spaltenbasiertes Dateiformat. Viel kleiner und schneller als CSV (`omni_1995.parquet`). |
| **Chunk** | Ein Stück einer großen Datei. Alex liest `omni_all.csv` in Stücken à 2 Mio Zeilen, damit der RAM reicht. |

## 6. Modell

| Begriff | Einfach erklärt |
|---|---|
| **Feature** | Eingabe-Spalte für das Modell (z. B. `bz_gsm`, `speed`) |
| **Target / Zielgröße** | Was vorhergesagt werden soll (bei uns `kp`) |
| **Feature Engineering** | Neue, nützlichere Spalten bauen, z. B. `b_sum` oder Steigungen ("Slopes") |
| **Slope** | Steigung: wie schnell sich ein Wert gerade ändert |
| **Regression** | Vorhersage einer Zahl (Kp = 6,3). Gegenteil: **Klassifikation** = Vorhersage einer Klasse (Sturm ja/nein). |
| **Baseline** | Einfachstes Vergleichsmodell. Das echte Modell muss besser sein, sonst taugt es nichts. |
| **DummyRegressor** | Baseline, die immer den Durchschnitt vorhersagt |
| **LightGBM** | Schnelles Modell aus vielen kleinen Entscheidungsbäumen, die sich gegenseitig verbessern (Gradient Boosting) |
| **Train / Validation / Test** | Daten zum Lernen / zum Einstellen / zur Endprüfung. Test-Daten sieht das Modell nie beim Lernen. |
| **R²** | Wie viel der Schwankung das Modell erklärt. 1 = perfekt, 0 = so gut wie der Durchschnitt, < 0 = schlechter. |
| **MAE** | Mittlerer absoluter Fehler: im Schnitt so viele Kp-Punkte daneben |
| **RMSE** | Wie MAE, bestraft große Fehler aber stärker |
| **Unausgewogene Daten** | 90 %+ der Zeit ist Kp < 5. Ohne Gegenmaßnahme lernt das Modell vor allem "ruhig". |
| **Vorhersagehorizont / Lead Time** | Wie weit in die Zukunft vorhergesagt wird. Bei uns begrenzt durch L1 → Erde (30–90 min). |
| **MLflow** | Werkzeug, das jeden Modell-Lauf mit Einstellungen und Ergebnissen speichert, damit man vergleichen kann |

## 7. Werkzeuge und Repo

| Begriff | Einfach erklärt |
|---|---|
| **uv** | Werkzeug, das Python und Pakete installiert. Ersetzt `pip` + `venv`. |
| **venv / `.venv`** | Eigene, abgeschottete Python-Umgebung fürs Projekt. Jeder baut sie selbst mit `uv sync`. |
| **`pyproject.toml`** | Rezept: welche Pakete das Projekt braucht |
| **`uv.lock`** | Einkaufszettel: exakte Version jedes Pakets, damit alle dasselbe haben |
| **`.python-version`** | Welche Python-Version (bei uns 3.14) |
| **dev-Pakete** | Nur fürs Entwickeln nötig (Jupyter, Plots), nicht fürs fertige Dashboard |
| **Kernel** | Das Python, mit dem ein Notebook läuft. Bei uns `.venv` auswählen. |
| **`.gitignore`** | Liste, was Git **nicht** hochladen soll (Daten, `.venv`, Modelle) |
| **`.gitkeep`** | Leere Datei, damit Git einen leeren Ordner (`_data/`, `_models/`) mitnimmt |
| **nbdime** | Zeigt Unterschiede in Notebooks lesbar an und hilft bei Merge-Konflikten |
| **Merge-Konflikt** | Zwei Leute haben dieselbe Stelle geändert. Git weiß nicht, welche Version gilt. |
| **Streamlit** | Python-Paket für einfache Web-Dashboards (geplant für die Live-Anzeige) |
| **API / JSON** | Schnittstelle im Netz, die Daten liefert, meist im Textformat JSON (z. B. NOAA-Live-Daten) |
