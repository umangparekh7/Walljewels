import json

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_ocr = json.load(f)

for entry in kr_ocr:
    if entry['page'] in [94, 95, 96, 97, 98]:
        print(f"\n--- Page {entry['page']} ---")
        for line in entry['lines']:
            print(f"  {line}")
