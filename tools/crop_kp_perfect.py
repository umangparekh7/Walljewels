import pymupdf
import os
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
doc = pymupdf.open(kp_pdf)

kp_dir = 'assets/img/collection/kala-parampara'
os.makedirs(kp_dir, exist_ok=True)

# For each page from 6 to 77
for i in range(5, min(77, len(doc))):
    page_num = i + 1
    page = doc[i]
    pix = page.get_pixmap(dpi=200)
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    w, h = img.size
    
    # In Kala Parampara, the gold dividing line ends at 50.4% width
    # The pure room mockup begins at 50.5% width
    cropped = img.crop((int(w * 0.505), 0, w, h))
    out_path = os.path.join(kp_dir, f"kp-plate-{page_num:02d}.jpg")
    cropped.save(out_path, quality=95)

print("Cropped all Kala Parampara plates to pure wallpaper photos with ZERO sidebar!")
