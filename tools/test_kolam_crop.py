import pymupdf
import io
import os
from PIL import Image

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('scratch/test_perfect_crops', exist_ok=True)

# Test on 94, 96, 98 (even) and 95, 97, 99 (odd)
for p in [94, 95, 96, 97, 98, 99]:
    page = doc_kr[p - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    if p % 2 == 0:
        # Even -> wallpaper is on LEFT
        cropped = img.crop((0, 0, int(w * 0.445), h))
    else:
        # Odd -> wallpaper is on RIGHT
        cropped = img.crop((int(w * 0.465), 0, w, h))
    cropped.save(f"scratch/test_perfect_crops/p_{p:03d}.jpg", quality=95)
    print(f"Saved page {p}: size = {cropped.size}")

print("Saved all test crops!")
