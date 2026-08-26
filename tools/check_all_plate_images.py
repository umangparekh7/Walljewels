import json
import os

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print(f"Total plates in data.js: {len(plates)}")
for i, p in enumerate(plates[:110]):
    img_path = p['img']
    exists = os.path.exists(img_path)
    sz = os.path.getsize(img_path) if exists else 0
    if not exists or sz < 1000:
        print(f"ERR: #{i+1:03d} -> ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Img='{img_path}' (EXISTS={exists}, SIZE={sz})")
    else:
        # print first 15 and 85-105
        if i < 5 or (85 <= i <= 106):
            print(f"#{i+1:03d} -> ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Img='{img_path}' ({sz} bytes)")
