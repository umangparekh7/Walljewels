import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (86, "media_1787727343900.png", "assets/img/collection/kala-rasa/kr-plate-025.jpg"),
    (87, "media_1787727362950.png", "assets/img/collection/kala-rasa/kr-plate-026.jpg"),
    (88, "media_1787727381404.png", "assets/img/collection/kala-rasa/kr-plate-027.jpg"),
    (105, "media_1787727448308.png", "assets/img/collection/kala-rasa/kr-plate-051.jpg"),
    (107, "media_1787727478787.png", "assets/img/collection/kala-rasa/kr-plate-053.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 7 (86, 87, 88, 105, 107) replaced successfully!")
