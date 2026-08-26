import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (52, "media_1787726732721.png", "assets/img/collection/kala-parampara/kp-plate-59.jpg"),
    (53, "media_1787726752023.png", "assets/img/collection/kala-parampara/kp-plate-60.jpg"),
    (55, "media_1787726779399.png", "assets/img/collection/kala-parampara/kp-plate-62.jpg"),
    (58, "media_1787726803419.png", "assets/img/collection/kala-parampara/kp-plate-65.jpg"),
    (61, "media_1787726838552.png", "assets/img/collection/kala-parampara/kp-plate-68.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 5 (52, 53, 55, 58, 61) replaced successfully!")
