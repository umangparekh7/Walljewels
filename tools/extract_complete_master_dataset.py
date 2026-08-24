import pymupdf
import json
import re
import os
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

def process_kala_parampara():
    print("Processing Kala Parampara...")
    doc = pymupdf.open(kp_pdf)
    results = []
    
    # In Kala Parampara, plates start at page 6 (index 5) through page 76
    for i in range(5, min(77, len(doc))):
        page_num = i + 1
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes('png')
        res, _ = ocr(img_bytes)
        lines = [r[1].strip() for r in res] if res else []
        
        # Save cropped artwork plate to assets/img/collection/kala-parampara/kp-plate-{page_num}.jpg
        # The artwork in KP is generally in the center/right, full width or 60-100% of page
        # Let's save high-res render of the page as plate
        pix_hi = page.get_pixmap(dpi=200)
        out_img = f"assets/img/collection/kala-parampara/kp-plate-{page_num:02d}.jpg"
        pix_hi.save(out_img)
        
        results.append({
            "page": page_num,
            "img": out_img,
            "lines": lines
        })
        print(f"KP Page {page_num}: {len(lines)} lines extracted -> {out_img}")
        
    with open('scratch/kp_full_raw_ocr.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Kala Parampara OCR complete!")

def process_kala_rasa():
    print("Processing Kala Rasa...")
    doc = pymupdf.open(kr_pdf)
    results = []
    
    # In Kala Rasa, plates run from page 8 to 185
    for i in range(7, min(186, len(doc))):
        page_num = i + 1
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes('png')
        res, _ = ocr(img_bytes)
        lines = [r[1].strip() for r in res] if res else []
        
        # Also ensure clean plate image exists in assets/img/collection/kala-rasa/kr-plate-{page_num:03d}.jpg
        pix_hi = page.get_pixmap(dpi=200)
        out_img = f"assets/img/collection/kala-rasa/kr-plate-{page_num:03d}.jpg"
        pix_hi.save(out_img)
        
        results.append({
            "page": page_num,
            "img": out_img,
            "lines": lines
        })
        if page_num % 10 == 0 or page_num == 8 or page_num == 185:
            print(f"KR Page {page_num}: {len(lines)} lines extracted -> {out_img}")
            
    with open('scratch/kr_full_raw_ocr.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Kala Rasa OCR complete!")

if __name__ == '__main__':
    process_kala_parampara()
    process_kala_rasa()
