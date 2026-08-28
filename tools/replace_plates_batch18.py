import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (190, "media_1787903190281.png", "assets/img/collection/kala-rasa/kr-plate-142.jpg"),
    (191, "media_1787903216153.png", "assets/img/collection/kala-rasa/kr-plate-143.jpg"),
    (192, "media_1787903234834.png", "assets/img/collection/kala-rasa/kr-plate-144.jpg"),
    (193, "media_1787903255055.png", "assets/img/collection/kala-rasa/kr-plate-145.jpg"),
    (194, "media_1787903272615.png", "assets/img/collection/kala-rasa/kr-plate-146.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 18 (190, 191, 192, 193, 194) replaced successfully!")
