/* ============================================================================
   WALL JEWELS — collection data
   ----------------------------------------------------------------------------
   Every image is genuine WJWP artwork, extracted from the published catalogue
   volumes (Kala Parampara Vol I, Kala Rasa Vol II and companion folios).
   No pricing appears anywhere by decision: price emerges in consultation.
   ========================================================================== */

const IMG = (slug) => `assets/img/collection/${slug}.jpg`;

const VOLUMES = [
  { id: 'kala-parampara', roman: 'I',  name: 'Kala Parampara', tag: 'India, interpreted through art.' },
  { id: 'kala-rasa',      roman: 'II', name: 'Kala Rasa',      tag: 'Where Indian artistry meets contemporary expression.' },
  { id: 'vishwa-darshan', roman: 'III', name: 'Vishwa Darshan', tag: 'The world through art.', soon: false },
  { id: 'prakriti',       roman: 'IV', name: 'Prakriti',        tag: 'Inspired by nature.', soon: true }
];

const SPACES = [
  { id: 'living',   label: 'Living Room',  note: 'Statement walls & artistic murals' },
  { id: 'bedroom',  label: 'Bedroom',      note: 'Calm, intimate & luxurious' },
  { id: 'dining',   label: 'Dining',       note: 'Art that starts conversations' },
  { id: 'kids',     label: 'Kids',         note: 'Imagination without limits' },
  { id: 'office',   label: 'Office',       note: 'Sophisticated walls for modern workspaces' },
  { id: 'hospitality', label: 'Hospitality', note: 'Hotels · Restaurants · Cafés' },
  { id: 'temple',   label: 'Temple & Pooja', note: 'Sacred & spiritual designs' },
  { id: 'powder',   label: 'Powder Room',  note: 'Small spaces. Big impact.' }
];

const CATEGORIES = [
  { id: 'heritage',  label: 'Art & Heritage' },
  { id: 'tropical',  label: 'Tropicals' },
  { id: 'botanical', label: 'Florals & Botanicals' },
  { id: 'abstract',  label: 'Modern Abstract' },
  { id: 'kids',      label: 'Kids & Nursery' },
  { id: 'world',     label: 'World & Travel' }
];

/* d: design entries.
   n  — name (from the catalogue where legible, in-world otherwise)
   no — WJWP design number where the catalogue shows one
   v  — volume  · c — category · s — space
   b  — one-line blurb
   tag — corner label (real catalogue standing only)                       */
const COLLECTION = [
  /* — Divine India (Kala Parampara) — */
  { n: 'The Himalayan Ascetic', no: 'WJWP-DVN-001', v: 'kala-parampara', c: 'heritage', s: 'temple',
    b: 'Mahadev in deep stillness against snow-bound peaks; cinematic realism for contemplative rooms.',
    img: IMG('divine-himalayan-ascetic'), tag: 'Signature' },
  { n: 'The Cosmic Dance', no: 'WJWP-DVN-004', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'Nataraja cast in bronze light — the rhythmic pulse of the universe on a single wall.',
    img: IMG('divine-cosmic-dance') },
  { n: 'The Devoted Breath', no: 'WJWP-DVN-010', v: 'kala-parampara', c: 'heritage', s: 'temple',
    b: 'Hanuman in saffron brushwork; unshakeable strength drawn in stillness.',
    img: IMG('divine-devoted-breath') },
  { n: 'Darbar of the Ancients', no: 'WJWP-DVN-014', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'A heritage mural of Rajarajeshwara court splendour, framed by carved arches.',
    img: IMG('divine-darbar-ancients') },
  { n: 'The Kadamba Melody', no: 'WJWP-DVN-018', v: 'kala-parampara', c: 'heritage', s: 'bedroom',
    b: 'Krishna beneath the kadamba tree — a flute frequency in emerald and gold.',
    img: IMG('divine-kadamba-melody') },
  { n: 'Ganesha Relief', no: 'WJWP-DVN-021', v: 'kala-parampara', c: 'heritage', s: 'temple',
    b: 'Carved-wood Ganesha rendered with true shadow depth for the pooja threshold.',
    img: IMG('divine-ganesha-relief') },
  { n: 'The Golden Obstacle Breaker', no: 'WJWP-DVN-022', v: 'kala-parampara', c: 'heritage', s: 'powder',
    b: 'A single gold line draws Ganesha on ivory — minimal, auspicious, serene.',
    img: IMG('divine-golden-obstacle') },
  { n: 'The Invincible Sovereign', no: 'WJWP-DVN-026', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'Durga with her lion in layered vermilion and gold, commanding a double-height stair.',
    img: IMG('divine-invincible-sovereign'), tag: 'Bestseller' },
  { n: 'The Temple Sovereign', no: 'WJWP-DVN-027', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'A gilded gopuram interior glowing over a formal seating court.',
    img: IMG('divine-temple-sovereign') },
  { n: 'Resonance of Om', no: 'WJWP-DVN-030', v: 'kala-parampara', c: 'heritage', s: 'temple',
    b: 'The primal syllable in beaten gold at the end of a lamp-lit corridor.',
    img: IMG('divine-resonance-om') },
  { n: 'Goddess of the Lotus', no: 'WJWP-DVN-033', v: 'kala-rasa', c: 'heritage', s: 'dining',
    b: 'Lakshmi enthroned in blush and rose-gold above a formal dining room.',
    img: IMG('divine-goddess-lotus') },
  { n: 'Ganesha in Terracotta', no: 'WJWP-DVN-047', v: 'kala-rasa', c: 'heritage', s: 'temple',
    b: 'A hand-pressed terracotta relief study, warm as a Chettinad wall at dusk.',
    img: IMG('divine-ganesha-plate') },
  { n: 'Pichwai: Moonlit Grove', no: 'WJWP-DVN-052', v: 'kala-parampara', c: 'heritage', s: 'dining',
    b: 'Nathdwara pichwai under a full moon — cows, kadamba and hanging garlands on deep indigo.',
    img: IMG('pichwai-moonlit-grove'), tag: 'Signature' },
  { n: 'Pichwai: Eternal Melody', no: 'WJWP-DVN-053', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'Krishna at the heart of a garlanded grove; devotion painted flower by flower.',
    img: IMG('pichwai-eternal-melody'), tag: 'Bestseller' },

  /* — Southern Heritage — */
  { n: 'Chola Pillars', no: 'WJWP-SIH-002', v: 'kala-parampara', c: 'heritage', s: 'hospitality',
    b: 'Monumental stone colonnades for reception halls that mean business.',
    img: IMG('heritage-chola-pillars') },
  { n: 'Abstract Gopuram', no: 'WJWP-SIH-004', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'The temple tower reduced to sunlit geometry — heritage for modern minimalists.',
    img: IMG('heritage-abstract-gopuram') },
  { n: 'Chettinad Grandeur', no: 'WJWP-SIH-006', v: 'kala-parampara', c: 'heritage', s: 'dining',
    b: 'Athangudi patterns and arched verandahs from the mansions of Karaikudi.',
    img: IMG('heritage-chettinad-grandeur') },
  { n: 'Tanjore Garden', no: 'WJWP-SIH-011', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'Antique gold botanicals on deep tapestry red, in the manner of temple murals.',
    img: IMG('heritage-tanjore-garden') },
  { n: 'Tanjore Echoes', no: 'WJWP-SIH-012', v: 'kala-parampara', c: 'heritage', s: 'bedroom',
    b: 'Embossed-gold peacocks over burgundy — the opulence of Tanjore painting, wall-scale.',
    img: IMG('heritage-tanjore-echoes'), tag: 'Bestseller' },
  { n: 'Kolam Rhythm', no: 'WJWP-SIH-015', v: 'kala-parampara', c: 'heritage', s: 'office',
    b: 'The dawn dot-grid of Tamil thresholds, drawn in indigo on soft white.',
    img: IMG('heritage-kolam-rhythm') },
  { n: 'The Royal Tusker', no: 'WJWP-SIH-016', v: 'kala-parampara', c: 'heritage', s: 'hospitality',
    b: 'Caparisoned elephants in carved-stone grisaille for grand lobbies.',
    img: IMG('heritage-royal-tusker') },
  { n: 'Gopuram at Dusk', no: 'WJWP-SIH-018', v: 'kala-rasa', c: 'heritage', s: 'living',
    b: 'The temple silhouette burning against an evening sky, over leather and lamplight.',
    img: IMG('heritage-gopuram-dusk') },
  { n: 'The Palace Corridor', no: 'WJWP-SIH-020', v: 'kala-rasa', c: 'heritage', s: 'hospitality',
    b: 'A receding colonnade that deepens any passage it faces.',
    img: IMG('heritage-palace-corridor') },
  { n: 'The Stone Chariot', no: 'WJWP-SIH-022', v: 'kala-rasa', c: 'heritage', s: 'office',
    b: 'Hampi’s chariot in painterly mist — history as a headboard for ambition.',
    img: IMG('heritage-stone-chariot') },
  { n: 'The Shrine Alcove', no: 'WJWP-SIH-024', v: 'kala-rasa', c: 'heritage', s: 'temple',
    b: 'A blush-toned pichwai shrine framing the household deity.',
    img: IMG('heritage-shrine-alcove') },
  { n: 'The Grand Study', no: 'WJWP-SIH-026', v: 'kala-rasa', c: 'heritage', s: 'office',
    b: 'A full-wall heritage tableau behind a writing desk — the room our clients ask for by name.',
    img: IMG('heritage-grand-study'), tag: 'Signature' },
  { n: 'The Mural Library', no: 'WJWP-SIH-028', v: 'kala-rasa', c: 'heritage', s: 'living',
    b: 'A palace city painted across a double-height library wall.',
    img: IMG('heritage-mural-library') },

  /* — Tropical & Botanical — */
  { n: 'Emerald Jungle', no: 'WJWP-BTS-001', v: 'kala-rasa', c: 'tropical', s: 'living',
    b: 'Dense understorey greens wrapped around velvet seating — the conservatory effect.',
    img: IMG('tropical-emerald-jungle') },
  { n: 'Lotus Bloom', no: 'WJWP-BTS-003', v: 'kala-rasa', c: 'botanical', s: 'living',
    b: 'Oversized lotus and peacock in lacquered pinks — softness at architectural scale.',
    img: IMG('botanical-lotus-bloom') },
  { n: 'Kerala Monsoon', no: 'WJWP-BTS-006', v: 'kala-parampara', c: 'tropical', s: 'bedroom',
    b: 'Rain-washed palms in ten shades of green; the calmest wall in the tropics.',
    img: IMG('tropical-kerala-monsoon') },
  { n: 'Malabar Coast', no: 'WJWP-BTS-008', v: 'kala-parampara', c: 'tropical', s: 'bedroom',
    b: 'A backwater vista in watercolour — houseboat, palms and evening light.',
    img: IMG('tropical-malabar-coast') },
  { n: 'Cabana Palms', no: 'WJWP-BTS-010', v: 'kala-parampara', c: 'tropical', s: 'powder',
    b: 'Bright banana fronds behind rattan — instant holiday, zero maintenance.',
    img: IMG('tropical-cabana-palms') },
  { n: 'The Verdant Hall', no: 'WJWP-BTS-012', v: 'kala-rasa', c: 'botanical', s: 'hospitality',
    b: 'Chinoiserie fruit and vine climbing a double-height dining hall.',
    img: IMG('botanical-verdant-hall') },
  { n: 'Lotus Bath', no: 'WJWP-BTS-014', v: 'kala-rasa', c: 'botanical', s: 'powder',
    b: 'Hand-painted lotus pond enclosing a brass-fitted bath.',
    img: IMG('botanical-lotus-bath') },
  { n: 'Banana Grove', no: 'WJWP-BTS-016', v: 'kala-rasa', c: 'tropical', s: 'hospitality',
    b: 'Broad leaves over café tables — the Tropical South, table height.',
    img: IMG('tropical-banana-grove') },
  { n: 'Midnight Palm', no: 'WJWP-BTS-018', v: 'kala-rasa', c: 'tropical', s: 'hospitality',
    b: 'Near-black palms for moody bars and late conversations.',
    img: IMG('tropical-midnight-palm') },
  { n: 'The Golden Shore', no: 'WJWP-BTS-020', v: 'kala-rasa', c: 'tropical', s: 'living',
    b: 'A west-coast sunset in oil-painted amber, horizon-wide.',
    img: IMG('tropical-golden-shore') },
  { n: 'Peacock Garden', no: 'WJWP-BTS-022', v: 'kala-rasa', c: 'botanical', s: 'bedroom',
    b: 'Peacocks among peonies in porcelain tones — quiet grandeur for principal bedrooms.',
    img: IMG('botanical-peacock-garden') },
  { n: 'Chintz Revival', no: 'WJWP-BTS-024', v: 'kala-rasa', c: 'botanical', s: 'dining',
    b: 'Jacobean florals recoloured for South Indian light.',
    img: IMG('botanical-chintz-revival') },
  { n: 'Emerald Block Print', no: 'WJWP-BTS-026', v: 'kala-rasa', c: 'botanical', s: 'living',
    b: 'A hand-block repeat scaled to the wall, in one committed green.',
    img: IMG('botanical-emerald-print') },

  /* — World & Travel — */
  { n: 'London Study', no: 'WJWP-WLD-001', v: 'vishwa-darshan', c: 'world', s: 'office',
    b: 'Westminster in sepia wash behind a leather-topped desk.',
    img: IMG('world-london-study') },
  { n: 'The Paris Library', no: 'WJWP-WLD-003', v: 'vishwa-darshan', c: 'world', s: 'living',
    b: 'The Seine drawn in bookish greys for readers and romantics.',
    img: IMG('world-paris-library') },
  { n: 'Colosseum Sketch', no: 'WJWP-WLD-005', v: 'vishwa-darshan', c: 'world', s: 'dining',
    b: 'Rome in architect’s pencil, dining-room scale.',
    img: IMG('world-rome-colosseum') },
  { n: 'Bosphorus Evening', no: 'WJWP-WLD-007', v: 'vishwa-darshan', c: 'world', s: 'living',
    b: 'Hagia Sophia over silk-dark waters in miniature-painting jewel tones.',
    img: IMG('world-bosphorus-lounge') },
  { n: 'India Gate', no: 'WJWP-WLD-009', v: 'vishwa-darshan', c: 'world', s: 'living',
    b: 'The sandstone arch in golden-hour monumental calm.',
    img: IMG('world-india-gate') },
  { n: 'Marine Drive', no: 'WJWP-WLD-010', v: 'vishwa-darshan', c: 'world', s: 'living',
    b: 'The Queen’s Necklace at dusk — Mumbai’s curve of light across your wall.',
    img: IMG('world-mumbai-marine'), tag: 'New' },
  { n: 'Gardens by the Bay', no: 'WJWP-WLD-012', v: 'vishwa-darshan', c: 'world', s: 'office',
    b: 'Singapore’s supertrees in watercolour for forward-looking rooms.',
    img: IMG('world-singapore-gardens') },
  { n: 'Manhattan Ascent', no: 'WJWP-WLD-014', v: 'vishwa-darshan', c: 'world', s: 'office',
    b: 'A pencil-grey skyline rising the full height of a stairwell.',
    img: IMG('world-manhattan-stair') },

  /* — Kids & Nursery — */
  { n: 'Little Gopala', no: 'WJWP-KDS-001', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'Baby Krishna with his calf and peacocks, painted soft enough for a nursery.',
    img: IMG('kids-little-gopala'), tag: 'Most requested' },
  { n: 'The Mango Grove', no: 'WJWP-KDS-003', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'Little Ganesha among mangoes and butterflies — mischief in watercolour.',
    img: IMG('kids-mango-grove') },
  { n: 'The Jungle Troop', no: 'WJWP-KDS-005', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'Langurs swing across a Kerala canopy above the toy shelf.',
    img: IMG('kids-jungle-troop') },
  { n: 'Orchard Play', no: 'WJWP-KDS-007', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'Children, deer and songbirds in a storybook orchard.',
    img: IMG('kids-orchard-play') },
  { n: 'Backwater Tale', no: 'WJWP-KDS-009', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'A gentle houseboat journey with elephants and swans, for bathtime voyagers.',
    img: IMG('kids-backwater-tale') },
  { n: 'The Lotus Parade', no: 'WJWP-KDS-011', v: 'kala-rasa', c: 'kids', s: 'kids',
    b: 'Pink elephants and parrots wading through a lily pond.',
    img: IMG('kids-lotus-parade') },

  /* — Modern Abstract & Texture — */
  { n: 'Amethyst Swirl', no: 'WJWP-MOD-001', v: 'kala-rasa', c: 'abstract', s: 'bedroom',
    b: 'A slow violet vortex behind copper pendant light.',
    img: IMG('modern-amethyst-swirl') },
  { n: 'Gilded Marble', no: 'WJWP-MOD-003', v: 'kala-rasa', c: 'abstract', s: 'living',
    b: 'Calacatta veining shot with gold, book-matched across the stair.',
    img: IMG('texture-gilded-marble') },
  { n: 'Blush Terra', no: 'WJWP-MOD-005', v: 'kala-rasa', c: 'abstract', s: 'living',
    b: 'Terracotta strata in soft focus — warmth without pattern.',
    img: IMG('modern-blush-terra') },
  { n: 'Terracotta Trellis', no: 'WJWP-MOD-007', v: 'kala-rasa', c: 'abstract', s: 'dining',
    b: 'A hand-ruled lattice in kiln reds for breakfast light.',
    img: IMG('modern-terracotta-trellis') },
  { n: 'Crimson Weave', no: 'WJWP-MOD-009', v: 'kala-rasa', c: 'abstract', s: 'bedroom',
    b: 'An endless silk knot in deep maroon — Kanjeevaram, abstracted.',
    img: IMG('modern-crimson-weave') },
  { n: 'Indigo Damask', no: 'WJWP-MOD-011', v: 'kala-rasa', c: 'abstract', s: 'office',
    b: 'A midnight damask repeat beside old leather and older books.',
    img: IMG('modern-indigo-damask') },
  { n: 'Teal Deco', no: 'WJWP-MOD-013', v: 'kala-rasa', c: 'abstract', s: 'powder',
    b: 'Marine-teal channels running floor to ceiling, gloss on matte.',
    img: IMG('modern-teal-deco') },
  { n: 'Azure Steps', no: 'WJWP-MOD-015', v: 'kala-rasa', c: 'abstract', s: 'living',
    b: 'Stepped geometry in five blues — order made ornamental.',
    img: IMG('modern-azure-steps') },
  { n: 'Marigold Sun', no: 'WJWP-MOD-017', v: 'kala-rasa', c: 'abstract', s: 'dining',
    b: 'A radiating marigold mandala that turns breakfast into an occasion.',
    img: IMG('modern-marigold-sun') },
  { n: 'Amber Dusk', no: 'WJWP-MOD-019', v: 'kala-rasa', c: 'abstract', s: 'living',
    b: 'A slow gradient from turmeric to smoke — colour as atmosphere.',
    img: IMG('modern-amber-dusk') },
  { n: 'Olive Current', no: 'WJWP-MOD-021', v: 'kala-rasa', c: 'abstract', s: 'office',
    b: 'Flowing olive strata that keep long meetings calm.',
    img: IMG('modern-olive-current') },

  /* — Spaces / hospitality showcases — */
  { n: 'The Pichwai Dining Hall', no: 'WJWP-HSP-001', v: 'kala-parampara', c: 'heritage', s: 'hospitality',
    b: 'A narrative mural running the length of a restaurant wall.',
    img: IMG('space-dining-pichwai') },
  { n: 'The Banquet Mural', no: 'WJWP-HSP-003', v: 'kala-parampara', c: 'heritage', s: 'hospitality',
    b: 'Festival processions in mural red for wedding halls and banquets.',
    img: IMG('space-banquet-mural') },
  { n: 'The Boardroom Lattice', no: 'WJWP-HSP-005', v: 'kala-rasa', c: 'abstract', s: 'office',
    b: 'A deep-green jaali pattern that gives a boardroom its spine.',
    img: IMG('space-boardroom-lattice') },
  { n: 'The Resort Cove', no: 'WJWP-HSP-007', v: 'kala-rasa', c: 'tropical', s: 'hospitality',
    b: 'An ocean-cliff panorama for lounges that sell the view they don’t have.',
    img: IMG('space-resort-cove') },
  { n: 'The Café Collage', no: 'WJWP-HSP-009', v: 'kala-rasa', c: 'abstract', s: 'hospitality',
    b: 'Cut-paper colour at espresso pace for daylight cafés.',
    img: IMG('space-cafe-collage') },
  { n: 'Office Metropolis', no: 'WJWP-HSP-011', v: 'vishwa-darshan', c: 'world', s: 'office',
    b: 'A silver-grey skyline keeping a workspace ambitious and unfussy.',
    img: IMG('space-office-metropolis') },

  /* — Sepia Heritage folio (Southern Heritage companion) — */
  { n: 'Temple Sanctuary', no: 'WJWP-SEP-001', v: 'kala-parampara', c: 'heritage', s: 'temple',
    b: 'A sepia gopuram among palms, from the Southern Heritage folio.',
    img: IMG('sepia-temple-sanctuary') },
  { n: 'Sacred Waters', no: 'WJWP-SEP-002', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'A temple tank at first light, etched in celadon and sand.',
    img: IMG('sepia-sacred-waters') },
  { n: 'Rooted in Heritage', no: 'WJWP-SEP-004', v: 'kala-parampara', c: 'heritage', s: 'living',
    b: 'A banyan and shrine composition holding four centuries still.',
    img: IMG('sepia-rooted-heritage') },
  { n: 'Pichwai: The Evening Grove', no: 'WJWP-PCH-009', v: 'kala-parampara', c: 'heritage', s: 'hospitality',
    b: 'Krishna beneath garlanded trees at dusk — bells, cows and lotus ponds in deep pichwai green.',
    img: IMG('sepia-southern-harmony') }
];

/* The Edit — curated doors into the collection */
const EDITS = [
  { name: 'Pichwai',            q: { search: 'pichwai' },     img: IMG('pichwai-eternal-melody') },
  { name: 'Indian Heritage',    q: { c: 'heritage' },         img: IMG('heritage-tanjore-echoes') },
  { name: 'Botanical',          q: { c: 'botanical' },        img: IMG('botanical-lotus-bloom') },
  { name: 'Luxury Landscapes',  q: { c: 'tropical' },         img: IMG('tropical-golden-shore') },
  { name: 'Contemporary Art',   q: { c: 'abstract' },         img: IMG('modern-marigold-sun') },
  { name: 'Kids',               q: { c: 'kids' },             img: IMG('kids-little-gopala') },
  { name: 'Textures',           q: { search: 'marble texture weave' }, img: IMG('texture-gilded-marble') },
  { name: 'Global Inspirations',q: { c: 'world' },            img: IMG('world-mumbai-marine') }
];

/* The record — real client names from the company profile */
const RECORD = {
  'Residences & Landmarks': [
    'A Cinema Legend’s Residence — name shared on request',
    'DLF Commander’s Court',
    'Lotus Service Apartments',
    'Casa Grande Corporate Office'
  ],
  'Hospitality & Retail': [
    'Express Avenue Mall',
    'Palazzo · Vijaya Forum Mall',
    'Soul Garden Bistro',
    'Ashpra Interiors',
    'Design DNA Architects'
  ],
  'Institutions': [
    'Apollo Hospitals',
    'Indian Railways',
    'MGR Engineering College',
    'Jeppiaar Engineering College',
    'ACS Medical College',
    'Akshayah International School'
  ]
};

const FINISHES = [
  { name: 'Non-Woven',     traits: 'Soft · Premium · Breathable',      best: 'Bedrooms',
    note: 'Our house favourite: dimensionally stable, paste-the-wall fitting, and a soft matte face that flatters artwork.' },
  { name: 'HD PVC',        traits: 'Durable · Washable · High-definition', best: 'High-traffic walls',
    note: 'Scrubbable vinyl that takes corridors, kids and kitchens in its stride without losing print depth.' },
  { name: 'Canvas',        traits: 'Rich texture · Gallery finish',    best: 'Feature walls',
    note: 'A woven face that reads as a stretched painting — the choice for murals meant to be admired up close.' },
  { name: 'Sandstone',     traits: 'Tactile · Mineral · Distinctive',  best: 'Lobbies',
    note: 'A fine granular surface with genuine relief; light rakes across it differently every hour.' },
  { name: 'Canvas Fabric', traits: 'Textile face · Acoustic softness', best: 'Studies & suites',
    note: 'A premium textile appearance that warms a room’s sound as well as its walls.' }
];

const PROCESS = [
  { t: 'Choose a design',            d: 'From 50,000+ designs across our volumes and 300+ international catalogues — or bring your own idea.' },
  { t: 'Share your wall dimensions', d: 'Width and height in feet is all we need. A photograph of the wall helps us advise.' },
  { t: 'We customise the artwork',   d: 'Our studio recomposes, recolours and scales the design to your exact wall — nothing is stretched or cropped blindly.' },
  { t: 'We manufacture it',          d: 'Printed on our own floor in Chennai on the finish you choose, with panel-true colour.' },
  { t: 'We install it',              d: 'Our two-man crews fit 400 sq.ft in about four hours. Furniture back before dinner.' }
];

const WHY = [
  { w: '1978',          f: '45+ years on the wall — the pioneers of wallpaper in South India.' },
  { w: 'Custom',        f: 'Every design resized, recoloured and recomposed to your exact wall.' },
  { w: 'Manufacturing', f: 'Our own printing floor in Chennai. No middlemen between art and wall.' },
  { w: 'Quality',       f: 'Premium substrates, fire-retardant grades, ten-year walls on our books.' },
  { w: 'Installation',  f: 'End-to-end service by our own fitting crews, not subcontractors.' },
  { w: 'Experience',    f: 'Three Chennai showrooms and design support from first idea to final wall.' }
];

const CONTACT = {
  phoneShowroom: '+91 98400 64205',
  phoneShowroomHref: 'tel:+919840064205',
  whatsapp: '+91 96770 42903',
  whatsappHref: 'https://wa.me/919677042903',
  email: 'info@walljewels.com',
  showrooms: [
    { city: 'Parry’s', area: 'Rattan Bazaar', flag: true,
      addr: 'No. 31 (Old 18), Rattan Bazaar, Park Town, Chennai 600 003',
      note: 'The 5,000 sq.ft flagship',
      maps: 'https://maps.google.com/?q=Wall+Jewels+Wallpaper+World+Rattan+Bazaar+Park+Town+Chennai' },
    { city: 'OMR', area: 'Old Mahabalipuram Road',
      addr: 'Call the showroom for directions — full address on request.',
      note: null, maps: null },
    { city: 'T. Nagar', area: 'Thyagaraya Nagar',
      addr: 'Call the showroom for directions — full address on request.',
      note: null, maps: null }
  ]
};
