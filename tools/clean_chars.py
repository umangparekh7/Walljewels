import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any stray replacement character with clean bullet
text = re.sub(r'\ufffd', ' · ', text)
text = re.sub(r'\s*·\s*', ' · ', text)

# Typo fixes
text = text.replace('Epicdevotion onamonumental scale.', 'Epic devotion on a monumental scale.')
text = text.replace('He ritage', 'Heritage')
text = text.replace('Contemporary He ritage', 'Contemporary Heritage')
text = text.replace('Luxury Patte rn', 'Luxury Pattern')
text = text.replace('Botanical SacredArt', 'Botanical Sacred Art')

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Polished data.js successfully!")
