import pymupdf

doc = pymupdf.open("data/_R2_WEB_rapport_annuel_2025_0326_BGLBNPP.pdf")
page = doc[35]  # teste sur une page avec un tableau
finder = page.find_tables()
tabs = finder.tables
print(f"Tables trouvées : {len(tabs)}")
for tab in tabs:
    print(tab.to_pandas().to_string())
