import pymupdf
import io
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

def crop_page_by_ocr(doc, page_num, out_path):
    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=200)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if not res:
        img.save(out_path, quality=95)
        return "full"
        
    # Calculate average X position of text
    x_centers = []
    min_x = w
    max_x = 0
    for box, text, score in res:
        xs = [pt[0] for pt in box]
        x_centers.append(sum(xs) / len(xs))
        min_x = min(min_x, min(xs))
        max_x = max(max_x, max(xs))
        
    avg_x = sum(x_centers) / len(x_centers)
    
    # If text is predominantly on the right half (avg_x > 0.5 * w)
    if avg_x > 0.5 * w:
        # Photo is on the LEFT!
        crop_x = min(int(w * 0.60), int(min_x) - 10)
        crop_x = max(crop_x, int(w * 0.48))
        cropped = img.crop((0, 0, crop_x, h))
        cropped.save(out_path, quality=95)
        return f"LEFT PHOTO (0 to {crop_x})"
    else:
        # Text is on the left half -> Photo is on the RIGHT!
        crop_x = max(int(w * 0.40), int(max_x) + 10)
        crop_x = min(crop_x, int(w * 0.52))
        cropped = img.crop((crop_x, 0, w, h))
        cropped.save(out_path, quality=95)
        return f"RIGHT PHOTO ({crop_x} to {w})"

kp_doc = pymupdf.open(r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf')
for pnum in range(6, 16):
    r = crop_page_by_ocr(kp_doc, pnum, f"scratch/test_crop_kp_{pnum}.jpg")
    print(f"KP Page {pnum}: {r}")

kr_doc = pymupdf.open(r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf')
for pnum in range(8, 16):
    r = crop_page_by_ocr(kr_doc, pnum, f"scratch/test_crop_kr_{pnum}.jpg")
    print(f"KR Page {pnum}: {r}")
