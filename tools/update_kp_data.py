import os
import re

# Read current data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# Build the 82 Kala Parampara collection entries
plates_meta = [
    (0, 'Kala Parampara (Volume I Cover)', 'WJWP-KP-000', 'heritage', 'living', 'The founding volume cover — 82 master plates of Indian artistry and architectural heritage.', 'Volume I Cover'),
    (1, 'India, Interpreted Through Art', 'WJWP-KP-001', 'heritage', 'living', 'The opening folio: sacred iconography, royal courts, and southern architectural lineages.', 'Foreword'),
    (2, 'Heritage Master Index', 'WJWP-KP-002', 'heritage', 'living', 'Index of 82 original wallpaper designs published by Wall Jewels Wallpaper World.', 'Master Index'),
    (3, 'Divine India: Sacred Iconography', 'WJWP-KP-003', 'heritage', 'temple', 'Deities, epics and sacred geometry translated out of convention and into architectural scale.', 'Chapter I'),
    (4, 'Sanatan Iconography Overview', 'WJWP-DVN-000', 'heritage', 'living', 'Cinematic realism and carved bas-relief designed for luxury contemporary interiors.', 'Curated'),
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
    (25, 'Southern Heritage Reimagined', 'WJWP-SIH-000', 'heritage', 'living', 'Granite colonnades, carved mandapams, and Athangudi palace patterns.', 'Chapter II'),
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
    (76, 'Rann of Kutch Moonlight', 'WJWP-WCS-028', 'abstract', 'bedroom', 'Infinite white salt desert gleaming beneath the full moon.', 'Curated'),
    (77, 'Prakriti: Forest Canopy', 'WJWP-PRK-001', 'botanical', 'living', 'Living rainforest canopy tableau in layered emeralds and sunlight.', 'Signature'),
    (78, 'Prakriti: River Confluence', 'WJWP-PRK-002', 'tropical', 'living', 'Pristine mountain streams merging over sculpted granite boulders.', 'Curated'),
    (79, 'Prakriti: Mountain Sanctuary', 'WJWP-PRK-003', 'heritage', 'bedroom', 'Misty pine ridges rising into eternal Himalayan clouds.', 'Curated'),
    (80, 'Kala Parampara Installation Folio', 'WJWP-FOL-001', 'heritage', 'living', 'Architectural proof folio showcasing four decades of Chennai installations.', 'Portfolio'),
    (81, 'Kala Parampara Master Collection Index', 'WJWP-FOL-002', 'heritage', 'living', 'Complete catalogue index of 82 numbered wallpaper master plates.', 'Volume Index')
]

kp_entries = []
for idx, n, no, c, s, b, tag in plates_meta:
    img_path = f'assets/img/collection/kala-parampara/kp-plate-{idx:02d}.jpg'
    tag_part = f", tag: '{tag}'" if tag else ""
    kp_entries.append(
        f"  {{ n: '{n}', no: '{no}', v: 'kala-parampara', c: '{c}', s: '{s}',\n"
        f"    b: '{b}',\n"
        f"    img: '{img_path}'{tag_part} }}"
    )

kp_code = "  /* ==========================================================================\n" \
          "     VOLUME I: KALA PARAMPARA (Complete 82 Master Catalogue Plates)\n" \
          "     ========================================================================== */\n" + \
          ",\n".join(kp_entries)

# Keep the remaining collections (Kala Rasa, Vishwa Darshan, Modern, Kids, etc.) that have v != 'kala-parampara'
# Let's extract existing items from COLLECTION that are not kala-parampara
other_entries = [
  # — Kala Rasa — Heritage & Temple —
  "  { n: 'Goddess of the Lotus', no: 'WJWP-DVN-033', v: 'kala-rasa', c: 'heritage', s: 'dining',\n    b: 'Lakshmi enthroned in blush and rose-gold above a formal dining room.',\n    img: IMG('divine-goddess-lotus') }",
  "  { n: 'Ganesha in Terracotta', no: 'WJWP-DVN-047', v: 'kala-rasa', c: 'heritage', s: 'temple',\n    b: 'A hand-pressed terracotta relief study, warm as a Chettinad wall at dusk.',\n    img: IMG('divine-ganesha-plate') }",
  "  { n: 'Gopuram at Dusk', no: 'WJWP-SIH-018', v: 'kala-rasa', c: 'heritage', s: 'living',\n    b: 'The temple silhouette burning against an evening sky, over leather and lamplight.',\n    img: IMG('heritage-gopuram-dusk') }",
  "  { n: 'The Palace Corridor', no: 'WJWP-SIH-020', v: 'kala-rasa', c: 'heritage', s: 'hospitality',\n    b: 'A receding colonnade that deepens any passage it faces.',\n    img: IMG('heritage-palace-corridor') }",
  "  { n: 'The Stone Chariot', no: 'WJWP-SIH-022', v: 'kala-rasa', c: 'heritage', s: 'office',\n    b: 'Hampi’s chariot in painterly mist — history as a headboard for ambition.',\n    img: IMG('heritage-stone-chariot') }",
  "  { n: 'The Shrine Alcove', no: 'WJWP-SIH-024', v: 'kala-rasa', c: 'heritage', s: 'temple',\n    b: 'A blush-toned pichwai shrine framing the household deity.',\n    img: IMG('heritage-shrine-alcove') }",
  "  { n: 'The Grand Study', no: 'WJWP-SIH-026', v: 'kala-rasa', c: 'heritage', s: 'office',\n    b: 'A full-wall heritage tableau behind a writing desk — the room our clients ask for by name.',\n    img: IMG('heritage-grand-study'), tag: 'Signature' }",
  "  { n: 'The Mural Library', no: 'WJWP-SIH-028', v: 'kala-rasa', c: 'heritage', s: 'living',\n    b: 'A palace city painted across a double-height library wall.',\n    img: IMG('heritage-mural-library') }",
  
  # — Kala Rasa — Tropical & Botanical —
  "  { n: 'Emerald Jungle', no: 'WJWP-BTS-001', v: 'kala-rasa', c: 'tropical', s: 'living',\n    b: 'Dense understorey greens wrapped around velvet seating — the conservatory effect.',\n    img: IMG('tropical-emerald-jungle') }",
  "  { n: 'Lotus Bloom', no: 'WJWP-BTS-003', v: 'kala-rasa', c: 'botanical', s: 'living',\n    b: 'Oversized lotus and peacock in lacquered pinks — softness at architectural scale.',\n    img: IMG('botanical-lotus-bloom') }",
  "  { n: 'The Verdant Hall', no: 'WJWP-BTS-012', v: 'kala-rasa', c: 'botanical', s: 'hospitality',\n    b: 'Chinoiserie fruit and vine climbing a double-height dining hall.',\n    img: IMG('botanical-verdant-hall') }",
  "  { n: 'Lotus Bath', no: 'WJWP-BTS-014', v: 'kala-rasa', c: 'botanical', s: 'powder',\n    b: 'Hand-painted lotus pond enclosing a brass-fitted bath.',\n    img: IMG('botanical-lotus-bath') }",
  "  { n: 'Banana Grove', no: 'WJWP-BTS-016', v: 'kala-rasa', c: 'tropical', s: 'hospitality',\n    b: 'Broad leaves over café tables — the Tropical South, table height.',\n    img: IMG('tropical-banana-grove') }",
  "  { n: 'Midnight Palm', no: 'WJWP-BTS-018', v: 'kala-rasa', c: 'tropical', s: 'hospitality',\n    b: 'Near-black palms for moody bars and late conversations.',\n    img: IMG('tropical-midnight-palm') }",
  "  { n: 'The Golden Shore', no: 'WJWP-BTS-020', v: 'kala-rasa', c: 'tropical', s: 'living',\n    b: 'A west-coast sunset in oil-painted amber, horizon-wide.',\n    img: IMG('tropical-golden-shore') }",
  "  { n: 'Peacock Garden', no: 'WJWP-BTS-022', v: 'kala-rasa', c: 'botanical', s: 'bedroom',\n    b: 'Peacocks among peonies in porcelain tones — quiet grandeur for principal bedrooms.',\n    img: IMG('botanical-peacock-garden') }",
  "  { n: 'Chintz Revival', no: 'WJWP-BTS-024', v: 'kala-rasa', c: 'botanical', s: 'dining',\n    b: 'Jacobean florals recoloured for South Indian light.',\n    img: IMG('botanical-chintz-revival') }",
  "  { n: 'Emerald Block Print', no: 'WJWP-BTS-026', v: 'kala-rasa', c: 'botanical', s: 'living',\n    b: 'A hand-block repeat scaled to the wall, in one committed green.',\n    img: IMG('botanical-emerald-print') }",

  # — World & Travel (Vishwa Darshan) —
  "  { n: 'London Study', no: 'WJWP-WLD-001', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'Westminster in sepia wash behind a leather-topped desk.',\n    img: IMG('world-london-study') }",
  "  { n: 'The Paris Library', no: 'WJWP-WLD-003', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The Seine drawn in bookish greys for readers and romantics.',\n    img: IMG('world-paris-library') }",
  "  { n: 'Colosseum Sketch', no: 'WJWP-WLD-005', v: 'vishwa-darshan', c: 'world', s: 'dining',\n    b: 'Rome in architect’s pencil, dining-room scale.',\n    img: IMG('world-rome-colosseum') }",
  "  { n: 'Bosphorus Evening', no: 'WJWP-WLD-007', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'Hagia Sophia over silk-dark waters in miniature-painting jewel tones.',\n    img: IMG('world-bosphorus-lounge') }",
  "  { n: 'India Gate', no: 'WJWP-WLD-009', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The sandstone arch in golden-hour monumental calm.',\n    img: IMG('world-india-gate') }",
  "  { n: 'Marine Drive', no: 'WJWP-WLD-010', v: 'vishwa-darshan', c: 'world', s: 'living',\n    b: 'The Queen’s Necklace at dusk — Mumbai’s curve of light across your wall.',\n    img: IMG('world-mumbai-marine'), tag: 'New' }",
  "  { n: 'Gardens by the Bay', no: 'WJWP-WLD-012', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'Singapore’s supertrees in watercolour for forward-looking rooms.',\n    img: IMG('world-singapore-gardens') }",
  "  { n: 'Manhattan Ascent', no: 'WJWP-WLD-014', v: 'vishwa-darshan', c: 'world', s: 'office',\n    b: 'A pencil-grey skyline rising the full height of a stairwell.',\n    img: IMG('world-manhattan-stair') }",

  # — Kids & Nursery —
  "  { n: 'Little Gopala', no: 'WJWP-KDS-001', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'Baby Krishna with his calf and peacocks, painted soft enough for a nursery.',\n    img: IMG('kids-little-gopala'), tag: 'Most requested' }",
  "  { n: 'The Mango Grove', no: 'WJWP-KDS-003', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'Little Ganesha among mangoes and butterflies — mischief in watercolour.',\n    img: IMG('kids-mango-grove') }",
  "  { n: 'The Jungle Troop', no: 'WJWP-KDS-005', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'Langurs swing across a Kerala canopy above the toy shelf.',\n    img: IMG('kids-jungle-troop') }",
  "  { n: 'Orchard Play', no: 'WJWP-KDS-007', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'Children, deer and songbirds in a storybook orchard.',\n    img: IMG('kids-orchard-play') }",
  "  { n: 'Backwater Tale', no: 'WJWP-KDS-009', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'A gentle houseboat journey with elephants and swans, for bathtime voyagers.',\n    img: IMG('kids-backwater-tale') }",
  "  { n: 'The Lotus Parade', no: 'WJWP-KDS-011', v: 'kala-rasa', c: 'kids', s: 'kids',\n    b: 'Pink elephants and parrots wading through a lily pond.',\n    img: IMG('kids-lotus-parade') }",

  # — Modern Abstract & Texture —
  "  { n: 'Amethyst Swirl', no: 'WJWP-MOD-001', v: 'kala-rasa', c: 'abstract', s: 'bedroom',\n    b: 'A slow violet vortex behind copper pendant light.',\n    img: IMG('modern-amethyst-swirl') }",
  "  { n: 'Gilded Marble', no: 'WJWP-MOD-003', v: 'kala-rasa', c: 'abstract', s: 'living',\n    b: 'Calacatta veining shot with gold, book-matched across the stair.',\n    img: IMG('texture-gilded-marble') }",
  "  { n: 'Blush Terra', no: 'WJWP-MOD-005', v: 'kala-rasa', c: 'abstract', s: 'living',\n    b: 'Terracotta strata in soft focus — warmth without pattern.',\n    img: IMG('modern-blush-terra') }",
  "  { n: 'Terracotta Trellis', no: 'WJWP-MOD-007', v: 'kala-rasa', c: 'abstract', s: 'dining',\n    b: 'A hand-ruled lattice in kiln reds for breakfast light.',\n    img: IMG('modern-terracotta-trellis') }",
  "  { n: 'Crimson Weave', no: 'WJWP-MOD-009', v: 'kala-rasa', c: 'abstract', s: 'bedroom',\n    b: 'An endless silk knot in deep maroon — Kanjeevaram, abstracted.',\n    img: IMG('modern-crimson-weave') }",
  "  { n: 'Indigo Damask', no: 'WJWP-MOD-011', v: 'kala-rasa', c: 'abstract', s: 'office',\n    b: 'A midnight damask repeat beside old leather and older books.',\n    img: IMG('modern-indigo-damask') }",
  "  { n: 'Teal Deco', no: 'WJWP-MOD-013', v: 'kala-rasa', c: 'abstract', s: 'powder',\n    b: 'Marine-teal channels running floor to ceiling, gloss on matte.',\n    img: IMG('modern-teal-deco') }",
  "  { n: 'Azure Steps', no: 'WJWP-MOD-015', v: 'kala-rasa', c: 'abstract', s: 'living',\n    b: 'Stepped geometry in five blues — order made ornamental.',\n    img: IMG('modern-azure-steps') }",
  "  { n: 'Marigold Sun', no: 'WJWP-MOD-017', v: 'kala-rasa', c: 'abstract', s: 'dining',\n    b: 'A radiating marigold mandala that turns breakfast into an occasion.',\n    img: IMG('modern-marigold-sun') }",
  "  { n: 'Amber Dusk', no: 'WJWP-MOD-019', v: 'kala-rasa', c: 'abstract', s: 'living',\n    b: 'A slow gradient from turmeric to smoke — colour as atmosphere.',\n    img: IMG('modern-amber-dusk') }",
  "  { n: 'Olive Current', no: 'WJWP-MOD-021', v: 'kala-rasa', c: 'abstract', s: 'office',\n    b: 'Flowing olive strata that keep long meetings calm.',\n    img: IMG('modern-olive-current') }"
]

other_code = "  /* ==========================================================================\n" \
             "     VOLUME II: KALA RASA & COMPANION COLLECTIONS\n" \
             "     ========================================================================== */\n" + \
             ",\n".join(other_entries)

full_collection_code = f"const COLLECTION = [\n{kp_code},\n\n{other_code}\n];\n"

# Replace COLLECTION = [...] in data.js
new_data_js = re.sub(r'const COLLECTION = \[[\s\S]*?\];', full_collection_code.strip(), data_js)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(new_data_js)

print("Updated data.js successfully with all 82 Kala Parampara plates!")
