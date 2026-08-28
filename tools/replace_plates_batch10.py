import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (125, "media_1787897649149.png", "assets/img/collection/kala-rasa/kr-plate-072.jpg"),
    (126, "media_1787897684498.png", "assets/img/collection/kala-rasa/kr-plate-073.jpg"),
    (128, "media_1787897710169.png", "assets/img/collection/kala-rasa/kr-plate-075.jpg"),
    (129, "media_1787897729442.png", "assets/img/collection/kala-rasa/kr-plate-076.jpg"),
    (130, "media_1787897748420.png", "assets/img/collection/kala-rasa/kr-plate-077.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 10 (125, 126, 128, 129, 130) replaced successfully!")
