import json

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries in kr_full_raw_ocr.json: {len(data)}")

# Let's inspect some pages: 16, 33..57, and 121..160, 167
for entry in data:
    p = entry.get('page')
    if p in [16, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 121, 122, 133, 137, 159, 160, 167]:
        print(f"\n--- PAGE {p} ---")
        for line in entry.get('lines', [])[:10]:
            print(f"  {line}")
