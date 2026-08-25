import json

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

cleanups = {
    'kp-74': {
        'n': 'Minimalist Marigold',
        'sub': 'Kala Parampara · Subtle Traditional References in Sage and Ivory.',
        'b': 'A masterclass in restraint. This design distills the vibrant energy of the sacred marigold into delicate, minimalist geometry in soothing sage and warm ivory tones.'
    },
    'kp-75': {
        'n': 'The Abstract Archway',
        'sub': 'Kala Parampara · Marble, Gold, and Indian Geometry.',
        'b': 'Crisp architectural arches rendered in polished marble textures and gold leaf linework, adding depth and structural balance to modern hallways.'
    },
    'kp-76': {
        'n': 'Sculpted Sands',
        'sub': 'Kala Parampara · Abstract Waves with Optical Depth.',
        'b': 'Bringing the fluidity of nature into the rigid angles of modern spaces with undulating, sculptural sand dune contours.'
    },
    'kp-77': {
        'n': 'Metallic Labyrinth',
        'sub': 'Kala Parampara · Geometric Depth in Charcoal and Antique Brass.',
        'b': 'Intricate geometric maze patterns rendered in rich charcoal and burnished brass highlights, creating a bold contemporary statement.'
    }
}

for p in plates:
    if p['id'] in cleanups:
        for k, v in cleanups[p['id']].items():
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

print("Updated data.js with clean contemporary plates!")
