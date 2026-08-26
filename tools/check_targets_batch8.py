import json, re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'\{\s*"id":\s*"([^"]+)",\s*"v":\s*"([^"]+)",\s*"n":\s*"([^"]+)",\s*"no":\s*"([^"]+)",\s*"sub":\s*"([^"]*)",\s*"b":\s*"([^"]*)",\s*"style":\s*"([^"]*)",\s*"palette":\s*"([^"]*)",\s*"ideal":\s*"([^"]*)",\s*"img":\s*"([^"]+)",\s*"sp":\s*"([^"]*)",\s*"cat":\s*"([^"]*)"\s*\}')

plates = pattern.findall(text)

targets = [108, 109, 110, 111, 112]
for t in targets:
    idx = t - 1
    p = plates[idx]
    print(f"#{t} -> ID: {p[0]} | Code: {p[3]} | Name: {p[2]} | Img: {p[9]}")
