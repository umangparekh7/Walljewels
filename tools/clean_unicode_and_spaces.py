import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any broken unicode or non-ascii oddities with standard clean middot ·
content = content.replace('', '·')
content = content.replace('\ufffd', '·')

# Fix common OCR typos in subtitles and descriptions
sub_fixes = [
    ('Epicdevotion onamonumental scale.', 'Epic devotion on a monumental scale.'),
    ('He ritage', 'Heritage'),
    ('Contemporary He ritage', 'Contemporary Heritage'),
    ('Luxury Patte rn', 'Luxury Pattern'),
    ('saicred', 'sacred'),
    ('silhoue tte s', 'silhouettes'),
    ('AVI BLE', 'AVAILABLE'),
    ('CUSTOMSIZEAVAILABLE', 'Custom Size Available'),
    ('Traditional Pic hwai', 'Traditional Pichwai'),
    ('StorybookMural', 'Storybook Mural'),
    ('PortraitMural', 'Portrait Mural'),
    ('PathwaysofAntiquity', 'Pathways of Antiquity'),
    ('OrnamentalHeritage', 'Ornamental Heritage'),
    ('MonumentalElegance', 'Monumental Elegance'),
    ('RepeatingElegance', 'Repeating Elegance'),
    ('Refined Geometry', 'Refined Geometry')
]

for orig, repl in sub_fixes:
    content = content.replace(orig, repl)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned all Unicode symbols and OCR spacing in data.js!")
