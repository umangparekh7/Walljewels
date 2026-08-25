import pymupdf
import os
from PIL import Image

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

os.makedirs('scratch/inspections', exist_ok=True)

# For pages 121..160, and 167, and also 16, 33..57:
# Let's save a side-by-side or overview of:
# (Left half of PDF), (Right half of PDF), and (Current cropped image in assets/img)
for p in list(range(121, 161)) + [167, 16, 33, 34, 35, 36, 37, 44, 46, 50]:
    if p <= len(doc):
        pix = doc[p - 1].get_pixmap(dpi=100)
        img = Image.open(pymupdf.io.BytesIO(pix.tobytes('png')))
        w, h = img.size
        # Left half
        left_half = img.crop((0, 0, int(w * 0.55), h))
        # Right half
        right_half = img.crop((int(w * 0.45), 0, w, h))
        
        left_half.save(f'scratch/inspections/p_{p:03d}_left.jpg', quality=80)
        right_half.save(f'scratch/inspections/p_{p:03d}_right.jpg', quality=80)

print("Saved left and right halves for inspection in scratch/inspections/")
