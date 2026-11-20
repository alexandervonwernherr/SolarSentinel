# Kp-Index: die ganze Geschichte

Wie ein Sonnensturm entsteht, wie man ihn misst und wo SolarSentinel ansetzt.
Die Code-Zellen 3–9 in `01_start.ipynb` zeigen jeden Schritt mit Live-Daten.

---

## 1. Die Kette von der Sonne bis zur Zahl

```
 Sonne          Sonnenwind / CME        L1-Punkt              Erde                  Messung
 ─────          ────────────────        ────────              ────                  ───────
 Ausbruch  ──►  geladene Teilchen  ──►  Satellit misst   ──►  Magnetfeld wird  ──►  Magnetometer
                + Magnetfeld            Bz + Tempo            gestört               → K → Kp → G-Klasse
                1–3 Tage unterwegs      ~1,5 Mio km vor       30–90 min später
                                        der Erde
```

| Schritt | Was passiert | Notebook |
|---|---|---|
| 1. Sonne | Eine Eruption (CME) oder ein schneller Sonnenwind-Strom schleudert geladene Teilchen ins All. | – |
| 2. L1 | Satelliten (DSCOVR, ACE, IMAP) sitzen zwischen Sonne und Erde und messen den Sonnenwind, **bevor** er ankommt. | Zelle 9 |
| 3. Bz | Zeigt das Magnetfeld des Sonnenwinds nach Süden (**Bz < 0**), koppelt es an das Erdmagnetfeld an und Energie strömt hinein. Bei Bz > 0 prallt das meiste ab. | Zelle 9, oberer Plot |
| 4. Erde | Das Erdmagnetfeld schwankt. Magnetometer am Boden messen das. | – |
| 5. Kp | Die Schwankung wird zu einer Zahl von 0 bis 9 zusammengefasst. | Zellen 5–8 |

---

## 2. Wie der Kp-Index gemessen wird

1. **~13 Magnetometer-Stationen** weltweit (mittlere Breiten, nicht am Pol).
2. Jede Station nimmt ein **3-Stunden-Fenster** und sucht die grösste Schwankung des horizontalen Magnetfelds.
3. Der normale Tagesgang (das Feld schwankt auch ohne Sturm ein bisschen) wird abgezogen.
4. Das Ergebnis wird auf eine Skala von **0–9** übersetzt → der **K-Wert** der Station.
5. Alle Stationen werden normiert und gemittelt → **Kp** („p" = planetar).

**Wichtig:**
- Die Skala ist **grob logarithmisch**. Kp 8 ist nicht doppelt so stark wie Kp 4, sondern um ein Vielfaches stärker.
- Kp kommt in **Dritteln**: `5-` = 4,67 · `5o` = 5,00 · `5+` = 5,33.
- Offizieller Herausgeber ist das **GFZ Potsdam**. NOAA (USA) veröffentlicht eine eigene schnelle Version.

---

## 3. Von Kp zur Sturmklasse (G-Skala)

Die NOAA übersetzt Kp in Sturmklassen. Zelle 4 zeigt die Tabelle, Zelle 6 zählt sie für heute.

| Kp | Klasse | Bedeutung |
|---|---|---|
| 0–4 | G0 | kein Sturm |
| 5 | G1 | schwach – Polarlichter im Norden, kleine Stromnetz-Schwankungen |
| 6 | G2 | mässig |
| 7 | G3 | stark – GPS-Fehler, Satelliten-Probleme |
| 8 | G4 | schwer |
| 9 | G5 | extrem – Stromnetz-Ausfälle möglich (z.B. Québec 1989) |

Offene Frage: Zählt `5-` (4,67) schon als G1? Im Notebook zählt es als G0. Vor dem Modell klären.

---

## 4. Ist Kp wirklich auf 3 Stunden begrenzt?

Nur der **offizielle** Kp. Es gibt feinere Varianten:

| Index | Auflösung | Quelle | Notebook |
|---|---|---|---|
| Kp (offiziell) | 3 Stunden | GFZ / NOAA | Zelle 5 |
| geschätzter Kp | 1 Minute | NOAA SWPC | Zelle 7 |
| Hp30 | 30 Minuten, nach oben offen | GFZ | Zelle 8 |
| Hp60 | 60 Minuten, nach oben offen | GFZ | – |

In **Zelle 7** sieht man, wie der Minutenwert innerhalb eines 3-Stunden-Fensters hin- und herspringt, während der offizielle Kp eine flache Stufe bleibt.
In **Zelle 8** sieht man, was Hp30 zeigt und der 3-Stunden-Kp glättet.

→ Die Aussage „Vorhersagen gibt es nur alle 3 Stunden" aus dem Meeting stimmt so nicht ganz. Feine Daten gibt es schon.

---

## 5. Kann man Kp vorhersagen?

Ja, es gibt zwei Zeithorizonte:

| Horizont | Grundlage | Genauigkeit |
|---|---|---|
| **30–90 Minuten** | Sonnenwind-Messung am L1-Punkt (Bz, Tempo, Dichte) | gut |
| **1–3 Tage** | Beobachtete Eruptionen auf der Sonne (CMEs) | grob |

Die Vorwarnzeit hängt vom **Tempo des Sonnenwinds** ab:

```
Vorwarnzeit = 1.500.000 km / Tempo
  300 km/s  → ~83 min   (ruhiger Sonnenwind)
  800 km/s  → ~31 min   (schneller CME)
```

Zelle 9 rechnet das live aus. Bei einem starken Sturm wird die Vorwarnzeit also **kürzer** – genau dann, wenn man sie am meisten braucht.

---

## 6. Was das für SolarSentinel heisst

- Die echte Grenze ist **die Laufzeit des Sonnenwinds von L1 zur Erde**, nicht die 3 Stunden des Kp.
- Ein sinnvolles Modell:
  - **Eingabe:** Sonnenwind-Minutendaten von L1 (Bz, Tempo, Dichte)
  - **Ziel:** Hp30 oder Kp für die nächsten 30–60 Minuten
- **Hp30 als Ziel** lohnt sich: feiner aufgelöst als Kp und nicht bei 9 gedeckelt.
- **Historische Daten:** Kp gibt es ab 1932, Sonnenwind-Daten (OMNI-Datensatz) ab etwa 1963. Das passt zu den „60 Jahren" aus dem Meeting.
- **Filtern auf Stürme** (Alex' Aufgabe) ist sinnvoll, weil 90 %+ der Zeit Kp < 5 ist. Ohne Filter lernt das Modell vor allem „ruhig".

---

## 7. Begriffe

| Begriff | Einfach erklärt |
|---|---|
| **CME** | Koronaler Massenauswurf – eine riesige Wolke aus Sonnenplasma |
| **Sonnenwind** | Ständiger Teilchenstrom von der Sonne, normal 300–500 km/s |
| **L1** | Lagrange-Punkt 1: Ort zwischen Sonne und Erde, an dem ein Satellit stabil „parken" kann |
| **Bz** | Nord-Süd-Komponente des Sonnenwind-Magnetfelds. Negativ = gefährlich |
| **GSM** | Koordinatensystem, das sich am Erdmagnetfeld ausrichtet (deshalb `bz_gsm`) |
| **Magnetometer** | Messgerät für die Stärke und Richtung des Magnetfelds |
| **nT** | Nanotesla, Einheit für Magnetfeldstärke |

---

## 8. Datenquellen im Notebook

| Daten | URL |
|---|---|
| Kp 3-stündlich | `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json` |
| Kp geschätzt, 1 min | `https://services.swpc.noaa.gov/json/planetary_k_index_1m.json` |
| Hp30 | `https://kp.gfz.de/app/json/?start=…&end=…&index=Hp30` |
| Sonnenwind Magnetfeld | `https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json` |
| Sonnenwind Plasma | `https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json` |

Alle frei, ohne API-Key. Stand 2026-11-17 erreichbar.

> Hinweis: Die physikalischen Erklärungen stammen aus allgemeinem Fachwissen und sind nicht gegen eine Quelle geprüft. Vor der Präsentation bei GFZ (kp.gfz.de) und NOAA SWPC (swpc.noaa.gov) gegenchecken – vor allem die Zahlen zu Stationen, OMNI-Startjahr und der G1-Grenze.
