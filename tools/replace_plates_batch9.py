import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (113, "media_1787737022585.png", "assets/img/collection/kala-rasa/kr-plate-059.jpg"),
    (114, "media_1787737039826.png", "assets/img/collection/kala-rasa/kr-plate-060.jpg"),
    (115, "media_1787737058624.png", "assets/img/collection/kala-rasa/kr-plate-061.jpg"),
    (122, "media_1787737122428.png", "assets/img/collection/kala-rasa/kr-plate-069.jpg"),
    (124, "media_1787737149238.png", "assets/img/collection/kala-rasa/kr-plate-071.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 9 (113, 114, 115, 122, 124) replaced successfully!")
