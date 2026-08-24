from PIL import Image

# For KP Page 6, 7, 8, 9
for pnum in [6, 7, 8, 9]:
    img = Image.open(f"scratch/raw_kp_{pnum}.jpg")
    w, h = img.size
    # Let's save left 60% and right 60%
    left_crop = img.crop((0, 0, int(w * 0.60), h))
    right_crop = img.crop((int(w * 0.40), 0, w, h))
    left_crop.save(f"scratch/kp_{pnum}_left.jpg")
    right_crop.save(f"scratch/kp_{pnum}_right.jpg")
    print(f"Saved KP {pnum} left & right crops")

# For KR Page 8, 9
for pnum in [8, 9]:
    img = Image.open(f"scratch/raw_kr_{pnum}.jpg")
    w, h = img.size
    left_crop = img.crop((0, 0, int(w * 0.60), h))
    right_crop = img.crop((int(w * 0.40), 0, w, h))
    left_crop.save(f"scratch/kr_{pnum}_left.jpg")
    right_crop.save(f"scratch/kr_{pnum}_right.jpg")
    print(f"Saved KR {pnum} left & right crops")
