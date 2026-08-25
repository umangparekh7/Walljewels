import json
import re

def clean_text(text):
    if not text:
        return ""
    # Remove replacement character or unusual control chars
    text = text.replace('\ufffd', ' · ').replace('', ' · ')
    # Clean multiple dots/separators
    text = re.sub(r'(\s*·\s*)+', ' · ', text)
    # Insert space between lower and Upper: "FountainsandFlora" -> "Fountains and Flora"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Insert space after comma if missing: "Red,Emerald,Gold" -> "Red, Emerald, Gold"
    text = re.sub(r',([^\s])', r', \1', text)
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

for p in plates:
    for k in ['n', 'sub', 'style', 'ideal', 'b']:
        if k in p:
            val = p[k]
            # Fix if it had spaced characters
            if ' ·  · ' in val or ' · ' in val:
                # remove bad spacer loops
                val = re.sub(r' · [A-Za-z] · ', '', val)
            p[k] = clean_text(p[k])

    # Ensure clean subtitle format
    sub = p.get('sub', '')
    if ' · ' in sub:
        parts = [pt.strip() for pt in sub.split(' · ') if pt.strip()]
        # Remove duplicate volume name if repeated
        clean_parts = []
        for pt in parts:
            if pt not in clean_parts:
                clean_parts.append(pt)
        p['sub'] = ' · '.join(clean_parts)

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

print("Saved clean data.js!")
