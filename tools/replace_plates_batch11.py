import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (132, "media_1787897939744.png", "assets/img/collection/kala-rasa/kr-plate-079.jpg"),
    (134, "media_1787897973844.png", "assets/img/collection/kala-rasa/kr-plate-081.jpg"),
    (136, "media_1787898000955.png", "assets/img/collection/kala-rasa/kr-plate-083.jpg"),
    (138, "media_1787898032854.png", "assets/img/collection/kala-rasa/kr-plate-085.jpg"),
    (139, "media_1787898055296.png", "assets/img/collection/kala-rasa/kr-plate-086.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 11 (132, 134, 136, 138, 139) replaced successfully!")
