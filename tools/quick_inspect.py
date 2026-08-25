import pymupdf
import io
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

def inspect_page(pnum):
    page = doc[pnum - 1]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    print(f"\n==================== PAGE {pnum} (w={w}, h={h}) ====================")
    if not res:
        print("  No text detected!")
        return
    for item in res:
        box, text, score = item[0], item[1], item[2]
        xs = [pt[0] for pt in box]
        ys = [pt[1] for pt in box]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        rel_x0, rel_x1 = min_x / w, max_x / w
        print(f"  [x={rel_x0:.2f}..{rel_x1:.2f}, y={min_y:.0f}..{max_y:.0f}]: {text}")

for p in [16, 33, 35, 40, 121, 133, 137, 159, 160, 167]:
    inspect_page(p)
