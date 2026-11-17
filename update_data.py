import time

import numpy as np
import pandas as pd
import pyspedas

try:
    from tqdm import tqdm
except ImportError:  # progress bar is optional
    tqdm = None

KP_EVENTS_FILE = "kp_events.csv"

# Inclusive range: 01.01.1970 .. 27.06.2019 (whole days)
START = pd.Timestamp("1970-01-01")
END = pd.Timestamp("2019-06-27")

# DSCOVR launched 2015-02-11; earlier days can only be NaN stubs, so skip the download.
DSCOVR_FIRST_DAY = pd.Timestamp("2015-02-11")

# Without tqdm: print a status line every N days
FALLBACK_PRINT_EVERY = 50


def log(msg):
    """Print without breaking the tqdm progress bar."""
    if tqdm is not None:
        tqdm.write(msg)
    else:
        print(msg)


def fmt_duration(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


def main():
    print("Updating NOAA Kp index, OMNI and DSCOVR data files...")
    noaa_update()


def tplot_to_frame(names):
    """Convert pyspedas tplot variable names into one time-indexed DataFrame (or None)."""
    parts = []
    for name in names or []:
        d = pyspedas.get_data(name)
        if d is None:
            continue
        idx = pd.to_datetime(d.times, unit="s")
        y = np.asarray(d.y)
        if y.ndim == 1:
            part = pd.Series(y, index=idx, name=name)
        else:
            y2 = y.reshape(len(y), -1)
            suffixes = ["x", "y", "z"] if y2.shape[1] == 3 else range(y2.shape[1])
            part = pd.DataFrame(y2, index=idx, columns=[f"{name}_{s}" for s in suffixes])
        part = part[~part.index.duplicated(keep="first")]
        parts.append(part)
    if not parts:
        return None
    return pd.concat(parts, axis=1)


def safe_load(label, day, loader, **kwargs):
    """Run a pyspedas loader for one day. Returns a DataFrame, or None if unavailable."""
    try:
        names = loader(**kwargs)
        return tplot_to_frame(names)
    except Exception as e:
        log(f"  {label}: no data for {day.date()} ({e})")
        return None
    finally:
        try:
            pyspedas.del_data("*")  # avoid stale variables leaking into the next day
        except Exception:
            pass


def nan_stub(day):
    """One all-NaN row at the start of the day; becomes NaN in every column after concat."""
    return pd.DataFrame(index=pd.DatetimeIndex([day]))


def has_data(df):
    return df is not None and not df.empty


def noaa_update():
    """
    Read the list of Kp events, take every distinct day between 1970-01-01 and
    2019-06-27 (inclusive) exactly once, and download Kp, OMNI and DSCOVR data
    for each day. Missing datasets are stubbed with NaN. Results are saved to
    kp_data.csv, omni_data.csv and dscovr_data.csv.
    """
    kp_events = pd.read_csv(KP_EVENTS_FILE)
    dates = pd.to_datetime(kp_events["date_utc"], errors="coerce", utc=True)
    n_total_events = len(dates)
    n_bad = int(dates.isna().sum())
    dates = dates.dropna()

    # Reduce to calendar days (tz-naive UTC), filter the range, one entry per day.
    days = dates.dt.tz_convert("UTC").dt.tz_localize(None).dt.normalize()
    n_in_range = int(((days >= START) & (days <= END)).sum())
    days = days[(days >= START) & (days <= END)].drop_duplicates().sort_values()
    total = len(days)

    print(f"Read {n_total_events} events ({n_bad} unparseable dates dropped).")
    print(f"{n_in_range} events in {START.date()}..{END.date()} -> {total} unique days to process.")
    if total == 0:
        print("Nothing to do.")
        return

    kp_frames, omni_frames, dscovr_frames = [], [], []
    got = {"Kp": 0, "OMNI": 0, "DSCOVR": 0}  # days with real (non-stub) data

    t0 = time.time()
    iterator = tqdm(days, total=total, unit="day", desc="Downloading") if tqdm else days

    for i, day in enumerate(iterator, start=1):
        day_str = day.strftime("%Y-%m-%d")
        trange = [f"{day_str}/00:00:00", f"{day_str}/23:59:59"]
        if tqdm is not None:
            iterator.set_description(f"Downloading {day_str}")

        # --- Kp -------------------------------------------------------------
        kp = safe_load("Kp", day, pyspedas.projects.noaa.noaa_load_kp,
                       trange=trange, time_clip=True)
        if has_data(kp):
            got["Kp"] += 1
            kp_frames.append(kp)
        else:
            kp_frames.append(nan_stub(day))

        # --- OMNI -----------------------------------------------------------
        omni = safe_load("OMNI", day, pyspedas.projects.omni.data,
                         trange=trange, datatype="1min", time_clip=True)
        if has_data(omni):
            got["OMNI"] += 1
            omni_frames.append(omni)
        else:
            omni_frames.append(nan_stub(day))

        # --- DSCOVR (mag + faraday cup) --------------------------------------
        parts = []
        if day >= DSCOVR_FIRST_DAY:
            for label, loader in (("DSCOVR mag", pyspedas.projects.dscovr.mag),
                                  ("DSCOVR fc", pyspedas.projects.dscovr.fc)):
                df = safe_load(label, day, loader, trange=trange, time_clip=True)
                if has_data(df):
                    parts.append(df)
        if parts:
            got["DSCOVR"] += 1
            dscovr_frames.append(pd.concat(parts, axis=1).resample("1min").mean())
        else:
            dscovr_frames.append(nan_stub(day))

        # --- progress ---------------------------------------------------------
        if tqdm is not None:
            iterator.set_postfix(Kp=got["Kp"], OMNI=got["OMNI"], DSCOVR=got["DSCOVR"])
        elif i % FALLBACK_PRINT_EVERY == 0 or i == total:
            elapsed = time.time() - t0
            eta = elapsed / i * (total - i)
            print(f"[{i}/{total}] {100 * i / total:5.1f}%  {day_str}  "
                  f"data days: Kp={got['Kp']} OMNI={got['OMNI']} DSCOVR={got['DSCOVR']}  "
                  f"elapsed {fmt_duration(elapsed)}, ETA {fmt_duration(eta)}")

    if tqdm is not None:
        iterator.close()

    print("\nSaving files...")
    save("kp_data.csv", kp_frames)
    save("omni_data.csv", omni_frames)
    save("dscovr_data.csv", dscovr_frames)

    print("\n=== Summary ===")
    print(f"Days processed: {total}   Total time: {fmt_duration(time.time() - t0)}")
    for name in ("Kp", "OMNI", "DSCOVR"):
        n = got[name]
        print(f"  {name:<7} real data: {n:>6} days   NaN-stubbed: {total - n:>6} days")


def save(path, frames):
    if not frames:
        print(f"  No data to save for {path}")
        return
    out = pd.concat(frames)
    out.index.name = "time_utc"
    out.to_csv(path)
    print(f"  Saved {path}: {out.shape[0]} rows, {out.shape[1]} columns")


if __name__ == "__main__":
    main()
