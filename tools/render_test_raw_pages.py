import pymupdf
import os
from PIL import Image

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)
os.makedirs('scratch/test_renders', exist_ok=True)

# Render full pages for 16, 33, 34, 35, 36, 37, 39..57, and 121..160, 167
test_pages = [16, 33, 34, 35, 36, 37] + list(range(39, 58)) + [121, 122, 133, 137, 159, 160, 167]

for p in test_pages:
    if p <= len(doc):
        pix = doc[p - 1].get_pixmap(dpi=150)
        pix.save(f'scratch/test_renders/raw_page_{p:03d}.jpg')

print("Rendered raw sample pages to scratch/test_renders/")
