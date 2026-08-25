import json
import re
import os

with open('scratch/kp_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kp_data = json.load(f)

with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
    kr_data = json.load(f)

def clean_spacing(s):
    if not s or not isinstance(s, str):
        return ""
    s = s.replace('\ufffd', ' ').replace('', ' ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    # Remove junk
    for j in [r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b', r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b']:
        s = re.sub(j, '', s, flags=re.IGNORECASE)
    # Split camelCase
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r',([^\s])', r', \1', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_entry(entry, vol_id):
    pnum = entry['page']
    lines = [clean_spacing(l) for l in entry.get('lines', []) if clean_spacing(l)]
    
    # Filter divider / intro pages
    if vol_id == 'kala-parampara':
        if pnum < 6 or pnum > 82 or pnum == 32:
            return None
        plate_id = f"kp-{pnum:02d}"
        img = f"assets/img/collection/kala-parampara/kp-plate-{pnum:02d}.jpg"
        vol_name = "Kala Parampara"
    else:
        if pnum < 8 or pnum > 185 or pnum in [38, 64, 91, 117, 133, 159, 186]:
            return None
        plate_id = f"kr-{pnum:03d}"
        img = f"assets/img/collection/kala-rasa/kr-plate-{pnum:03d}.jpg"
        vol_name = "Kala Rasa"

    # Find Code
    code = ""
    code_idx = -1
    for i, l in enumerate(lines):
        m = re.search(r'WJWP-[A-Z0-9]+-[0-9A-Z]+', l.replace(' ', ''))
        if m:
            code = m.group(0).replace('O', '0').replace('B0T', 'BOT').replace('Q0', '00')
            code_idx = i
            break
            
    # Default fallbacks
    name = ""
    sub = ""
    style = ""
    ideal = ""
    blurb_lines = []
    
    # Extract sections
    style_idx = -1
    pal_idx = -1
    ideal_idx = -1
    
    for i, l in enumerate(lines):
        if l.upper() in ['STYLE', 'STYL']:
            style_idx = i
        elif l.upper() in ['PALETTE', 'PALET']:
            pal_idx = i
        elif 'IDEAL' in l.upper():
            ideal_idx = i

    # Name and Subtitle
    if code_idx != -1 and style_idx != -1 and style_idx > code_idx:
        title_lines = lines[code_idx + 1:style_idx]
        if len(title_lines) == 1:
            name = title_lines[0]
        elif len(title_lines) >= 2:
            name = title_lines[0]
            sub = title_lines[1]
    elif style_idx != -1 and style_idx > 1:
        name = lines[1]
        if style_idx > 2:
            sub = lines[2]

    # Style
    if style_idx != -1:
        limit = pal_idx if pal_idx != -1 else (ideal_idx if ideal_idx != -1 else len(lines))
        if limit > style_idx + 1:
            style = " ".join(lines[style_idx + 1:limit])

    # Ideal
    if ideal_idx != -1:
        if ideal_idx + 1 < len(lines):
            ideal = lines[ideal_idx + 1]

    # Description (blurb)
    # usually after ideal_idx + 1 or trailing lines
    start_b = ideal_idx + 2 if (ideal_idx != -1 and ideal_idx + 2 < len(lines)) else (ideal_idx + 1 if ideal_idx != -1 else 3)
    for i in range(start_b, len(lines)):
        l = lines[i]
        if not re.search(r'WJWP-[A-Z0-9]+-[0-9A-Z]+', l.replace(' ', '')) and not l.isdigit() and len(l) > 10:
            if not l.startswith('SOUTHERN') and not l.startswith('INDIA') and not l.startswith('KOLAM') and not l.startswith('DIVINE'):
                blurb_lines.append(l)

    blurb = " ".join(blurb_lines)
    
    # Specific curated overrides for key plates
    overrides = {
        'kr-016': ('Durga: The Protector', 'Contemporary Heritage Mural', 'A modern, grounded interpretation of divine protection. Goddess Durga surrounded by regal lions, vibrant florals, and subtle celestial geometry, creating a strong spiritual anchor for contemporary spaces.'),
        'kr-031': ('Divine Family', 'Heritage Composition', 'A refined, heritage-inspired composition uniting Shiva, Parvati, Ganesha, Kartikeya, and Nandi in harmonious sandstone, terracotta, and emerald balance.'),
        'kr-032': ('Divine India: Sacred Harmony', 'Contemporary Masterpiece', 'The magnum opus. A deeply sophisticated contemporary masterpiece interweaving the symbolic elements of Ganesha, Shiva, Krishna, Lakshmi, Saraswati, and Durga in harmonious sacred balance.'),
        'kr-033': ('Pichwai: Divine Companions', 'Traditional Pichwai Art', 'A celebration of the sacred bond between cow and calf, inspired by the traditional Pichwai art of Nathdwara. Blends lush foliage, lotus-filled waters, and intricate detailing to bring peace, prosperity, and divine grace.'),
        'kr-034': ('Pichwai: Eternal Melody', 'Traditional Pichwai Heritage', 'Inspired by the sacred Pichwai art of Nathdwara, this design reflects the eternal melody of devotion and nature. Krishna at the heart surrounded by cows, lotuses, peacocks, and temple charm.'),
        'kr-035': ('Rama of the Forest Arches', 'Sovereign in the Sacred Grove', 'Lord Rama stands at the centre of a carved triple arch, the forest and its rivers opening behind him. Ornamental sandstone framing gives the composition architectural weight.'),
        'kr-036': ('Ganesha: Four Aspects', 'One Deity, Four Registers', 'Four distinct iconography registers of Lord Ganesha depicted in serene meditative and celebratory postures across emerald, rose, and sandstone panels.'),
        'kr-037': ('Ganesha Enthroned', 'The Vertical Sanctum', 'Lord Ganesha seated in divine grandeur beneath ornate temple arches. The vertical orientation and rich jewel tones create a monumental spiritual focal point.'),
        'kr-039': ('Chola Temple Chronicles', 'Epic Narratives in Stone', 'Monumental stone carvings and friezes celebrating the timeless architectural genius of the Chola dynasty. Warm granite textures and lifelike bas-relief shadows create historic dignity.'),
        'kr-040': ('Gopuram Grandeur', 'Monumental Elegance', 'Towering Dravidian gopuram silhouettes rendered in gold, sandstone, and warm terracotta. Captures the majestic verticality and spiritual aura of ancient temples.'),
        'kr-041': ('Bronze and Lotus', 'Sacred Flora', 'Lustrous antique bronze sculptural forms intertwined with delicate, hand-painted South Indian temple lotuses against a rich, atmospheric patina backdrop.'),
        'kr-042': ('Thanjavur Golden Garden', 'Ornamental Heritage', 'Inspired by Thanjavur gold-foil traditions, featuring intricate botanical tendrils, stylized birds, and classical South Indian ornamentation on an aged metallic canvas.'),
        'kr-043': ('Temple Corridor Tales', 'Pathways of Antiquity', 'A breathtaking perspective through a thousand-pillared temple corridor with dramatic light filtering through stone colonnades, creating immense architectural depth.'),
        'kr-044': ('Dravidian Stone Stories', 'Etched in Time', 'Etched stone reliefs documenting sacred dynastic lore, carved temple friezes, and architectural stonework in delicate sepia and charcoal tones.'),
        'kr-045': ('Sacred Water', 'Serene Mural', 'A contemplative portrayal of temple tank waters reflecting sanctum pillars, sacred steps, and morning skies in tranquil dusk blue and stone grey.'),
        'kr-046': ('Mandala of Madurai', 'Divine Geometry', 'Intricate concentric mandala geometry inspired by the ceiling vaults and sacred architectural grids of Madurai Meenakshi Amman Temple.'),
        'kr-047': ('Chettinad Heritage', "The Merchant's Courtyard", 'The stately symmetry of Chettinad mansion courtyards with carved teak pillars, Athangudi tiled borders, and sunlit central courtyards.'),
        'kr-048': ('Mysore Palace Reverie', 'Royal Elegance', 'Opulent stained-glass radiance, gold-leaf colonnades, and durbar hall splendour capturing the regal spirit of Mysore Palace.'),
        'kr-049': ('Hampi in the Monsoon', 'Ruins in the Rain', 'Atmospheric basalt boulders and ancient Vijayanagara ruins shrouded in dramatic monsoon clouds, deep indigo rain, and fresh emerald moss.'),
        'kr-050': ('Deccan Palace Garden', 'Fountains and Flora', 'Geometric Charbagh water channels, ornate stone fountains, and stylized cypress trees from royal Deccan pleasure gardens in indigo and terracotta.'),
        'kr-051': ('Kalamkari Royal Court', 'The Woven Court', 'Hand-drawn pen Kalamkari textile murals depicting royal courts, celestial dancers, and ornate flowering trees dyed in rich natural vegetable hues.'),
        'kr-052': ('Sacred Banyan Stories', 'Roots of the Divine', 'Sprawling aerial roots and sheltering banyan canopy symbolizing cosmic longevity, spiritual wisdom, and South Indian village sanctums.'),
        'kr-053': ('The Temple Tank', 'Sacred Reflections', 'Stepped stone theppakulam reservoir reflecting temple spires and floating lotus blossoms in serene indigo and cool emerald ripples.'),
        'kr-054': ('Pillars of Time', 'Rhythmic Monumentality', 'A rhythmic sequence of monolithic carved granite pillars showcasing the timeless architectural grandeur of South Indian temple colonnades.'),
        'kr-055': ('Temple Floral Archive', 'Classical Blossoms', 'Classical botanical studies of sacred South Indian temple flowers: jasmine, champaka, marigold, and lotus rendered with archival delicate line-work.'),
        'kr-056': ('Chola Garden Procession', 'A Walk Through History', 'Royal ceremonial processions through palace gardens with caparisoned elephants, flag-bearers, and courtiers amidst lush Chola greenery.'),
        'kr-057': ('Gopuram at Dusk', 'Silhouettes of the Sacred', 'Dramatic dusk skies framing layered silhouettes of towering temple gopurams in rich terracotta, charcoal, and twilight bronze.'),
        'kr-094': ('Terracotta Kolam', 'Warmth in Order', 'Warm terracotta tones and bold sacred geometric kolam lines creating structured warmth for dining suites and family living.'),
        'kr-095': ('Kolam Weave', 'The Interlace', 'Kolam forms intricately inspired by the rhythmic interlacing and symmetry of traditional South Indian textiles.'),
        'kr-096': ('Kolam Archive', 'The Curated Symbol', 'A contemporary, curated symbol archive bringing architectural rhythm and contemplative balance to executive suites and hallways.'),
        'kr-097': ('Minimal Kolam', 'Sophisticated Silence', 'Clean ivory and neutral linework stripped down for sophisticated modern interiors and serene corridors.'),
        'kr-098': ('Heritage Kolam', 'The Grand Ornament', 'A rich ornamental pattern seamlessly blending traditional rhythm with commanding modern composition in burgundy and antique gold.'),
        'kr-099': ('Lotus Kolam', 'Sacred Petals', 'Graceful lotus motifs expanding from central geometric nodes to bring auspicious charm and beauty to bedroom suites.'),
        'kr-100': ('Kolam Bloom', 'Organic Expansion', 'A vibrant floral Kolam composition balancing geometric precision with blooming organic motifs for sunlit living spaces.'),
        'kr-101': ('Kolam Garden', 'Leaf, Flower, Wing', 'Sacred geometry beautifully intertwined with delicate leaves and floral blooms for bright garden rooms and corridors.'),
        'kr-102': ('Peacock Kolam', 'The Measured Plume', 'Stylized peacock feather plumes arranged in harmonious geometric frameworks in rich jewel and sandstone tones.'),
        'kr-103': ('Kolam and Jasmine', 'Fine Line, Soft Bloom', 'Razor-fine geometric lines paired with tender jasmine blossom silhouettes for elegant bedrooms and alcoves.'),
        'kr-104': ('Kolam Peacock Garden', 'Avian Symmetry', 'A towering botanical pattern framed by stately peacocks in formal symmetry for luxury reception lounges.'),
        'kr-116': ('The Great Kolam', 'The Signature Masterpiece', 'The signature large-scale composition of the collection. A breathtaking synthesis combining rigorous sacred geometry, flowing botanicals, and antique gold accents.'),
        'kr-137': ("Ganesha's Little Festival", 'A Joyful Celebration of Heritage', 'A vibrant celebration of South Indian festivity. Ganesha is surrounded by beautifully illustrated traditional lamps, fresh mango leaves, and joyful floral garlands.'),
        'kr-160': ('Modern Madurai', 'Architectural Rhythms', 'Abstract architectural forms, sacred stone ratios, and terracotta colour blocks reinterpreting ancient temple rhythms for contemporary minimalist interiors.'),
        'kr-167': ('Indigo Botanica', 'The Midnight Tropics', 'Lush midnight foliage rendered in deep indigo, teal, and sage with gold leaf accents on a moody dark backdrop.'),
        'kr-184': ('New South', 'The Heritage Synthesis', 'The pinnacle of the collection. A bold, monumental contemporary composition that flawlessly weaves subtle architectural geometry, sweeping botanical lines, and intricate textile references.')
    }

    if plate_id in overrides:
        name = overrides[plate_id][0]
        sub = overrides[plate_id][1]
        blurb = overrides[plate_id][2]

    # Clean up name & sub
    name = clean_spacing(name)
    sub = clean_spacing(sub)
    if not sub:
        sub = code if code else vol_name
    if not sub.startswith(vol_name):
        sub = f"{vol_name} · {sub}"
        
    if not name:
        name = f"{vol_name} Plate {pnum}"
        
    if not blurb or len(blurb) < 15:
        blurb = f"Custom scaled and printed to your wall's exact measure on your choice of 5 luxury architectural substrates. In-house manufactured in Chennai since 1978."

    return {
        'id': plate_id,
        'v': vol_id,
        'no': code if code else f"WJWP-{vol_id[:2].upper()}-{pnum:03d}",
        'n': name,
        'sub': sub,
        'style': clean_spacing(style) if style else "Luxury Architectural Wallpaper",
        'ideal': clean_spacing(ideal) if ideal else "Living Rooms, Dining Suites, Master Bedrooms",
        'b': clean_spacing(blurb),
        'img': img
    }

all_plates = []
for entry in kp_data:
    p = parse_entry(entry, 'kala-parampara')
    if p:
        all_plates.append(p)

for entry in kr_data:
    p = parse_entry(entry, 'kala-rasa')
    if p:
        all_plates.append(p)

kp_count = len([p for p in all_plates if p['v'] == 'kala-parampara'])
kr_count = len([p for p in all_plates if p['v'] == 'kala-rasa'])

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

const COLLECTION = {json.dumps(all_plates, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print(f"Generated clean data.js with {len(all_plates)} plates (KP: {kp_count}, KR: {kr_count})")
