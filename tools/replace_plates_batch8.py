import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (108, "media_1787736793013.png", "assets/img/collection/kala-rasa/kr-plate-054.jpg"),
    (109, "media_1787736814404.png", "assets/img/collection/kala-rasa/kr-plate-055.jpg"),
    (110, "media_1787736837827.png", "assets/img/collection/kala-rasa/kr-plate-056.jpg"),
    (111, "media_1787736857095.png", "assets/img/collection/kala-rasa/kr-plate-057.jpg"),
    (112, "media_1787736883961.png", "assets/img/collection/kala-rasa/kr-plate-058.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 8 (108, 109, 110, 111, 112) replaced successfully!")
