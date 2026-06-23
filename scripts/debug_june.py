import pdfplumber
import re
import pandas as pd
from pathlib import Path

pdf_path = Path("data/raw_pdfs/Kenya-Consumer-Price-Indices-and-Inflation-Rates-June-2025.pdf")

full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

total_line_pattern = r"Total\s+100\.0000\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
match = re.search(total_line_pattern, full_text)

if match:
    mom_change, yoy_inflation = match.groups()
    print(f"Month-on-month change: {mom_change}")
    print(f"Year-on-year inflation: {yoy_inflation}")
else:
    print("No match found")

df = pd.read_csv("data/processed/overall_cpi_inflation.csv")

may_2025_row = df[(df["month"] == "May") & (df["year"] == 2025)]
may_cpi = may_2025_row["overall_cpi"].values[0] if not may_2025_row.empty else None
print(f"May 2025 CPI: {may_cpi}")

# Step 1: Calculate June and July CPI values
june_cpi = may_cpi * (1 + 0.5/100)
july_cpi = june_cpi * (1 + 0.1/100)

# Step 2: Drop the stray garbage row from July
df_clean = df[~((df["month"] == "July") & (df["year"] == 2025) & (df["overall_cpi"] == 5.0))]

print(f"Rows before cleaning: {len(df)}")
print(f"Rows after cleaning: {len(df_clean)}")

# Step 3: Build the two new rows
new_rows = pd.DataFrame([
    {
        "month": "June",
        "year": 2025,
        "overall_cpi": round(june_cpi, 2),
        "inflation_rate": 3.8,
        "source_file": "Kenya-Consumer-Price-Indices-and-Inflation-Rates-June-2025.pdf"
    },
    {
        "month": "July",
        "year": 2025,
        "overall_cpi": round(july_cpi, 2),
        "inflation_rate": 4.1,
        "source_file": "Kenya-Consumer-Price-Indices-and-Inflation-Rates-July-2025_1.pdf"
    },
])

# Step 4: Combine and save
df_final = pd.concat([df_clean, new_rows], ignore_index=True)
df_final.to_csv("data/processed/overall_cpi_inflation.csv", index=False)
print(f"Final row count: {len(df_final)}")
print(df_final[df_final["year"] == 2025][["month", "year", "overall_cpi", "inflation_rate"]].to_string())