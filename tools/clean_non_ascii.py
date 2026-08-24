with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any character with code > 127 that isn't ₹ with · or proper ascii
clean = []
for ch in text:
    if ch == '₹' or ord(ch) < 128:
        clean.append(ch)
    else:
        clean.append(' · ')

text = "".join(clean)
import re
text = re.sub(r'(\s*·\s*)+', ' · ', text)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced all non-ascii characters with clean bullet symbols!")
