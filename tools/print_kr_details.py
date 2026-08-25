import os
import json

# Let's inspect data.js for each plate from 121 to 160 and 167
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

kr_plates = [p for p in plates if p['v'] == 'kala-rasa']
print(f"Total KR plates: {len(kr_plates)}")

# Check pages 121 to 160, 167
for p in kr_plates:
    img = p['img']
    for target_p in list(range(121, 161)) + [167]:
        if f"-{target_p:03d}." in img or f"-{target_p}." in img:
            print(f"ID: {p['id']} | Code: {p.get('no')} | Img: {p['img']} | Name: {p['n']} | Sub: {p.get('sub')}")
