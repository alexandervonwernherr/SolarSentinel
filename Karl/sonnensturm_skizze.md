# Sonnensturm: von der Sonne bis zum Stromausfall

Skizze der ganzen Kette. Wie Kp gemessen wird, steht in [kp_index_erklaert.md](kp_index_erklaert.md). Das wird hier nicht wiederholt.

> **Kurz richtiggestellt:** Es geht nicht um Lichtjahre. Ein Lichtjahr sind ca. 9,5 Billionen km.
> Die Sonne ist nur ca. **150 Mio km** weg. Licht braucht dafür **ca. 8 Minuten**.
> Ein Sonnensturm braucht **Stunden bis Tage**, nicht Jahre.

---

## 1. Die Kette

```
 SONNE                                                                    ERDE
   |                                                                        |
   |<------------------------- ca. 150 Mio km ---------------------------->|
   |                                                    |<- 1,5 Mio km ->|
   |                                                    L1                  |
   |                                                                        |
[1] AUSBRUCH                                                                |
    a) Flare (Lichtblitz, Röntgen) ========== Licht: ca. 8 min =========>  [R] Funkstörung
    b) CME (Plasmawolke)        ----- typisch 1-3 Tage, Rekord ca. 15-20 h ---->
    c) schneller Sonnenwind aus koronalem Loch ---- ca. 2-4 Tage --------->
         |
         v
[2] REISE DURCHS ALL: Teilchen + eingebautes Magnetfeld (300-800 km/s, Sturm >1000)
         |
         v
[3] MESSUNG AM L1  (DSCOVR, ACE, neu: IMAP, SWFO-L1)
    misst: bz_gsm, speed, density, pressure
         |
         |   ######## HIER SETZT SOLARSENTINEL AN ########
         |   Vorwarnzeit L1 -> Erde: ca. 30-90 min
         |   (1,5 Mio km / Tempo; schneller Sturm = kürzere Warnung)
         |   ##############################################
         v
[4] ANKUNFT AN DER ERDE: trifft die Magnetosphäre
    Bz < 0 (Süd)  -> Felder koppeln, Energie strömt rein  -> STURM
    Bz > 0 (Nord) -> das meiste prallt ab                  -> ruhig
         |
         v
[5] MESSUNG AM BODEN: Magnetometer -> K (pro Station) -> Kp (0-9) -> G-Skala
    sichtbar auch in sym_h, dst (Ring-Strom) und ae (Polarlicht-Zone)
         |
         v
[6] FOLGEN: Stromnetz, Satelliten, GPS, Funk, Pipelines, Polarlichter
```

**Warum Bz < 0 der Schlüssel ist:** Das Erdmagnetfeld zeigt an der Tagseite nach Norden.
Zeigt das Feld des Sonnenwinds nach Süden, verbinden sich beide Felder wie zwei Magnete.
Dann fließt Energie in die Magnetosphäre. Ein schneller Sturm mit Bz > 0 bleibt oft harmlos.
Ein mittlerer Sturm mit lange stark negativem Bz kann heftig werden.

**Was SolarSentinel macht:** Der offizielle Kp kommt nur alle 3 Stunden. Die L1-Daten kommen jede Minute.
Das Modell nutzt die 30–90 Minuten zwischen L1-Messung und Wirkung an der Erde.

---

## 2. Drei verschiedene Arten von "Sonnensturm"

| Skala | Was | Ursache | Ankunft | Hauptfolge |
|---|---|---|---|---|
| **R** (Radio Blackout) | Flare | Röntgen- und UV-Licht | ca. 8 min | Kurzwellenfunk fällt auf der Tagseite aus |
| **S** (Solar Radiation Storm) | Strahlungssturm | sehr schnelle Protonen | ca. 10 min bis Stunden | Strahlung für Astronauten, Polarflüge, Satelliten-Elektronik |
| **G** (Geomagnetic Storm) | geomagnetischer Sturm | CME / schneller Sonnenwind | 1–3 Tage | Stromnetz, GPS, Satelliten, Polarlicht |

**SolarSentinel sagt nur die G-Skala voraus. Das ist unser Kp.**
Ein starker Flare heißt nicht automatisch ein starker G-Sturm. Entscheidend ist, ob eine CME die Erde trifft und wie Bz steht.

---

## 3. Kp → G-Klasse (NOAA Space Weather Scale)

| Kp | G | Name | Häufigkeit pro Sonnenzyklus (ca. 11 Jahre) | Folgen (Auswahl) | Polarlicht bis ca. |
|---|---|---|---|---|---|
| 5 | G1 | minor | 1.700× (ca. 900 Tage) | leichte Netzschwankungen | hoher Norden (Skandinavien) |
| 6 | G2 | moderate | 600× (ca. 360 Tage) | Spannungsalarme im Norden, Bahnvorhersagen ungenauer | ca. 55° geomagn. Breite |
| 7 | G3 | strong | 200× (ca. 130 Tage) | Spannungskorrekturen, Satelliten laden sich auf, mehr Luftwiderstand, GPS zeitweise gestört | ca. 50° |
| 8 (inkl. 9-) | **G4** | **severe** | **100× (ca. 60 Tage)** | siehe unten | ca. 45° |
| 9 | **G5** | **extreme** | **4× (ca. 4 Tage)** | siehe unten | ca. 40° |

Quelle: NOAA SWPC, Space Weather Scales. Die Breitengrade sind **geomagnetisch**. Europa liegt geomagnetisch etwas südlicher als geografisch. Deshalb sieht man Polarlicht in Deutschland meist erst ab ca. Kp 7–8.

### Kp 8 – G4 "severe"

- **Stromnetz:** weit verbreitete Spannungsprobleme möglich. Schutzsysteme können wichtige Anlagen fälschlich abschalten.
- **Satelliten:** Oberflächen laden sich auf. Bahnverfolgung wird schwierig. Lage muss nachkorrigiert werden.
- **GPS/GNSS:** Satellitennavigation stundenlang ungenau.
- **Kurzwellenfunk:** immer wieder gestört.
- **Pipelines:** induzierte Ströme, Gegenmaßnahmen nötig (Korrosionsschutz).

### Kp 9 – G5 "extreme"

- **Stromnetz:** Spannungsprobleme überall. Teile des Netzes können zusammenbrechen. **Transformatoren können beschädigt werden.**
  Warum? Das schwankende Erdfeld erzeugt Ströme in langen Leitungen (GIC = geomagnetisch induzierte Ströme).
  Die fließen als Gleichstrom durch die Trafos. Die Trafos werden heiß und brummen.
- **Satelliten:** starke Aufladung, Probleme bei Funkverbindung und Lage.
  Die Hochatmosphäre heizt sich auf und dehnt sich aus. Satelliten in niedriger Bahn werden gebremst und sinken.
- **GPS/GNSS:** Navigation **tagelang** ungenau (wichtig z. B. für Präzisions-Landwirtschaft, Vermessung).
- **Kurzwellenfunk:** in vielen Gebieten **1–2 Tage** unmöglich (Flugfunk über den Ozeanen).
- **Pipelines:** Ströme von **hunderten Ampere**.
- **Polarlicht:** bis ca. 40° geomagnetisch. Ganz Deutschland, sogar Südeuropa.

---

## 4. Echte Stürme

| Sturm | Stärke | Was passierte |
|---|---|---|
| **Carrington, Sept. 1859** | stärkster bekannter Sturm | CME brauchte nur ca. 17,6 h zur Erde (Tsurutani et al. 2003). Telegrafen sprühten Funken. Polarlicht bis in die Karibik. |
| **Québec, 13. März 1989** | Kp 9 | Netz von Hydro-Québec brach in unter 1 Minute zusammen. Ca. 6 Mio Menschen über 9 Stunden ohne Strom. |
| **Halloween, Okt. 2003** | G5 | Stromausfall in Malmö (Schweden, ca. 50.000 Kunden, ca. 1 h). Trafoschäden in Südafrika. Viele Satelliten gestört. |
| **Starlink, Feb. 2022** | nur G1–G2 | 38 frisch gestartete Starlink-Satelliten verglühten. Sie flogen noch sehr tief (ca. 210 km) und wurden vom stärkeren Luftwiderstand gebremst. |
| **Gannon-Sturm, 10.–11. Mai 2024** | **G5, Kp 9** (im Projekt-Notebook) | Erster G5 seit 2003. Mehrere CMEs hintereinander. Polarlicht in ganz Deutschland und bis Südeuropa. Fast die Hälfte aller aktiven Satelliten in niedriger Bahn musste gleichzeitig ausweichen (Parker & Linares 2024). Kein großer Stromausfall: Netzbetreiber waren vorgewarnt. |

**Lehre aus 2022:** Schon ein kleiner Sturm kann teuer werden, wenn man ihn nicht einplant.
**Lehre aus 2024:** Vorwarnung wirkt. Genau dafür ist eine gute Kp-Vorhersage da.

---

## 5. Quellen

- NOAA SWPC – Space Weather Scales (G/R/S, Häufigkeiten, Folgen): https://www.swpc.noaa.gov/noaa-scales-explanation
- GFZ Potsdam – Kp-Index: https://kp.gfz.de
- NASA – Space Weather / Sonnenstürme: https://science.nasa.gov/heliophysics/focus-areas/space-weather/
- USGS – Space Weather Events of May 10, 2024: https://www.usgs.gov/programs/geomagnetism/science/may-10-2024-magnetic-disturbance
- Hydro-Québec – Tempête de mars 1989: https://www.hydroquebec.com/learning/notions-de-base/tempete-mars-1989.html
- Parker & Linares (2024), Satellite drag analysis during the May 2024 storm: https://arxiv.org/abs/2406.08617
- Tsurutani et al. (2003), The extreme magnetic storm of 1–2 September 1859, JGR 108(A7)

> Nicht gegengeprüft (aus Fachwissen, mit "ca." markiert): Laufzeit schneller Sonnenwind 2–4 Tage,
> Carrington 17,6 h, Malmö 2003 (50.000 Kunden, 1 h), Starlink-Bahnhöhe 210 km, Kp-Schwelle für Polarlicht in Deutschland.
