import os
from PIL import Image

def crop_kala_parampara():
    kp_dir = 'assets/img/collection/kala-parampara'
    for f in os.listdir(kp_dir):
        if not f.endswith('.jpg'):
            continue
        p = os.path.join(kp_dir, f)
        img = Image.open(p)
        w, h = img.size
        # The room mockup in KP is located on the right (~32% to 100%)
        # For full-page spreads, keep full, for pages with left text bar, crop left 32%
        # Let's crop left text bar:
        cropped = img.crop((int(w * 0.325), 0, w, h))
        cropped.save(p, quality=95)
    print("Cropped all Kala Parampara wallpaper plates!")

def crop_kala_rasa():
    kr_dir = 'assets/img/collection/kala-rasa'
    for f in os.listdir(kr_dir):
        if not f.endswith('.jpg'):
            continue
        p = os.path.join(kr_dir, f)
        img = Image.open(p)
        w, h = img.size
        # The room mockup in KR is on the left (~0% to 58%)
        cropped = img.crop((0, 0, int(w * 0.575), h))
        cropped.save(p, quality=95)
    print("Cropped all Kala Rasa wallpaper plates!")

if __name__ == '__main__':
    crop_kala_parampara()
    crop_kala_rasa()
