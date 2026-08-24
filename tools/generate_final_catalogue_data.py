import json
import re

with open('scratch/master_combined_plates.json', 'r', encoding='utf-8') as f:
    plates = json.load(f)

# Polish OCR typos and words merged together
word_fixes = [
    (r'instoneand', 'in stone and'),
    (r'theCosmos', 'the Cosmos'),
    (r'Acelestialvision', 'A celestial vision'),
    (r'deepmeditation', 'deep meditation'),
    (r'inspira-\s*tionfrom', 'inspiration from'),
    (r'cinematicrealism', 'cinematic realism'),
    (r'cinematic realism', 'cinematic realism'),
    (r'therugged', 'the rugged'),
    (r'ContemporarySacredArt', 'Contemporary Sacred Art'),
    (r'Atmospheric Spiritual Mural', 'Atmospheric Spiritual Mural'),
    (r'ClassicalStorybookMural', 'Classical Storybook Mural'),
    (r'Romantic Indian Painting', 'Romantic Indian Painting'),
    (r'Classical Heritage Art', 'Classical Heritage Art'),
    (r'Luxury Ornamental Mural', 'Luxury Ornamental Mural'),
    (r'RefinedClassical lllustration', 'Refined Classical Illustration'),
    (r'Dramatic Heritage Mural', 'Dramatic Heritage Mural'),
    (r'Antiq ue', 'Antique'),
    (r'Anti que', 'Antique'),
    (r'DeepBlue', 'Deep Blue'),
    (r'Muted Pink', 'Muted Pink'),
    (r'BoutiqueLobbie', 'Boutique Lobbies'),
    (r'LivingSpaces', 'Living Spaces'),
    (r'MusicRooms', 'Music Rooms'),
    (r'PrivateSuites', 'Private Suites'),
    (r'Formal Dining', 'Formal Dining'),
    (r'Heritage Interiors', 'Heritage Interiors'),
    (r'WealthCorners', 'Wealth Corners'),
    (r'PremiumDining', 'Premium Dining'),
    (r'LuxuryMasterSuites', 'Luxury Master Suites'),
    (r'PoojaRooms', 'Pooja Rooms'),
    (r'Grand Entrances', 'Grand Entrances'),
    (r'LivingRooms', 'Living Rooms'),
    (r'MeditationRooms', 'Meditation Rooms'),
    (r'ModernSanctuaries', 'Modern Sanctuaries'),
    (r'MinimalistStudies', 'Minimalist Studies'),
    (r'CreativeStudios', 'Creative Studios'),
    (r'Children\'sSanctuaries', 'Children\'s Sanctuaries'),
    (r'Grand Foyers', 'Grand Foyers'),
    (r'Statement Walls', 'Statement Walls'),
    (r'throughsweepingcelestialcurves', 'through sweeping celestial curves'),
    (r'backdropallowstheexplosivecopperand', 'backdrop allows the explosive copper and'),
    (r'saffronmetallictexturestovisuallyleapfrom', 'saffron metallic textures to visually leap from'),
    (r'designedforspacesthatdemand', 'designed for spaces that demand'),
    (r'Thebalanceof', 'The balance of'),
    (r'Anintenselysophisticated', 'An intensely sophisticated'),
    (r'representationofShivaandShakti', 'representation of Shiva and Shakti'),
    (r'Ratherthan', 'Rather than'),
    (r'literalportraiture', 'literal portraiture'),
    (r'artisticlanguageto', 'artistic language to'),
    (r'expresstheperfectunion', 'express the perfect union'),
    (r'divinemasculineandferninine', 'divine masculine and feminine'),
    (r'Sweeping,intertwinedformsin', 'Sweeping, intertwined forms in'),
    (r'deepviolet', 'deep violet'),
    (r'and luminous coppercreateahypnotic', 'and luminous copper create a hypnotic'),
    (r'theabsolutestillness', 'the absolute stillness'),
    (r'Lord Shivain', 'Lord Shiva in'),
    (r'Himalayanlandscapearerenderedinsophisticated', 'Himalayan landscape are rendered in sophisticated'),
    (r'isfelt inthe', 'is felt in the')
]

for p in plates:
    for orig, repl in word_fixes:
        p['n'] = re.sub(orig, repl, p['n'])
        p['sub'] = re.sub(orig, repl, p['sub'])
        p['b'] = re.sub(orig, repl, p['b'])
        p['style'] = re.sub(orig, repl, p['style'])
        p['palette'] = re.sub(orig, repl, p['palette'])
        p['ideal'] = re.sub(orig, repl, p['ideal'])

# Filter out non-plate folios if any
clean_plates = []
seen_ids = set()
for p in plates:
    if p['id'] in seen_ids:
        continue
    seen_ids.add(p['id'])
    
    # Clean up empty or broken titles
    if not p['n'] or p['n'].startswith('WJWP-') or p['n'] == '01' or p['n'] == '02':
        if p['v'] == 'kala-parampara':
            p['n'] = f"Kala Parampara · {p['no']}"
        else:
            p['n'] = f"Kala Rasa · {p['no']}"
            
    clean_plates.append(p)

print(f"Cleaned plates total: {len(clean_plates)}")

# Write to assets/js/data.js
data_js = f'''// Wall Jewels Wallpaper World — Canonical Catalogue Dataset
// Synchronized directly from Kala Parampara (Volume I) & Kala Rasa (Volume II)

const VOLUMES = [
  {{ id: 'kala-parampara', name: 'Kala Parampara', no: 'Volume I', desc: '82 master plates of classical sacred iconography, southern heritage, and world architectures.', count: {len([p for p in clean_plates if p['v'] == 'kala-parampara'])} }},
  {{ id: 'kala-rasa', name: 'Kala Rasa', no: 'Volume II', desc: '178 plates of divine devotion, Pichwai traditions, lush tropicals, modern abstractions, and serene landscapes.', count: {len([p for p in clean_plates if p['v'] == 'kala-rasa'])} }}
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

const COLLECTION = {json.dumps(clean_plates, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print("Wrote updated canonical assets/js/data.js!")
