import os
from PIL import Image

def compare_images(pnum):
    raw_path = f"scratch/test_renders/raw_page_{pnum:03d}.jpg"
    curr_path = f"assets/img/collection/kala-rasa/kr-plate-{pnum:03d}.jpg"
    
    if os.path.exists(raw_path):
        with Image.open(raw_path) as r_img:
            rw, rh = r_img.size
    else:
        rw, rh = 0, 0
        
    if os.path.exists(curr_path):
        with Image.open(curr_path) as c_img:
            cw, ch = c_img.size
    else:
        cw, ch = 0, 0
        
    print(f"Page {pnum:03d} -> Raw: ({rw}x{rh}), Cropped: ({cw}x{ch})")

test_pages = [16, 33, 34, 35, 36, 37] + list(range(39, 58)) + [121, 122, 133, 137, 159, 160, 167]
for p in test_pages:
    compare_images(p)
