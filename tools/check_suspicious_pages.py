import json

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_ocr = json.load(f)

for entry in kr_ocr:
    if entry['page'] in [31, 32, 116, 117, 118, 184, 185, 186]:
        print(f"\n--- PAGE {entry['page']} ---")
        for l in entry['lines']:
            print(f"  {l}")
