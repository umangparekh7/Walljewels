import pymupdf
import io
import os
import numpy as np
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('scratch/test_side_detection', exist_ok=True)

def detect_photo_side(page):
    pix = page.get_pixmap(dpi=72)
    img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    
    left = arr[:, :int(w * 0.48)]
    right = arr[:, int(w * 0.52):]
    
    # Measure image detail: standard deviation of color + edge energy
    # Text sidebar has a flat solid background -> low std dev across large patches
    # Photo has high variance across the entire field
    left_std = np.std(left)
    right_std = np.std(right)
    
    # Also check fraction of pixels that are near the background color (flat area)
    # A sidebar is >60% identical solid color
    def flat_fraction(half):
        # find most common color bin
        hist, _ = np.histogramdd(half.reshape(-1, 3), bins=(8, 8, 8))
        max_bin = np.max(hist)
        return max_bin / (half.shape[0] * half.shape[1])
        
    left_flat = flat_fraction(left)
    right_flat = flat_fraction(right)
    
    # The half with higher flat fraction is the TEXT SIDEBAR!
    # The half with lower flat fraction is the PHOTO!
    if left_flat > right_flat + 0.05:
        # Left is sidebar -> Photo is on RIGHT
        return 'RIGHT', (int(w * 0.46), 0, w, h), left_flat, right_flat
    elif right_flat > left_flat + 0.05:
        # Right is sidebar -> Photo is on LEFT
        return 'LEFT', (0, 0, int(w * 0.54), h), left_flat, right_flat
    else:
        # Fallback to std dev
        if left_std > right_std:
            return 'LEFT (by std)', (0, 0, int(w * 0.54), h), left_flat, right_flat
        else:
            return 'RIGHT (by std)', (int(w * 0.46), 0, w, h), left_flat, right_flat

print("Testing side detection on KP pages 6 to 25:")
for p in range(6, 26):
    side, box, lf, rf = detect_photo_side(doc_kp[p - 1])
    print(f"KP Page {p:02d} -> Photo on {side} (L_flat={lf:.2f}, R_flat={rf:.2f})")
