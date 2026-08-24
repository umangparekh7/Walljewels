import json
import os

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract json
json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

print(f"Total plates in data.js: {len(plates)}")

# Check each query
queries = [
    "Sanjeevani",
    "Durga",
    "32", "33", "34",
    "Forest Arches",
    "Enthroned",
    "CONTINUES",
    "Chola Temple",
    "Gopuram Grandeur",
    "Bronze and Lotus",
    "Thanjavur Golden",
    "Temple Corridor"
]

for q in queries:
    matches = [p for p in plates if q.lower() in p['n'].lower() or q.lower() in p['sub'].lower() or q.lower() in p['id'].lower() or q.lower() in p['no'].lower()]
    print(f"\n--- QUERY: '{q}' ({len(matches)} matches) ---")
    for m in matches:
        print(f"ID: {m['id']} | Vol: {m['v']} | No: {m['no']} | Name: {m['n']} | Sub: {m['sub']} | Img: {m['img']}")
