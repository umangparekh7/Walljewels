import pymupdf
import io
import os
import json
import re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

print(f"KP pages: {len(doc_kp)}, KR pages: {len(doc_kr)}")

def find_exact_crop(page):
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if not res or len(res) <= 1:
        # Full spread artwork
        return (0, 0, w, h), "FULL"
        
    # Get all text bounding boxes
    text_boxes = []
    for item in res:
        box, text = item[0], item[1]
        xs = [pt[0] for pt in box]
        ys = [pt[1] for pt in box]
        text_boxes.append({
            'min_x': min(xs), 'max_x': max(xs),
            'min_y': min(ys), 'max_y': max(ys),
            'text': text,
            'center_x': sum(xs) / len(xs)
        })
        
    # Separate into left half (< 0.5*w) and right half (>= 0.5*w)
    left_boxes = [b for b in text_boxes if b['center_x'] < 0.5 * w]
    right_boxes = [b for b in text_boxes if b['center_x'] >= 0.5 * w]
    
    # Filter out tiny page numbers or corner marks
    # (e.g. len < 6 and near the outer edge)
    left_significant = [b for b in left_boxes if not (len(b['text']) < 6 and b['min_x'] < 0.08 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    right_significant = [b for b in right_boxes if not (len(b['text']) < 6 and b['max_x'] > 0.92 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    
    # Decide which half has the text sidebar:
    if len(left_significant) > len(right_significant):
        # Sidebar is on the LEFT -> WALLPAPER IS ON THE RIGHT
        # Crop from right edge of left sidebar to right edge of page
        max_left_x = max([b['max_x'] for b in left_significant])
        crop_start_x = max(int(max_left_x + 10), int(w * 0.46))
        return (crop_start_x, 0, w, h), f"RIGHT_PHOTO (from {crop_start_x}/{w})"
    else:
        # Sidebar is on the RIGHT -> WALLPAPER IS ON THE LEFT
        # Crop from 0 to left edge of right sidebar
        min_right_x = min([b['min_x'] for b in right_significant])
        crop_end_x = min(int(min_right_x - 10), int(w * 0.54))
        return (0, 0, crop_end_x, h), f"LEFT_PHOTO (0..{crop_end_x}/{w})"

# Let's test on 10 random pages across both volumes
for p in [10, 15, 33, 44, 75, 95, 98, 110, 140, 160, 175]:
    if p <= len(doc_kr):
        box, typ = find_exact_crop(doc_kr[p - 1])
        print(f"KR Page {p:03d} -> {typ} Box: {box}")
