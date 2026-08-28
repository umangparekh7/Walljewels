import os
from PIL import Image

base_upload_dir = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded"

replacements = [
    (184, "media_1787901599566.png", "assets/img/collection/kala-rasa/kr-plate-134.jpg"),
    (185, "media_1787901622738.png", "assets/img/collection/kala-rasa/kr-plate-135.jpg"),
    (188, "media_1787901702188.png", "assets/img/collection/kala-rasa/kr-plate-138.jpg"),
    (190, "media_1787901731647.png", "assets/img/collection/kala-rasa/kr-plate-140.jpg"),
    (191, "media_1787901753696.png", "assets/img/collection/kala-rasa/kr-plate-141.jpg"),
]

for num, src_name, dst_path in replacements:
    src_full = os.path.join(base_upload_dir, src_name)
    im = Image.open(src_full).convert('RGB')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    im.save(dst_path, 'JPEG', quality=95)
    print(f"Plate #{num} -> Replaced {dst_path} with {src_name} (Size: {im.size})")

# Delete kr-136 and kr-137 from data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find and remove kr-136 and kr-137 entries
# Each entry is { ... } inside window.DESIGNS array
pattern_136 = re.compile(r'\s*\{\s*"id":\s*"kr-136"[^}]+?\},\n?')
pattern_137 = re.compile(r'\s*\{\s*"id":\s*"kr-137"[^}]+?\},\n?')

new_content = pattern_136.sub('', content)
new_content = pattern_137.sub('', new_content)

if new_content != content:
    with open('assets/js/data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("\nSuccessfully removed kr-136 (#186) and kr-137 (#187) from assets/js/data.js!")
else:
    print("\nWARNING: Could not find kr-136 / kr-137 to remove!")

print("\nBatch 17 replaced & 186/187 deleted successfully!")
