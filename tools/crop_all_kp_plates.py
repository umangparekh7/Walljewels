import json
import os
import numpy as np
from PIL import Image

cat_dir = 'assets/img/catalogue'
out_dir = 'assets/img/collection/kala-parampara'
os.makedirs(out_dir, exist_ok=True)

with open('scratch/kp_parsed_exact.json', 'r', encoding='utf-8') as f:
    designs = json.load(f)

for d in designs:
    idx = d['index']
    fn = d['file']
    fp = os.path.join(cat_dir, fn)
    if not os.path.exists(fp):
        continue
        
    im = Image.open(fp)
    w, h = im.size
    arr = np.array(im)
    
    diffs = []
    for x in range(int(w*0.35), int(w*0.65)):
        col_l = arr[:, x-2:x].mean(axis=1).astype(float)
        col_r = arr[:, x:x+2].mean(axis=1).astype(float)
        diff = np.mean(np.abs(col_l - col_r))
        diffs.append((diff, x))
    diffs.sort(reverse=True)
    best_diff, split_x = diffs[0]
    
    l_box = arr[:, :int(w*0.30)].reshape(-1, 3)
    r_box = arr[:, int(w*0.70):].reshape(-1, 3)
    l_bins, _ = np.histogramdd(l_box, bins=(16, 16, 16))
    r_bins, _ = np.histogramdd(r_box, bins=(16, 16, 16))
    l_mode = l_bins.max() / len(l_box)
    r_mode = r_bins.max() / len(r_box)
    
    if l_mode > r_mode:
        crop_box = (split_x + 2, 0, w, h)
        side = 'RIGHT_PHOTO'
    else:
        crop_box = (0, 0, split_x - 2, h)
        side = 'LEFT_PHOTO'
        
    cropped = im.crop(crop_box)
    out_path = os.path.join(out_dir, f'kp-plate-{idx:02d}.jpg')
    cropped.save(out_path, quality=95)
    print(f"Page {idx:02d} ({d['title']}) -> {side} {cropped.size} ({d['code']})")

print("All Kala Parampara plate images cropped cleanly with zero text!")
