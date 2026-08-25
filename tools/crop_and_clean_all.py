import pymupdf
import io
import os
import json
import re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

os.makedirs('assets/img/collection/kala-parampara', exist_ok=True)
os.makedirs('assets/img/collection/kala-rasa', exist_ok=True)

# -------------------------------------------------------------
# 1. OCR-GUIDED CLEAN CROPPING FUNCTION
# -------------------------------------------------------------
def get_clean_crop(page, pnum, vol):
    # Specific custom overrides
    pix = page.get_pixmap(dpi=200)
    img_bytes = pix.tobytes('png')
    res, _ = ocr(img_bytes)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size
    
    if vol == 'kr' and pnum == 16:
        # Durga niche
        return img.crop((int(w * 0.18), 0, int(w * 0.58), h))
    if vol == 'kp' and pnum == 15:
        # Sanjeevani
        return img.crop((0, 0, int(w * 0.54), h))
        
    if not res or len(res) <= 1:
        return img
        
    text_boxes = []
    for item in res:
        box, text = item[0], item[1]
        xs = [pt[0] for pt in box]
        ys = [pt[1] for pt in box]
        text_boxes.append({
            'min_x': min(xs), 'max_x': max(xs),
            'min_y': min(ys), 'max_y': max(ys),
            'text': text,
            'center_x': sum(xs) / len(xs)
        })
        
    left_boxes = [b for b in text_boxes if b['center_x'] < 0.5 * w]
    right_boxes = [b for b in text_boxes if b['center_x'] >= 0.5 * w]
    
    # Filter out lone page numbers (len < 6 near outer corners)
    left_sig = [b for b in left_boxes if not (len(b['text']) < 6 and b['min_x'] < 0.08 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    right_sig = [b for b in right_boxes if not (len(b['text']) < 6 and b['max_x'] > 0.92 * w and (b['min_y'] > 0.9 * h or b['min_y'] < 0.1 * h))]
    
    if len(left_sig) > len(right_sig):
        # Sidebar is on LEFT -> Wallpaper room mockup is on RIGHT
        max_left_x = max([b['max_x'] for b in left_sig])
        crop_start_x = max(int(max_left_x + 12), int(w * 0.46))
        return img.crop((crop_start_x, 0, w, h))
    else:
        # Sidebar is on RIGHT -> Wallpaper room mockup is on LEFT
        min_right_x = min([b['min_x'] for b in right_sig])
        crop_end_x = min(int(min_right_x - 12), int(w * 0.54))
        return img.crop((0, 0, crop_end_x, h))

print("=== CROPPING ALL KALA PARAMPARA PLATES (1..82) ===")
for p in range(6, len(doc_kp) + 1):
    if p == 32:  # divider
        continue
    out_path = f"assets/img/collection/kala-parampara/kp-plate-{p:02d}.jpg"
    try:
        cropped = get_clean_crop(doc_kp[p - 1], p, 'kp')
        cropped.save(out_path, quality=95)
        if p % 15 == 0 or p == 6:
            print(f"KP Page {p:02d} -> Saved pure wallpaper image {out_path}")
    except Exception as e:
        print(f"Error cropping KP page {p}: {e}")

print("\n=== CROPPING ALL KALA RASA PLATES (1..185) ===")
for p in range(8, len(doc_kr) + 1):
    if p in [38, 64, 91, 117, 133, 159, 186]:  # section dividers & back page
        continue
    out_path = f"assets/img/collection/kala-rasa/kr-plate-{p:03d}.jpg"
    try:
        cropped = get_clean_crop(doc_kr[p - 1], p, 'kr')
        cropped.save(out_path, quality=95)
        if p % 20 == 0 or p in [95, 98, 100, 161]:
            print(f"KR Page {p:03d} -> Saved pure wallpaper image {out_path}")
    except Exception as e:
        print(f"Error cropping KR page {p}: {e}")

# -------------------------------------------------------------
# 2. STRING CLEANING HELPER (Fix all CamelCase, spaces, and junk)
# -------------------------------------------------------------
def fix_text_formatting(s):
    if not s or not isinstance(s, str):
        return ""
    # Standardize punctuation
    s = s.replace('\ufffd', ' ').replace('', ' ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # Remove OCR junk tags
    junk_patterns = [
        r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b',
        r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b'
    ]
    for jp in junk_patterns:
        s = re.sub(jp, '', s, flags=re.IGNORECASE)
        
    # Split camelCase words: "TheGrandOrnament" -> "The Grand Ornament"
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    
    # Comma spacing: "Red,Emerald,Gold" -> "Red, Emerald, Gold"
    s = re.sub(r',([^\s])', r', \1', s)
    
    # Remove multiple spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# -------------------------------------------------------------
# 3. LOAD DATA.JS & APPLY COMPREHENSIVE FIXES
# -------------------------------------------------------------
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Filter out divider pages
filtered_plates = []
for p in plates:
    pid = p['id']
    name = p.get('n', '')
    if pid in ['kp-32', 'kr-038', 'kr-064', 'kr-091', 'kr-117', 'kr-133', 'kr-159', 'kr-186', 'kr-plate-133', 'kr-plate-159']:
        continue
    if "CONTINUES" in name.upper() or "COLLECTION 0" in name.upper() or "DESIGNED AROUND YOUR SPACE" in name.upper():
        continue
    filtered_plates.append(p)

for p in filtered_plates:
    # Clean all fields
    for field in ['n', 'sub', 'style', 'ideal', 'b']:
        if field in p:
            p[field] = fix_text_formatting(p[field])
            
    # Fix blurb if starting with IdealFor / spaces
    desc = p.get('b', '')
    # If description has stuck keywords like "ExecutiveOffices,Halways..."
    if any(k in desc for k in ["Executive Offices", "Heritage Properties", "Dining Spaces", "Modern Niches", "Pooja Rooms"]):
        # If it starts with room locations followed by the description text
        # e.g. "Heritage Properties, Restaurants A rich ornamental pattern..."
        m = re.match(r'^([A-Za-z\s,]+)\s+([A-Z][a-z].+)$', desc)
        if m and len(m.group(1)) < 45 and not m.group(1).startswith('A ') and not m.group(1).startswith('The '):
            p['b'] = m.group(2).strip()

    # Separate any subtitle stuck in name
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
        "Minimalist Perfection", "The Root of Rhythm", "The Curated Symbol",
        "Fine Line, Soft Bloom", "Avian Symmetry", "Water Under Tension", "One Bloom, One Wall",
        "The Quietest Hour on the Water", "High-Altitude Drama", "One Deity, Four Registers", "Etched in Time",
        "A Sovereign in the Sacred Grove", "The Vertical Sanctum", "Epic Narratives in Stone",
        "Monumental Elegance", "Sacred Flora", "Ornamental Heritage", "Pathways of Antiquity",
        "Serene Mural", "Heritage Composition", "The Signature Masterpiece", "The Heritage Synthesis"
    ]:
        if phrase in name and len(name) > len(phrase) + 2:
            parts = name.split(phrase, 1)
            prefix = parts[0].strip(' ,-·')
            if len(prefix) >= 3:
                p['n'] = prefix
                vol_label = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
                p['sub'] = f"{vol_label} · {phrase}"

    # Ensure clean subtitle format
    sub = p.get('sub', '')
    vol_label = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
    if sub:
        # Remove repeated volume prefix
        sub_clean = sub.replace('Kala Rasa ·', '').replace('Kala Parampara ·', '').replace('Kala Rasa', '').replace('Kala Parampara', '').strip(' ·,-')
        p['sub'] = f"{vol_label} · {sub_clean}"
    else:
        p['sub'] = f"{vol_label} · {p.get('no', '')}"

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

print(f"\nSuccessfully cleaned and updated data.js! Total plates: {len(filtered_plates)} (KP: {kp_count}, KR: {kr_count})")
