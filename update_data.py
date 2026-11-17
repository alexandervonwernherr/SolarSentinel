import requests
from pathlib import Path
from datetime import date

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date

BASE = "https://spdf.gsfc.nasa.gov/pub/data/omni"
OUT = Path("omni_raw"); OUT.mkdir(exist_ok=True)

def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print("skip", dest.name); return
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=60) as r:
        if r.status_code == 404:
            print("not found", url); return
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    tmp.rename(dest)
    print("ok  ", dest.name, f"{dest.stat().st_size/1e6:.0f} MB")

# 1) Hourly OMNI2 (contains Kp, Dst, F10.7, sunspot number)
fetch(f"{BASE}/low_res_omni/omni2_all_years.dat", OUT / "omni2_all_years.dat")

# 2) 1-minute OMNI, one file per year
for year in range(1981, date.today().year + 1):
    fetch(f"{BASE}/high_res_omni/omni_min{year}.asc", OUT / f"omni_min{year}.asc")

    RAW = Path("omni_raw")
OUT = Path("omni_all.csv")
TMP = OUT.with_suffix(".csv.part")

def make_time(df):
    return (pd.to_datetime(df["year"].astype(str), format="%Y")
            + pd.to_timedelta(df["doy"] - 1, unit="D")
            + pd.to_timedelta(df["hour"], unit="h")
            + pd.to_timedelta(df.get("minute", 0), unit="m"))

def clean(df, fills):
    for col, fill in fills.items():
        df[col] = df[col].where(~np.isclose(df[col], fill))   # fill value -> NaN
    return df

# ---------- hourly OMNI2: Kp, Dst, F10.7, sunspot number, ap ----------
hcols = {0: "year", 1: "doy", 2: "hour", 38: "kp10", 39: "sunspot",
         40: "dst", 49: "ap", 50: "f107"}
h = pd.read_csv(RAW / "omni2_all_years.dat", sep=r"\s+", header=None,
                usecols=list(hcols)).rename(columns=hcols)
h = clean(h, {"kp10": 99, "sunspot": 999, "dst": 99999, "ap": 999, "f107": 999.9})
h["kp"] = h["kp10"] / 10.0                      # stored as Kp*10 (27 = 2+)
h["time"] = make_time(h)
h = (h[["time", "kp", "sunspot", "dst", "ap", "f107"]]
     .drop_duplicates("time").sort_values("time"))

# ---------- 1-minute OMNI ----------
mcols = {0: "year", 1: "doy", 2: "hour", 3: "minute", 9: "timeshift_s",
         13: "b_mag", 14: "bx_gsm", 17: "by_gsm", 18: "bz_gsm",
         21: "speed", 25: "density", 26: "temp", 27: "pressure",
         28: "e_field", 37: "ae", 38: "al", 39: "au",
         41: "sym_h", 43: "asy_h", 44: "pc_n"}
mfills = {"timeshift_s": 999999, "b_mag": 9999.99, "bx_gsm": 9999.99,
          "by_gsm": 9999.99, "bz_gsm": 9999.99, "speed": 99999.9,
          "density": 999.99, "temp": 9999999., "pressure": 99.99,
          "e_field": 999.99, "ae": 99999, "al": 99999, "au": 99999,
          "sym_h": 99999, "asy_h": 99999, "pc_n": 999.99}

total, first = 0, True
for year in range(1981, date.today().year + 1):
    f = RAW / f"omni_min{year}.asc"
    if not f.exists():
        print("missing", f.name); continue

    df = pd.read_csv(f, sep=r"\s+", header=None, usecols=list(mcols)).rename(columns=mcols)
    df = clean(df, mfills)
    df["time"] = make_time(df)
    df = df.drop(columns=["year", "doy", "hour", "minute"])
    df = df.drop_duplicates("time").sort_values("time")

    df = pd.merge_asof(df, h, on="time", direction="backward",
                       tolerance=pd.Timedelta("1h"))

    df = df[["time"] + [c for c in df.columns if c != "time"]]
    df.to_csv(TMP, mode="w" if first else "a", header=first, index=False,
              float_format="%.5g", date_format="%Y-%m-%d %H:%M")
    first = False
    total += len(df)
    print(year, f"{len(df):,} rows")

TMP.replace(OUT)
print(f"done: {total:,} rows -> {OUT} ({OUT.stat().st_size/1e9:.1f} GB)")