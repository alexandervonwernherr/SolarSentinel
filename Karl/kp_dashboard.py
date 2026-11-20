import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

st.title("KP-Index: geomagnetische Stürme")

#KP_Index abrufen (NOAA, 3-Stunden-Werte der letzten 7 Tage)
response = requests.get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json", timeout=30)
response.raise_for_status()
df = pd.DataFrame(response.json())
df["time"] = pd.to_datetime(df["time_tag"])

#G-Klasse nach NOAA: Kp 5 = G1 ... Kp 9 = G5; 5- (4,67) zählt wie im Notebook noch als G0
df["klasse"] = "G" + (df["Kp"].astype(int) - 4).clip(lower=0).astype(str)

#Heute (UTC, weil NOAA in UTC misst)
today = datetime.now(timezone.utc).date()
heute = df[df["time"].dt.date == today]

classes = ["G0", "G1", "G2", "G3", "G4", "G5"]
counts = heute["klasse"].value_counts().reindex(classes, fill_value=0)

#Daten anzeigen
st.metric("Kp aktuell", heute["Kp"].iloc[-1] if len(heute) else "–", help=f"Stand {df['time'].iloc[-1]:%d.%m. %H:%M} UTC")
st.subheader(f"Heute ({today:%d.%m.%Y}, UTC)")
st.dataframe(heute[["time", "Kp", "klasse"]], hide_index=True)
st.bar_chart(counts)
st.subheader("Letzte 7 Tage")
st.line_chart(df.set_index("time")["Kp"])
