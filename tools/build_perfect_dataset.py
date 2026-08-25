import json
import re

with open('scratch/master_combined_plates.json', 'r', encoding='utf-8') as f:
    plates = json.load(f)

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

def clean_text_field(s):
    if not s or not isinstance(s, str):
        return ""
    # Standardize replacements
    s = s.replace('\ufffd', ' ').replace('', ' ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # Strip OCR junk
    for j in [r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b', r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b']:
        s = re.sub(j, '', s, flags=re.IGNORECASE)
        
    # Split camelCase words
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r',([^\s])', r', \1', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,-·')
    return s

# Curated overrides for perfect presentation
curated = {
    'kp-06': ('The Himalayan Ascetic', 'Stillness carved in stone and snow.', 'Capturing the ultimate stillness of Mahadev in deep meditation, this composition contrasts the rugged, snow-capped Himalayan peaks against the serene, powerful presence of Shiva.'),
    'kp-07': ('The Cosmic Dance', 'The rhythmic pulse of the universe.', 'The Nataraja represents the continuous cycle of creation and dissolution. Inspired by antique bronze sculptures and sacred geometry, transforming blank walls into moving celestial theatre.'),
    'kp-15': ('The Sanjeevani Flight', 'Heroic devotion soaring across the night sky.', 'A dynamic, high-contrast composition depicting Lord Hanuman carrying the Dronagiri mountain through midnight clouds with heroic grace.'),
    'kr-016': ('Durga: The Protector', 'Contemporary Heritage Mural', 'A modern, grounded interpretation of divine protection. Goddess Durga surrounded by regal lions, vibrant florals, and subtle celestial geometry, creating a strong spiritual anchor for contemporary spaces.'),
    'kr-031': ('Divine Family', 'Heritage Composition', 'A refined, heritage-inspired composition uniting Shiva, Parvati, Ganesha, Kartikeya, and Nandi in harmonious sandstone, terracotta, and emerald balance.'),
    'kr-032': ('Divine India: Sacred Harmony', 'Contemporary Masterpiece', 'The magnum opus. A deeply sophisticated contemporary masterpiece interweaving the symbolic elements of Ganesha, Shiva, Krishna, Lakshmi, Saraswati, and Durga in harmonious sacred balance.'),
    'kr-033': ('Pichwai: Divine Companions', 'Traditional Pichwai Art', 'A celebration of the sacred bond between cow and calf, inspired by the traditional Pichwai art of Nathdwara. Blends lush foliage, lotus-filled waters, and intricate detailing to bring peace, prosperity, and divine grace.'),
    'kr-034': ('Pichwai: Eternal Melody', 'Traditional Pichwai Heritage', 'Inspired by the sacred Pichwai art of Nathdwara, this design reflects the eternal melody of devotion and nature. Krishna at the heart surrounded by cows, lotuses, peacocks, and temple charm.'),
    'kr-035': ('Rama of the Forest Arches', 'Sovereign in the Sacred Grove', 'Lord Rama stands at the centre of a carved triple arch, the forest and its rivers opening behind him. Ornamental sandstone framing gives the composition an architectural weight.'),
    'kr-036': ('Ganesha: Four Aspects', 'One Deity, Four Registers', 'Four distinct iconography registers of Lord Ganesha depicted in serene meditative and celebratory postures across emerald, rose, and sandstone panels.'),
    'kr-037': ('Ganesha Enthroned', 'The Vertical Sanctum', 'Lord Ganesha seated in divine grandeur beneath ornate temple arches. The vertical orientation and rich jewel tones create a monumental spiritual focal point.'),
    'kr-039': ('Chola Temple Chronicles', 'Epic Narratives in Stone', 'Monumental stone carvings and friezes celebrating the timeless architectural genius of the Chola dynasty. Warm granite textures and lifelike bas-relief shadows create historic dignity.'),
    'kr-040': ('Gopuram Grandeur', 'Monumental Elegance', 'Towering Dravidian gopuram silhouettes rendered in gold, sandstone, and warm terracotta. Captures the majestic verticality and spiritual aura of ancient South Indian temples.'),
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
    'kr-121': ('Coconut Grove Reverie', 'Vertical Grace over Jungle Chaos', 'Swaying coconut palm fronds capturing golden tropical light with vertical botanical rhythm and coastal serenity.'),
    'kr-122': ('Monsoon in Munnar', 'The Electric Tension of High-Altitude Rain', 'Rolling tea-plantation slopes and misty high-altitude mountain contours under dramatic monsoon cloud formations in rich forest greens and slate blues.'),
    'kr-123': ('Coorg Coffee Estate', 'The Shaded Geometry of the Coffee Lands', 'Canopied coffee bushes, silver oak shade trees, and pepper vines illustrated with fine engraving precision in earthy greens and deep bronze.'),
    'kr-124': ('Malabar Fishing Village', 'The Rhythm of Life on the Arabian Sea', 'Traditional wooden country boats, coastal palm shorelines, and gentle waves of the Malabar coast in breezy contemporary tones.'),
    'kr-125': ('Lotus and Waterlily', 'Aquatic Botanical Geometry', 'Floating lotus pads, flowering aquatic buds, and clear water ripples in serene botanical harmony.'),
    'kr-126': ('Banana Leaf Canopy', 'Architectural Foliage', 'Oversized, sculptural banana leaves overlapping in lush emerald and olive layers, creating dramatic tropical depth.'),
    'kr-127': ('Temple Garden Monsoon', 'Ancient Stone Yielding to the Rain', 'Ancient stone temple masonry embraced by fresh green moss, rain-washed foliage, and glistening lotus ponds.'),
    'kr-128': ('Konkan Coast Dream', 'The Rugged Edge of the Western Shore', 'Red laterite cliffs, crashing Arabian Sea foam, and wild coastal palms under luminous atmospheric skies.'),
    'kr-129': ('Spice Forest', 'The Tangled Origins of Southern Flavour', 'Cardamom clusters, climbing black pepper vines, and cinnamon foliage intertwined in a rich, aromatic botanical tapestry.'),
    'kr-130': ('Southern Rainforest', 'The Vibrating Apex of the Canopy', 'Multi-layered Western Ghats evergreen canopy teeming with giant ferns, orchids, and diffused emerald light.'),
    'kr-131': ('Tropical South', 'The Signature Synthesis', 'The definitive panoramic expression of South Indian flora, mist-shrouded hills, and peaceful water bodies in harmonious balance.'),
    'kr-132': ('Coast of Golden Light', 'Where the Falls Meet the Sea', 'Sun-drenched coastal waterfalls tumbling into coastal lagoons amidst glowing amber and gold reflections.'),
    'kr-134': ('Little Krishna of Vrindavan', 'A Divine Pastoral Dreamscape', 'Gentle, storybook depiction of Little Krishna playing flute amidst friendly cows, blooming Kadamba trees, and soft pastoral hills.'),
    'kr-135': ('Krishna\'s Peacock Garden', 'Immersed in Vibrant Foliage', 'Playful peacocks dancing under blossoming jasmine arches and fresh tropical greenery in charming watercolour style.'),
    'kr-136': ('Ganesha\'s Mango Garden', 'A Playful Orchard Discovery', 'Young Ganesha joyfully discovering golden ripe mangoes in a sunlit southern orchard with friendly woodland creatures.'),
    'kr-137': ('Ganesha\'s Little Festival', 'A Joyful Celebration of Heritage', 'A vibrant celebration of South Indian festivity. Ganesha is surrounded by beautifully illustrated traditional lamps, fresh mango leaves, and joyful floral garlands.'),
    'kr-138': ('The Elephant Parade', 'Gentle Giants in Tropical Greenery', 'Gentle decorated temple elephants strolling happily through lush tropical banana and palm groves.'),
    'kr-139': ('Elephant Temple Journey', 'A Graceful Architectural Procession', 'A graceful procession past temple towers with friendly elephants, auspicious motifs, and charming architectural detail.'),
    'kr-140': ('Peacock Palace', 'Regal Birds in Enchanted Courtyards', 'Majestic peacocks displaying colourful plumage across palace terraces, carved balustrades, and rose-tinted arches.'),
    'kr-141': ('Peacock Rain Garden', 'Lush Tropical Monsoon Beauty', 'Dancing peacocks rejoicing under cooling monsoon rain showers amidst oversized lotus leaves and water droplets.'),
    'kr-142': ('The Monkey Kingdom', 'Swinging Through Ancient Canopies', 'Playful monkeys swinging from ancient tree branches and temple stone ledges in a vibrant tropical forest setting.'),
    'kr-143': ('Monkey Forest Adventure', 'A Storybook Forest Expedition', 'Adventurous little monkeys exploring hollow ancient banyan trees and jungle vines filled with friendly wildlife.'),
    'kr-144': ('Whimsical South Indian Safari', 'The Menagerie, Continued', 'Charming deer, elephants, peacocks, and squirrels gathered peacefully in a joyful South Indian forest sanctuary.'),
    'kr-145': ('Little Jungle of the South', 'Dense, Colourful, Alive', 'Colourful tropical jungle filled with friendly jungle birds, spotted fawns, and flowering creepers.'),
    'kr-146': ('Lotus Lake Friends', 'A Tranquil Blooming Pond', 'Little swans, ducks, and leaping fish playing among giant pink lotus blossoms on a calm village lake.'),
    'kr-147': ('Little Kathakali', 'Traditional Characters Reimagined', 'Reimagined child-friendly Kathakali dancers with vibrant crown headdresses, expressive eyes, and colourful costumes.'),
    'kr-148': ('Kathakali Storybook', 'A Gracefully Illustrated Epic', 'Epic stories brought to life with friendly classical dancers, rhythm drums, and decorative stage backdrops.'),
    'kr-149': ('The Magical Temple Town', 'A Charming Architectural Landscape', 'A fairy-tale South Indian temple town with colourful gopurams, festival flags, and cheerful village houses.'),
    'kr-150': ('Temple Garden Adventure', 'Secrets Among the Stone Pathways', 'Secret stone garden paths meandering past carved temple pillars, flowering frangipani, and friendly butterflies.'),
    'kr-151': ('South Indian Storybook Village', 'Everyday Magic in the Village', 'Everyday life rendered in magical detail: traditional tiled houses, clay potters, swaying palms, and joyful children playing.'),
    'kr-152': ('Festival in the Little Village', 'A Joyful Cultural Celebration', 'A joyful cultural village festival with kolam rangoli designs on doorsteps, temple carts, and glowing brass oil lamps.'),
    'kr-153': ('Forest of the Western Ghats', 'A Dense, Breathing Rainforest', 'Lush mountain flora of the Western Ghats with giant tree ferns, wild orchids, and gentle mountain streams.'),
    'kr-154': ('Western Ghats Discovery', 'A Landscape of Mountain Wonders', 'Discovering mountain trails, rolling misty valleys, and hidden waterfalls in a warm storybook illustration.'),
    'kr-155': ('Mango Grove Adventures', 'Hide and Seek in the Orchard', 'Kids and woodland friends playing hide and seek under sweet-scented flowering mango trees.'),
    'kr-156': ('The Secret Mango Tree', 'The Towering Tree of Tales', 'A towering century-old mango tree with treehouses, swings, and endless storybook charm.'),
    'kr-157': ('Kerala Monsoon Playground', 'Joyful Splashing in the Backwaters', 'Paper boats sailing down gentle Kerala backwater streams bordered by lush coconut palms and rain lilies.'),
    'kr-158': ('Banana Leaf Wonderland', 'A Micro-World of Oversized Flora', 'Whimsical oversized tropical foliage creating a magical sheltered wonderland for little adventurers.'),
    'kr-160': ('Modern Madurai', 'Architectural Rhythms', 'Abstract architectural forms, sacred stone ratios, and terracotta colour blocks reinterpreting ancient temple rhythms for contemporary minimalist interiors.'),
    'kr-167': ('Indigo Botanica', 'The Midnight Tropics', 'Lush midnight foliage rendered in deep indigo, teal, and sage with gold leaf accents on a moody dark backdrop.'),
    'kr-184': ('New South', 'The Heritage Synthesis', 'The pinnacle of the collection. A bold, monumental contemporary composition that flawlessly weaves subtle architectural geometry, sweeping botanical lines, and intricate textile references.')
}

for p in filtered_plates:
    pid = p['id']
    vol_label = 'Kala Rasa' if p['v'] == 'kala-rasa' else 'Kala Parampara'
    
    if pid in curated:
        p['n'] = curated[pid][0]
        p['sub'] = f"{vol_label} · {curated[pid][1]}"
        p['b'] = curated[pid][2]
    else:
        p['n'] = clean_text_field(p.get('n', ''))
        sub = clean_text_field(p.get('sub', ''))
        sub_core = sub.replace('Kala Rasa ·', '').replace('Kala Parampara ·', '').replace('Kala Rasa', '').replace('Kala Parampara', '').strip(' ·,-')
        p['sub'] = f"{vol_label} · {sub_core}" if sub_core else f"{vol_label} · {p.get('no', '')}"
        
        desc = clean_text_field(p.get('b', ''))
        # Strip leading location strings
        for loc in [
            "Heritage Properties, Restaurants", "Executive Offices, Hallways", "Executive Offices, Halways",
            "Dining Spaces, Warm Living", "Dining Spaces, Living Foyers", "Pooja Rooms, Entrance Halls",
            "Modern Niches, Entrance Halls", "Living Rooms, Feature Walls", "Master Suites, Formal Living",
            "Restaurants, Hospitality Interiors"
        ]:
            if desc.startswith(loc):
                desc = desc[len(loc):].strip(' ,-·')
                
        if not desc or len(desc) < 15:
            desc = "Custom scaled and printed to your wall's exact measure on your choice of 5 luxury architectural substrates. In-house manufactured in Chennai since 1978."
        elif desc[0].islower():
            desc = desc[0].upper() + desc[1:]
        p['b'] = desc

    p['style'] = clean_text_field(p.get('style', 'Luxury Architectural Wallpaper'))
    p['ideal'] = clean_text_field(p.get('ideal', 'Living Rooms, Dining Suites, Master Bedrooms'))

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

print("Built 100% clean assets/js/data.js!")
