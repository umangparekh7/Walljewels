import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (63, "media_1787726871903.png", "assets/img/collection/kala-parampara/kp-plate-70.jpg"),
    (68, "media_1787726935203.png", "assets/img/collection/kala-parampara/kp-plate-76.jpg"),
    (69, "media_1787726965421.png", "assets/img/collection/kala-parampara/kp-plate-77.jpg"),
    (84, "media_1787727043034.png", "assets/img/collection/kala-rasa/kr-plate-022.jpg"),
    (85, "media_1787727067243.png", "assets/img/collection/kala-rasa/kr-plate-024.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 6 (63, 68, 69, 84, 85) replaced successfully!")
