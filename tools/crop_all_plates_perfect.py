import pymupdf
import io
import os
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

def smart_crop_page(page, out_path):
    pix = page.get_pixmap(dpi=200)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if not res or len(res) <= 2:
        # Full spread artwork without sidebar
        img.save(out_path, quality=95)
        return "FULL"
        
    x_centers = []
    min_x = w
    max_x = 0
    for box, text, score in res:
        xs = [pt[0] for pt in box]
        x_centers.append(sum(xs) / len(xs))
        min_x = min(min_x, min(xs))
        max_x = max(max_x, max(xs))
        
    avg_x = sum(x_centers) / len(x_centers)
    
    # If text is on the right half (avg_x > 0.5 * w) -> PHOTO IS ON LEFT
    if avg_x > 0.5 * w:
        crop_x = min(int(w * 0.60), int(min_x) - 10)
        crop_x = max(crop_x, int(w * 0.48))
        cropped = img.crop((0, 0, crop_x, h))
        cropped.save(out_path, quality=95)
        return f"LEFT (0..{crop_x})"
    else:
        # Text is on the left half -> PHOTO IS ON RIGHT
        crop_x = max(int(w * 0.40), int(max_x) + 10)
        crop_x = min(crop_x, int(w * 0.52))
        cropped = img.crop((crop_x, 0, w, h))
        cropped.save(out_path, quality=95)
        return f"RIGHT ({crop_x}..{w})"

def process_all_kp():
    print("=== CROPPING ALL KALA PARAMPARA PLATES ===")
    doc = pymupdf.open(kp_pdf)
    for pnum in range(6, min(78, len(doc) + 1)):
        out_path = f"assets/img/collection/kala-parampara/kp-plate-{pnum:02d}.jpg"
        r = smart_crop_page(doc[pnum - 1], out_path)
        if pnum % 10 == 0 or pnum == 6:
            print(f"KP Page {pnum}: {r} -> {out_path}")
    print("Completed all Kala Parampara plate crops!")

def process_all_kr():
    print("\n=== CROPPING ALL KALA RASA PLATES ===")
    doc = pymupdf.open(kr_pdf)
    for pnum in range(8, min(186, len(doc) + 1)):
        out_path = f"assets/img/collection/kala-rasa/kr-plate-{pnum:03d}.jpg"
        r = smart_crop_page(doc[pnum - 1], out_path)
        if pnum % 20 == 0 or pnum == 8:
            print(f"KR Page {pnum}: {r} -> {out_path}")
    print("Completed all Kala Rasa plate crops!")

if __name__ == '__main__':
    process_all_kp()
    process_all_kr()
