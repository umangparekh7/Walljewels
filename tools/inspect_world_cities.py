import pymupdf
import json

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
doc = pymupdf.open(kp_pdf)

for p in range(53, 73):
    page = doc[p - 1]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"scratch/inspections/kp_page_{p:02d}.jpg")
    print(f"Saved KP page {p}")

with open('scratch/kp_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kp_ocr = json.load(f)

for item in kp_ocr:
    if 53 <= item['page'] <= 72:
        print(f"\n--- KP Page {item['page']} ---")
        for line in item['lines']:
            print(f"  {line}")
