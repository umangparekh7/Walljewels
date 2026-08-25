import json

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_ocr = json.load(f)

# Let's inspect each entry in kr_ocr for page 121..160, 167
for entry in kr_ocr:
    p = entry['page']
    if p in list(range(121, 161)) + [167]:
        print(f"\n================ PAGE {p} ================")
        for line in entry['lines']:
            print(f"  {line}")
