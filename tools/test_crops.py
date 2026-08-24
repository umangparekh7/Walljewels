import pymupdf
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

# Render full uncropped page 6, 8, 9 of KP
for pnum in [6, 7, 8, 9, 10, 11, 33, 45]:
    page = doc_kp[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"scratch/raw_kp_{pnum}.jpg")
    img = Image.open(f"scratch/raw_kp_{pnum}.jpg")
    print(f"KP Page {pnum} dimensions:", img.size)

# Render full uncropped page 8, 9, 10 of KR
for pnum in [8, 9, 10, 11, 50, 100]:
    page = doc_kr[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"scratch/raw_kr_{pnum}.jpg")
    img = Image.open(f"scratch/raw_kr_{pnum}.jpg")
    print(f"KR Page {pnum} dimensions:", img.size)
