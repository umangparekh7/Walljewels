import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

for i in range(50, 78):
    if i < len(plates):
        p = plates[i]
        print(f"#{i+1:03d} -> ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Sub='{p.get('sub')}', Img='{p.get('img')}'")
