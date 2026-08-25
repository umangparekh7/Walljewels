import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Filter out kp-53 divider page
plates = [p for p in plates if p['id'] not in ['kp-53', 'kp-32', 'kr-038', 'kr-064', 'kr-091', 'kr-117', 'kr-133', 'kr-159', 'kr-186']]

kp_cleanups = {
    'kp-34': {
        'n': 'Chola Pillars',
        'sub': 'Kala Parampara · Monumental design for towering spaces.',
        'b': 'Featuring the intricately carved granite pillars characteristic of Dravidian temple architecture. This striking vertical composition lends historic authority and height to expansive reception halls.'
    },
    'kp-37': {
        'n': 'Chettinad Grandeur',
        'sub': 'Kala Parampara · Echoes of aristocratic elegance.',
        'b': 'A homage to the palatial mansions of Karaikudi. This stately design incorporates carved teak pillars, Athangudi tile motifs, and courtyard symmetry in earthy heritage tones.'
    },
    'kp-39': {
        'n': 'Tanjore Garden',
        'sub': 'Kala Parampara · Gilded heritage for the modern connoisseur.',
        'b': 'Inspired by the opulent detailing of Thanjavur paintings, this design layers gold-foil botanical tendrils, stylized birds, and classical South Indian ornamentation on an aged metallic canvas.'
    },
    'kp-40': {
        'n': 'Tanjore Echoes',
        'sub': 'Kala Parampara · Antique Gold and Deep Burgundy Botanicals.',
        'b': 'Drawing inspiration from the opulence of Tanjore paintings and vintage South Indian silks, this design weaves stylized floral bouquets and gold-dusted borders.'
    },
    'kp-42': {
        'n': 'Kolam Rhythm',
        'sub': 'Kala Parampara · The sacred geometry of dawn.',
        'b': 'A minimalist, contemporary take on the daily ritual of threshold kolam art. Clean geometric symmetry and natural ivory lines bring peaceful structure to foyers.'
    }
}

for p in plates:
    if p['id'] in kp_cleanups:
        for k, v in kp_cleanups[p['id']].items():
            p[k] = v

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

print("Updated data.js with clean KP titles and filtered dividers!")
