import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (173, "media_1787900247520.png", "assets/img/collection/kala-rasa/kr-plate-122.jpg"),
    (174, "media_1787900269980.png", "assets/img/collection/kala-rasa/kr-plate-123.jpg"),
    (175, "media_1787900289797.png", "assets/img/collection/kala-rasa/kr-plate-124.jpg"),
    (177, "media_1787900317168.png", "assets/img/collection/kala-rasa/kr-plate-126.jpg"),
    (178, "media_1787900338443.png", "assets/img/collection/kala-rasa/kr-plate-127.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 15 (173, 174, 175, 177, 178) replaced successfully!")
