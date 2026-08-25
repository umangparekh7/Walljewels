import pymupdf
import io
import os
import json
import re
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('assets/img/collection/kala-parampara', exist_ok=True)
os.makedirs('assets/img/collection/kala-rasa', exist_ok=True)

# -------------------------------------------------------------
# 1. CROP ALL KP PLATES
# -------------------------------------------------------------
print("Cropping all Kala Parampara plates (6..82)...")
for p in range(6, len(doc_kp) + 1):
    if p == 32:
        continue
    page = doc_kp[p - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    
    if p == 15:
        cropped = img.crop((0, 0, int(w * 0.54), h))
    elif p % 2 == 0:
        cropped = img.crop((0, 0, int(w * 0.445), h))
    else:
        cropped = img.crop((int(w * 0.465), 0, w, h))
        
    out_path = f"assets/img/collection/kala-parampara/kp-plate-{p:02d}.jpg"
    cropped.save(out_path, quality=95)

print("Finished cropping all Kala Parampara plates!")

# -------------------------------------------------------------
# 2. CROP ALL KR PLATES
# -------------------------------------------------------------
print("\nCropping all Kala Rasa plates (8..185)...")
for p in range(8, len(doc_kr) + 1):
    if p in [38, 64, 91, 117, 133, 159, 186]:
        continue
    page = doc_kr[p - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    
    if p == 16:
        cropped = img.crop((int(w * 0.18), 0, int(w * 0.58), h))
    elif p % 2 == 0:
        # Even -> wallpaper is on LEFT
        cropped = img.crop((0, 0, int(w * 0.445), h))
    else:
        # Odd -> wallpaper is on RIGHT
        cropped = img.crop((int(w * 0.465), 0, w, h))
        
    out_path = f"assets/img/collection/kala-rasa/kr-plate-{p:03d}.jpg"
    cropped.save(out_path, quality=95)

print("Finished cropping all Kala Rasa plates!")

# -------------------------------------------------------------
# 3. CLEAN DATA.JS & ENHANCE ALL DESCRIPTIONS
# -------------------------------------------------------------
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Filter divider pages
filtered_plates = []
for p in plates:
    pid = p['id']
    name = p.get('n', '')
    if pid in ['kp-32', 'kr-038', 'kr-064', 'kr-091', 'kr-117', 'kr-133', 'kr-159', 'kr-186', 'kr-plate-133', 'kr-plate-159']:
        continue
    if "CONTINUES" in name.upper() or "COLLECTION 0" in name.upper() or "DESIGNED AROUND YOUR SPACE" in name.upper():
        continue
    filtered_plates.append(p)

def clean_str(s):
    if not s or not isinstance(s, str):
        return ""
    s = s.replace('\ufffd', ' ').replace('', ' ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    # Remove OCR junk
    for junk in [r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b', r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b']:
        s = re.sub(junk, '', s, flags=re.IGNORECASE)
    # Split camelCase
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r',([^\s])', r', \1', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

for p in filtered_plates:
    for f in ['n', 'sub', 'style', 'ideal', 'b']:
        if f in p:
            p[f] = clean_str(p[f])
            
    # Clean description if starting with misplaced location headers
    desc = p.get('b', '')
    for loc_header in [
        "Heritage Properties, Restaurants", "Executive Offices, Hallways", "Executive Offices, Halways",
        "Dining Spaces, Warm Living", "Dining Spaces, Living Foyers", "Pooja Rooms, Entrance Halls",
        "Modern Niches, Entrance Halls", "Living Rooms, Feature Walls", "Master Suites, Formal Living"
    ]:
        if desc.startswith(loc_header):
            desc = desc[len(loc_header):].strip(' ,-·')
    
    # If description starts with lower case letter, capitalize
    if desc and desc[0].islower():
        desc = desc[0].upper() + desc[1:]
    p['b'] = desc

    # Split joined subtitle from name if present
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
        "Minimalist Perfection", "The Root of Rhythm",
        "Fine Line, Soft Bloom", "Avian Symmetry", "Water Under Tension", "One Bloom, One Wall",
        "The Quietest Hour on the Water", "High-Altitude Drama", "One Deity, Four Registers", "Etched in Time"
    ]:
        if phrase in name and len(name) > len(phrase) + 2:
            parts = name.split(phrase, 1)
            prefix = parts[0].strip(' ,-·')
            if len(prefix) >= 3:
                p['n'] = prefix
                vol = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
                p['sub'] = f"{vol} · {phrase}"

    # Clean sub prefix
    sub = p.get('sub', '')
    vol = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
    if sub:
        sub_core = sub.replace('Kala Rasa ·', '').replace('Kala Parampara ·', '').replace('Kala Rasa', '').replace('Kala Parampara', '').strip(' ·,-')
        p['sub'] = f"{vol} · {sub_core}"
    else:
        p['sub'] = f"{vol} · {p.get('no', '')}"

kp_count = len([p for p in filtered_plates if p['v'] == 'kala-parampara'])
kr_count = len([p for p in filtered_plates if p['v'] == 'kala-rasa'])

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

const COLLECTION = {json.dumps(filtered_plates, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print(f"Data successfully cleaned and updated! Total: {len(filtered_plates)} plates (KP: {kp_count}, KR: {kr_count})")
