"""Converts the raw OMNI files per year in _data/<year>/ into one Parquet file.

Same columns and cleaning as update_data.py, same Parquet format as Alex
in SolarSentinel.ipynb (index = time, float32, zstd, empty future rows cut off).

Run from the repo root:  uv run python Karl/tools/omni_year_to_parquet.py 1989 2003 2022 2024
Result:                  _data/<year>/omni_<year>.parquet
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("_data")

# shortcut: columns + fill values copied from update_data.py (that script downloads on import);
#           import them from there once update_data.py has functions.
HCOLS = {0: "year", 1: "doy", 2: "hour", 38: "kp10", 39: "sunspot",
         40: "dst", 49: "ap", 50: "f107"}
HFILLS = {"kp10": 99, "sunspot": 999, "dst": 99999, "ap": 999, "f107": 999.9}
MCOLS = {0: "year", 1: "doy", 2: "hour", 3: "minute", 9: "timeshift_s",
         13: "b_mag", 14: "bx_gsm", 17: "by_gsm", 18: "bz_gsm",
         21: "speed", 25: "density", 26: "temp", 27: "pressure",
         28: "e_field", 37: "ae", 38: "al", 39: "au",
         41: "sym_h", 43: "asy_h", 44: "pc_n"}
MFILLS = {"timeshift_s": 999999, "b_mag": 9999.99, "bx_gsm": 9999.99,
          "by_gsm": 9999.99, "bz_gsm": 9999.99, "speed": 99999.9,
          "density": 999.99, "temp": 9999999., "pressure": 99.99,
          "e_field": 999.99, "ae": 99999, "al": 99999, "au": 99999,
          "sym_h": 99999, "asy_h": 99999, "pc_n": 999.99}


def make_time(df):
    return (pd.to_datetime(df["year"].astype(str), format="%Y")
            + pd.to_timedelta(df["doy"] - 1, unit="D")
            + pd.to_timedelta(df["hour"], unit="h")
            + pd.to_timedelta(df.get("minute", 0), unit="m"))


def clean(df, fills):
    for col, fill in fills.items():
        df[col] = df[col].where(~np.isclose(df[col], fill))  # fill value -> NaN
    return df


def read(path, cols, fills):
    df = pd.read_csv(path, sep=r"\s+", header=None, usecols=list(cols)).rename(columns=cols)
    df = clean(df, fills)
    df["time"] = make_time(df)
    return df.drop_duplicates("time").sort_values("time")


def convert(year):
    folder = DATA / str(year)
    h = read(folder / f"omni2_{year}.dat", HCOLS, HFILLS)
    h["kp"] = h["kp10"] / 10.0  # stored as Kp*10 (27 = 2+)
    h = h[["time", "kp", "sunspot", "dst", "ap", "f107"]]

    m = read(folder / f"omni_min{year}.asc", MCOLS, MFILLS)
    m = m.drop(columns=["year", "doy", "hour", "minute"])

    df = pd.merge_asof(m, h, on="time", direction="backward", tolerance=pd.Timedelta("1h"))
    df = df.set_index("time")
    df = df.loc[:df["bz_gsm"].last_valid_index()]  # like Alex: drop empty future rows
    df = df.astype("float32")

    assert df.index.is_monotonic_increasing and not df.index.duplicated().any()
    assert (df.index.year == year).all() and df["kp"].notna().any()

    out = folder / f"omni_{year}.parquet"
    df.to_parquet(out, compression="zstd")
    print(year, df.shape, f"{out.stat().st_size / 1e6:.0f} MB", "max Kp", df["kp"].max())


if __name__ == "__main__":
    for y in sys.argv[1:]:
        convert(int(y))
