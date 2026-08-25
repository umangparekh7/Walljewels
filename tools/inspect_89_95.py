import json
import os
import glob
import time

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print("--- Current plates around index 85-98 ---")
for i in range(85, 98):
    if i < len(plates):
        p = plates[i]
        print(f"Index {i+1:03d} -> ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Img='{p.get('img')}'")

print("\n--- Newly uploaded images ---")
recent = []
for root, dirs, files in os.walk('C:/Users/Chintan Kamani/.gemini/antigravity-ide/brain/99a8f198-e31a-4099-b444-928a9a1ef591/.user_uploaded/'):
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            p = os.path.join(root, f)
            recent.append((p, os.path.getmtime(p), os.path.getsize(p)))

for r in sorted(recent, key=lambda x: x[1], reverse=True)[:8]:
    print(r[0], r[2])
