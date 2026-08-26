import json, re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect CATEGORIES and SPACES definitions
cat_match = re.search(r'const CATEGORIES\s*=\s*(\[.*?\]);', code, re.DOTALL)
sp_match = re.search(r'const SPACES\s*=\s*(\[.*?\]);', code, re.DOTALL)
vol_match = re.search(r'const VOLUMES\s*=\s*(\[.*?\]);', code, re.DOTALL)

print("CATEGORIES:", cat_match.group(1) if cat_match else "None")
print("SPACES:", sp_match.group(1) if sp_match else "None")
print("VOLUMES:", vol_match.group(1) if vol_match else "None")

# Inspect actual plates
# Extract all values of cat, sp, c, s
all_cats = re.findall(r'[\'"](?:cat|c)[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', code)
all_sps = re.findall(r'[\'"](?:sp|s)[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', code)
all_vs = re.findall(r'[\'"]v[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', code)

from collections import Counter
print("\nUnique 'cat' values in COLLECTION:", Counter(all_cats))
print("\nUnique 'sp' values in COLLECTION:", Counter(all_sps))
print("\nUnique 'v' values in COLLECTION:", Counter(all_vs))
