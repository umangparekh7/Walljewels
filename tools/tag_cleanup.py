import json, re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect all plates
pattern = re.compile(r'\{\s*"id":\s*"([^"]+)",\s*"v":\s*"([^"]+)",\s*"n":\s*"([^"]+)",\s*"no":\s*"([^"]+)",\s*"sub":\s*"([^"]*)",\s*"b":\s*"([^"]*)",\s*"style":\s*"([^"]*)",\s*"palette":\s*"([^"]*)",\s*"ideal":\s*"([^"]*)",\s*"img":\s*"([^"]+)",\s*"sp":\s*"([^"]*)",\s*"cat":\s*"([^"]*)"\s*\}')

plates = pattern.findall(text)
print(f"Found {len(plates)} formatted plates in data.js")

for p in plates[:15]:
    print(f"{p[3]} | {p[2]} | v:{p[1]} | cat:{p[11]} | sp:{p[10]} | ideal:{p[8]}")
