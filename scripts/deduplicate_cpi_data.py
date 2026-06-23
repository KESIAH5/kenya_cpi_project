import pandas as pd

df_final = pd.read_csv("data/processed/overall_cpi_inflation.csv")

print(f"Rows before deduplication: {len(df_final)}")

# Keep the first occurrence of each month/year combination
df_deduped = df_final.drop_duplicates(subset=["month", "year"], keep="first")

print(f"Rows after deduplication: {len(df_deduped)}")

# Save the cleaned, deduplicated dataset
df_deduped.to_csv("data/processed/overall_cpi_inflation_clean.csv", index=False)
print("Saved cleaned dataset to data/processed/overall_cpi_inflation_clean.csv")
df_sorted = df_deduped.copy()

month_order = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
df_sorted["month_num"] = df_sorted["month"].apply(lambda m: month_order.index(m) + 1)

df_sorted = df_sorted.sort_values(["year", "month_num"]).reset_index(drop=True)

print(df_sorted[["month", "year", "overall_cpi", "inflation_rate"]].to_string())