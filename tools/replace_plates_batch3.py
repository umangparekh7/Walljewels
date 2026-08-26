import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (26, "media_1787723927385.png", "assets/img/collection/kala-parampara/kp-plate-31.jpg"),
    (31, "media_1787723991220.png", "assets/img/collection/kala-parampara/kp-plate-37.jpg"),
    (32, "media_1787724017236.png", "assets/img/collection/kala-parampara/kp-plate-38.jpg"),
    (33, "media_1787724033151.png", "assets/img/collection/kala-parampara/kp-plate-39.jpg"),
    (37, "media_1787724070622.png", "assets/img/collection/kala-parampara/kp-plate-43.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 3 (26, 31, 32, 33, 37) replaced successfully!")
