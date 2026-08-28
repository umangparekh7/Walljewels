import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (201, "media_1787910502544.png", "assets/img/collection/kala-rasa/kr-plate-160.jpg"),
    (203, "media_1787910536592.png", "assets/img/collection/kala-rasa/kr-plate-162.jpg"),
    (204, "media_1787910557233.png", "assets/img/collection/kala-rasa/kr-plate-163.jpg"),
    (205, "media_1787910581403.png", "assets/img/collection/kala-rasa/kr-plate-164.jpg"),
    (206, "media_1787910599843.png", "assets/img/collection/kala-rasa/kr-plate-165.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 20 (201, 203, 204, 205, 206) replaced successfully!")
