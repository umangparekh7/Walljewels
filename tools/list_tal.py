import json, re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'\{\s*"id":\s*"([^"]+)",\s*"v":\s*"([^"]+)",\s*"n":\s*"([^"]+)",\s*"no":\s*"([^"]+)"[^}]+?"img":\s*"([^"]+)"', re.DOTALL)

plates = pattern.findall(text)

for idx, p in enumerate(plates):
    if 'TAL' in p[3] or idx >= 180:
        print(f"Index {idx+1} -> ID: {p[0]} | Code: {p[3]} | Name: {p[2]} | Img: {p[4]}")
