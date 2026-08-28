import os, re
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (195, "media_1787909431825.png", "assets/img/collection/kala-rasa/kr-plate-147.jpg"),
    (196, "media_1787909606514.png", "assets/img/collection/kala-rasa/kr-plate-148.jpg"),
    (197, "media_1787909621666.png", "assets/img/collection/kala-rasa/kr-plate-149.jpg"),
    (198, "media_1787909642968.png", "assets/img/collection/kala-rasa/kr-plate-150.jpg"),
    (204, "media_1787909735725.png", "assets/img/collection/kala-rasa/kr-plate-156.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

# Delete 199, 200, 201, 202, 205, 206 from data.js
to_delete_ids = ['kr-151', 'kr-152', 'kr-153', 'kr-154', 'kr-157', 'kr-158']

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

for did in to_delete_ids:
    pat = re.compile(rf'\s*\{{\s*"id":\s*"{did}"[^}}]+?\}},\n?')
    content, count = pat.subn('', content)
    print(f"Deleted {did} from data.js: {count} occurrence(s)")

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Delete image files
for did in to_delete_ids:
    num_str = did.replace('kr-', '')
    img_path = f"assets/img/collection/kala-rasa/kr-plate-{num_str}.jpg"
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f"Removed image file {img_path}")

print("\nBatch 19 replacements and deletions complete!")
