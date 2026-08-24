import pymupdf
from PIL import Image, ImageStat
import numpy as np

def detect_and_crop_photo(img):
    w, h = img.size
    # Split into left half (0 to 58%) and right half (42% to 100%)
    left = img.crop((0, 0, int(w * 0.58), h))
    right = img.crop((int(w * 0.42), 0, w, h))
    
    # Calculate standard deviation of pixels (room photo has high std dev, editorial text has low std dev)
    stat_l = ImageStat.Stat(left)
    stat_r = ImageStat.Stat(right)
    
    std_l = sum(stat_l.stddev) / len(stat_l.stddev)
    std_r = sum(stat_r.stddev) / len(stat_r.stddev)
    
    # If left has significantly higher variance, photo is on the left
    # If right has higher variance, photo is on the right
    if std_l >= std_r:
        # Photo is on the left
        return left, 'left', std_l, std_r
    else:
        # Photo is on the right
        return right, 'right', std_l, std_r

# Let's test on KP pages 6 to 15
kp_doc = pymupdf.open(r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf')
for pnum in range(6, 16):
    page = kp_doc[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"scratch/raw_{pnum}.png")
    img = Image.open(f"scratch/raw_{pnum}.png")
    cropped, side, sl, sr = detect_and_crop_photo(img)
    cropped.save(f"scratch/detected_kp_{pnum}.jpg")
    print(f"KP Page {pnum}: detected photo on {side.upper()} (std_l={sl:.1f}, std_r={sr:.1f})")

# Let's test on KR pages 8 to 15
kr_doc = pymupdf.open(r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf')
for pnum in range(8, 16):
    page = kr_doc[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"scratch/raw_kr_{pnum}.png")
    img = Image.open(f"scratch/raw_kr_{pnum}.png")
    cropped, side, sl, sr = detect_and_crop_photo(img)
    cropped.save(f"scratch/detected_kr_{pnum}.jpg")
    print(f"KR Page {pnum}: detected photo on {side.upper()} (std_l={sl:.1f}, std_r={sr:.1f})")
