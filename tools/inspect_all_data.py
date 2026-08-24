import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Let's extract COLLECTION array
match = re.search(r'const COLLECTION\s*=\s*(\[.*?\]);', js_text, re.DOTALL)
if match:
    # Convert JS object literal to JSON
    json_like = match.group(1)
    # quote unquoted keys
    json_like = re.sub(r'(\s*)(id|v|n|no|sub|b|img|sp|cat|tag):', r'\1"\2":', json_like)
    # remove trailing commas
    json_like = re.sub(r',\s*([\]}])', r'\1', json_like)
    data = json.loads(json_like)
    print(f"Loaded {len(data)} items from data.js")
    
    kp_items = [d for d in data if d.get('v') == 'kala-parampara']
    kr_items = [d for d in data if d.get('v') == 'kala-rasa']
    print(f"Kala Parampara items: {len(kp_items)}")
    print(f"Kala Rasa items: {len(kr_items)}")
    
    print("\n--- First 15 Kala Parampara Items ---")
    for d in kp_items[:15]:
        print(f"{d['id']} | {d['no']} | {d['n']} | {d.get('sub', '')} | img: {d['img']}")
        
    print("\n--- First 15 Kala Rasa Items ---")
    for d in kr_items[:15]:
        print(f"{d['id']} | {d['no']} | {d['n']} | {d.get('sub', '')} | img: {d['img']}")
