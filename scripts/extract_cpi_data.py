import pdfplumber
import re
import pandas as pd
from pathlib import Path

raw_pdf_folder = Path("data/raw_pdfs")
pdf_files = list(raw_pdf_folder.glob("*.pdf"))

pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\s+(\d+\.\d+)\s+(-?\d+\.\d+)"

# This will collect rows from ALL pdfs, not just one
all_rows = []

for pdf_path in pdf_files:
    print(f"Processing: {pdf_path.name}")

    #combine text from allpages into one string
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # some pages might have no text at all
                full_text += page_text + "\n"
    
    matches = re.finditer(pattern, full_text)
    
    rows_from_this_file = 0
    for match in matches:
        month, year, cpi, inflation = match.groups()
        row = {
            "month": month,
            "year": int(year),
            "overall_cpi": float(cpi),
            "inflation_rate": float(inflation),
            "source_file": pdf_path.name  # track which PDF this came from
        }
        all_rows.append(row)
        rows_from_this_file += 1
    
    print(f"  -> extracted {rows_from_this_file} rows")

print(f"\nTotal rows from all files: {len(all_rows)}")

df = pd.DataFrame(all_rows)
df.to_csv("data/processed/overall_cpi_inflation.csv", index=False)
print("Saved to data/processed/overall_cpi_inflation.csv")

