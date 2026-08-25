import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

for pid in ['kr-094', 'kr-095', 'kr-096', 'kr-097', 'kr-098', 'kr-099', 'kr-100', 'kr-101', 'kr-102', 'kr-103', 'kr-104']:
    match = [p for p in plates if p['id'] == pid]
    if match:
        p = match[0]
        print(f"{p['id']} ({p.get('no')}): Title='{p['n']}', Sub='{p['sub']}', Blurb='{p['b'][:80]}...', Img='{p['img']}'")
