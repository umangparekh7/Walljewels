import json
import re

def clean_pure_string(s):
    if not s or not isinstance(s, str):
        return ""
    # Remove any stray replacement characters or isolated dots/symbols
    s = s.replace('\ufffd', ' ').replace('·', ' · ')
    # Keep only standard printable characters, clean punctuation
    # If string was polluted with ' · ' between letters: e.g. "T · e · r · r · a"
    if re.search(r'[A-Za-z]\s*·\s*[A-Za-z]', s):
        # Strip the dots between letters
        s = re.sub(r'(?<=[A-Za-z])\s*·\s*(?=[A-Za-z])', '', s)
        
    # Join single-letter spaces: "T e r r a c o t t a" -> "Terracotta"
    while re.search(r'(?<=[A-Za-z0-9]) (?=[A-Za-z0-9](?: |$|[,\.—]))', s):
        s = re.sub(r'(?<=[A-Za-z0-9]) (?=[A-Za-z0-9](?: |$|[,\.—]))', '', s)
        
    # Clean OCR junk
    for j in [r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b', r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b']:
        s = re.sub(j, '', s, flags=re.IGNORECASE)

    # Split camelCase
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r',([^\s])', r', \1', s)
    s = re.sub(r'(\s*·\s*)+', ' · ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

for p in plates:
    for f in ['n', 'sub', 'style', 'ideal', 'b']:
        if f in p:
            p[f] = clean_pure_string(p[f])
            
    # Fix sub volume prefix
    sub = p.get('sub', '')
    vol = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
    if sub:
        sub_core = sub.replace('Kala Rasa ·', '').replace('Kala Parampara ·', '').replace('Kala Rasa', '').replace('Kala Parampara', '').strip(' ·,-')
        p['sub'] = f"{vol} · {sub_core}"
    else:
        p['sub'] = f"{vol} · {p.get('no', '')}"

kp_count = len([p for p in plates if p['v'] == 'kala-parampara'])
kr_count = len([p for p in plates if p['v'] == 'kala-rasa'])

data_js = f'''// Wall Jewels Wallpaper World — Canonical Catalogue Dataset
// Synchronized directly from Kala Parampara (Volume I) & Kala Rasa (Volume II)

const VOLUMES = [
  {{ id: 'kala-parampara', name: 'Kala Parampara', no: 'Volume I', desc: '82 master plates of classical sacred iconography, southern heritage, and world architectures.', count: {kp_count} }},
  {{ id: 'kala-rasa', name: 'Kala Rasa', no: 'Volume II', desc: '176 plates of divine devotion, Pichwai traditions, lush tropicals, modern abstractions, and serene landscapes.', count: {kr_count} }}
];

const CATEGORIES = [
  {{ id: 'heritage', label: 'Sanatan & Heritage' }},
  {{ id: 'botanical', label: 'Botanical & Tropical' }},
  {{ id: 'world', label: 'World Cities' }},
  {{ id: 'abstract', label: 'Contemporary & 3D' }},
  {{ id: 'kids', label: 'Kids & Nursery' }}
];

const SPACES = [
  {{ id: 'living', label: 'Living Rooms' }},
  {{ id: 'dining', label: 'Dining Suites' }},
  {{ id: 'bedroom', label: 'Bedrooms' }},
  {{ id: 'temple', label: 'Pooja & Temple' }},
  {{ id: 'office', label: 'Executive Offices' }}
];

const COLLECTION = {json.dumps(plates, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print("Repaired data.js completely!")
