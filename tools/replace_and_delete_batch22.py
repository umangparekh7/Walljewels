import os, re
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

# Replace 211
src_full = os.path.join(base_upload_dir, "media_1787911544538.png")
dst_path = "assets/img/collection/kala-rasa/kr-plate-170.jpg"
im = Image.open(src_full).convert('RGB')
os.makedirs(os.path.dirname(dst_path), exist_ok=True)
im.save(dst_path, 'JPEG', quality=95)
print(f"Plate #211 -> Replaced {dst_path} with media_1787911544538.png (Size: {im.size})")

# Delete 212 to 215 from data.js
to_delete_ids = ['kr-171', 'kr-172', 'kr-173', 'kr-174']

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

print("\nBatch 22 replacement and deletion complete!")
