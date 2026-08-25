import pymupdf
from PIL import Image

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

# Let's inspect pages 92 to 116 (Kolam section)
for p in [92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115]:
    page = doc[p - 1]
    pix = page.get_pixmap(dpi=150)
    print(f"Page {p:03d} -> width={pix.width}, height={pix.height}")
    pix.save(f"scratch/inspections/raw_p_{p:03d}.jpg")

print("Saved raw sample pages in scratch/inspections/")
