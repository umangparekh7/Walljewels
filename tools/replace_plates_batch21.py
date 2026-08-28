import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (207, "media_1787910631386.png", "assets/img/collection/kala-rasa/kr-plate-166.jpg"),
    (208, "media_1787910653091.png", "assets/img/collection/kala-rasa/kr-plate-167.jpg"),
    (209, "media_1787910668892.png", "assets/img/collection/kala-rasa/kr-plate-168.jpg"),
    (210, "media_1787910684808.png", "assets/img/collection/kala-rasa/kr-plate-169.jpg"),
    (211, "media_1787910720923.png", "assets/img/collection/kala-rasa/kr-plate-170.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 21 (207, 208, 209, 210, 211) replaced successfully!")
