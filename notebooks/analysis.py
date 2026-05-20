import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")

df = pd.read_csv("data/sheet1_procedures.csv", parse_dates=["Date"])
pts = pd.read_csv("data/sheet3_patients.csv")

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["YearMonth"] = df["Date"].dt.to_period("M")

print("Making charts...")

# Chart 1 - Monthly volume
monthly = df.groupby("YearMonth").size().reset_index(name="n")
fig, ax = plt.subplots(figsize=(14,5))
ax.bar(range(len(monthly)), monthly["n"], color="steelblue", alpha=0.85)
ax.set_xticks(range(0, len(monthly), 3))
ax.set_xticklabels([str(x) for x in monthly["YearMonth"][::3]], rotation=45, ha="right")
ax.set_title("Monthly Procedure Volume (2022-2025)", fontweight="bold", fontsize=14)
ax.set_ylabel("Number of Procedures")
plt.tight_layout()
plt.savefig("outputs/fig01_monthly_volume.png", dpi=150)
plt.close()
print("Chart 1 done")

# Chart 2 - Procedures by year
yearly = df.groupby("Year").size()
fig, ax = plt.subplots(figsize=(8,5))
yearly.plot(kind="bar", ax=ax, color="steelblue", rot=0)
ax.set_title("Annual Procedure Volume", fontweight="bold", fontsize=14)
ax.set_ylabel("Number of Procedures")
ax.set_xlabel("Year")
plt.tight_layout()
plt.savefig("outputs/fig02_annual_volume.png", dpi=150)
plt.close()
print("Chart 2 done")

# Chart 3 - Procedure type mix
proc_cols = ["Angioplasty","CTO","PRIMARY","TAVI","PFO","IAB","Valvuloplasty"]
totals = {c: int(df[c].sum()) for c in proc_cols if c in df.columns}
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(list(totals.keys()), list(totals.values()), color=sns.color_palette("Blues_d", len(totals)))
ax.bar_label(bars, fmt="%,.0f", padding=4)
ax.set_title("Total Procedures by Type (2022-2025)", fontweight="bold", fontsize=14)
ax.set_xlabel("Count")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/fig03_procedure_mix.png", dpi=150)
plt.close()
print("Chart 3 done")

# Chart 4 - IVUS OCT FFR by year
imaging = df.groupby("Year")[["IVUS","OCT","FFR"]].sum()
imaging.plot(kind="bar", figsize=(10,5), rot=0)
plt.title("Imaging & Physiology Tool Use Per Year", fontweight="bold", fontsize=14)
plt.ylabel("Cases")
plt.tight_layout()
plt.savefig("outputs/fig04_imaging_tools.png", dpi=150)
plt.close()
print("Chart 4 done")

# Chart 5 - Age distribution
fig, ax = plt.subplots(figsize=(9,5))
ax.hist(pts["Age"], bins=20, color="steelblue", edgecolor="white")
ax.axvline(pts["Age"].median(), color="red", linestyle="--", label=f'Median = {pts["Age"].median():.0f}')
ax.set_title("Patient Age Distribution", fontweight="bold", fontsize=14)
ax.set_xlabel("Age (years)")
ax.set_ylabel("Number of Patients")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/fig05_age_distribution.png", dpi=150)
plt.close()
print("Chart 5 done")

# Chart 6 - Gender split
fig, ax = plt.subplots(figsize=(6,6))
pts["Gender"].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%",
    colors=["steelblue","salmon"], startangle=90,
    wedgeprops={"edgecolor":"white","linewidth":2})
ax.set_title("Gender Split", fontweight="bold", fontsize=14)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("outputs/fig06_gender.png", dpi=150)
plt.close()
print("Chart 6 done")

# Chart 7 - Risk factors
risk_cols = ["Smoking","Diabetes","Hypertension","Prior_MI"]
risk_pct = (pts[risk_cols].mean() * 100).sort_values()
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.barh(risk_pct.index, risk_pct.values, color=sns.color_palette("Reds", len(risk_pct)))
ax.bar_label(bars, fmt="%.1f%%", padding=4)
ax.set_xlim(0,100)
ax.set_title("Risk Factor Prevalence", fontweight="bold", fontsize=14)
ax.set_xlabel("% of Patients")
plt.tight_layout()
plt.savefig("outputs/fig07_risk_factors.png", dpi=150)
plt.close()
print("Chart 7 done")

# Chart 8 - Outcomes
fig, ax = plt.subplots(figsize=(10,5))
pts["Outcome"].value_counts().plot(kind="bar", ax=ax, color=sns.color_palette("Set2"), rot=30)
ax.set_title("Patient Outcomes", fontweight="bold", fontsize=14)
ax.set_ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("outputs/fig08_outcomes.png", dpi=150)
plt.close()
print("Chart 8 done")

# Chart 9 - Diagnosis breakdown
fig, ax = plt.subplots(figsize=(10,5))
pts["Diagnosis"].value_counts().plot(kind="barh", ax=ax, color="steelblue")
ax.set_title("Diagnosis Distribution", fontweight="bold", fontsize=14)
ax.set_xlabel("Number of Patients")
plt.tight_layout()
plt.savefig("outputs/fig09_diagnosis.png", dpi=150)
plt.close()
print("Chart 9 done")

# Chart 10 - Length of stay
fig, ax = plt.subplots(figsize=(9,5))
ax.hist(pts["Length_of_Stay_days"], bins=15, color="mediumseagreen", edgecolor="white")
ax.set_title("Length of Stay Distribution", fontweight="bold", fontsize=14)
ax.set_xlabel("Days")
ax.set_ylabel("Patients")
plt.tight_layout()
plt.savefig("outputs/fig10_length_of_stay.png", dpi=150)
plt.close()
print("Chart 10 done")

print("\nALL DONE! Check your outputs folder - you have 10 charts ready.")
