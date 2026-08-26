import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (16, "media_1787723799523.png", "assets/img/collection/kala-parampara/kp-plate-21.jpg"),
    (17, "media_1787723823232.png", "assets/img/collection/kala-parampara/kp-plate-22.jpg"),
    (21, "media_1787723857673.png", "assets/img/collection/kala-parampara/kp-plate-26.jpg"),
    (23, "media_1787723881079.png", "assets/img/collection/kala-parampara/kp-plate-28.jpg"),
    (25, "media_1787723902562.png", "assets/img/collection/kala-parampara/kp-plate-30.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 2 (16, 17, 21, 23, 25) replaced successfully!")
