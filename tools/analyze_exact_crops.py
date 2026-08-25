import pymupdf
import io
import os
import json
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

def analyze_crop(pnum):
    page = doc[pnum - 1]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if not res:
        return {'page': pnum, 'type': 'FULL', 'crop_box': (0, 0, w, h), 'text_side': 'NONE'}
        
    # Find text clusters: ignore tiny page numbers/corner codes (e.g. text length <= 6 and at far margin)
    significant_boxes = []
    for item in res:
        box, text = item[0], item[1]
        xs = [pt[0] for pt in box]
        ys = [pt[1] for pt in box]
        bw = max(xs) - min(xs)
        bh = max(ys) - min(ys)
        # ignore single small word in corner
        significant_boxes.append({
            'min_x': min(xs), 'max_x': max(xs),
            'min_y': min(ys), 'max_y': max(ys),
            'text': text,
            'center_x': sum(xs) / len(xs)
        })
        
    # Count boxes on left (< 0.5*w) vs right (> 0.5*w)
    left_boxes = [b for b in significant_boxes if b['center_x'] < 0.5 * w]
    right_boxes = [b for b in significant_boxes if b['center_x'] >= 0.5 * w]
    
    # Filter out lone page numbers (len < 5 and near extreme borders)
    left_content = [b for b in left_boxes if not (len(b['text']) < 6 and b['min_x'] < 0.08 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    right_content = [b for b in right_boxes if not (len(b['text']) < 6 and b['max_x'] > 0.92 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    
    # Decide which side has the sidebar text:
    if len(left_content) >= 3 and len(right_content) <= 2:
        # Text is on the LEFT -> WALLPAPER PHOTO IS ON THE RIGHT!
        # The crop should take the RIGHT side, from ~0.45*w to w
        # Find the rightmost edge of left text
        max_left_x = max([b['max_x'] for b in left_content])
        crop_start_x = max(int(max_left_x + 15), int(w * 0.44))
        crop_box = (crop_start_x, 0, w, h)
        return {'page': pnum, 'type': 'PHOTO_ON_RIGHT', 'crop_box': crop_box, 'sidebar_side': 'LEFT', 'text_sample': [b['text'] for b in left_content[:3]]}
        
    elif len(right_content) >= 3 and len(left_content) <= 2:
        # Text is on the RIGHT -> WALLPAPER PHOTO IS ON THE LEFT!
        # The crop should take the LEFT side, from 0 to min_right_x
        min_right_x = min([b['min_x'] for b in right_content])
        crop_end_x = min(int(min_right_x - 15), int(w * 0.56))
        crop_box = (0, 0, crop_end_x, h)
        return {'page': pnum, 'type': 'PHOTO_ON_LEFT', 'crop_box': crop_box, 'sidebar_side': 'RIGHT', 'text_sample': [b['text'] for b in right_content[:3]]}
        
    else:
        # Either two-column or divider page or complex layout
        return {'page': pnum, 'type': 'COMPLEX', 'crop_box': (0, 0, w, h), 'left_count': len(left_content), 'right_count': len(right_content), 'left_sample': [b['text'] for b in left_content[:3]], 'right_sample': [b['text'] for b in right_content[:3]]}

# Test across pages 16, 33..57, and 121..160, 167
test_list = [16, 33, 34, 35, 36, 37] + list(range(39, 58)) + list(range(121, 161)) + [167]
results = {}
for p in test_list:
    r = analyze_crop(p)
    results[p] = r
    print(f"Page {p:03d} -> {r['type']} (Box: {r.get('crop_box')}) | Text on: {r.get('sidebar_side', r.get('type'))}")
