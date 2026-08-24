import os
import re

# Read current data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# 1. KALA PARAMPARA (Filtered: ONLY actual wallpaper designs, removing all 8 requested index/intro pages)
# List of items to REMOVE:
# 'India, Interpreted Through Art', 'Heritage Master Index', 'Divine India: Sacred Iconography', 
# 'Prakriti: Forest Canopy', 'Prakriti: River Confluence', 'Prakriti: Mountain Sanctuary', 
# 'Kala Parampara Installation Folio', 'Kala Parampara Master Collection Index', 
# 'Kala Parampara (Volume I Cover)', 'Sanatan Iconography Overview', 'Southern Heritage Reimagined'

kp_raw_meta = [
    (5, 'The Himalayan Ascetic', 'WJWP-DVN-001', 'heritage', 'temple', 'Mahadev in deep stillness against snow-bound peaks; cinematic realism for contemplative rooms.', 'Signature'),
    (6, 'The Cosmic Dance', 'WJWP-DVN-002', 'heritage', 'living', 'Nataraja cast in bronze light — the rhythmic pulse of the universe on a single wall.', 'Bestseller'),
    (7, 'The Eternal Preserver', 'WJWP-DVN-003', 'heritage', 'living', 'Vishnu in golden serenity with radiant chakra and celestial radiance.', 'Signature'),
    (8, 'The Lotus Recliner', 'WJWP-DVN-004', 'heritage', 'bedroom', 'Anantha Padmanabha in cosmic repose across an emerald and gold horizon.', 'Bestseller'),
    (9, 'The Radiant Flutist', 'WJWP-DVN-005', 'heritage', 'bedroom', 'Krishna beneath the kadamba tree — flute frequencies in emerald and gold.', 'Curated'),
    (10, 'The Devoted Breath', 'WJWP-DVN-006', 'heritage', 'temple', 'Hanuman in saffron brushwork; unshakeable strength drawn in stillness.', 'Signature'),
    (11, 'The Golden Ganesha', 'WJWP-DVN-007', 'heritage', 'powder', 'A single gold line draws Ganesha on ivory — minimal, auspicious, serene.', 'Bestseller'),
    (12, 'Ganesha Bas-Relief', 'WJWP-DVN-008', 'heritage', 'temple', 'Carved-wood Ganesha rendered with true shadow depth for the pooja threshold.', 'Signature'),
    (13, 'The Invincible Sovereign', 'WJWP-DVN-009', 'heritage', 'living', 'Durga with her lion in layered vermilion and gold, commanding a double-height stair.', 'Bestseller'),
    (14, 'The Temple Sovereign', 'WJWP-DVN-010', 'heritage', 'living', 'A gilded gopuram interior glowing over a formal seating court.', 'Curated'),
    (15, 'Darbar of the Ancients', 'WJWP-DVN-011', 'heritage', 'living', 'A heritage mural of Rajarajeshwara court splendour, framed by carved arches.', 'Signature'),
    (16, 'The Sacred Flute', 'WJWP-DVN-012', 'heritage', 'bedroom', 'Krishna in the moonlit groves of Vrindavan with dancing peacocks.', 'Curated'),
    (17, 'Pichwai: Moonlit Grove', 'WJWP-DVN-013', 'heritage', 'dining', 'Nathdwara pichwai under a full moon — cows, kadamba and hanging garlands on deep indigo.', 'Signature'),
    (18, 'Pichwai: Eternal Melody', 'WJWP-DVN-014', 'heritage', 'living', 'Krishna at the heart of a garlanded grove; devotion painted flower by flower.', 'Bestseller'),
    (19, 'Shree Yantra Mandala', 'WJWP-DVN-015', 'heritage', 'temple', 'Sacred geometry and cosmic convergence in radiant gold foil and obsidian.', 'Signature'),
    (20, 'Resonance of Om', 'WJWP-DVN-016', 'heritage', 'temple', 'The primal syllable in beaten gold at the end of a lamp-lit corridor.', 'Curated'),
    (21, 'Tirupati Balaji Sanctum', 'WJWP-DVN-017', 'heritage', 'temple', 'Lord Venkateswara adorned in divine temple gold and flower garlands.', 'Signature'),
    (22, 'Goddess Saraswati Harmony', 'WJWP-DVN-018', 'heritage', 'office', 'Veena melodies and celestial swans in soft pearl, gold and ivory.', 'Curated'),
    (23, 'Lakshmi Lotus Throne', 'WJWP-DVN-019', 'heritage', 'dining', 'Ashta Lakshmi blessings enthroned upon blooming pink lotuses.', 'Bestseller'),
    (24, 'Ayodhya Ram Mandir Horizon', 'WJWP-DVN-020', 'heritage', 'living', 'Maryada Purushottam Ram in monumental sandstone architecture.', 'Signature'),
    (26, 'Chola Grand Colonnade', 'WJWP-SIH-001', 'heritage', 'hospitality', 'Monumental stone corridors of Thanjavur rendered with depth perspective.', 'Signature'),
    (27, 'Chola Pillars', 'WJWP-SIH-002', 'heritage', 'hospitality', 'Monumental stone colonnades for reception halls that mean business.', 'Bestseller'),
    (28, 'Brihadeeswara Silhouette', 'WJWP-SIH-003', 'heritage', 'living', 'The great temple vimana carved against the golden morning light.', 'Curated'),
    (29, 'Abstract Gopuram', 'WJWP-SIH-004', 'heritage', 'living', 'The temple tower reduced to sunlit geometry — heritage for modern minimalists.', 'Signature'),
    (30, 'Madurai Meenakshi Corridor', 'WJWP-SIH-005', 'heritage', 'living', 'The thousand pillar hall in deep atmospheric shadow and temple lamp glow.', 'Bestseller'),
    (31, 'Chettinad Grandeur', 'WJWP-SIH-006', 'heritage', 'dining', 'Athangudi patterns and arched verandahs from the mansions of Karaikudi.', 'Signature'),
    (32, 'Karaikudi Courtyard', 'WJWP-SIH-007', 'heritage', 'dining', 'Burma teak pillars and sun-washed central courtyards of Chettinad.', 'Curated'),
    (33, 'Athangudi Geometric Lattice', 'WJWP-SIH-008', 'heritage', 'powder', 'Handcrafted tile motifs in kiln red, mustard ochre, and deep bottle green.', 'Curated'),
    (34, 'Hampi Stone Chariot', 'WJWP-SIH-009', 'heritage', 'office', 'Hampi’s chariot in painterly mist — history as a headboard for ambition.', 'Signature'),
    (35, 'Tanjore Golden Peacocks', 'WJWP-SIH-010', 'heritage', 'bedroom', 'Embossed gold foil peacocks over deep tapestry red and gold leaf.', 'Bestseller'),
    (36, 'Tanjore Garden', 'WJWP-SIH-011', 'heritage', 'living', 'Antique gold botanicals on deep tapestry red, in the manner of temple murals.', 'Signature'),
    (37, 'Tanjore Echoes', 'WJWP-SIH-012', 'heritage', 'bedroom', 'Embossed-gold peacocks over burgundy — the opulence of Tanjore painting, wall-scale.', 'Bestseller'),
    (38, 'Kanchipuram Silk Lattice', 'WJWP-SIH-013', 'heritage', 'bedroom', 'Zari weave geometry and silk luster inspired by legendary South Indian looms.', 'Curated'),
    (39, 'The Great Kolam', 'WJWP-SIH-014', 'heritage', 'living', 'Antique gold kolam lattice and lotus vines across a grand chandelier-lit hall.', 'Signature'),
    (40, 'Kolam Rhythm', 'WJWP-SIH-015', 'heritage', 'office', 'The dawn dot-grid of Tamil thresholds, drawn in indigo on soft white.', 'Bestseller'),
    (41, 'The Royal Tusker', 'WJWP-SIH-016', 'heritage', 'hospitality', 'Caparisoned elephants in carved-stone grisaille for grand lobbies.', 'Signature'),
    (42, 'Kerala Backwaters Horizon', 'WJWP-BTS-001', 'tropical', 'bedroom', 'A backwater vista in watercolour — houseboat, palms and evening light.', 'Bestseller'),
    (43, 'Malabar Coast Palm', 'WJWP-BTS-002', 'tropical', 'bedroom', 'Coastal palms and serene waters under warm tropical twilight.', 'Curated'),
    (44, 'Tropical Emerald Jungle', 'WJWP-BTS-003', 'tropical', 'living', 'Dense understorey greens wrapped around velvet seating — the conservatory effect.', 'Signature'),
    (45, 'Kerala Monsoon', 'WJWP-BTS-004', 'tropical', 'bedroom', 'Rain-washed palms in ten shades of green; the calmest wall in the tropics.', 'Bestseller'),
    (46, 'Banana Grove Cabana', 'WJWP-BTS-005', 'tropical', 'powder', 'Bright banana fronds behind rattan — instant holiday, zero maintenance.', 'Curated'),
    (47, 'Lotus Bloom Serenity', 'WJWP-BTS-006', 'botanical', 'living', 'Oversized lotus and peacock in lacquered pinks — softness at architectural scale.', 'Signature'),
    (48, 'Verdant Chinoiserie Hall', 'WJWP-BTS-007', 'botanical', 'hospitality', 'Chinoiserie fruit and vine climbing a double-height dining hall.', 'Curated'),
    (49, 'Chintz Botanical Revival', 'WJWP-BOT-007', 'botanical', 'dining', 'Jacobean florals recoloured for South Indian light.', 'Signature'),
    (50, 'Emerald Block Print', 'WJWP-BOT-008', 'botanical', 'living', 'A hand-block repeat scaled to the wall, in one committed green.', 'Bestseller'),
    (51, 'Peacock Sanctuary', 'WJWP-BOT-009', 'botanical', 'bedroom', 'Peacocks among peonies in porcelain tones — quiet grandeur for principal bedrooms.', 'Curated'),
    (52, 'Monsoon Lotus Pond', 'WJWP-BOT-010', 'botanical', 'powder', 'Hand-painted lotus pond enclosing a brass-fitted bath.', 'Curated'),
    (53, 'Nilgiri Tea Mist', 'WJWP-BOT-011', 'botanical', 'living', 'Rolling green tea plantations in morning fog and eucalyptus mist.', 'Curated'),
    (54, 'Gulmohar Canopy', 'WJWP-BOT-012', 'botanical', 'dining', 'Fiery vermilion gulmohar blossoms over light wood furniture.', 'Curated'),
    (55, 'Royal Banyan Grove', 'WJWP-BOT-013', 'botanical', 'hospitality', 'Ancient banyan canopy with sunlight filtering through emerald leaves.', 'Signature'),
    (56, 'London Westminster Study', 'WJWP-WCS-001', 'world', 'office', 'Westminster in sepia wash behind a leather-topped desk.', 'Signature'),
    (57, 'Parisian Boulevard & Seine', 'WJWP-WCS-002', 'world', 'living', 'The Seine drawn in bookish greys for readers and romantics.', 'Curated'),
    (58, 'New York Manhattan Skyline', 'WJWP-WCS-003', 'world', 'office', 'A pencil-grey skyline rising the full height of a stairwell.', 'Signature'),
    (59, 'Rome Colosseum Arches', 'WJWP-WCS-004', 'world', 'dining', 'Rome in architect’s pencil, dining-room scale.', 'Bestseller'),
    (60, 'Colosseum Architectural Suite', 'WJWP-WCS-008', 'world', 'dining', 'Monumental Roman colonnades wrapping a grand banquet room.', 'Signature'),
    (61, 'Venetian Grand Canal', 'WJWP-WCS-009', 'world', 'living', 'Historic palazzos and gondolas in soft watercolours.', 'Curated'),
    (62, 'Bosphorus Twilight', 'WJWP-WCS-010', 'world', 'living', 'Hagia Sophia over silk-dark waters in miniature-painting jewel tones.', 'Signature'),
    (63, 'Dubai Future Skyline', 'WJWP-WCS-011', 'world', 'office', 'Geometric towers and golden sands at futuristic dusk.', 'Curated'),
    (64, 'Singapore Gardens Bay', 'WJWP-WCS-012', 'world', 'office', 'Singapore’s supertrees in watercolour for forward-looking rooms.', 'Signature'),
    (65, 'Tokyo Cherry Blossom Alley', 'WJWP-WCS-013', 'world', 'bedroom', 'Delicate sakura branches and Japanese pagodas in gentle mist.', 'Curated'),
    (66, 'Sydney Harbour Brilliance', 'WJWP-WCS-018', 'world', 'living', 'The crystalline clarity of coastal modernism — Opera House & Harbour Bridge.', 'Signature'),
    (67, 'Mumbai Marine Drive', 'WJWP-WCS-019', 'world', 'living', 'The Queen’s Necklace at dusk — Mumbai’s curve of light across your wall.', 'Bestseller'),
    (68, 'Delhi India Gate Monument', 'WJWP-WCS-020', 'world', 'living', 'The sandstone arch in golden-hour monumental calm.', 'Curated'),
    (69, 'Jaipur Hawa Mahal Lattice', 'WJWP-WCS-021', 'heritage', 'living', 'The iconic honeycomb pink facade in delicate royal gouache.', 'Signature'),
    (70, 'Udaipur Lake Palace Vista', 'WJWP-WCS-022', 'heritage', 'bedroom', 'White marble reflections across the tranquil waters of Pichola.', 'Bestseller'),
    (71, 'Varanasi Ghats at Dawn', 'WJWP-WCS-023', 'heritage', 'temple', 'Spiritual riverfront steps illuminated by golden morning lamps.', 'Signature'),
    (72, 'Amritsar Golden Temple Glow', 'WJWP-WCS-024', 'heritage', 'temple', 'Harmandir Sahib glowing in the sacred waters of the Amrit Sarovar.', 'Bestseller'),
    (73, 'Kolkata Howrah Bridge Mist', 'WJWP-WCS-025', 'world', 'living', 'The majestic steel bridge spanning the Hooghly at twilight.', 'Curated'),
    (74, 'Goa Portuguese Balcao', 'WJWP-WCS-026', 'tropical', 'dining', 'Heritage terracotta tiles and sunlit yellow villa verandahs.', 'Curated'),
    (75, 'Himalayan Monastery Peak', 'WJWP-WCS-027', 'heritage', 'office', 'High-altitude Tibetan monastery amidst snow-crowned peaks.', 'Signature'),
    (76, 'Rann of Kutch Moonlight', 'WJWP-WCS-028', 'abstract', 'bedroom', 'Infinite white salt desert gleaming beneath the full moon.', 'Curated')
]

kp_entries = []
for idx, n, no, c, s, b, tag in kp_raw_meta:
    img_path = f'assets/img/collection/kala-parampara/kp-plate-{idx:02d}.jpg'
    tag_part = f", tag: '{tag}'" if tag else ""
    kp_entries.append(
        f"  {{ n: '{n}', no: '{no}', v: 'kala-parampara', c: '{c}', s: '{s}',\n"
        f"    b: '{b}',\n"
        f"    img: '{img_path}'{tag_part} }}"
    )

kp_code = "  /* ==========================================================================\n" \
          "     VOLUME I: KALA PARAMPARA (Pure Wallpaper Artwork Plates)\n" \
          "     ========================================================================== */\n" + \
          ",\n".join(kp_entries)

# 2. KALA RASA (Complete 179 Plates from page 7 to 185)
kr_categories = [
    # Pages 7..36 -> Divine India (Sacred Deities)
    (7, 36, 'heritage', 'temple', 'WJWP-DVN', 'Divine India'),
    # Pages 37..62 -> Dravidian Heritage Murals
    (37, 62, 'heritage', 'living', 'WJWP-DRV', 'Dravidian Heritage'),
    # Pages 63..88 -> South Indian Art Murals
    (63, 88, 'heritage', 'dining', 'WJWP-SIH', 'South Indian Art'),
    # Pages 89..114 -> The Kolam Collection
    (89, 114, 'abstract', 'living', 'WJWP-KLM', 'Kolam Masterpiece'),
    # Pages 115..140 -> Tropical South
    (115, 140, 'tropical', 'bedroom', 'WJWP-TRP', 'Tropical South'),
    # Pages 141..160 -> South Indian Tales / Kids
    (141, 160, 'kids', 'kids', 'WJWP-KDS', 'South Indian Tales'),
    # Pages 161..185 -> South Indian Modernism / Abstract
    (161, 185, 'abstract', 'office', 'WJWP-MOD', 'South Indian Modernism')
]

# Curated specific names for Kala Rasa key designs
kr_named = {
    7: ('Divine India Masterpiece Collection', 'Overview of sacred iconography and temple deities.', 'Curated'),
    8: ('Ganesha: The Auspicious Beginning', 'Contemporary sacred Ganesha with blooming lotuses in ivory and antique gold.', 'Signature'),
    9: ('Mahadev in Cosmic Solitude', 'Shiva in deep meditation amidst sacred cosmic mists and gold radiance.', 'Bestseller'),
    10: ('Nataraja: The Celestial Rhythm', 'The cosmic dancer in swirling dynamic motion and molten bronze light.', 'Signature'),
    11: ('Lord Murugan with Peacock', 'The warrior god of southern hills with regal peacock and sacred vel.', 'Bestseller'),
    12: ('Balaji Tirupati Divine Darshan', 'Lord Venkateswara adorned in diamond temple jewelry and fresh tulsi garlands.', 'Signature'),
    13: ('Goddess Lakshmi Lotus Sanctuary', 'Goddess of abundance upon pink lotus blooms in warm golden light.', 'Bestseller'),
    14: ('Saraswati Veena Harmony', 'Goddess of learning and arts in serene ivory, pearl and golden strings.', 'Signature'),
    15: ('Hanuman: Pillar of Devotion', 'Saffron-rendered strength and steadfast devotion for meditative spaces.', 'Curated'),
    16: ('Krishna with Kadamba & Flute', 'The divine flutist in moonlit Vrindavan grove with dancing peacocks.', 'Bestseller'),
    17: ('Pichwai: Shrinathji Sanctum', 'Traditional Nathdwara temple backdrop in rich ultramarine and gold foil.', 'Signature'),
    18: ('Pichwai: Lotus Pond Symphony', 'Cows and blooming lotus clusters under the full autumn moon.', 'Bestseller'),
    19: ('Durga Mahishasuramardini', 'The divine protector on her golden lion in radiant vermilion victory.', 'Signature'),
    20: ('Ardhanarishvara Balance', 'The sacred union of Shiva and Shakti in balanced bronze and lotus tones.', 'Curated'),
    21: ('Radha Krishna Eternal Love', 'Divine love painted in lush monsoon groves with blossoming vines.', 'Signature'),
    22: ('Ayodhya Rama Rajyabhisheka', 'The coronation of Lord Rama amidst golden arches and royal darbar.', 'Bestseller'),
    23: ('Chola Nataraja Bronze Relief', 'Architectural stone and bronze bas-relief for grand entrance foyers.', 'Signature'),
    24: ('Navagraha Mandala Sphere', 'The nine celestial planetary forces arranged in geometric cosmic harmony.', 'Curated'),
    25: ('Panchamukhi Hanuman Guardian', 'The five-faced protector in dynamic warrior poise and golden armor.', 'Signature'),
    26: ('Dhanvantari Healing Herb Grove', 'The divine physician amidst medicinal herbs and ambrosia nectar.', 'Curated'),
    27: ('Kamakshi Amman Golden Sanctum', 'Kanchipuram goddess in royal silk sari and golden temple aura.', 'Signature'),
    28: ('Meenakshi Sundareswarar Wedding', 'The celestial wedding of Madurai rendered in opulent temple colors.', 'Bestseller'),
    29: ('Vishnu Anantasayana Ocean', 'The cosmic preserver resting upon Sheshanaga on the milk ocean.', 'Signature'),
    30: ('Ganesha Terracotta Relief', 'Hand-pressed terracotta pooja room panel with deep tactile relief.', 'Curated'),
    31: ('Kashi Vishwanath Corridor', 'Sacred ghats and temple bells echoing along the ancient Ganga.', 'Signature'),
    32: ('Ranganathaswamy Gopuram Grandeur', 'The towering multi-tiered gopuram of Srirangam in sunset gold.', 'Bestseller'),
    33: ('Subrahmanya Dhandayuthapani', 'Palani hill temple ascetic form in pure spiritual stillness.', 'Curated'),
    34: ('Bhairava Night Sanctuary', 'Fierce guardian deity in midnight indigo and antique copper flame.', 'Curated'),
    35: ('Ashta Lakshmi Floral Court', 'Eight manifestations of prosperity surrounding a sacred lotus pond.', 'Signature'),
    36: ('Om Namah Shivaya Calligraphy', 'Sacred Sanskrit mantras woven into radiant gold leaf geometry.', 'Bestseller'),

    # Dravidian Heritage Murals (37..62)
    37: ('Dravidian Heritage Murals', 'Monumental temple halls, stone chariots, and granite colonnades.', 'Curated'),
    38: ('Thanjavur Palace Courtyard', 'Royal Nayak palace pillars with carved arches and Athangudi flooring.', 'Signature'),
    39: ('Madurai Thousand Pillar Hall', 'Atmospheric perspective of stone colonnades in lamp-lit evening mist.', 'Bestseller'),
    40: ('Brihadeeswara Temple Colonnade', 'Granite corridor of the Big Temple with historic relief carvings.', 'Signature'),
    41: ('Hampi Stone Chariot at Dawn', 'The iconic Vijayanagara chariot framed by morning mist and ruins.', 'Bestseller'),
    42: ('Chettinad Mansion Verandah', 'Burma teak carved columns and sunlit interior courtyard arches.', 'Signature'),
    43: ('Athangudi Heritage Floral Tile', 'Handmade heritage geometric patterns in earth ochre and terracotta.', 'Curated'),
    44: ('Kumbakonam Mahamaham Tank', 'Sacred temple stepwell surrounded by sixteen decorative mandapams.', 'Curated'),
    45: ('Padmanabhapuram Wooden Palace', 'Intricate Kerala woodwork and antique lattice windows overlooking gardens.', 'Signature'),
    46: ('Mahabalipuram Shore Temple', 'Ancient monoliths standing proud against the crashing ocean waves.', 'Bestseller'),
    47: ('Kanchipuram Ekambareswarar Arches', 'Sacred temple mango tree sanctum framed by monumental stone arches.', 'Signature'),
    48: ('Tiruvannamalai Annamalaiyar Glow', 'The sacred holy mountain illuminated by the Karthigai Deepam fire.', 'Signature'),
    49: ('Srirangam Temple Gateway', 'Towering Rajagopuram rising into the morning sky above coconut groves.', 'Bestseller'),
    50: ('Karaikudi Heritage Dining Court', 'Grand banquet court framed by multi-arched verandahs and fountains.', 'Signature'),
    51: ('Chettinad Teak Doorway Passage', 'Intricately carved doorway with brass hardware and Athangudi tiles.', 'Curated'),
    52: ('Chola Royal War Fleet', 'Ancient South Indian naval ships sailing into the Bay of Bengal.', 'Curated'),
    53: ('Lepakshi Hanging Pillar Mystery', 'Carved monolithic granite pillar defying gravity in the Veerabhadra hall.', 'Signature'),
    54: ('Gingee Fort Mountain Citadel', 'Impregnable mountain fortress rising into the golden dusk clouds.', 'Curated'),
    55: ('Rameshwaram Corridor of Pillars', 'The world’s longest temple corridor with rhythmic carved columns.', 'Bestseller'),
    56: ('Belur Chennakeshava Filigree', 'Hoysala stone filigree and celestial dancing apsaras carved in soapstone.', 'Signature'),
    57: ('Halebidu Hoysaleswara Relief', 'Layered friezes of war elephants, lions, and mythological epics.', 'Signature'),
    58: ('Tanjore Maratha Royal Library', 'Historic Saraswathi Mahal library tableau with vintage maps and folios.', 'Curated'),
    59: ('Pondicherry French Quarter Colonnade', 'Colonial mustard yellow arches and bougainvillea over heritage streets.', 'Curated'),
    60: ('Cochin Fort Dutch Palace Mural', 'Rich tempera murals depicting the Ramayana in earthy ochres and indigo.', 'Signature'),
    61: ('Hampi Virupaksha Riverbank', 'Ancient bazaar ruins along the Tungabhadra river under sunset light.', 'Bestseller'),
    62: ('Dravidian Architectural Panorama', 'Composite panorama of South India’s greatest architectural wonders.', 'Signature'),

    # South Indian Art Murals (63..88)
    63: ('South Indian Art Murals', 'Classical Tanjore, Kerala murals, and traditional textile motifs.', 'Curated'),
    64: ('Tanjore Gold Leaf Peacocks', '24K embossed gold foil peacocks with semi-precious gem accents on ruby.', 'Signature'),
    65: ('Kerala Temple Mural Lotus', 'Natural vegetable dye fresco of lotuses and peacocks on earthen plaster.', 'Bestseller'),
    66: ('Kalamkari Tree of Life', 'Hand-painted pen Kalamkari tree with paradise birds and floral branches.', 'Signature'),
    67: ('Mysore Gilded Court Painting', 'Delicate gesso work and gold foil depicting royal durbar splendor.', 'Curated'),
    68: ('Poompuhar Ancient Port Tale', 'Sangam era coastal trade and silk merchants in painterly gouache.', 'Curated'),
    69: ('Tanjore Royal Durbar Tableau', 'King Serfoji II in his ceremonial court framed by draped velvet curtains.', 'Signature'),
    70: ('Kanchipuram Zari Brocade Repeat', 'Pure silk zari weave pattern scaled to architectural wall proportions.', 'Bestseller'),
    71: ('Chettinad Terracotta Folk Art', 'Aiyanar terracotta horses guarding village thresholds under banyan trees.', 'Curated'),
    72: ('Kerala Mural Elephant Parade', 'Caparisoned temple elephants in traditional gold Nettipattam headdresses.', 'Signature'),
    73: ('Tanjore Floral Arabesque', 'Gold leaf floral vines weaving across a deep emerald tapestry ground.', 'Bestseller'),
    74: ('Chola Bronze Master Sculptor', 'Lost-wax bronze casting atelier in the historic town of Swamimalai.', 'Curated'),
    75: ('Kalamkari Peacock Medallion', 'Circular floral medallion with intertwined peacocks in madder red and indigo.', 'Signature'),
    76: ('Tanjore Saraswati Gold Relief', 'Goddess of music and wisdom embellished with authentic 24K gold foil.', 'Signature'),
    77: ('Kerala Murals: Radha Madhava', 'Krishna and Radha surrounded by gopis and cows in classical mural tones.', 'Bestseller'),
    78: ('Athangudi Artisan Tile Rhythm', 'Hand-poured cement tile geometry in vibrant mustard and royal cobalt.', 'Curated'),
    79: ('Tanjore Royal Elephant Procession', 'Gilded temple tuskers carrying the royal deity under velvet umbrellas.', 'Signature'),
    80: ('South Indian Classical Dance Mudras', 'Bharatanatyam hand gestures and postures illustrated in fine gold lines.', 'Curated'),
    81: ('Kalamkari Forest Hunt Tapestry', 'Historic royal hunting scene framed by blooming lotus and deer.', 'Curated'),
    82: ('Tanjore Balaji Golden Icon', 'Lord of Seven Hills embossed in heavy gold gesso relief on crimson.', 'Bestseller'),
    83: ('Kerala Temple Boat Race Thrill', 'Chundan Vallam snake boats slicing through backwaters with hundred oars.', 'Signature'),
    84: ('Pichwai Gold Cow Medallion', 'Sacred Kamadhenu cow surrounded by lotuses and silver kadamba blooms.', 'Signature'),
    85: ('Tanjore Krishna Butter Thief', 'Little Makhan Chor Krishna with butter pots in sparkling golden leaf.', 'Bestseller'),
    86: ('Mysore Rosewood Inlay Floral', 'Geometric floral inlays reminiscent of royal Mysore palace woodwork.', 'Curated'),
    87: ('South Indian Temple Bell Symphony', 'Bronze temple bells hanging from carved granite temple ceilings.', 'Curated'),
    88: ('Tanjore Golden Gopuram Crest', 'The pinnacle kalasam of a temple gopuram glowing under the midday sun.', 'Signature'),

    # The Kolam Collection (89..114)
    89: ('The Kolam Collection', 'Sacred geometry, rice flour threshold art, and dawn mandala grids.', 'Curated'),
    90: ('The Grand Kolam of Madurai', 'Continuous labyrinthine gold loop knot over deep midnight charcoal.', 'Signature'),
    91: ('Margazhi Dawn Lotus Kolam', 'Threshold flower mandala drawn in rice flour with kaavi border lines.', 'Bestseller'),
    92: ('Sacred Sikku Kolam Matrix', 'Interlocking geometric knot lines weaving around symmetric dots.', 'Signature'),
    93: ('Hridaya Kamala Heart Lotus', 'Eight-petaled heart lotus mandala invoking auspicious cosmic balance.', 'Bestseller'),
    94: ('Brahma Mudi Infinity Knot', 'Endless loop knot without beginning or end in gleaming 24K gold foil.', 'Signature'),
    95: ('Chariot Ratha Kolam Grid', 'Temple chariot drawn in precise dot geometry for festive doorways.', 'Curated'),
    96: ('Kuberan Wealth Geometric Grid', 'Sacred yantra numbers and symmetry bringing prosperity to living rooms.', 'Signature'),
    97: ('Peacock Mayil Kolam Flourish', 'Graceful peacock forms woven from continuous rice-flour curves.', 'Bestseller'),
    98: ('Aishwarya Star Kolam Harmony', 'Overlapping geometric stars in soft ivory on warm terra cotta.', 'Curated'),
    99: ('Agni Sacred Fire Kolam', 'Radiant solar mandala with flame petals and cosmic geometric rings.', 'Curated'),
    100: ('Emerald Block Print & Kolam', 'White floral woodblock repeats intertwined with subtle kolam lattices.', 'Signature'),
    101: ('Gold Wire Pulli Dot Kolam', 'Minimalist metallic gold lines weaving through precise ivory dots.', 'Bestseller'),
    102: ('Navagraha Nine Dot Kolam', 'Cosmic planetary alignment drawn in sacred threshold symmetry.', 'Curated'),
    103: ('Neli Kolam Curved Wave Matrix', 'Flowing water waves and vine loops in deep indigo and pearl.', 'Signature'),
    104: ('Swastika Auspicious Kolam', 'Four-fold rotational symmetry in gold leaf on raw linen texture.', 'Curated'),
    105: ('Chitira Festival Star Kolam', 'Intricate geometric starburst celebrating the Tamil New Year.', 'Signature'),
    106: ('Deepam Lamp Kolam Ring', 'Array of earthen oil lamps surrounded by glowing geometric flourishes.', 'Bestseller'),
    107: ('Thousand Dot Temple Floor Kolam', 'Monumental temple courtyard floor pattern rendered at full wall scale.', 'Signature'),
    108: ('Padi Kolam Stepped Threshold', 'Structured parallel lines and geometric borders for grand hallways.', 'Curated'),
    109: ('Kurinji Blossom Kolam Rhythm', 'Rare twelve-year mountain blossom geometry in royal purple and gold.', 'Curated'),
    110: ('Gopuram Geometric Pinnacle', 'Temple tower silhouette constructed entirely from precise dot grids.', 'Signature'),
    111: ('Kaavi Red & Ivory Kolam Contrast', 'Traditional red clay ground with crisp white rice-powder ribbons.', 'Bestseller'),
    112: ('Modernist Minimal Kolam Line', 'Contemporary architectural interpretation with single continuous line.', 'Signature'),
    113: ('Sahasrara Crown Chakra Kolam', 'Thousand-petaled lotus mandala for yoga and meditation sanctuaries.', 'Signature'),
    114: ('Kolam Geometric Master Tableau', 'Panoramic tapestry of the South’s most sacred threshold designs.', 'Signature'),

    # Tropical South (115..140)
    115: ('Tropical South Collection', 'Lush Kerala backwaters, banana groves, and coastal palm sanctuaries.', 'Curated'),
    116: ('Backwater Haven Sunset', 'Traditional houseboat gliding through palm reflections at golden dusk.', 'Signature'),
    117: ('Emerald Jungle Canopy', 'Deep layered rainforest leaves wrapping velvet seating in green calm.', 'Bestseller'),
    118: ('Malabar Coastal Palm Grove', 'Swaying coconut palms against the azure Arabian Sea horizon.', 'Signature'),
    119: ('Kerala Monsoon on Broad Leaves', 'Rain-washed banana leaves and water droplets in ten green shades.', 'Bestseller'),
    120: ('Banana Leaf & Cane Retreat', 'Broad tropical leaves behind rattan seating for sunlit verandahs.', 'Curated'),
    121: ('Lotus Lagoon Serenade', 'Giant pink lotus blossoms floating over clear fresh spring waters.', 'Signature'),
    122: ('Misty Nilgiri Tea Hills', 'Rolling emerald plantations blanketed in morning mountain clouds.', 'Bestseller'),
    123: ('Chintz Foliage & Songbirds', 'Jacobean climbing vines and exotic birds recoloured for Indian light.', 'Signature'),
    124: ('Tropical Water Lily Conservatory', 'Aquatic garden filled with purple and white lilies under glass.', 'Curated'),
    125: ('Gulmohar Red Blossom Avenue', 'Fiery crimson canopy shading a sunlit coastal avenue.', 'Curated'),
    126: ('Sacred Banyan Aerial Canopy', 'Ancient banyan tree roots filtering golden sunlight across the wall.', 'Signature'),
    127: ('Malabar Spice Garden Vista', 'Cardamom, pepper vines and cinnamon trees in lush botanical detail.', 'Curated'),
    128: ('Silent Valley Rainforest Mist', 'Untouched Western Ghats canopy in deep moss and emerald layers.', 'Signature'),
    129: ('Coromandel Coast Wave & Palm', 'Dramatic ocean breakers against coastal cliffs and casuarina groves.', 'Bestseller'),
    130: ('Tropical Fern Cathedral', 'Towering giant tree ferns creating a natural architectural canopy.', 'Signature'),
    131: ('Mangrove Estuary Reflections', 'Pristine Sundarban and Pichavaram waterways with wading birds.', 'Curated'),
    132: ('Peacock in Tropical Bamboo Grove', 'Wild peacocks perched amongst golden bamboo stems and orchids.', 'Signature'),
    133: ('Wayanad Coffee Plantation Mist', 'Flowering white coffee blossoms and shade trees on gentle slopes.', 'Curated'),
    134: ('Anamalai Elephant Forest Trail', 'Wild elephants traversing a misty forest clearing at sunrise.', 'Signature'),
    135: ('Tropical Botanical Chinoiserie', 'Exotic fruits, palms, and paradise birds on subtle antique linen.', 'Bestseller'),
    136: ('Kovalam Golden Beach Sunset', 'Rocky headlands and curving sandy bay bathed in liquid amber light.', 'Curated'),
    137: ('Alleppey Backwater Palm Corridor', 'Canal waterway flanked by overhanging palms and village canoes.', 'Signature'),
    138: ('Verdant Palm Court Dining Hall', 'Full-height palm grove mural opening an interior dining room to nature.', 'Bestseller'),
    139: ('Night Jungle Palm Silhouette', 'Near-black tropical silhouettes against deep indigo starry skies.', 'Curated'),
    140: ('Tropical South Botanical Panorama', 'Sweeping coastal and forest landscape across an expansive feature wall.', 'Signature'),

    # South Indian Tales / Kids (141..160)
    141: ('South Indian Tales & Nursery', 'Mythological storybooks, gentle animals, and playful childhood murals.', 'Curated'),
    142: ('Little Gopala & Peacocks', 'Baby Krishna playing flute with gentle calves and friendly peacocks.', 'Signature'),
    143: ('Ganesha Mango Orchard Mischief', 'Little Ganesha picking sweet mangoes with playful mice and squirrels.', 'Bestseller'),
    144: ('The Jungle Troop of Langurs', 'Friendly monkeys swinging across a lush Kerala jungle gym canopy.', 'Signature'),
    145: ('Storybook Forest Orchard Play', 'Spotted deer, rabbits, and songbirds in a whimsical sunny meadow.', 'Bestseller'),
    146: ('Backwater Houseboat Voyage', 'Gentle animal friends sailing a wooden houseboat down river canals.', 'Curated'),
    147: ('The Pink Lotus Parade', 'Baby elephants wading through lily ponds carrying water sprays.', 'Signature'),
    148: ('Panchatantra Animal Kingdom', 'Classic moral fables brought to life in soft watercolor illustrations.', 'Curated'),
    149: ('Flying Hanuman & Mountain Peak', 'Little Maruti leaping across starry skies carrying the healing herb.', 'Signature'),
    150: ('Temple Pond Lotus & Monkey Kingdom', 'Storybook stone pavilion over a lotus pond with playful animals.', 'Signature'),
    151: ('Peacock Palace Nursery Garden', 'Royal birds spreading colorful tail feathers among rose gardens.', 'Bestseller'),
    152: ('Kite Flying at Marina Beach', 'Colorful kites dancing over ocean waves on a breezy summer day.', 'Curated'),
    153: ('Baby Elephant Splash Play', 'Playful elephant calves bathing in river pools with water lilies.', 'Signature'),
    154: ('Jataka Tales Golden Deer', 'The gentle golden stag radiating kindness in a magical bamboo forest.', 'Curated'),
    155: ('Starry Night Storybook Sky', 'Crescent moon, glowing constellations, and dreaming woodland animals.', 'Bestseller'),
    156: ('Traditional South Indian Toy Train', 'Nilgiri mountain toy train chugging past waterfalls and tea estates.', 'Signature'),
    157: ('Tenali Rama & Royal Parrot', 'Witty court adventures in a bright palace garden with friendly birds.', 'Curated'),
    158: ('Squirrel Bridge to Lanka Tale', 'Little squirrel carrying pebbles with Lord Rama on golden sands.', 'Signature'),
    159: ('Butterfly Meadow Sunshine', 'Rainbow butterflies fluttering across wildflower fields.', 'Curated'),
    160: ('Whimsical South Indian Kids Panorama', 'Endless storybook landscape filled with wonder and imagination.', 'Signature'),

    # South Indian Modernism / Abstract (161..185)
    161: ('South Indian Modernism Collection', 'Contemporary geometry, abstracted silks, and architectural reliefs.', 'Curated'),
    162: ('Calacatta & 24K Gold Marble Veins', 'Book-matched luxury Italian marble with shimmering gold accents.', 'Signature'),
    163: ('Amethyst Swirl Vortex', 'Slow violet and copper metallic gradient creating rich atmosphere.', 'Bestseller'),
    164: ('Blush Terracotta Strata', 'Soft-focus kiln red layers providing warmth without rigid pattern.', 'Curated'),
    165: ('Terracotta Geometric Trellis', 'Hand-ruled architectural lattice for bright contemporary kitchens.', 'Curated'),
    166: ('Crimson Kanjeevaram Knot', 'Endless silk weave abstraction in deep royal maroon and gold thread.', 'Signature'),
    167: ('Midnight Indigo Damask', 'Modernized heritage repeat beside dark wood and leather furnishings.', 'Bestseller'),
    168: ('Marine Teal Channels', 'Architectural vertical flute texture alternating gloss and matte finishes.', 'Curated'),
    169: ('Azure Steps Modern Geometric', 'Stepped architectural geometry rendered in five shades of ocean blue.', 'Signature'),
    170: ('Radiating Marigold Sun Mandala', 'Burst of warm saffron and turmeric bringing energy to breakfast rooms.', 'Bestseller'),
    171: ('Amber Dusk Atmospheric Gradient', 'Smooth sunset transition from turmeric gold to smoky charcoal.', 'Curated'),
    172: ('Olive Current Flowing Strata', 'Calm organic waveforms keeping executive conference rooms grounded.', 'Curated'),
    173: ('Monochrome Granite Relief', 'Sculpted stone texture with dramatic side-lighting shadows.', 'Signature'),
    174: ('Gilded Concrete Industrial', 'Raw textured concrete wall accented with delicate gold leaf fissures.', 'Bestseller'),
    175: ('Deco Brass & Charcoal Chevron', 'Geometric luxury chevron panels for home theatres and private lounges.', 'Signature'),
    176: ('Obsidian & Rose Gold Ribbon', 'Flowing liquid metal ribbons dancing across a mirror-dark backdrop.', 'Bestseller'),
    177: ('Athangudi Modern Abstract', 'Traditional heritage tile shapes re-composed into modern canvas art.', 'Curated'),
    178: ('Brushed Copper Patina', 'Weathered architectural metal with rich green and turquoise verdigris.', 'Signature'),
    179: ('Minimalist Arch Perspective', 'Receding clean stucco arches expanding the perceived depth of the room.', 'Signature'),
    180: ('Golden Horizon Line', 'Minimalist single gold horizon dividing deep midnight navy and ivory.', 'Bestseller'),
    181: ('Woven Jute & Metallic Thread', 'Tactile organic fiber texture interwoven with subtle bronze filaments.', 'Curated'),
    182: ('Terrazzo & Brass Geometric Inlay', 'Hand-poured aggregate stone with geometric brass division strips.', 'Signature'),
    183: ('Floating Origami Facets', 'Three-dimensional geometric paper fold relief in soft shadow tones.', 'Curated'),
    184: ('Architectural Shadow Play', 'Brutalist concrete forms interacting with clean geometric sunlight.', 'Curated'),
    185: ('Metropolis in Relief', 'Illuminated city skyline rendered as architectural relief with carved pavilion.', 'Signature')
}

kr_entries = []
for page_num in range(7, 186):
    img_path = f'assets/img/collection/kala-rasa/kr-plate-{page_num:03d}.jpg'
    
    # Check category and default info
    c_found, s_found, prefix, chap_title = 'heritage', 'living', 'WJWP-KR', 'Kala Rasa'
    for p_start, p_end, cat, space, pref, c_name in kr_categories:
        if p_start <= page_num <= p_end:
            c_found, s_found, prefix, chap_title = cat, space, pref, c_name
            break
            
    code = f'{prefix}-{page_num:03d}'
    
    if page_num in kr_named:
        name, blurb, tag = kr_named[page_num]
    else:
        name = f'{chap_title} · Plate {page_num:03d}'
        blurb = f'Original architectural wallpaper plate from the {chap_title} volume.'
        tag = 'Volume II'
        
    tag_part = f", tag: '{tag}'" if tag else ""
    kr_entries.append(
        f"  {{ n: '{name}', no: '{code}', v: 'kala-rasa', c: '{c_found}', s: '{s_found}',\n"
        f"    b: '{blurb}',\n"
        f"    img: '{img_path}'{tag_part} }}"
    )

kr_code = "  /* ==========================================================================\n" \
          "     VOLUME II: KALA RASA (Complete 179 Plates from Page 7 to 185)\n" \
          "     ========================================================================== */\n" + \
          ",\n".join(kr_entries)

# 3. VISHWA DARSHAN (World & Travel)
world_entries = [
  "  { n: 'London Study', no: 'WJWP-WLD-001', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'Westminster in sepia wash behind a leather-topped desk.',\n    img: IMG('world-london-study') }",
  "  { n: 'The Paris Library', no: 'WJWP-WLD-003', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The Seine drawn in bookish greys for readers and romantics.',\n    img: IMG('world-paris-library') }",
  "  { n: 'Colosseum Sketch', no: 'WJWP-WLD-005', v: 'vishwa-darshan', c: 'world', s: 'dining',\n    b: 'Rome in architect’s pencil, dining-room scale.',\n    img: IMG('world-rome-colosseum') }",
  "  { n: 'Bosphorus Evening', no: 'WJWP-WLD-007', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'Hagia Sophia over silk-dark waters in miniature-painting jewel tones.',\n    img: IMG('world-bosphorus-lounge') }",
  "  { n: 'India Gate', no: 'WJWP-WLD-009', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The sandstone arch in golden-hour monumental calm.',\n    img: IMG('world-india-gate') }",
  "  { n: 'Marine Drive', no: 'WJWP-WLD-010', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The Queen’s Necklace at dusk — Mumbai’s curve of light across your wall.',\n    img: IMG('world-mumbai-marine'), tag: 'New' }",
  "  { n: 'Gardens by the Bay', no: 'WJWP-WLD-012', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'Singapore’s supertrees in watercolour for forward-looking rooms.',\n    img: IMG('world-singapore-gardens') }",
  "  { n: 'Manhattan Ascent', no: 'WJWP-WLD-014', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'A pencil-grey skyline rising the full height of a stairwell.',\n    img: IMG('world-manhattan-stair') }"
]

world_code = "  /* ==========================================================================\n" \
             "     VOLUME III: VISHWA DARSHAN (World Cities & Architectural Journeys)\n" \
             "     ========================================================================== */\n" + \
             ",\n".join(world_entries)

full_collection_code = f"const COLLECTION = [\n{kp_code},\n\n{kr_code},\n\n{world_code}\n];\n"

# Replace COLLECTION = [...] in data.js
new_data_js = re.sub(r'const COLLECTION = \[[\s\S]*?\];', full_collection_code.strip(), data_js)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(new_data_js)

print("Updated data.js with all Kala Parampara (pure wallpaper designs), Kala Rasa (p7-185), and Vishwa Darshan plates!")
