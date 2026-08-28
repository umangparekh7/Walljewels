import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (179, "media_1787900466098.png", "assets/img/collection/kala-rasa/kr-plate-128.jpg"),
    (180, "media_1787900488462.png", "assets/img/collection/kala-rasa/kr-plate-129.jpg"),
    (181, "media_1787900505521.png", "assets/img/collection/kala-rasa/kr-plate-130.jpg"),
    (182, "media_1787900521740.png", "assets/img/collection/kala-rasa/kr-plate-131.jpg"),
    (183, "media_1787900539807.png", "assets/img/collection/kala-rasa/kr-plate-132.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 16 (179, 180, 181, 182, 183) replaced successfully!")
