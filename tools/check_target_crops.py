import os
import pymupdf
import io
import json
from PIL import Image

# Let's inspect the bounding box of text and the image currently saved
# in assets/img/collection/kala-rasa/ for each of these plates!

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_ocr = json.load(f)

# Map page to lines
page_lines = {entry['page']: entry['lines'] for entry in kr_ocr}

target_pages = [16, 33, 34, 35, 36, 37] + list(range(39, 58)) + list(range(121, 161)) + [167]

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

for p in target_pages:
    img_path = f"assets/img/collection/kala-rasa/kr-plate-{p:03d}.jpg"
    if os.path.exists(img_path):
        with Image.open(img_path) as im:
            sz = im.size
    else:
        sz = (0, 0)
    lines = page_lines.get(p, [])
    print(f"Page {p:03d} (Img: {sz[0]}x{sz[1]}): {len(lines)} OCR lines | First 2: {lines[:2]}")
