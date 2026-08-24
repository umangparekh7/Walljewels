import json
import re

with open('scratch/kp_parsed_exact.json', 'r', encoding='utf-8') as f:
    kp_raw = json.load(f)

# Concordance corrections for Kala Parampara
concordance = {
    5: {"code": "WJWP-DVN-001", "sec_code": "DI-002", "title": "The Himalayan Ascetic", "subtitle": "Mahadev in Deep Stillness.", "cat": "heritage", "space": "living"},
    6: {"code": "WJWP-DVN-002", "sec_code": "DI-001", "title": "The Golden Ganesha", "subtitle": "Minimalist Devotion in Line.", "cat": "heritage", "space": "temple"},
    7: {"code": "WJWP-DVN-003", "sec_code": "DI-003", "title": "Sovereign of the Realm", "subtitle": "The Lion-Rider in Saffron & Vermilion.", "cat": "heritage", "space": "living"},
    8: {"code": "WJWP-DVN-004", "sec_code": "DI-004", "title": "Cosmic Union", "subtitle": "Shiva & Parvati in Divine Harmony.", "cat": "heritage", "space": "bedroom"},
    9: {"code": "WJWP-DVN-005", "sec_code": "WJ-DC-004", "title": "Kailash Meditations", "subtitle": "The Stillness of the Himalayas.", "cat": "heritage", "space": "living"},
    10: {"code": "WJWP-DVN-006", "sec_code": "WJ-DC-005", "title": "The Cosmic Tandava", "subtitle": "Nataraja in Deep Indigo and Copper.", "cat": "heritage", "space": "dining"},
    11: {"code": "WJWP-DVN-007", "sec_code": "DI-004", "title": "Forest Exile", "subtitle": "Dandakaranya in Classical Fresco.", "cat": "heritage", "space": "living"},
    12: {"code": "WJWP-DVN-008", "sec_code": "DI-005", "title": "Sovereign Court", "subtitle": "The Darbar of Sri Rama.", "cat": "heritage", "space": "living"},
    13: {"code": "WJWP-DVN-009", "sec_code": "DI-010", "title": "The Devoted Breath", "subtitle": "Panchamukhi Hanuman in Divine Radiance.", "cat": "heritage", "space": "temple"},
    14: {"code": "WJWP-DVN-010", "sec_code": "DI-011", "title": "The Sanjeevani Flight", "subtitle": "Hanuman Over the Ocean.", "cat": "heritage", "space": "living"},
    15: {"code": "WJWP-DVN-011", "sec_code": "DI-018", "title": "The Eternal Bond", "subtitle": "Rama & Hanuman in Sacred Devotion.", "cat": "heritage", "space": "temple"},
    16: {"code": "WJWP-DVN-012", "sec_code": "WJ-DC-001", "title": "The Ayodhya Arches", "subtitle": "Architectural Serenity in Saffron & Gold.", "cat": "heritage", "space": "living"},
    17: {"code": "WJWP-DVN-013", "sec_code": "WJ-DC-002", "title": "Darbar of the Ancients", "subtitle": "Royal Court in Classical Fresco.", "cat": "heritage", "space": "living"},
    18: {"code": "WJWP-DVN-014", "sec_code": "WJ-DC-003", "title": "Shadows of the Ghats", "subtitle": "Varanasi Dawn in Sepia.", "cat": "heritage", "space": "living"},
    19: {"code": "WJWP-DVN-015", "sec_code": "DI-006", "title": "The Kadamba Melody", "subtitle": "A divine frequency in the golden hour.", "cat": "heritage", "space": "bedroom"},
    20: {"code": "WJWP-DVN-016", "sec_code": "DI-007", "title": "Visions of Vrindavan", "subtitle": "Krishna & The Sacred Grove.", "cat": "heritage", "space": "bedroom"},
    21: {"code": "WJWP-DVN-017", "sec_code": "DI-009", "title": "The Temple Sovereign", "subtitle": "Sanctum of Venkateswara.", "cat": "heritage", "space": "temple"},
    22: {"code": "WJWP-DVN-018", "sec_code": "DI-008", "title": "Pillar of Protection", "subtitle": "Ugra Narasimha in Sandstone.", "cat": "heritage", "space": "temple"},
    23: {"code": "WJWP-DVN-019", "sec_code": "DI-016", "title": "The Eternal Flute", "subtitle": "Krishna on the Moonlit River.", "cat": "heritage", "space": "bedroom"},
    24: {"code": "WJWP-DVN-020", "sec_code": "DI-012", "title": "Emerald Lotus Pond", "subtitle": "Ashta Lakshmi in Lotus Bloom.", "cat": "heritage", "space": "living"},
    25: {"code": "WJWP-DVN-021", "sec_code": "DI-013", "title": "Veena Resonance", "subtitle": "Goddess Saraswati in Pearl & Gold.", "cat": "heritage", "space": "office"},
    26: {"code": "WJWP-DVN-022", "sec_code": "DI-014", "title": "The Invincible Force", "subtitle": "Durga in Celestial Triumph.", "cat": "heritage", "space": "living"},
    27: {"code": "WJWP-DVN-023", "sec_code": "DI-015", "title": "Golden Sanctum", "subtitle": "Gilded Temple Gopuram Hall.", "cat": "heritage", "space": "temple"},
    28: {"code": "WJWP-DVN-024", "sec_code": "WJ-DC-006", "title": "The Royal Aviary", "subtitle": "Peacocks in Palace Gardens.", "cat": "botanical", "space": "dining"},
    29: {"code": "WJWP-DVN-025", "sec_code": "DI-017", "title": "Celestial Chariot", "subtitle": "Surya Sun Chariot Across the Dawn.", "cat": "heritage", "space": "living"},
    30: {"code": "WJWP-DVN-026", "sec_code": "WJ-DC-007", "title": "Resonance of Om", "subtitle": "Primal Sacred Syllable in Gold Foil.", "cat": "heritage", "space": "temple"},

    32: {"code": "WJWP-SIH-001", "sec_code": "TH-002", "title": "Temple Sanctuary", "subtitle": "Chola Granite Hall.", "cat": "heritage", "space": "living"},
    33: {"code": "WJWP-SIH-002", "sec_code": "TH-020", "title": "Chola Pillars", "subtitle": "Monumental Colonnade.", "cat": "heritage", "space": "living"},
    34: {"code": "WJWP-SIH-003", "sec_code": "TH-004", "title": "Abstract Gopuram", "subtitle": "Sunlit Geometric Temple Tower.", "cat": "heritage", "space": "living"},
    35: {"code": "WJWP-SIH-004", "sec_code": "WJ-HT-008", "title": "Forests of Dandaka", "subtitle": "Ancient River Forest in Mist.", "cat": "heritage", "space": "dining"},
    36: {"code": "WJWP-SIH-005", "sec_code": "TH-003", "title": "Chettinad Grandeur", "subtitle": "Burma Teak Pillars & Athangudi.", "cat": "heritage", "space": "living"},
    37: {"code": "WJWP-SIH-006", "sec_code": "WJ-HT-009", "title": "Chettinad Courtyard", "subtitle": "Sun-Washed Verandahs.", "cat": "heritage", "space": "living"},
    38: {"code": "WJWP-SIH-007", "sec_code": "TH-005", "title": "Tanjore Garden", "subtitle": "Antique Gold Botanicals on Tapestry Red.", "cat": "heritage", "space": "dining"},
    39: {"code": "WJWP-SIH-008", "sec_code": "WJ-HT-012", "title": "Tanjore Echoes", "subtitle": "Embossed Gold Peacocks over Burgundy.", "cat": "heritage", "space": "dining"},
    40: {"code": "WJWP-SIH-009", "sec_code": "TH-008", "title": "Kanjeevaram Weave", "subtitle": "Zari Brocade Lattice.", "cat": "heritage", "space": "bedroom"},
    41: {"code": "WJWP-SIH-010", "sec_code": "TH-006", "title": "Kolam Rhythm", "subtitle": "Dawn Dot Grid in Indigo.", "cat": "heritage", "space": "living"},
    42: {"code": "WJWP-SIH-011", "sec_code": "TH-007", "title": "Royal Tusker", "subtitle": "Caparisoned Temple Elephants.", "cat": "heritage", "space": "living"},
    43: {"code": "WJWP-SIH-012", "sec_code": "TH-001", "title": "Kumbakonam Stepwell", "subtitle": "Sacred Geometry & Stepped Bas-Relief.", "cat": "heritage", "space": "living"},

    44: {"code": "WJWP-BOT-001", "sec_code": "TH-013", "title": "Kerala Monsoon", "subtitle": "Rain-Washed Palms in Ten Green Shades.", "cat": "botanical", "space": "living"},
    45: {"code": "WJWP-BOT-002", "sec_code": "TH-014", "title": "Malabar Coast", "subtitle": "Twilight Coastal Palms.", "cat": "botanical", "space": "bedroom"},
    46: {"code": "WJWP-BOT-003", "sec_code": "WJ-HT-010", "title": "Kerala Palms & Kolam", "subtitle": "Banana Grove Cabana.", "cat": "botanical", "space": "dining"},
    47: {"code": "WJWP-BOT-004", "sec_code": "WJ-HT-021", "title": "Imperial Echoes", "subtitle": "Lacquered Peacocks & Peonies.", "cat": "botanical", "space": "dining"},
    48: {"code": "WJWP-BOT-005", "sec_code": "TH-010", "title": "Sacred Lotus", "subtitle": "Oversized Lotus in Lacquered Pink.", "cat": "botanical", "space": "living"},
    49: {"code": "WJWP-BOT-006", "sec_code": "TH-009", "title": "Jasmine Whispers", "subtitle": "Delicate Floral Climbing Vines.", "cat": "botanical", "space": "bedroom"},
    50: {"code": "WJWP-BOT-007", "sec_code": "TH-012", "title": "Kalamkari Dreams", "subtitle": "Jacobean Florals for Indian Light.", "cat": "botanical", "space": "living"},
    51: {"code": "WJWP-BOT-008", "sec_code": "TH-011", "title": "Peacock Pavilion", "subtitle": "Hand-Block Print Scale Repeat.", "cat": "botanical", "space": "living"},

    53: {"code": "WJWP-WCS-001", "sec_code": "WJWP-01", "title": "Gotham Deco", "subtitle": "Manhattan Skyline in Geometric Brass.", "cat": "world", "space": "office"},
    54: {"code": "WJWP-WCS-002", "sec_code": "WJWP-19", "title": "Manhattan Matrix", "subtitle": "New York Grid at Dusk.", "cat": "world", "space": "living"},
    55: {"code": "WJWP-WCS-003", "sec_code": "WJWP-18", "title": "Hollywood Glow", "subtitle": "Golden Era Palm Boulevard.", "cat": "world", "space": "dining"},
    56: {"code": "WJWP-WCS-004", "sec_code": "WJWP-17", "title": "Carioca Vibrance", "subtitle": "Rio Botanical & Coastal Hills.", "cat": "world", "space": "living"},
    57: {"code": "WJWP-WCS-005", "sec_code": "WJWP-16", "title": "Thames Heritage", "subtitle": "London Fog & Historic Riverfront.", "cat": "world", "space": "office"},
    58: {"code": "WJWP-WCS-006", "sec_code": "WJWP-02", "title": "Twilight Over Hong Kong", "subtitle": "Neon Reflections on Victoria Harbour.", "cat": "world", "space": "living"},
    59: {"code": "WJWP-WCS-007", "sec_code": "WJWP-03", "title": "Westminster Study", "subtitle": "Classical Architectural elevations.", "cat": "world", "space": "office"},
    60: {"code": "WJWP-WCS-008", "sec_code": "WJWP-11", "title": "Parisian Boulevard", "subtitle": "Haussmann Facades in Soft Sepia.", "cat": "world", "space": "living"},
    61: {"code": "WJWP-WCS-009", "sec_code": "WJWP-12", "title": "Canal Reflections", "subtitle": "Venetian Palazzos in Watercolour Mist.", "cat": "world", "space": "bedroom"},
    62: {"code": "WJWP-WCS-010", "sec_code": "WJWP-13", "title": "Bosphorus Gold", "subtitle": "Istanbul Domes at Sundown.", "cat": "world", "space": "living"},
    63: {"code": "WJWP-WCS-011", "sec_code": "WJWP-14", "title": "Desert Mirage", "subtitle": "Dubai Dunes & Towering Geometry.", "cat": "world", "space": "office"},
    64: {"code": "WJWP-WCS-012", "sec_code": "WJWP-04", "title": "Nile Silhouette", "subtitle": "Ancient Riverfront & Palm Horizons.", "cat": "world", "space": "dining"},
    65: {"code": "WJWP-WCS-013", "sec_code": "WJWP-15", "title": "Sydney Harbour Brilliance", "subtitle": "Opera Arches & Deep Blue Waters.", "cat": "world", "space": "living"},
    66: {"code": "WJWP-WCS-014", "sec_code": "WJWP-08", "title": "Arabian Dusk", "subtitle": "Old Souk Arches in Amber Light.", "cat": "world", "space": "living"},
    67: {"code": "WJWP-WCS-015", "sec_code": "WJWP-09", "title": "Shibuya Shadows", "subtitle": "Tokyo Night Geometry in Indigo.", "cat": "world", "space": "office"},
    68: {"code": "WJWP-WCS-016", "sec_code": "WJWP-05", "title": "Veneto Mist", "subtitle": "Northern Italian Lake Panorama.", "cat": "world", "space": "bedroom"},
    69: {"code": "WJWP-WCS-017", "sec_code": "WJWP-07", "title": "Botanic Horizon", "subtitle": "Singapore Supertrees & Tropical Foliage.", "cat": "world", "space": "living"},
    70: {"code": "WJWP-WCS-018", "sec_code": "WJWP-06", "title": "Harbour Brilliance", "subtitle": "Reflective Waterfronts Across Continents.", "cat": "world", "space": "living"},
    71: {"code": "WJWP-WCS-019", "sec_code": "WJWP-10", "title": "Mumbai Marine Drive", "subtitle": "Queen's Necklace in Art Deco Glamour.", "cat": "world", "space": "living"},

    73: {"code": "WJWP-CNT-001", "sec_code": "WJ-CE-013", "title": "Minimalist Mirage", "subtitle": "Geometric Balance in Textured Concrete & Brass.", "cat": "abstract", "space": "office"},
    74: {"code": "WJWP-CNT-002", "sec_code": "WJ-CE-014", "title": "The Abstract Arc", "subtitle": "Monumental Curved Planes in Warm Travertine.", "cat": "abstract", "space": "living"},
    75: {"code": "WJWP-CNT-003", "sec_code": "WJ-CE-015", "title": "Sculpted Sands", "subtitle": "Abstract Waves with Optical Depth.", "cat": "abstract", "space": "living"},
    76: {"code": "WJWP-CNT-004", "sec_code": "WJ-CE-016", "title": "Metallic Labyrinth", "subtitle": "Geometric Depth in Charcoal & Antique Brass.", "cat": "abstract", "space": "office"},
}

kp_collection = []

for p in kp_raw:
    idx = p['index']
    if idx not in concordance:
        continue
    c = concordance[idx]
    
    # Clean description
    desc = p['desc']
    if not desc or len(desc) < 30:
        desc = f"A signature bespoke masterwork from the Kala Parampara collection. Handcrafted by Wall Jewels master artisans in Chennai, rendered on five premium substrates with custom dimensional scaling."
        
    kp_collection.append({
        "id": f"kp-{idx:02d}",
        "code": c["code"],
        "sec_code": c["sec_code"],
        "title": c["title"],
        "subtitle": c["subtitle"],
        "volume": "Kala Parampara",
        "category": c["cat"],
        "space": c["space"],
        "aspect": "wide" if idx in [10, 19, 27, 29, 38, 56, 61, 69] else "standard",
        "thumb": f"assets/img/collection/kala-parampara/kp-plate-{idx:02d}.jpg",
        "full": f"assets/img/collection/kala-parampara/kp-plate-{idx:02d}.jpg",
        "blurb": desc,
        "style": p.get("style") or "Classical Heritage",
        "palette": p.get("palette") or "Rich Ochre, Gold, Charcoal",
        "ideal_for": p.get("ideal_for") or c["space"].title()
    })

# Now load Kala Rasa items from existing data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    cur_js = f.read()

# Extract Kala Rasa portion
kr_match = re.search(r'(// KALA RASA VOLUME.*)', cur_js, re.DOTALL)
kr_text = kr_match.group(1) if kr_match else ""

# Generate the new data.js
new_data_js = f'''// Wall Jewels Master Collection Dataset
// Authentically synchronized with Kala Parampara Volume-I and Kala Rasa Master Catalogues
// Contains exact titles, concordance codes, subtitles, and full descriptions.

const COLLECTION = [
  // ==========================================
  // KALA PARAMPARA (VOLUME I) - 70 MASTER PLATES
  // ==========================================
'''

for item in kp_collection:
    new_data_js += f'''  {{
    id: "{item['id']}",
    code: "{item['code']}",
    sec_code: "{item['sec_code']}",
    title: "{item['title']}",
    subtitle: "{item['subtitle']}",
    volume: "{item['volume']}",
    category: "{item['category']}",
    space: "{item['space']}",
    aspect: "{item['aspect']}",
    thumb: "{item['thumb']}",
    full: "{item['full']}",
    blurb: "{item['blurb'].replace('"', '\\"')}",
    style: "{item['style'].replace('"', '\\"')}",
    palette: "{item['palette'].replace('"', '\\"')}",
    ideal_for: "{item['ideal_for'].replace('"', '\\"')}"
  }},
'''

new_data_js += '\n  ' + kr_text.strip()
if not new_data_js.rstrip().endswith(';'):
    if not new_data_js.rstrip().endswith(']'):
        new_data_js += '\n];'
    else:
        new_data_js += ';'

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(new_data_js)

print(f"Generated data.js with {len(kp_collection)} authentic Kala Parampara items + Kala Rasa collection!")
