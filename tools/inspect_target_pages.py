import json
import os

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print('Total plates in data.js:', len(plates))

target_codes = [
    'WJWP-DVN-035', 'WJWP-DVN-052', 'WJWP-DVN-053', 'WJWP-DVN-054', 'WJWP-DVN-055', 'WJWP-DVN-056',
    'WJWP-SIH-012', 'WJWP-SIH-013', 'WJWP-SIH-014', 'WJWP-SIH-015', 'WJWP-SIH-016', 'WJWP-SIH-017',
    'WJWP-SIH-018', 'WJWP-SIH-019', 'WJWP-SIH-020', 'WJWP-SIH-021', 'WJWP-SIH-022', 'WJWP-SIH-023',
    'WJWP-SIH-024', 'WJWP-SIH-025', 'WJWP-SIH-026', 'WJWP-SIH-027', 'WJWP-SIH-028', 'WJWP-SIH-029',
    'WJWP-SIH-030'
]

print("\n=== TARGET CODES FROM USER REQUEST ===")
for code in target_codes:
    matched = [p for p in plates if p.get('no') == code]
    if matched:
        for p in matched:
            print(f"{code} -> ID: {p['id']}, Name: '{p['n']}', Sub: '{p.get('sub','')}', Img: {p['img']}")
    else:
        print(f"{code} -> NOT FOUND IN data.js!")

# print("\n=== PLATES WITH IMG NUMBERS 121 TO 160, 167 ===")
# for p in plates:
#     img = p['img']
#     for num in list(range(121, 161)) + [167]:
#         if f"-{num}." in img or f"-{num:03d}." in img:
#             print(f"Num {num} -> ID: {p['id']}, Code: {p.get('no')}, Name: '{p['n']}', Sub: '{p.get('sub','')}', Img: {p['img']}")
