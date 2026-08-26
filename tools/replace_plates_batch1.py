import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (1, "media_1787723406554.png", "assets/img/collection/kala-parampara/kp-plate-06.jpg"),
    (3, "media_1787723485878.png", "assets/img/collection/kala-parampara/kp-plate-08.jpg"),
    (6, "media_1787723530308.png", "assets/img/collection/kala-parampara/kp-plate-11.jpg"),
    (8, "media_1787723563773.png", "assets/img/collection/kala-parampara/kp-plate-13.jpg"),
    (14, "media_1787723611906.png", "assets/img/collection/kala-parampara/kp-plate-19.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nAll 5 images replaced successfully!")
