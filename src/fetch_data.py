import requests
import pandas as pd
import io
import os

CENSUS_KEY = "YOUR_KEY_HERE"  # paste your key here

os.makedirs("data/raw", exist_ok=True)

# ── 1. Unemployment (local file) ───────────────────────────────────────────
print("Reading unemployment data...")
unemp_df = pd.read_excel("data/raw/laucnty24.xlsx", skiprows=4)
print(unemp_df.head())

# ── 2. Population (local file) ─────────────────────────────────────────────
print("\nReading population data...")
pop_df = pd.read_excel("data/raw/NST-EST2024-POP.xlsx", skiprows=3)
print(pop_df.head())

# ── 3. Income (Census API) ─────────────────────────────────────────────────
print("\nFetching income data from Census API...")
url = "https://api.census.gov/data/2024/acs/acs1"
params = {
    "get": "NAME,B19013_001E",
    "for": "state:*",
    "key": "f42328379271e928cbb59b73cfc074a79cfead10"
}
r = requests.get(url, params=params)
data = r.json()
income_df = pd.DataFrame(data[1:], columns=data[0])
income_df = income_df.rename(columns={"NAME": "state", "B19013_001E": "median_income"})
income_df["median_income"] = pd.to_numeric(income_df["median_income"])
print(income_df.head())

print("\nDone!")

income_df.to_excel("data/raw/census_income.xlsx", index=False)
print("All three files saved to data/raw/")