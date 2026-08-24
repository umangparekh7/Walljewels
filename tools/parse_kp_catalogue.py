import json
import re
import os

with open('scratch/kp_ocr_results.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    idx = p['index']
    fn = p['file']
    lines = p['texts']
    
    print(f"\n==================== PAGE {idx:02d} ({fn}) ====================")
    for i, line in enumerate(lines):
        print(f"  [{i:02d}] {line}")
