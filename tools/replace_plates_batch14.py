import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (167, "media_1787899705715.png", "assets/img/collection/kala-rasa/kr-plate-115.jpg"),
    (168, "media_1787899754718.png", "assets/img/collection/kala-rasa/kr-plate-116.jpg"),
    (169, "media_1787899776045.png", "assets/img/collection/kala-rasa/kr-plate-118.jpg"),
    (171, "media_1787899808380.png", "assets/img/collection/kala-rasa/kr-plate-120.jpg"),
    (172, "media_1787899832931.png", "assets/img/collection/kala-rasa/kr-plate-121.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 14 (167, 168, 169, 171, 172) replaced successfully!")
