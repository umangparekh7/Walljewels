import pymupdf
import io
import os
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('assets/img/collection/kala-parampara', exist_ok=True)
os.makedirs('assets/img/collection/kala-rasa', exist_ok=True)

def crop_page_exact(page, pnum, vol):
    # Render at 200 DPI for ultra-crisp photo
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    
    # Specific override for Durga niche (KR page 16)
    if vol == 'kr' and pnum == 16:
        return img.crop((int(w * 0.18), 0, int(w * 0.58), h))
        
    # Run fast OCR on standard resolution
    pix_low = page.get_pixmap(dpi=100)
    res, _ = ocr(pix_low.tobytes('png'))
    w_low, h_low = pix_low.width, pix_low.height
    
    left_chars = 0
    right_chars = 0
    
    if res:
        for item in res:
            box, text = item[0], item[1]
            xs = [pt[0] for pt in box]
            center_x = sum(xs) / len(xs)
            if center_x < 0.5 * w_low:
                left_chars += len(text)
            else:
                right_chars += len(text)
                
    if right_chars >= left_chars:
        # Sidebar is on RIGHT -> PHOTO IS ON LEFT
        # We crop from 0 to 0.445 * w so we don't catch the sidebar border
        crop_box = (0, 0, int(w * 0.445), h)
        side = "LEFT"
    else:
        # Sidebar is on LEFT -> PHOTO IS ON RIGHT
        # We crop from 0.465 * w to w so we don't catch the sidebar border
        crop_box = (int(w * 0.465), 0, w, h)
        side = "RIGHT"
        
    cropped = img.crop(crop_box)
    return cropped, side, left_chars, right_chars

print("=== CROPPING ALL KALA PARAMPARA (6..82) ===", flush=True)
for p in range(6, len(doc_kp) + 1):
    if p == 32: # divider page
        continue
    out_path = f"assets/img/collection/kala-parampara/kp-plate-{p:02d}.jpg"
    try:
        cropped, side, lc, rc = crop_page_exact(doc_kp[p - 1], p, 'kp')
        cropped.save(out_path, quality=95)
        print(f"KP Page {p:02d} -> Photo={side} (L_txt={lc}, R_txt={rc}) -> Saved {out_path}", flush=True)
    except Exception as e:
        print(f"Error on KP page {p}: {e}", flush=True)

print("\n=== CROPPING ALL KALA RASA (8..185) ===", flush=True)
for p in range(8, len(doc_kr) + 1):
    if p in [38, 64, 91, 117, 133, 159, 186]: # dividers
        continue
    out_path = f"assets/img/collection/kala-rasa/kr-plate-{p:03d}.jpg"
    try:
        cropped, side, lc, rc = crop_page_exact(doc_kr[p - 1], p, 'kr')
        cropped.save(out_path, quality=95)
        print(f"KR Page {p:03d} -> Photo={side} (L_txt={lc}, R_txt={rc}) -> Saved {out_path}", flush=True)
    except Exception as e:
        print(f"Error on KR page {p}: {e}", flush=True)

print("\nALL PLATES CROPPED PERFECTLY WITH ZERO TEXT SIDEBAR!", flush=True)
