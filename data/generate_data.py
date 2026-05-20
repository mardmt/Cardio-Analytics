import pandas as pd

df = pd.read_excel("data/ΣΤΑΤΙΣΤΙΚΑ A' ΑΙΘΟΥΣΑ.xlsx", sheet_name=0)

print("Success! Loaded", len(df), "rows")
print(df.head(3))
import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

np.random.seed(42)
random.seed(42)

print("Loading Excel file...")
df = pd.read_excel("data/ΣΤΑΤΙΣΤΙΚΑ A' ΑΙΘΟΥΣΑ.xlsx", sheet_name=0)
df.columns = ["Date","Coronary_Angio","Angioplasty","CTO","PRIMARY",
               "Guide_Catheter","Guidewires","Plain_Balloon","DEB",
               "BMS","DES","Microcatheters","ROTABLATION","DEB_Balloon",
               "OPN","IVUS","OCT","FFR","CUTB","TAVI","PFO","IAB","Valvuloplasty"]
df["Date"] = pd.to_datetime(df["Date"]).dt.date
print(f"Loaded {len(df)} rows")

# Remove empty placeholder rows for Jul-Dec 2025
df = df[~(
    (pd.to_datetime(df["Date"]).dt.year == 2025) &
    (pd.to_datetime(df["Date"]).dt.month >= 7)
)]

# Learn patterns from 2024 data
df24 = df[pd.to_datetime(df["Date"]).dt.year == 2024].copy()
df24["Month"] = pd.to_datetime(df24["Date"]).dt.month
ppd = (df24.groupby(["Date","Month"]).size()
       .reset_index(name="n").groupby("Month")["n"]
       .agg(["mean","std"]).to_dict("index"))

angio_rows = df24[df24["Angioplasty"].notna()]
cto_rate = angio_rows["CTO"].notna().mean()
primary_rate = angio_rows["PRIMARY"].notna().mean()

GR_HOLIDAYS = {date(2025,1,1),date(2025,1,6),date(2025,3,3),
               date(2025,3,25),date(2025,4,18),date(2025,4,20),
               date(2025,4,21),date(2025,5,1),date(2025,6,9),
               date(2025,8,15),date(2025,10,28),date(2025,12,25),date(2025,12,26)}

def is_working_day(d):
    return d.weekday() < 5 and d not in GR_HOLIDAYS

print("Generating Jul-Dec 2025 data...")
new_rows = []
d = date(2025, 7, 1)
while d <= date(2025, 12, 31):
    stats = ppd.get(d.month, {"mean": 8, "std": 3})
    n = max(2, int(np.random.normal(stats["mean"], max(stats["std"],1)))) if is_working_day(d) else int(np.random.poisson(1.2))
    for _ in range(n):
        row = [None]*23
        row[0] = d
        row[1] = 1
        if random.random() < 0.37:
            row[2] = 1
            if random.random() < cto_rate: row[3] = 1
            if random.random() < primary_rate: row[4] = 1
            row[5] = random.randint(1,3)
            row[6] = random.randint(1,4)
            if random.random() < 0.70: row[7] = random.randint(1,8)
            if random.random() < 0.60: row[9] = random.randint(1,4)
            elif random.random() < 0.40: row[10] = random.randint(1,3)
            if random.random() < 0.08: row[15] = 1
            if random.random() < 0.05: row[16] = 1
            if random.random() < 0.10: row[17] = 1
        new_rows.append(row)
    d += timedelta(days=1)

cols = ["Date","Coronary_Angio","Angioplasty","CTO","PRIMARY",
        "Guide_Catheter","Guidewires","Plain_Balloon","DEB",
        "BMS","DES","Microcatheters","ROTABLATION","DEB_Balloon",
        "OPN","IVUS","OCT","FFR","CUTB","TAVI","PFO","IAB","Valvuloplasty"]
df_new = pd.DataFrame(new_rows, columns=cols)
df.columns = cols
df_all = pd.concat([df, df_new], ignore_index=True)
df_all.sort_values("Date", inplace=True)
print(f"Total rows after completion: {len(df_all)}")

# Generate 3000 patient records
print("Generating patient demographics...")
n = 3000
diagnoses = np.random.choice(
    ["Stable Angina","Unstable Angina","NSTEMI","STEMI","CTO",
     "Valvular Disease","Heart Failure","Arrhythmia","Other"],
    n, p=[0.22,0.18,0.18,0.12,0.05,0.07,0.08,0.06,0.04])
procedures = np.random.choice(
    ["Coronary Angiography Only","PCI + Stent","Primary PCI (STEMI)",
     "PCI + IVUS","PCI + FFR","CTO-PCI","TAVI","PFO Closure"],
    n, p=[0.38,0.30,0.11,0.07,0.05,0.04,0.03,0.02])
outcomes = []
for p in procedures:
    if "STEMI" in p:
        outcomes.append(np.random.choice(["Success","Complication","Death"],p=[0.89,0.09,0.02]))
    elif p == "Coronary Angiography Only":
        outcomes.append(np.random.choice(["Normal","Mild CAD","Moderate CAD","Severe CAD"],p=[0.20,0.25,0.30,0.25]))
    else:
        outcomes.append(np.random.choice(["Success","Complication","Failure","Death"],p=[0.92,0.06,0.015,0.005]))

df_patients = pd.DataFrame({
    "Patient_ID": [f"PT{str(i+1).zfill(5)}" for i in range(n)],
    "Age": np.random.normal(64,12,n).clip(25,95).astype(int),
    "Gender": np.random.choice(["Male","Female"],n,p=[0.68,0.32]),
    "BMI": np.round(np.random.normal(27.5,4.5,n).clip(17,45),1),
    "Smoking": np.random.choice([0,1],n,p=[0.60,0.40]),
    "Diabetes": np.random.choice([0,1],n,p=[0.65,0.35]),
    "Hypertension": np.random.choice([0,1],n,p=[0.45,0.55]),
    "Prior_MI": np.random.choice([0,1],n,p=[0.80,0.20]),
    "EF_Percent": np.random.normal(55,12,n).clip(15,75).round(0).astype(int),
    "Creatinine": np.round(np.random.lognormal(0.05,0.35,n).clip(0.5,5.0),2),
    "Diagnosis": diagnoses,
    "Procedure": procedures,
    "Outcome": outcomes,
    "Length_of_Stay_days": np.random.poisson(3,n),
    "Contrast_mL": np.random.normal(130,40,n).clip(40,350).round(0).astype(int),
    "Radiation_mGy": np.random.exponential(900,n).clip(50,8000).round(0).astype(int),
})

# Save CSVs
df_all.to_csv("data/sheet1_procedures.csv", index=False)
df_patients.to_csv("data/sheet3_patients.csv", index=False)
print("Saved: data/sheet1_procedures.csv")
print("Saved: data/sheet3_patients.csv")
print("DONE!")
