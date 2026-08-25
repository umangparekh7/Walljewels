import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print("--- Inspecting indices 25 to 35 ---")
for i in range(25, 36):
    if i < len(plates):
        p = plates[i]
        print(f"Index {i+1}: ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Sub='{p.get('sub')}', Blurb='{p.get('b')[:60]}...'")

print("\n--- Inspecting indices 45 to 55 ---")
for i in range(45, 56):
    if i < len(plates):
        p = plates[i]
        print(f"Index {i+1}: ID={p['id']}, Code={p.get('no')}, Name='{p.get('n')}', Sub='{p.get('sub')}', Blurb='{p.get('b')[:60]}...'")
