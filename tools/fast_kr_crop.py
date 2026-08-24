import pymupdf
import io
import os
from PIL import Image
from concurrent.futures import ProcessPoolExecutor

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

def crop_single_kr(pnum):
    doc = pymupdf.open(kr_pdf)
    page = doc[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    
    out_path = f"assets/img/collection/kala-rasa/kr-plate-{pnum:03d}.jpg"
    
    # In Kala Rasa, even page = Photo on LEFT, odd page = Photo on RIGHT
    if pnum % 2 == 0:
        # Photo is on LEFT
        cropped = img.crop((0, 0, int(w * 0.58), h))
    else:
        # Photo is on RIGHT
        cropped = img.crop((int(w * 0.42), 0, w, h))
        
    cropped.save(out_path, quality=95)
    return pnum

if __name__ == '__main__':
    doc = pymupdf.open(kr_pdf)
    total_pages = len(doc)
    pages = list(range(8, min(186, total_pages + 1)))
    
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(crop_single_kr, pages))
        
    print(f"Fast cropped {len(results)} Kala Rasa plates in parallel!")
