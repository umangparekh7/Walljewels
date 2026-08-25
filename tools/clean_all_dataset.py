import json
import re
import pymupdf
import io
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

# 1. Clean spacing helper
def clean_spacing(text):
    if not text:
        return ""
    # Clean non-ascii artifacts
    text = text.replace('', ' · ')
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

# Filter out non-plate divider and back pages
filtered = []
for p in plates:
    pid = p['id']
    name = p.get('n', '')
    sub = p.get('sub', '')
    
    if pid in ['kp-32', 'kr-038', 'kr-064', 'kr-091', 'kr-117', 'kr-133', 'kr-159', 'kr-186', 'kr-plate-133', 'kr-plate-159']:
        continue
    if "CONTINUES" in name.upper() or "COLLECTION 0" in name.upper() or "DESIGNED AROUND YOUR SPACE" in name.upper():
        continue
    filtered.append(p)

for p in filtered:
    pid = p['id']
    
    # Specific targeted cleanups
    if pid == 'kr-031' or p.get('no') == 'WJWP-DVN-050':
        p['n'] = "Divine Family"
        p['sub'] = "Kala Rasa · Heritage Composition"
        p['style'] = "Heritage Composition"
        p['ideal'] = "Heritage Dining Halls, Formal Interiors, Pooja Spaces"
        p['b'] = "A refined, heritage-inspired composition uniting Shiva, Parvati, Ganesha, Kartikeya, and Nandi in harmonious sandstone, terracotta, and emerald balance."
        
    elif pid == 'kr-116' or p.get('no') == 'WJWP-KOL-025':
        p['n'] = "The Great Kolam"
        p['sub'] = "Kala Rasa · The Signature Masterpiece"
        p['style'] = "Signature Masterpiece"
        p['ideal'] = "Grand Entrances, Statement Walls, Living Foyers"
        p['b'] = "The signature large-scale composition of the collection. A breathtaking synthesis combining rigorous sacred geometry, flowing botanicals, and antique gold accents on a deep charcoal ground."

    elif pid == 'kr-184' or p.get('no') == 'WJWP-MOD-025':
        p['n'] = "New South"
        p['sub'] = "Kala Rasa · The Heritage Synthesis"
        p['style'] = "Contemporary Heritage Masterpiece"
        p['ideal'] = "Grand Architectural Spaces, Flagship Stores, Executive Lounges"
        p['b'] = "The pinnacle of the collection. A bold, monumental contemporary composition that flawlessly weaves subtle architectural geometry, sweeping botanical lines, and intricate textile references into a single cohesive masterpiece."

    # General spacing cleanups for all plates
    p['n'] = clean_spacing(p.get('n', ''))
    p['sub'] = clean_spacing(p.get('sub', ''))
    p['style'] = clean_spacing(p.get('style', ''))
    p['ideal'] = clean_spacing(p.get('ideal', ''))
    p['b'] = clean_spacing(p.get('b', ''))
    
    # Clean any leftover subtitles stuck in name
    for sep in [
        "One Deity, Four Registers", "Etched in Time", "Divine Geometry", "The Merchant's Courtyard",
        "Royal Elegance", "Ruins in the Rain", "Fountains and Flora", "The Woven Court", "Roots of the Divine",
        "Sacred Reflections", "Rhythmic Monumentality", "Classical Blossoms", "A Walk Through History",
        "Silhouettes of the Sacred", "Vertical Grace over Jungle Chaos", "The Electric Tension of High-Altitude Rain",
        "The Shaded Geometry of the Coffee Lands", "The Rhythm of Life on the Arabian Sea", "Aquatic Botanical Geometry",
        "Architectural Foliage", "Ancient Stone Yielding to the Rain", "The Rugged Edge of the Western Shore",
        "The Tangled Origins of Southern Flavour", "The Vibrating Apex of the Canopy", "The Signature Synthesis",
        "Where the Falls Meet the Sea", "A Divine Pastoral Dreamscape", "Immersed in Vibrant Foliage",
        "A Playful Orchard Discovery", "Gentle Giants in Tropical Greenery", "A Graceful Architectural Procession",
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
        "Minimalist Perfection", "The Root of Rhythm", "The Curated Symbol", "The Grand Ornament",
        "Fine Line, Soft Bloom", "Avian Symmetry", "Water Under Tension", "One Bloom, One Wall",
        "The Quietest Hour on the Water", "High-Altitude Drama"
    ]:
        if sep in p['n']:
            prefix, _ = p['n'].split(sep, 1)
            p['n'] = prefix.strip()
            p['sub'] = f"Kala Rasa · {sep}"

    # Ensure prefix volume in sub
    if p.get('sub') and not p['sub'].startswith('Kala Rasa') and not p['sub'].startswith('Kala Parampara'):
        vol_label = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
        p['sub'] = f"{vol_label} · {p['sub']}"

kp_count = len([p for p in filtered if p['v'] == 'kala-parampara'])
kr_count = len([p for p in filtered if p['v'] == 'kala-rasa'])

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

const COLLECTION = {json.dumps(filtered, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print(f"Data successfully cleaned and written! Total plates: {len(filtered)} (KP: {kp_count}, KR: {kr_count})")
