import pandas as pd

df = pd.read_csv("data/cleaned/merged_state_data.csv")
#Normalize each metric
#Higher income = Better
df["income_score"] = (df["median_income"] - df["median_income"].min()) / (df["median_income"].max() - df["median_income"].min()) * 100
#Lower unemployment = Better
df["employment_score"] = (df["unemployment_rate"].max() - df["unemployment_rate"]) / (df["unemployment_rate"].max() - df["unemployment_rate"].min()) * 100
#Higher Population = Better
df["population_score"] = (df["population"] - df["population"].min()) / (df["population"].max() - df["population"].min()) * 100


#Calculate Business Score
#Weights: Income: 40%, Employment: 40%, Population 20%
df["business_score"] = (df["income_score"] * 0.4 + df["employment_score"] * 0.4 + df["population_score"] + 0.2).round(2)

#Ranking the States
df["rank"] = df["business_score"].rank(ascending=False).astype(int)
df = df.sort_values("rank")
print(df[["rank", "state", "business_score"]].head(10))

#Save final file
df.to_csv("data/cleaned/final_scored_states.csv", index=False)
print("Saved!")