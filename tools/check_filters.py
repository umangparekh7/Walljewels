import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse collection items
# Each item has img: "...", v: "...", c: "...", s: "..."
plates = re.findall(r'\{\s*img:\s*[\'"]([^\'"]+)[\'"],\s*n:\s*[\'"]([^\'"]+)[\'"].*?v:\s*[\'"]([^\'"]+)[\'"].*?c:\s*[\'"]([^\'"]+)[\'"].*?s:\s*[\'"]([^\'"]+)[\'"]', text, re.DOTALL)
print(f"Parsed {len(plates)} plates from data.js")

with open('collection.html', 'r', encoding='utf-8') as f:
    html = f.read()

chips = re.findall(r'data-filter=[\'"]([^\'"]+)[\'"]', html)
print(f"Filter chips found in HTML ({len(chips)}):", chips)
