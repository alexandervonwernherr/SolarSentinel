import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

st.title("Kp index: geomagnetic storms")

# fetch Kp (NOAA, 3-hour values of the last 7 days)
response = requests.get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json", timeout=30)
response.raise_for_status()
df = pd.DataFrame(response.json())
df["time"] = pd.to_datetime(df["time_tag"])

# NOAA G-class: Kp 5 = G1 ... Kp 9 = G5; 5- (4.67) still counts as G0, like in the notebook
df["g_class"] = "G" + (df["Kp"].astype(int) - 4).clip(lower=0).astype(str)

# today (UTC, because NOAA measures in UTC)
today = datetime.now(timezone.utc).date()
df_today = df[df["time"].dt.date == today]

classes = ["G0", "G1", "G2", "G3", "G4", "G5"]
counts = df_today["g_class"].value_counts().reindex(classes, fill_value=0)

# show data
st.metric("Kp now", df_today["Kp"].iloc[-1] if len(df_today) else "–", help=f"as of {df['time'].iloc[-1]:%Y-%m-%d %H:%M} UTC")
st.subheader(f"Today ({today:%Y-%m-%d}, UTC)")
st.dataframe(df_today[["time", "Kp", "g_class"]], hide_index=True)
st.bar_chart(counts)
st.subheader("Last 7 days")
st.line_chart(df.set_index("time")["Kp"])
