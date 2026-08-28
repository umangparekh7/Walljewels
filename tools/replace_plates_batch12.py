import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (140, "media_1787898131886.png", "assets/img/collection/kala-rasa/kr-plate-087.jpg"),
    (142, "media_1787898152577.png", "assets/img/collection/kala-rasa/kr-plate-089.jpg"),
    (145, "media_1787898204940.png", "assets/img/collection/kala-rasa/kr-plate-093.jpg"),
    (149, "media_1787898241271.png", "assets/img/collection/kala-rasa/kr-plate-097.jpg"),
    (154, "media_1787898284798.png", "assets/img/collection/kala-rasa/kr-plate-102.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 12 (140, 142, 145, 149, 154) replaced successfully!")
