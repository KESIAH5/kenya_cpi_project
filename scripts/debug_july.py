import pdfplumber
import re
from pathlib import Path
import pandas as pd

pdf_path = Path("data/raw_pdfs/Kenya-Consumer-Price-Indices-and-Inflation-Rates-July-2025_1.pdf")

full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

# now test the Table 1 regex against the combined text
total_line_pattern = r"Total\s+100\.0000\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
match = re.search(total_line_pattern, full_text)

if match:
    mom_change, yoy_inflation = match.groups()
    print(f"Month-on-month change: {mom_change}")
    print(f"Year-on-year inflation: {yoy_inflation}")
else:
    print("No match found")
df = pd.read_csv("data/processed/overall_cpi_inflation.csv")

june_2025_row = df[(df["month"] == "June") & (df["year"] == 2025)]
print(june_2025_row)
print (df[df["year"] == 2025])