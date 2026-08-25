import json
import re

def remove_single_letter_spaces(s):
    if not s or not isinstance(s, str):
        return ""
    # Clean non-ascii
    s = s.replace('\ufffd', ' · ').replace('', ' · ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # If string has spaced characters
    tokens = s.split()
    single_count = sum(1 for t in tokens if len(t) == 1)
    if len(tokens) > 3 and single_count / len(tokens) > 0.35:
        # Split by punctuation or multi-space or word boundaries
        # Join consecutive single letters
        words = re.split(r'(\s{2,}|[,\.—·:])', s)
        fixed_pieces = []
        for w in words:
            if re.match(r'[,\.—·:]', w) or w.startswith('  '):
                fixed_pieces.append(w)
            else:
                # Remove single space between single chars
                fixed_pieces.append(w.replace(' ', ''))
        s = "".join(fixed_pieces)

    # Remove OCR junk
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
            p[f] = remove_single_letter_spaces(p[f])
            
    # Fix name & sub separation
    name = p.get('n', '')
    for phrase in [
        "The Grand Ornament", "The Curated Symbol", "Warmth in Order", "Divine Geometry",
        "The Merchant's Courtyard", "Royal Elegance", "Ruins in the Rain", "Fountains and Flora",
        "The Woven Court", "Roots of the Divine", "Sacred Reflections", "Rhythmic Monumentality",
        "Classical Blossoms", "A Walk Through History", "Silhouettes of the Sacred",
        "Vertical Grace over Jungle Chaos", "The Electric Tension of High-Altitude Rain",
        "The Shaded Geometry of the Coffee Lands", "The Rhythm of Life on the Arabian Sea",
        "Aquatic Botanical Geometry", "Architectural Foliage", "Ancient Stone Yielding to the Rain",
        "The Rugged Edge of the Western Shore", "The Tangled Origins of Southern Flavour",
        "The Vibrating Apex of the Canopy", "The Signature Synthesis", "Where the Falls Meet the Sea",
        "A Divine Pastoral Dreamscape", "Immersed in Vibrant Foliage", "A Playful Orchard Discovery",
        "Gentle Giants in Tropical Greenery", "A Graceful Architectural Procession",
        "Regal Birds in Enchanted Courtyards", "Lush Tropical Monsoon Beauty", "Swinging Through Ancient Canopies",
        "A Storybook Forest Expedition", "The Menagerie, Continued", "Dense, Colourful, Alive",
        "A Tranquil Blooming Pond", "Traditional Characters Reimagined", "A Gracefully Illustrated Epic",
        "A Charming Architectural Landscape", "Secrets Among the Stone Pathways", "Everyday Magic in the Village",
        "A Joyful Cultural Celebration", "A Dense, Breathing Rainforest", "A Landscape of Mountain Wonders",
        "Hide and Seek in the Orchard", "The Towering Tree of Tales", "Joyful Splashing in the Backwaters",
        "A Micro-World of Oversized Flora", "Architectural Rhythms", "The Midnight Tropics",
        "The Evening Gradient", "Ancient Proportions, Modern Grid", "Inner Sanctuaries", "Rhythmic Geometry",
        "Fronds in Flux", "The Cartography of Culture", "Organic Rhythm", "Where Land Meets Sea",
        "The City Held in Gold", "The Essence of the Maker", "The Temple Garden", "A Symphony of Celebration",
        "The Scroll Unfurled", "A Modern Epic", "Delicate Splendour", "Tradition Meets Modernity",
        "A Lush Tropical Tapestry", "Repeating Elegance", "Nature Reclaims", "The Flow of Tradition",
        "Minimalist Perfection", "The Root of Rhythm", "Fine Line, Soft Bloom", "Avian Symmetry",
        "Water Under Tension", "One Bloom, One Wall", "The Quietest Hour on the Water", "High-Altitude Drama",
        "One Deity, Four Registers", "Etched in Time", "The Signature Masterpiece", "The Heritage Synthesis",
        "A Joyful Celebration of Heritage"
    ]:
        if phrase in name and len(name) > len(phrase) + 2:
            parts = name.split(phrase, 1)
            prefix = parts[0].strip(' ,-·')
            if len(prefix) >= 3:
                p['n'] = prefix
                vol = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
                p['sub'] = f"{vol} · {phrase}"

    # Clean sub volume prefix
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

print("Saved clean data.js!")
