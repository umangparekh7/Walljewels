import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print(f"Auditing all {len(plates)} plates in data.js...")

for i, p in enumerate(plates):
    name = p.get('n', '')
    sub = p.get('sub', '')
    desc = p.get('b', '')
    
    # Check for CamelCase jams without space like "OneDeity,FourRegisters" or "FountainsandFlora"
    camels = re.findall(r'[a-z][A-Z]', name)
    if camels and not any(k in name for k in ['Mc', 'Mac', 'iPhone', 'iPad']):
        print(f"[{p['id']}] CamelCase in Name: '{name}'")
        
    camels_sub = re.findall(r'[a-z][A-Z]', sub)
    if camels_sub:
        print(f"[{p['id']}] CamelCase in Sub: '{sub}'")
        
    # Check if name is numeric or too short
    if name.isdigit() or len(name) < 3:
        print(f"[{p['id']}] Suspicious Name: '{name}'")
        
    # Check if subtitle is too long (e.g. paragraph in sub)
    if len(sub) > 90:
        print(f"[{p['id']}] Very long Sub: '{sub}'")
