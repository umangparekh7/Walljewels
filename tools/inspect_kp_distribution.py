import pymupdf
import io
import os
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('scratch/inspections/all_kp', exist_ok=True)

# Let's inspect KP pages 6 to 25
for p in range(6, 26):
    page = doc_kp[p - 1]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    # Count characters on left half vs right half
    left_char_count = 0
    right_char_count = 0
    
    if res:
        for item in res:
            box, text = item[0], item[1]
            xs = [pt[0] for pt in box]
            center_x = sum(xs) / len(xs)
            if center_x < 0.5 * w:
                left_char_count += len(text)
            else:
                right_char_count += len(text)
                
    # If right half has more text -> Photo is on LEFT (0..0.5*w)
    # If left half has more text -> Photo is on RIGHT (0.5*w..w)
    if right_char_count > left_char_count:
        photo_side = "LEFT (crop 0..52%)"
        crop_box = (0, 0, int(w * 0.52), h)
    else:
        photo_side = "RIGHT (crop 48%..100%)"
        crop_box = (int(w * 0.48), 0, w, h)
        
    print(f"KP Page {p:02d} -> LeftChars={left_char_count:3d}, RightChars={right_char_count:3d} ==> PHOTO IS ON {photo_side}")
    cropped = img.crop(crop_box)
    cropped.save(f"scratch/inspections/all_kp/kp_{p:02d}.jpg")
