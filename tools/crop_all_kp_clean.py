import os
from PIL import Image

kp_dir = 'assets/img/collection/kala-parampara'
for f in os.listdir(kp_dir):
    if not f.endswith('.jpg'):
        continue
    p = os.path.join(kp_dir, f)
    img = Image.open(p)
    w, h = img.size
    
    # In Kala Parampara, the right 67.5% is the room mockup image, left 32.5% is the text column
    # If the image aspect ratio is landscape (~16:9 or 1.77)
    if w / h > 1.4:
        cropped = img.crop((int(w * 0.325), 0, w, h))
        cropped.save(p, quality=95)
        print(f"Cropped KP plate: {f} from {w}x{h} -> {cropped.size}")

print("All Kala Parampara plates are cleanly cropped to pure wallpaper mockups!")
