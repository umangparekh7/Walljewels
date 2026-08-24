import json
import pymupdf
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

with open('scratch/kp_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kp_ocr = json.load(f)

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_ocr = json.load(f)

print("--- KP PAGE 15 OCR ---")
for p in kp_ocr:
    if p['page'] == 15:
        print("\n".join(p['lines']))

print("\n--- KR PAGE 16 OCR ---")
for p in kr_ocr:
    if p['page'] == 16:
        print("\n".join(p['lines']))

print("\n--- KR PAGES 31-35 OCR ---")
for p in kr_ocr:
    if 31 <= p['page'] <= 35:
        print(f"\n[PAGE {p['page']}]")
        print("\n".join(p['lines']))

# Save raw pages for visual check
pix_kp15 = doc_kp[14].get_pixmap(dpi=200)
pix_kp15.save("scratch/raw_kp_15.jpg")

pix_kr16 = doc_kr[15].get_pixmap(dpi=200)
pix_kr16.save("scratch/raw_kr_16.jpg")

for pnum in [32, 33, 34, 38, 117]:
    pix = doc_kr[pnum - 1].get_pixmap(dpi=200)
    pix.save(f"scratch/raw_kr_{pnum}.jpg")
