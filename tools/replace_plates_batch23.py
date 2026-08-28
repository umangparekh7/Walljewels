import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (213, "media_1787912431414.png", "assets/img/collection/kala-rasa/kr-plate-176.jpg"),
    (214, "media_1787912451109.png", "assets/img/collection/kala-rasa/kr-plate-177.jpg"),
    (215, "media_1787912468663.png", "assets/img/collection/kala-rasa/kr-plate-178.jpg"),
    (217, "media_1787912489766.png", "assets/img/collection/kala-rasa/kr-plate-180.jpg"),
    (218, "media_1787912511015.png", "assets/img/collection/kala-rasa/kr-plate-181.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

print("\nBatch 23 (213, 214, 215, 217, 218) replaced successfully!")
