import pymupdf
import json
import os
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

def inspect_pdf(pdf_path, name):
    print(f"\n==========================================")
    print(f"Inspecting: {name} ({pdf_path})")
    doc = pymupdf.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    # Check first 15 pages for text
    for i in range(min(15, len(doc))):
        page = doc[i]
        text = page.get_text().strip()
        print(f"--- Page {i+1} ---")
        if text:
            print(f"[Direct Text]:\n{text[:300]}")
        else:
            # Run OCR on pixmap
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes('png')
            res, _ = ocr(img_bytes)
            if res:
                lines = [r[1] for r in res]
                print(f"[OCR Text ({len(lines)} lines)]:")
                print(" | ".join(lines[:10]))
            else:
                print("[No text detected]")

inspect_pdf(kp_pdf, "KALA PARAMPARA")
inspect_pdf(kr_pdf, "KALA RASA")
