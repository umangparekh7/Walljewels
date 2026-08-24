import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Common OCR word merges to split
replacements = [
    (r'theultimate', 'the ultimate'),
    (r'thiscompositiondraws', 'this composition draws'),
    (r'thevast,uncontained', 'the vast, uncontained'),
    (r'universeitself', 'universe itself'),
    (r'weavesthe', 'weaves the'),
    (r'sacredriver', 'sacred river'),
    (r'deity\'sfaceis', "deity's face is"),
    (r'calm, realistic,and', 'calm, realistic, and'),
    (r'majestic\.It', 'majestic. It'),
    (r'contemporarysurrealismand', 'contemporary surrealism and'),
    (r'astronomicalphotography', 'astronomical photography'),
    (r'Arefined,contemporaryinvocationofLordGanesha', 'A refined, contemporary invocation of Lord Ganesha'),
    (r'establishinganatmosphereofauspiciousnessandgrace', 'establishing an atmosphere of auspiciousness and grace'),
    (r'Intricatesacredgeometryblendsseamlesslywithelegant', 'Intricate sacred geometry blends seamlessly with elegant'),
    (r'grounded by sere ne lotus motifs\. BLE', 'grounded by serene lotus motifs.'),
    (r'sere ne', 'serene'),
    (r'Godde ss', 'Goddess'),
    (r'pinnac le', 'pinnacle'),
    (r'Apowerful,dramaticheritagecompositionfeaturinggracefullion', 'A powerful, dramatic heritage composition featuring graceful lion'),
    (r'beautifulyrenderedamonglushkadambatrees,elegant', 'beautifully rendered among lush kadamba trees, elegant'),
    (r'Anintenselysophisticated,abstract', 'An intensely sophisticated, abstract'),
    (r'representationofShivaandShakti', 'representation of Shiva and Shakti'),
    (r'Rather than literal portraiture,this pieceutilizessymbolic', 'Rather than literal portraiture, this piece utilizes symbolic'),
    (r'artistic languageto expresstheperfectunion', 'artistic language to express the perfect union'),
    (r'divine masculine andferninine energies', 'divine masculine and feminine energies'),
    (r'forms indeep violet', 'forms in deep violet'),
    (r'andluminous copper create', 'and luminous copper create'),
    (r'speakstoultimate cosmic', 'speaks to ultimate cosmic'),
    (r'Theminimalluxuryaesthetic', 'The minimal luxury aesthetic'),
    (r'ensuresitfunctionsasadeeplyromantic', 'ensures it functions as a deeply romantic'),
    (r'groundinganchorformaster suites and', 'grounding anchor for master suites and'),
    (r'privatesanctuaries', 'private sanctuaries')
]

for orig, repl in replacements:
    text = re.sub(orig, repl, text)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Polished all description texts in data.js!")
