import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (159, "media_1787898984084.png", "assets/img/collection/kala-rasa/kr-plate-107.jpg"),
    (160, "media_1787899002380.png", "assets/img/collection/kala-rasa/kr-plate-108.jpg"),
    (162, "media_1787899028819.png", "assets/img/collection/kala-rasa/kr-plate-110.jpg"),
    (163, "media_1787899049935.png", "assets/img/collection/kala-rasa/kr-plate-111.jpg"),
    (166, "media_1787899084978.png", "assets/img/collection/kala-rasa/kr-plate-114.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 13 (159, 160, 162, 163, 166) replaced successfully!")
