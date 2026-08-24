import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

targets = ['kp-15', 'kr-016', 'kr-032', 'kr-033', 'kr-034', 'kr-035', 'kr-037', 'kr-039', 'kr-040', 'kr-041', 'kr-042', 'kr-043']
print(f"Total valid plates: {len(plates)}")
for tid in targets:
    p = next((x for x in plates if x['id'] == tid), None)
    if p:
        print(f"[{p['id']}] {p['no']} | Name: {p['n']} | Sub: {p['sub']}")
    else:
        print(f"[{tid}] NOT FOUND")
