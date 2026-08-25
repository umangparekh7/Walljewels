import pymupdf
import io
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

print("Checking pages 121 to 160, 167...")
for p in list(range(121, 161)) + [167]:
    if p > len(doc):
        continue
    pix = doc[p - 1].get_pixmap(dpi=150)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if not res:
        print(f"Page {p:03d}: NO OCR TEXT DETECTED (Full spread)")
        continue
        
    left_boxes = []
    right_boxes = []
    for item in res:
        box, text = item[0], item[1]
        xs = [pt[0] for pt in box]
        avg_box_x = sum(xs) / len(xs)
        if avg_box_x < 0.5 * w:
            left_boxes.append((min(xs), max(xs), text))
        else:
            right_boxes.append((min(xs), max(xs), text))
            
    print(f"\nPage {p:03d}: Total text lines = {len(res)} (Left: {len(left_boxes)}, Right: {len(right_boxes)})")
    if left_boxes:
        sample_left = [b[2] for b in left_boxes[:3]]
        print(f"  LEFT text sample: {sample_left}")
    if right_boxes:
        sample_right = [b[2] for b in right_boxes[:3]]
        print(f"  RIGHT text sample: {sample_right}")
