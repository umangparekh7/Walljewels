import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (38, "media_1787724159862.png", "assets/img/collection/kala-parampara/kp-plate-44.jpg"),
    (42, "media_1787724190437.png", "assets/img/collection/kala-parampara/kp-plate-48.jpg"),
    (47, "media_1787724240051.png", "assets/img/collection/kala-parampara/kp-plate-54.jpg"),
    (49, "media_1787724269935.png", "assets/img/collection/kala-parampara/kp-plate-56.jpg"),
    (50, "media_1787724290293.png", "assets/img/collection/kala-parampara/kp-plate-57.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 4 (38, 42, 47, 49, 50) replaced successfully!")
