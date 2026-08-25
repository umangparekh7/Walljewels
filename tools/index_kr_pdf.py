import pymupdf
import json
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)
print(f"Total pages in KR PDF: {len(doc)}")

# Check pages 1 to 186
results = []
for pnum in range(1, len(doc) + 1):
    pix = doc[pnum - 1].get_pixmap(dpi=150)
    res, _ = ocr(pix.tobytes('png'))
    text = " ".join([r[1] for r in res]) if res else ""
    results.append({'page': pnum, 'text': text[:200], 'res_count': len(res) if res else 0})

with open('scratch/kr_pdf_page_index.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Saved scratch/kr_pdf_page_index.json")
