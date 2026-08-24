import json
import re

with open('scratch/kp_parsed_exact.json', 'r', encoding='utf-8') as f:
    kp_raw = json.load(f)

# Official Kala Parampara Concordance Mapping
concordance = {
    5: {"code": "WJWP-DVN-001", "sec_code": "DI-002", "title": "The Himalayan Ascetic", "sub": "Mahadev in Deep Stillness", "cat": "heritage", "sp": "living", "tag": "Signature"},
    6: {"code": "WJWP-DVN-002", "sec_code": "DI-001", "title": "The Golden Ganesha", "sub": "Minimalist Devotion in Line", "cat": "heritage", "sp": "temple", "tag": "Devotional"},
    7: {"code": "WJWP-DVN-003", "sec_code": "DI-003", "title": "Sovereign of the Realm", "sub": "The Lion-Rider in Saffron & Vermilion", "cat": "heritage", "sp": "living", "tag": ""},
    8: {"code": "WJWP-DVN-004", "sec_code": "DI-004", "title": "Cosmic Union", "sub": "Shiva & Parvati in Divine Harmony", "cat": "heritage", "sp": "bedroom", "tag": ""},
    9: {"code": "WJWP-DVN-005", "sec_code": "WJ-DC-004", "title": "Kailash Meditations", "sub": "The Stillness of the Himalayas", "cat": "heritage", "sp": "living", "tag": ""},
    10: {"code": "WJWP-DVN-006", "sec_code": "WJ-DC-005", "title": "The Cosmic Tandava", "sub": "Nataraja in Deep Indigo and Copper", "cat": "heritage", "sp": "dining", "tag": "Masterwork"},
    11: {"code": "WJWP-DVN-007", "sec_code": "DI-004", "title": "Forest Exile", "sub": "Dandakaranya in Classical Fresco", "cat": "heritage", "sp": "living", "tag": ""},
    12: {"code": "WJWP-DVN-008", "sec_code": "DI-005", "title": "Sovereign Court", "sub": "The Darbar of Sri Rama", "cat": "heritage", "sp": "living", "tag": ""},
    13: {"code": "WJWP-DVN-009", "sec_code": "DI-010", "title": "The Devoted Breath", "sub": "Panchamukhi Hanuman in Divine Radiance", "cat": "heritage", "sp": "temple", "tag": ""},
    14: {"code": "WJWP-DVN-010", "sec_code": "DI-011", "title": "The Sanjeevani Flight", "sub": "Hanuman Over the Ocean", "cat": "heritage", "sp": "living", "tag": ""},
    15: {"code": "WJWP-DVN-011", "sec_code": "DI-018", "title": "The Eternal Bond", "sub": "Rama & Hanuman in Sacred Devotion", "cat": "heritage", "sp": "temple", "tag": ""},
    16: {"code": "WJWP-DVN-012", "sec_code": "WJ-DC-001", "title": "The Ayodhya Arches", "sub": "Architectural Serenity in Saffron & Gold", "cat": "heritage", "sp": "living", "tag": ""},
    17: {"code": "WJWP-DVN-013", "sec_code": "WJ-DC-002", "title": "Darbar of the Ancients", "sub": "Royal Court in Classical Fresco", "cat": "heritage", "sp": "living", "tag": ""},
    18: {"code": "WJWP-DVN-014", "sec_code": "WJ-DC-003", "title": "Shadows of the Ghats", "sub": "Varanasi Dawn in Sepia", "cat": "heritage", "sp": "living", "tag": ""},
    19: {"code": "WJWP-DVN-015", "sec_code": "DI-006", "title": "The Kadamba Melody", "sub": "A Divine Frequency in the Golden Hour", "cat": "heritage", "sp": "bedroom", "tag": "Popular"},
    20: {"code": "WJWP-DVN-016", "sec_code": "DI-007", "title": "Visions of Vrindavan", "sub": "Krishna & The Sacred Grove", "cat": "heritage", "sp": "bedroom", "tag": ""},
    21: {"code": "WJWP-DVN-017", "sec_code": "DI-009", "title": "The Temple Sovereign", "sub": "Sanctum of Venkateswara", "cat": "heritage", "sp": "temple", "tag": ""},
    22: {"code": "WJWP-DVN-018", "sec_code": "DI-008", "title": "Pillar of Protection", "sub": "Ugra Narasimha in Sandstone", "cat": "heritage", "sp": "temple", "tag": ""},
    23: {"code": "WJWP-DVN-019", "sec_code": "DI-016", "title": "The Eternal Flute", "sub": "Krishna on the Moonlit River", "cat": "heritage", "sp": "bedroom", "tag": ""},
    24: {"code": "WJWP-DVN-020", "sec_code": "DI-012", "title": "Emerald Lotus Pond", "sub": "Ashta Lakshmi in Lotus Bloom", "cat": "heritage", "sp": "living", "tag": ""},
    25: {"code": "WJWP-DVN-021", "sec_code": "DI-013", "title": "Veena Resonance", "sub": "Goddess Saraswati in Pearl & Gold", "cat": "heritage", "sp": "office", "tag": ""},
    26: {"code": "WJWP-DVN-022", "sec_code": "DI-014", "title": "The Invincible Force", "sub": "Durga in Celestial Triumph", "cat": "heritage", "sp": "living", "tag": ""},
    27: {"code": "WJWP-DVN-023", "sec_code": "DI-015", "title": "Golden Sanctum", "sub": "Gilded Temple Gopuram Hall", "cat": "heritage", "sp": "temple", "tag": ""},
    28: {"code": "WJWP-DVN-024", "sec_code": "WJ-DC-006", "title": "The Royal Aviary", "sub": "Peacocks in Palace Gardens", "cat": "botanical", "sp": "dining", "tag": ""},
    29: {"code": "WJWP-DVN-025", "sec_code": "DI-017", "title": "Celestial Chariot", "sub": "Surya Sun Chariot Across the Dawn", "cat": "heritage", "sp": "living", "tag": ""},
    30: {"code": "WJWP-DVN-026", "sec_code": "WJ-DC-007", "title": "Resonance of Om", "sub": "Primal Sacred Syllable in Gold Foil", "cat": "heritage", "sp": "temple", "tag": ""},

    32: {"code": "WJWP-SIH-001", "sec_code": "TH-002", "title": "Temple Sanctuary", "sub": "Chola Granite Hall", "cat": "heritage", "sp": "living", "tag": ""},
    33: {"code": "WJWP-SIH-002", "sec_code": "TH-020", "title": "Chola Pillars", "sub": "Monumental Colonnade", "cat": "heritage", "sp": "living", "tag": ""},
    34: {"code": "WJWP-SIH-003", "sec_code": "TH-004", "title": "Abstract Gopuram", "sub": "Sunlit Geometric Temple Tower", "cat": "heritage", "sp": "living", "tag": ""},
    35: {"code": "WJWP-SIH-004", "sec_code": "WJ-HT-008", "title": "Forests of Dandaka", "sub": "Ancient River Forest in Mist", "cat": "heritage", "sp": "dining", "tag": ""},
    36: {"code": "WJWP-SIH-005", "sec_code": "TH-003", "title": "Chettinad Grandeur", "sub": "Burma Teak Pillars & Athangudi", "cat": "heritage", "sp": "living", "tag": ""},
    37: {"code": "WJWP-SIH-006", "sec_code": "WJ-HT-009", "title": "Chettinad Courtyard", "sub": "Sun-Washed Verandahs", "cat": "heritage", "sp": "living", "tag": ""},
    38: {"code": "WJWP-SIH-007", "sec_code": "TH-005", "title": "Tanjore Garden", "sub": "Antique Gold Botanicals on Tapestry Red", "cat": "heritage", "sp": "dining", "tag": ""},
    39: {"code": "WJWP-SIH-008", "sec_code": "WJ-HT-012", "title": "Tanjore Echoes", "sub": "Embossed Gold Peacocks over Burgundy", "cat": "heritage", "sp": "dining", "tag": ""},
    40: {"code": "WJWP-SIH-009", "sec_code": "TH-008", "title": "Kanjeevaram Weave", "sub": "Zari Brocade Lattice", "cat": "heritage", "sp": "bedroom", "tag": ""},
    41: {"code": "WJWP-SIH-010", "sec_code": "TH-006", "title": "Kolam Rhythm", "sub": "Dawn Dot Grid in Indigo", "cat": "heritage", "sp": "living", "tag": ""},
    42: {"code": "WJWP-SIH-011", "sec_code": "TH-007", "title": "Royal Tusker", "sub": "Caparisoned Temple Elephants", "cat": "heritage", "sp": "living", "tag": ""},
    43: {"code": "WJWP-SIH-012", "sec_code": "TH-001", "title": "Kumbakonam Stepwell", "sub": "Sacred Geometry & Stepped Bas-Relief", "cat": "heritage", "sp": "living", "tag": ""},

    44: {"code": "WJWP-BOT-001", "sec_code": "TH-013", "title": "Kerala Monsoon", "sub": "Rain-Washed Palms in Ten Green Shades", "cat": "botanical", "sp": "living", "tag": ""},
    45: {"code": "WJWP-BOT-002", "sec_code": "TH-014", "title": "Malabar Coast", "sub": "Twilight Coastal Palms", "cat": "botanical", "sp": "bedroom", "tag": ""},
    46: {"code": "WJWP-BOT-003", "sec_code": "WJ-HT-010", "title": "Kerala Palms & Kolam", "sub": "Banana Grove Cabana", "cat": "botanical", "sp": "dining", "tag": ""},
    47: {"code": "WJWP-BOT-004", "sec_code": "WJ-HT-021", "title": "Imperial Echoes", "sub": "Lacquered Peacocks & Peonies", "cat": "botanical", "sp": "dining", "tag": ""},
    48: {"code": "WJWP-BOT-005", "sec_code": "TH-010", "title": "Sacred Lotus", "sub": "Oversized Lotus in Lacquered Pink", "cat": "botanical", "sp": "living", "tag": ""},
    49: {"code": "WJWP-BOT-006", "sec_code": "TH-009", "title": "Jasmine Whispers", "sub": "Delicate Floral Climbing Vines", "cat": "botanical", "sp": "bedroom", "tag": ""},
    50: {"code": "WJWP-BOT-007", "sec_code": "TH-012", "title": "Kalamkari Dreams", "sub": "Jacobean Florals for Indian Light", "cat": "botanical", "sp": "living", "tag": ""},
    51: {"code": "WJWP-BOT-008", "sec_code": "TH-011", "title": "Peacock Pavilion", "sub": "Hand-Block Print Scale Repeat", "cat": "botanical", "sp": "living", "tag": ""},

    53: {"code": "WJWP-WCS-001", "sec_code": "WJWP-01", "title": "Gotham Deco", "sub": "Manhattan Skyline in Geometric Brass", "cat": "world", "sp": "office", "tag": ""},
    54: {"code": "WJWP-WCS-002", "sec_code": "WJWP-19", "title": "Manhattan Matrix", "sub": "New York Grid at Dusk", "cat": "world", "sp": "living", "tag": ""},
    55: {"code": "WJWP-WCS-003", "sec_code": "WJWP-18", "title": "Hollywood Glow", "sub": "Golden Era Palm Boulevard", "cat": "world", "sp": "dining", "tag": ""},
    56: {"code": "WJWP-WCS-004", "sec_code": "WJWP-17", "title": "Carioca Vibrance", "sub": "Rio Botanical & Coastal Hills", "cat": "world", "sp": "living", "tag": ""},
    57: {"code": "WJWP-WCS-005", "sec_code": "WJWP-16", "title": "Thames Heritage", "sub": "London Fog & Historic Riverfront", "cat": "world", "sp": "office", "tag": ""},
    58: {"code": "WJWP-WCS-006", "sec_code": "WJWP-02", "title": "Twilight Over Hong Kong", "sub": "Neon Reflections on Victoria Harbour", "cat": "world", "sp": "living", "tag": ""},
    59: {"code": "WJWP-WCS-007", "sec_code": "WJWP-03", "title": "Westminster Study", "sub": "Classical Architectural elevations", "cat": "world", "sp": "office", "tag": ""},
    60: {"code": "WJWP-WCS-008", "sec_code": "WJWP-11", "title": "Parisian Boulevard", "sub": "Haussmann Facades in Soft Sepia", "cat": "world", "sp": "living", "tag": ""},
    61: {"code": "WJWP-WCS-009", "sec_code": "WJWP-12", "title": "Canal Reflections", "sub": "Venetian Palazzos in Watercolour Mist", "cat": "world", "sp": "bedroom", "tag": ""},
    62: {"code": "WJWP-WCS-010", "sec_code": "WJWP-13", "title": "Bosphorus Gold", "sub": "Istanbul Domes at Sundown", "cat": "world", "sp": "living", "tag": ""},
    63: {"code": "WJWP-WCS-011", "sec_code": "WJWP-14", "title": "Desert Mirage", "sub": "Dubai Dunes & Towering Geometry", "cat": "world", "sp": "office", "tag": ""},
    64: {"code": "WJWP-WCS-012", "sec_code": "WJWP-04", "title": "Nile Silhouette", "sub": "Ancient Riverfront & Palm Horizons", "cat": "world", "sp": "dining", "tag": ""},
    65: {"code": "WJWP-WCS-013", "sec_code": "WJWP-15", "title": "Sydney Harbour Brilliance", "sub": "Opera Arches & Deep Blue Waters", "cat": "world", "sp": "living", "tag": ""},
    66: {"code": "WJWP-WCS-014", "sec_code": "WJWP-08", "title": "Arabian Dusk", "sub": "Old Souk Arches in Amber Light", "cat": "world", "sp": "living", "tag": ""},
    67: {"code": "WJWP-WCS-015", "sec_code": "WJWP-09", "title": "Shibuya Shadows", "sub": "Tokyo Night Geometry in Indigo", "cat": "world", "sp": "office", "tag": ""},
    68: {"code": "WJWP-WCS-016", "sec_code": "WJWP-05", "title": "Veneto Mist", "sub": "Northern Italian Lake Panorama", "cat": "world", "sp": "bedroom", "tag": ""},
    69: {"code": "WJWP-WCS-017", "sec_code": "WJWP-07", "title": "Botanic Horizon", "sub": "Singapore Supertrees & Tropical Foliage", "cat": "world", "sp": "living", "tag": ""},
    70: {"code": "WJWP-WCS-018", "sec_code": "WJWP-06", "title": "Harbour Brilliance", "sub": "Reflective Waterfronts Across Continents", "cat": "world", "sp": "living", "tag": ""},
    71: {"code": "WJWP-WCS-019", "sec_code": "WJWP-10", "title": "Mumbai Marine Drive", "sub": "Queen's Necklace in Art Deco Glamour", "cat": "world", "sp": "living", "tag": ""},

    73: {"code": "WJWP-CNT-001", "sec_code": "WJ-CE-013", "title": "Minimalist Mirage", "sub": "Geometric Balance in Textured Concrete & Brass", "cat": "abstract", "sp": "office", "tag": ""},
    74: {"code": "WJWP-CNT-002", "sec_code": "WJ-CE-014", "title": "The Abstract Arc", "sub": "Monumental Curved Planes in Warm Travertine", "cat": "abstract", "sp": "living", "tag": ""},
    75: {"code": "WJWP-CNT-003", "sec_code": "WJ-CE-015", "title": "Sculpted Sands", "sub": "Abstract Waves with Optical Depth", "cat": "abstract", "sp": "living", "tag": ""},
    76: {"code": "WJWP-CNT-004", "sec_code": "WJ-CE-016", "title": "Metallic Labyrinth", "sub": "Geometric Depth in Charcoal & Antique Brass", "cat": "abstract", "sp": "office", "tag": ""},
}

all_items = []

for p in kp_raw:
    idx = p['index']
    if idx not in concordance:
        continue
    c = concordance[idx]
    
    desc = p['desc']
    if not desc or len(desc) < 30:
        desc = f"{c['sub']}. A signature bespoke masterwork from the Kala Parampara collection. Handcrafted by Wall Jewels master artisans in Chennai, rendered on five premium substrates with custom dimensional scaling."
    else:
        # Clean OCR artifacts
        desc = re.sub(r'DESIGNNUMBER:[^\n]+', '', desc, flags=re.IGNORECASE)
        desc = re.sub(r'STYLE:[^\n]+', '', desc, flags=re.IGNORECASE)
        desc = re.sub(r'COLOURPALETTE:[^\n]+', '', desc, flags=re.IGNORECASE)
        desc = re.sub(r'IDEALFOR:[^\n]+', '', desc, flags=re.IGNORECASE)
        desc = re.sub(r'CUSTOMSIZEAVAILABLE:[^\n]+', '', desc, flags=re.IGNORECASE)
        desc = desc.strip()
        
    all_items.append({
        "id": f"kp-{idx:02d}",
        "v": "kala-parampara",
        "n": c["title"],
        "no": c["code"],
        "sub": c["sub"],
        "b": desc,
        "img": f"assets/img/collection/kala-parampara/kp-plate-{idx:02d}.jpg",
        "tag": c["tag"],
        "sp": c["sp"],
        "cat": c["cat"],
        "w": 3600,
        "h": 2700
    })

# Add Kala Rasa items
# Let's read the 179 Kala Rasa items from images
chapters = [
    {"r": range(7, 30), "cat": "heritage", "sp": "temple", "n_prefix": "Divine India — Masterpiece"},
    {"r": range(30, 48), "cat": "heritage", "sp": "living", "n_prefix": "Pichwai & Sacred Shrines"},
    {"r": range(48, 85), "cat": "botanical", "sp": "dining", "n_prefix": "Prakriti & Living Canopy"},
    {"r": range(85, 120), "cat": "botanical", "sp": "bedroom", "n_prefix": "Botanical Sanctuaries"},
    {"r": range(120, 145), "cat": "heritage", "sp": "living", "n_prefix": "Varanasi, Ghats & Sacred Waters"},
    {"r": range(145, 165), "cat": "abstract", "sp": "living", "n_prefix": "Scenic Panoramas & Mountain Sanctuaries"},
    {"r": range(165, 186), "cat": "abstract", "sp": "office", "n_prefix": "Monochrome & Contemporary Bas-Relief"}
]

for ch_idx, ch in enumerate(chapters, 1):
    for p_num in ch["r"]:
        img_p = f"assets/img/collection/kala-rasa/kr-plate-{p_num:03d}.jpg"
        code = f"WJWP-KR-{p_num:03d}"
        title = f"{ch['n_prefix']} #{p_num}"
        sub = f"Kala Rasa Chapter {ch_idx}"
        desc = f"Signature bespoke wallpaper mural from the prestigious Kala Rasa volume. Custom manufactured in Chennai by Wall Jewels since 1978 on five archival substrates."
        all_items.append({
            "id": f"kr-{p_num:03d}",
            "v": "kala-rasa",
            "n": title,
            "no": code,
            "sub": sub,
            "b": desc,
            "img": img_p,
            "tag": "",
            "sp": ch["sp"],
            "cat": ch["cat"],
            "w": 3600,
            "h": 2700
        })

print(f"Total unified collection items: {len(all_items)}")

# Generate data.js
data_js_content = f'''// Wall Jewels Master Collection Dataset
// Authentically synchronized with Kala Parampara Volume-I and Kala Rasa Master Catalogues

const VOLUMES = [
  {{ id: "kala-parampara", name: "Kala Parampara" }},
  {{ id: "kala-rasa", name: "Kala Rasa" }}
];

const SPACES = [
  {{ id: "living", label: "Living Rooms" }},
  {{ id: "dining", label: "Dining Suites" }},
  {{ id: "bedroom", label: "Bedrooms" }},
  {{ id: "temple", label: "Pooja & Temple" }},
  {{ id: "office", label: "Executive Offices" }}
];

const CATEGORIES = [
  {{ id: "heritage", label: "Sanatan & Heritage" }},
  {{ id: "botanical", label: "Botanical & Tropical" }},
  {{ id: "world", label: "World Cities" }},
  {{ id: "abstract", label: "Contemporary & 3D" }}
];

const COLLECTION = [
'''

for it in all_items:
    b_esc = it['b'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    n_esc = it['n'].replace('\\', '\\\\').replace('"', '\\"')
    sub_esc = it['sub'].replace('\\', '\\\\').replace('"', '\\"')
    data_js_content += f'''  {{
    id: "{it['id']}",
    v: "{it['v']}",
    n: "{n_esc}",
    no: "{it['no']}",
    sub: "{sub_esc}",
    b: "{b_esc}",
    img: "{it['img']}",
    tag: "{it['tag']}",
    sp: "{it['sp']}",
    cat: "{it['cat']}",
    w: {it['w']},
    h: {it['h']}
  }},
'''

data_js_content += '];\n'

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js_content)

print("Saved assets/js/data.js successfully!")
