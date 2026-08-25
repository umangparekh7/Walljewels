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

# 1. CROP FUNCTION WITH PRECISE LOGIC
def crop_kr_page(pnum):
    page = doc_kr[pnum - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    w, h = img.size
    
    # Specific custom-adjusted pages
    if pnum == 16:
        # Durga: The Protector - Niche / Architectural mockup
        cropped = img.crop((int(w * 0.18), 0, int(w * 0.58), h))
    elif pnum == 33:
        # Pichwai: Divine Companions - Photo on RIGHT
        cropped = img.crop((int(w * 0.46), 0, w, h))
    elif pnum == 34:
        # Pichwai: Eternal Melody - Photo on LEFT
        cropped = img.crop((0, 0, int(w * 0.54), h))
    elif pnum == 35:
        # Rama of the Forest Arches - Photo on RIGHT
        cropped = img.crop((int(w * 0.46), 0, w, h))
    elif pnum == 36:
        # Ganesha: Four Aspects - Photo on LEFT
        cropped = img.crop((0, 0, int(w * 0.54), h))
    elif pnum == 37:
        # Ganesha Enthroned - Photo on RIGHT
        cropped = img.crop((int(w * 0.46), 0, w, h))
    elif pnum in [38, 117, 133, 159]:
        # Section dividers
        return None
    elif pnum % 2 == 0:
        # Even pages in KR standard: Sidebar text is on the RIGHT -> Photo is on LEFT
        cropped = img.crop((0, 0, int(w * 0.53), h))
    else:
        # Odd pages in KR standard: Sidebar text is on the LEFT -> Photo is on RIGHT
        cropped = img.crop((int(w * 0.47), 0, w, h))
        
    out_path = f"assets/img/collection/kala-rasa/kr-plate-{pnum:03d}.jpg"
    cropped.save(out_path, quality=95)
    return out_path

print("Cropping target KR pages...")
target_kr_pages = [16, 33, 34, 35, 36, 37] + list(range(39, 58)) + list(range(121, 161)) + [167]
for p in target_kr_pages:
    if p <= len(doc_kr):
        res = crop_kr_page(p)
        if res:
            print(f"Cropped KR Page {p:03d} -> {res}")

# 2. LOAD AND CLEAN DATA.JS
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Filter out divider section pages
filtered_plates = []
for p in plates:
    if p['id'] in ['kp-32', 'kr-038', 'kr-117', 'kr-133', 'kr-159', 'kr-plate-133', 'kr-plate-159']:
        print(f"Removed divider section: {p['id']} ({p.get('n')})")
        continue
    if "CONTINUES" in p.get('n', '').upper() or "COLLECTION 0" in p.get('n', '').upper():
        print(f"Removed divider section: {p['id']} ({p.get('n')})")
        continue
    filtered_plates.append(p)

# Canonical mapping for specific user issues
fixes = {
    # WJWP-DVN-035
    'kr-016': {
        'n': "Durga: The Protector",
        'sub': "Kala Rasa · Contemporary Heritage Mural",
        'style': "Contemporary Heritage Mural",
        'ideal': "Modern Niches, Entrance Halls, Living Foyers",
        'b': "A modern, grounded interpretation of divine protection. Goddess Durga surrounded by regal lions, vibrant florals, and subtle celestial geometry, creating a strong spiritual anchor for contemporary spaces."
    },
    # WJWP-DVN-052
    'kr-033': {
        'n': "Pichwai: Divine Companions",
        'sub': "Kala Rasa · Traditional Pichwai Art",
        'style': "Traditional Pichwai",
        'ideal': "Pooja Rooms, Formal Living, Heritage Interiors",
        'b': "A celebration of the sacred bond between cow and calf, inspired by the traditional Pichwai art of Nathdwara. Blends lush foliage, lotus-filled waters, and intricate detailing to bring peace, prosperity, and divine grace into living spaces."
    },
    # WJWP-DVN-053
    'kr-034': {
        'n': "Pichwai: Eternal Melody",
        'sub': "Kala Rasa · Traditional Pichwai Heritage",
        'style': "Traditional Pichwai",
        'ideal': "Pooja Rooms, Formal Living, Heritage Interiors",
        'b': "Inspired by the sacred Pichwai art of Nathdwara, this design reflects the eternal melody of devotion and nature. Krishna at the heart surrounded by cows, lotuses, peacocks, and temple charm — a timeless tribute to love, harmony, and heritage."
    },
    # WJWP-DVN-054
    'kr-035': {
        'n': "Rama of the Forest Arches",
        'sub': "Kala Rasa · Sovereign in the Sacred Grove",
        'style': "Ornamental Storybook Mural",
        'ideal': "Entrance Halls, Pooja Rooms, Formal Living",
        'b': "Lord Rama stands at the centre of a carved triple arch, the forest and its rivers opening behind him. Ornamental sandstone framing gives the composition an architectural weight that lets a devotional subject sit comfortably in a contemporary room."
    },
    # WJWP-DVN-055
    'kr-036': {
        'n': "Ganesha: Four Aspects",
        'sub': "Kala Rasa · One Deity, Four Registers",
        'style': "Panelled Contemporary Sacred Art",
        'ideal': "Long Walls, Corridors, Reception Areas",
        'b': "Four distinct iconography registers of Lord Ganesha depicted in serene meditative and celebratory postures across emerald, rose, and sandstone panels."
    },
    # WJWP-DVN-056
    'kr-037': {
        'n': "Ganesha Enthroned",
        'sub': "Kala Rasa · The Vertical Sanctum",
        'style': "Ornamental Portrait Mural",
        'ideal': "Narrow Alcoves, Pooja Rooms, Stairwell Walls",
        'b': "Lord Ganesha seated in divine grandeur beneath ornate temple arches. The vertical orientation and rich jewel tones create a monumental spiritual focal point for grand entries and sacred sanctums."
    },
    # WJWP-SIH-012
    'kr-039': {
        'n': "Chola Temple Chronicles",
        'sub': "Kala Rasa · Epic Narratives in Stone",
        'style': "Classical Storytelling Mural",
        'ideal': "Grand Living, Corridors, Heritage Suites",
        'b': "Monumental stone carvings and friezes celebrating the timeless architectural genius of the Chola dynasty. Warm granite textures and lifelike bas-relief shadows create depth and historic dignity."
    },
    # WJWP-SIH-013
    'kr-040': {
        'n': "Gopuram Grandeur",
        'sub': "Kala Rasa · Monumental Elegance",
        'style': "Architectural Illustration",
        'ideal': "Double Height Walls, Staircases, Grand Foyers",
        'b': "Towering Dravidian gopuram silhouettes rendered in gold, sandstone, and warm terracotta. Captures the majestic verticality and spiritual aura of ancient South Indian temples."
    },
    # WJWP-SIH-014
    'kr-041': {
        'n': "Bronze and Lotus",
        'sub': "Kala Rasa · Sacred Flora",
        'style': "Painterly Botanical",
        'ideal': "Dining Rooms, Living Suites, Master Bedrooms",
        'b': "Lustrous antique bronze sculptural forms intertwined with delicate, hand-painted South Indian temple lotuses against a rich, atmospheric patina backdrop."
    },
    # WJWP-SIH-015
    'kr-042': {
        'n': "Thanjavur Golden Garden",
        'sub': "Kala Rasa · Ornamental Heritage",
        'style': "Engraved Artwork",
        'ideal': "Dining Halls, Formal Reception, Master Suites",
        'b': "Inspired by Thanjavur gold-foil traditions, featuring intricate botanical tendrils, stylized birds, and classical South Indian ornamentation on an aged metallic canvas."
    },
    # WJWP-SIH-016
    'kr-043': {
        'n': "Temple Corridor Tales",
        'sub': "Kala Rasa · Pathways of Antiquity",
        'style': "Architectural Illustration",
        'ideal': "Long Hallways, Corridors, Gallery Passages",
        'b': "A breathtaking perspective through a thousand-pillared temple corridor with dramatic light filtering through stone colonnades, creating immense architectural depth."
    },
    # WJWP-SIH-017
    'kr-044': {
        'n': "Dravidian Stone Stories",
        'sub': "Kala Rasa · Etched in Time",
        'style': "Etched Artwork",
        'ideal': "Living Rooms, Executive Studies, Libraries",
        'b': "Etched stone reliefs documenting sacred dynastic lore, carved temple friezes, and architectural stonework in delicate sepia and charcoal tones."
    },
    # WJWP-SIH-018
    'kr-045': {
        'n': "Sacred Water",
        'sub': "Kala Rasa · Serene Mural",
        'style': "Serene Mural",
        'ideal': "Courtyards, Bath Suites, Living Lounges",
        'b': "A contemplative portrayal of temple tank waters reflecting sanctum pillars, sacred steps, and morning skies in tranquil dusk blue and stone grey."
    },
    # WJWP-SIH-019
    'kr-046': {
        'n': "Mandala of Madurai",
        'sub': "Kala Rasa · Divine Geometry",
        'style': "Contemporary Geometric",
        'ideal': "Dining Spaces, Feature Walls, Ceilings",
        'b': "Intricate concentric mandala geometry inspired by the ceiling vaults and sacred architectural grids of Madurai Meenakshi Amman Temple."
    },
    # WJWP-SIH-020
    'kr-047': {
        'n': "Chettinad Heritage",
        'sub': "Kala Rasa · The Merchant's Courtyard",
        'style': "Architectural Illustration",
        'ideal': "Open-plan Living, Verandas, Dining Halls",
        'b': "The stately symmetry of Chettinad mansion courtyards with carved teak pillars, Athangudi tiled borders, and sunlit central courtyards."
    },
    # WJWP-SIH-021
    'kr-048': {
        'n': "Mysore Palace Reverie",
        'sub': "Kala Rasa · Royal Elegance",
        'style': "Painterly Art",
        'ideal': "Formal Living Rooms, Master Bedrooms, Foyers",
        'b': "Opulent stained-glass radiance, gold-leaf colonnades, and durbar hall splendour capturing the regal spirit of Mysore Palace."
    },
    # WJWP-SIH-022
    'kr-049': {
        'n': "Hampi in the Monsoon",
        'sub': "Kala Rasa · Ruins in the Rain",
        'style': "Atmospheric Landscape",
        'ideal': "Feature Walls, Living Rooms, Contemporary Lounges",
        'b': "Atmospheric basalt boulders and ancient Vijayanagara ruins shrouded in dramatic monsoon clouds, deep indigo rain, and fresh emerald moss."
    },
    # WJWP-SIH-023
    'kr-050': {
        'n': "Deccan Palace Garden",
        'sub': "Kala Rasa · Fountains and Flora",
        'style': "Classical Architecture",
        'ideal': "Courtyard Walls, Verandas, Dining Rooms",
        'b': "Geometric Charbagh water channels, ornate stone fountains, and stylized cypress trees from royal Deccan pleasure gardens in indigo and terracotta."
    },
    # WJWP-SIH-024
    'kr-051': {
        'n': "Kalamkari Royal Court",
        'sub': "Kala Rasa · The Woven Court",
        'style': "Royal Narrative",
        'ideal': "Living Lounges, Master Suites, Galleries",
        'b': "Hand-drawn pen Kalamkari textile murals depicting royal courts, celestial dancers, and ornate flowering trees dyed in rich natural vegetable hues."
    },
    # WJWP-SIH-025
    'kr-052': {
        'n': "Sacred Banyan Stories",
        'sub': "Kala Rasa · Roots of the Divine",
        'style': "Symbolic Storytelling",
        'ideal': "Courtyards, Foyers, Meditative Spaces",
        'b': "Sprawling aerial roots and sheltering banyan canopy symbolizing cosmic longevity, spiritual wisdom, and South Indian village sanctums."
    },
    # WJWP-SIH-026
    'kr-053': {
        'n': "The Temple Tank",
        'sub': "Kala Rasa · Sacred Reflections",
        'style': "Serene Landscape",
        'ideal': "Wellness Rooms, Living Rooms, Bedrooms",
        'b': "Stepped stone theppakulam reservoir reflecting temple spires and floating lotus blossoms in serene indigo and cool emerald ripples."
    },
    # WJWP-SIH-027
    'kr-054': {
        'n': "Pillars of Time",
        'sub': "Kala Rasa · Rhythmic Monumentality",
        'style': "Contemporary Pattern",
        'ideal': "Corridors, Long Walls, Commercial Foyers",
        'b': "A rhythmic sequence of monolithic carved granite pillars showcasing the timeless architectural grandeur of South Indian temple colonnades."
    },
    # WJWP-SIH-028
    'kr-055': {
        'n': "Temple Floral Archive",
        'sub': "Kala Rasa · Classical Blossoms",
        'style': "Botanical Archive",
        'ideal': "Powder Rooms, Master Bedrooms, Dining Halls",
        'b': "Classical botanical studies of sacred South Indian temple flowers: jasmine, champaka, marigold, and lotus rendered with archival delicate line-work."
    },
    # WJWP-SIH-029
    'kr-056': {
        'n': "Chola Garden Procession",
        'sub': "Kala Rasa · A Walk Through History",
        'style': "Historical Procession",
        'ideal': "Long Corridors, Living Suites, Heritage Hotels",
        'b': "Royal ceremonial processions through palace gardens with caparisoned elephants, flag-bearers, and courtiers amidst lush Chola greenery."
    },
    # WJWP-SIH-030
    'kr-057': {
        'n': "Gopuram at Dusk",
        'sub': "Kala Rasa · Silhouettes of the Sacred",
        'style': "Layered Silhouette",
        'ideal': "Feature Walls, Living Rooms, Double-Height Spaces",
        'b': "Dramatic dusk skies framing layered silhouettes of towering temple gopurams in rich terracotta, charcoal, and twilight bronze."
    },
    
    # 121..160, 167
    'kr-121': {
        'n': "Coconut Grove Reverie",
        'sub': "Kala Rasa · Vertical Grace over Jungle Chaos",
        'style': "Refined Tropical Pattern",
        'ideal': "Sunrooms, Dining Suites, Verandas",
        'b': "Swaying coconut palm fronds capturing golden tropical light with vertical botanical rhythm and coastal serenity."
    },
    'kr-122': {
        'n': "Monsoon in Munnar",
        'sub': "Kala Rasa · The Electric Tension of High-Altitude Rain",
        'style': "Atmospheric Landscape",
        'ideal': "Living Rooms, Bedrooms, Feature Walls",
        'b': "Rolling tea-plantation slopes and misty high-altitude mountain contours under dramatic monsoon cloud formations in rich forest greens and slate blues."
    },
    'kr-123': {
        'n': "Coorg Coffee Estate",
        'sub': "Kala Rasa · The Shaded Geometry of the Coffee Lands",
        'style': "Engraved Botanical Landscape",
        'ideal': "Executive Studies, Living Lounges, Dining Rooms",
        'b': "Canopied coffee bushes, silver oak shade trees, and pepper vines illustrated with fine engraving precision in earthy greens and deep bronze."
    },
    'kr-124': {
        'n': "Malabar Fishing Village",
        'sub': "Kala Rasa · The Rhythm of Life on the Arabian Sea",
        'style': "Refined Narrative Mural",
        'ideal': "Living Rooms, Coastal Villas, Dining Suites",
        'b': "Traditional wooden country boats, coastal palm shorelines, and gentle waves of the Malabar coast in breezy contemporary tones."
    },
    'kr-125': {
        'n': "Lotus and Waterlily",
        'sub': "Kala Rasa · Aquatic Botanical Geometry",
        'style': "Botanical Illustration",
        'ideal': "Powder Rooms, Master Bathrooms, Bedroom Alcoves",
        'b': "Floating lotus pads, flowering aquatic buds, and clear water ripples in serene botanical harmony."
    },
    'kr-126': {
        'n': "Banana Leaf Canopy",
        'sub': "Kala Rasa · Architectural Foliage",
        'style': "Bold Tropical Botanical",
        'ideal': "Dining Suites, Verandas, Feature Walls",
        'b': "Oversized, sculptural banana leaves overlapping in lush emerald and olive layers, creating dramatic tropical depth."
    },
    'kr-127': {
        'n': "Temple Garden Monsoon",
        'sub': "Kala Rasa · Ancient Stone Yielding to the Rain",
        'style': "Painterly Heritage Landscape",
        'ideal': "Living Rooms, Corridors, Courtyards",
        'b': "Ancient stone temple masonry embraced by fresh green moss, rain-washed foliage, and glistening lotus ponds."
    },
    'kr-128': {
        'n': "Konkan Coast Dream",
        'sub': "Kala Rasa · The Rugged Edge of the Western Shore",
        'style': "Atmospheric Coastal Landscape",
        'ideal': "Living Rooms, Bed Backdrops, Lounges",
        'b': "Red laterite cliffs, crashing Arabian Sea foam, and wild coastal palms under luminous atmospheric skies."
    },
    'kr-129': {
        'n': "Spice Forest",
        'sub': "Kala Rasa · The Tangled Origins of Southern Flavour",
        'style': "Dense Tropical Botanical",
        'ideal': "Dining Rooms, Kitchen Breakfast Nooks, Verandas",
        'b': "Cardamom clusters, climbing black pepper vines, and cinnamon foliage intertwined in a rich, aromatic botanical tapestry."
    },
    'kr-130': {
        'n': "Southern Rainforest",
        'sub': "Kala Rasa · The Vibrating Apex of the Canopy",
        'style': "Painterly Rainforest Mural",
        'ideal': "Feature Walls, Master Suites, Living Spaces",
        'b': "Multi-layered Western Ghats evergreen canopy teeming with giant ferns, orchids, and diffused emerald light."
    },
    'kr-131': {
        'n': "Tropical South",
        'sub': "Kala Rasa · The Signature Synthesis",
        'style': "Masterwork Atmospheric Mural",
        'ideal': "Grand Foyers, Living Rooms, Commercial Spaces",
        'b': "The definitive panoramic expression of South Indian flora, mist-shrouded hills, and peaceful water bodies in harmonious balance."
    },
    'kr-132': {
        'n': "Coast of Golden Light",
        'sub': "Kala Rasa · Where the Falls Meet the Sea",
        'style': "Illuminated Landscape Relief",
        'ideal': "Dining Halls, Master Suites, Feature Alcoves",
        'b': "Sun-drenched coastal waterfalls tumbling into coastal lagoons amidst glowing amber and gold reflections."
    },
    'kr-134': {
        'n': "Little Krishna of Vrindavan",
        'sub': "Kala Rasa · A Divine Pastoral Dreamscape",
        'style': "Storybook Illustration",
        'ideal': "Kids Rooms, Nurseries, Pooja Spaces",
        'b': "Gentle, storybook depiction of Little Krishna playing flute amidst friendly cows, blooming Kadamba trees, and soft pastoral hills."
    },
    'kr-135': {
        'n': "Krishna's Peacock Garden",
        'sub': "Kala Rasa · Immersed in Vibrant Foliage",
        'style': "Botanical Watercolour",
        'ideal': "Kids Rooms, Nurseries, Family Lounges",
        'b': "Playful peacocks dancing under blossoming jasmine arches and fresh tropical greenery in charming watercolour style."
    },
    'kr-136': {
        'n': "Ganesha's Mango Garden",
        'sub': "Kala Rasa · A Playful Orchard Discovery",
        'style': "Contemporary Children's Illustration",
        'ideal': "Kids Bedrooms, Study Rooms, Play Areas",
        'b': "Young Ganesha joyfully discovering golden ripe mangoes in a sunlit southern orchard with friendly woodland creatures."
    },
    'kr-137': {
        'n': "Ganesha's Little Festival",
        'sub': "Kala Rasa · A Joyful Celebration of Heritage",
        'style': "Heritage Patterns",
        'ideal': "Kids Rooms, Pooja Spaces, Living Foyers",
        'b': "A vibrant celebration of South Indian festivity. Ganesha is surrounded by beautifully illustrated traditional lamps, fresh mango leaves, and joyful floral garlands, creating a dynamic and culturally rich backdrop."
    },
    'kr-138': {
        'n': "The Elephant Parade",
        'sub': "Kala Rasa · Gentle Giants in Tropical Greenery",
        'style': "Painterly Children's Mural",
        'ideal': "Kids Bedrooms, Playrooms, Corridors",
        'b': "Gentle decorated temple elephants strolling happily through lush tropical banana and palm groves."
    },
    'kr-139': {
        'n': "Elephant Temple Journey",
        'sub': "Kala Rasa · A Graceful Architectural Procession",
        'style': "Heritage Storybook Illustration",
        'ideal': "Kids Rooms, Nurseries, Family Spaces",
        'b': "A graceful procession past temple towers with friendly elephants, auspicious motifs, and charming architectural detail."
    },
    'kr-140': {
        'n': "Peacock Palace",
        'sub': "Kala Rasa · Regal Birds in Enchanted Courtyards",
        'style': "Storybook Architectural",
        'ideal': "Kids Rooms, Bedrooms, Playrooms",
        'b': "Majestic peacocks displaying colourful plumage across palace terraces, carved balustrades, and rose-tinted arches."
    },
    'kr-141': {
        'n': "Peacock Rain Garden",
        'sub': "Kala Rasa · Lush Tropical Monsoon Beauty",
        'style': "Watercolour Botanical",
        'ideal': "Kids Bedrooms, Nurseries, Reading Nooks",
        'b': "Dancing peacocks rejoicing under cooling monsoon rain showers amidst oversized lotus leaves and water droplets."
    },
    'kr-142': {
        'n': "The Monkey Kingdom",
        'sub': "Kala Rasa · Swinging Through Ancient Canopies",
        'style': "Contemporary Children's Illustration",
        'ideal': "Kids Playrooms, Activity Rooms, Bedrooms",
        'b': "Playful monkeys swinging from ancient tree branches and temple stone ledges in a vibrant tropical forest setting."
    },
    'kr-143': {
        'n': "Monkey Forest Adventure",
        'sub': "Kala Rasa · A Storybook Forest Expedition",
        'style': "Painterly Children's Mural",
        'ideal': "Kids Bedrooms, Playrooms, Daycares",
        'b': "Adventurous little monkeys exploring hollow ancient banyan trees and jungle vines filled with friendly wildlife."
    },
    'kr-144': {
        'n': "Whimsical South Indian Safari",
        'sub': "Kala Rasa · The Menagerie, Continued",
        'style': "Storybook Illustration",
        'ideal': "Nurseries, Kids Rooms, Toddler Spaces",
        'b': "Charming deer, elephants, peacocks, and squirrels gathered peacefully in a joyful South Indian forest sanctuary."
    },
    'kr-145': {
        'n': "Little Jungle of the South",
        'sub': "Kala Rasa · Dense, Colourful, Alive",
        'style': "Botanical Children's Art",
        'ideal': "Kids Bedrooms, Playrooms, Study Areas",
        'b': "Colourful tropical jungle filled with friendly jungle birds, spotted fawns, and flowering creepers."
    },
    'kr-146': {
        'n': "Lotus Lake Friends",
        'sub': "Kala Rasa · A Tranquil Blooming Pond",
        'style': "Watercolour Botanical",
        'ideal': "Nurseries, Bedrooms, Reading Corners",
        'b': "Little swans, ducks, and leaping fish playing among giant pink lotus blossoms on a calm village lake."
    },
    'kr-147': {
        'n': "Little Kathakali",
        'sub': "Kala Rasa · Traditional Characters Reimagined",
        'style': "Whimsical Heritage Art",
        'ideal': "Kids Rooms, Cultural Studios, Activity Areas",
        'b': "Reimagined child-friendly Kathakali dancers with vibrant crown headdresses, expressive eyes, and colourful costumes."
    },
    'kr-148': {
        'n': "Kathakali Storybook",
        'sub': "Kala Rasa · A Gracefully Illustrated Epic",
        'style': "Storybook Illustration",
        'ideal': "Kids Bedrooms, Reading Rooms, Lounges",
        'b': "Epic stories brought to life with friendly classical dancers, rhythm drums, and decorative stage backdrops."
    },
    'kr-149': {
        'n': "The Magical Temple Town",
        'sub': "Kala Rasa · A Charming Architectural Landscape",
        'style': "Painterly Children's Mural",
        'ideal': "Kids Bedrooms, Corridors, Playrooms",
        'b': "A fairy-tale South Indian temple town with colourful gopurams, festival flags, and cheerful village houses."
    },
    'kr-150': {
        'n': "Temple Garden Adventure",
        'sub': "Kala Rasa · Secrets Among the Stone Pathways",
        'style': "Botanical Architectural Art",
        'ideal': "Kids Rooms, Activity Spaces, Corridors",
        'b': "Secret stone garden paths meandering past carved temple pillars, flowering frangipani, and friendly butterflies."
    },
    'kr-151': {
        'n': "South Indian Storybook Village",
        'sub': "Kala Rasa · Everyday Magic in the Village",
        'style': "Storybook Illustration",
        'ideal': "Kids Bedrooms, Playrooms, Family Living",
        'b': "Everyday life rendered in magical detail: traditional tiled houses, clay potters, swaying palms, and joyful children playing."
    },
    'kr-152': {
        'n': "Festival in the Little Village",
        'sub': "Kala Rasa · A Joyful Cultural Celebration",
        'style': "Painterly Children's Mural",
        'ideal': "Kids Rooms, Play Areas, Corridors",
        'b': "A joyful cultural village festival with kolam rangoli designs on doorsteps, temple carts, and glowing brass oil lamps."
    },
    'kr-153': {
        'n': "Forest of the Western Ghats",
        'sub': "Kala Rasa · A Dense, Breathing Rainforest",
        'style': "Botanical Watercolour",
        'ideal': "Kids Rooms, Study Rooms, Bedrooms",
        'b': "Lush mountain flora of the Western Ghats with giant tree ferns, wild orchids, and gentle mountain streams."
    },
    'kr-154': {
        'n': "Western Ghats Discovery",
        'sub': "Kala Rasa · A Landscape of Mountain Wonders",
        'style': "Storybook Landscape",
        'ideal': "Kids Bedrooms, Nurseries, Reading Nooks",
        'b': "Discovering mountain trails, rolling misty valleys, and hidden waterfalls in a warm storybook illustration."
    },
    'kr-155': {
        'n': "Mango Grove Adventures",
        'sub': "Kala Rasa · Hide and Seek in the Orchard",
        'style': "Contemporary Illustration",
        'ideal': "Kids Playrooms, Bedrooms, Daycares",
        'b': "Kids and woodland friends playing hide and seek under sweet-scented flowering mango trees."
    },
    'kr-156': {
        'n': "The Secret Mango Tree",
        'sub': "Kala Rasa · The Towering Tree of Tales",
        'style': "Painterly Children's Mural",
        'ideal': "Kids Bedrooms, Feature Walls, Playrooms",
        'b': "A towering century-old mango tree with treehouses, swings, and endless storybook charm."
    },
    'kr-157': {
        'n': "Kerala Monsoon Playground",
        'sub': "Kala Rasa · Joyful Splashing in the Backwaters",
        'style': "Watercolour Landscape",
        'ideal': "Kids Rooms, Nurseries, Bath Suites",
        'b': "Paper boats sailing down gentle Kerala backwater streams bordered by lush coconut palms and rain lilies."
    },
    'kr-158': {
        'n': "Banana Leaf Wonderland",
        'sub': "Kala Rasa · A Micro-World of Oversized Flora",
        'style': "Botanical Art for Children",
        'ideal': "Nurseries, Kids Bedrooms, Playrooms",
        'b': "Whimsical oversized tropical foliage creating a magical sheltered wonderland for little adventurers."
    },
    'kr-160': {
        'n': "Modern Madurai",
        'sub': "Kala Rasa · Architectural Rhythms",
        'style': "Contemporary Architectural Art",
        'ideal': "Premium Commercial Lounges, Modern Living Rooms, Foyers",
        'b': "Abstract architectural forms, sacred stone ratios, and terracotta colour blocks reinterpreting ancient temple rhythms for contemporary minimalist interiors."
    },
    'kr-167': {
        'n': "Indigo Botanica",
        'sub': "Kala Rasa · The Midnight Tropics",
        'style': "Contemporary Botanical",
        'ideal': "Wellness Spaces, Spa Bathrooms, Master Bedrooms",
        'b': "Lush midnight foliage rendered in deep indigo, teal, and sage with gold leaf accents on a moody dark backdrop."
    }
}

# Apply fixes to filtered_plates
for p in filtered_plates:
    pid = p['id']
    if pid in fixes:
        for k, v in fixes[pid].items():
            p[k] = v
            
    # Also fix any remaining merged subtitles in 'n'
    name = p.get('n', '')
    if " " in name and len(name.split()) > 4:
        for phrase in [
            ("OneDeity,FourRegisters", "Ganesha: Four Aspects", "Kala Rasa · One Deity, Four Registers"),
            ("Etched in Time", "Dravidian Stone Stories", "Kala Rasa · Etched in Time"),
            ("Divine Geometry", "Mandala of Madurai", "Kala Rasa · Divine Geometry"),
            ("The Merchant's Courtyard", "Chettinad Heritage", "Kala Rasa · The Merchant's Courtyard"),
            ("Royal Elegance", "Mysore Palace Reverie", "Kala Rasa · Royal Elegance"),
            ("Ruins in the Rain", "Hampi in the Monsoon", "Kala Rasa · Ruins in the Rain"),
            ("FountainsandFlora", "Deccan Palace Garden", "Kala Rasa · Fountains and Flora"),
            ("The Woven Court", "Kalamkari Royal Court", "Kala Rasa · The Woven Court"),
            ("Roots of the Divine", "Sacred Banyan Stories", "Kala Rasa · Roots of the Divine"),
            ("SacredReflections", "The Temple Tank", "Kala Rasa · Sacred Reflections"),
            ("Rhythmic Monumentality", "Pillars of Time", "Kala Rasa · Rhythmic Monumentality"),
            ("ClassicalBlossoms", "Temple Floral Archive", "Kala Rasa · Classical Blossoms"),
            ("AWalkThroughHistory", "Chola Garden Procession", "Kala Rasa · A Walk Through History"),
            ("Silhouettesofthe Sacred", "Gopuram at Dusk", "Kala Rasa · Silhouettes of the Sacred"),
            ("VerticalGraceover JungleChaos", "Coconut Grove Reverie", "Kala Rasa · Vertical Grace over Jungle Chaos"),
            ("The Electric Tension of High-Altitude Rain", "Monsoon in Munnar", "Kala Rasa · The Electric Tension of High-Altitude Rain"),
            ("The Shaded Geometry of the Coffee Lands", "Coorg Coffee Estate", "Kala Rasa · The Shaded Geometry of the Coffee Lands"),
            ("TheRhythmof Lifeonthe ArabianSea", "Malabar Fishing Village", "Kala Rasa · The Rhythm of Life on the Arabian Sea"),
            ("Aquatic BotanicalGeometry", "Lotus and Waterlily", "Kala Rasa · Aquatic Botanical Geometry"),
            ("Architectural Foliage", "Banana Leaf Canopy", "Kala Rasa · Architectural Foliage"),
            ("Ancient Stone Yielding totheRain", "Temple Garden Monsoon", "Kala Rasa · Ancient Stone Yielding to the Rain"),
            ("The Rugged Edge of the Western Shore", "Konkan Coast Dream", "Kala Rasa · The Rugged Edge of the Western Shore"),
            ("The Tangled Origins of Southern Flavour", "Spice Forest", "Kala Rasa · The Tangled Origins of Southern Flavour"),
            ("TheVibratingApexof theCanopy", "Southern Rainforest", "Kala Rasa · The Vibrating Apex of the Canopy"),
            ("TheSignature Synthesis", "Tropical South", "Kala Rasa · The Signature Synthesis"),
            ("WheretheFalls MeettheSea", "Coast of Golden Light", "Kala Rasa · Where the Falls Meet the Sea"),
            ("ADivinePastoral Dreamscape", "Little Krishna of Vrindavan", "Kala Rasa · A Divine Pastoral Dreamscape"),
            ("Immersed in Vibrant Foliage", "Krishna's Peacock Garden", "Kala Rasa · Immersed in Vibrant Foliage"),
            ("APlayful Orchard Discovery", "Ganesha's Mango Garden", "Kala Rasa · A Playful Orchard Discovery"),
            ("GentleGiantsinTropicalGreenery", "The Elephant Parade", "Kala Rasa · Gentle Giants in Tropical Greenery"),
            ("AGracefulArchitecturalProcession", "Elephant Temple Journey", "Kala Rasa · A Graceful Architectural Procession"),
            ("RegalBirds in Enchanted Courtyards", "Peacock Palace", "Kala Rasa · Regal Birds in Enchanted Courtyards"),
            ("LushTropical MonsoonBeauty", "Peacock Rain Garden", "Kala Rasa · Lush Tropical Monsoon Beauty"),
            ("SwingingThroughAncientCanopies", "The Monkey Kingdom", "Kala Rasa · Swinging Through Ancient Canopies"),
            ("AStorybook ForestExpedition", "Monkey Forest Adventure", "Kala Rasa · A Storybook Forest Expedition"),
            ("The Menagerie,Continued", "Whimsical South Indian Safari", "Kala Rasa · The Menagerie, Continued"),
            ("Dense,Colourful,Alive", "Little Jungle of the South", "Kala Rasa · Dense, Colourful, Alive"),
            ("ATranquil Blooming Pond", "Lotus Lake Friends", "Kala Rasa · A Tranquil Blooming Pond"),
            ("Traditional Characters Reimagined", "Little Kathakali", "Kala Rasa · Traditional Characters Reimagined"),
            ("AGracefullyIllustratedEpic", "Kathakali Storybook", "Kala Rasa · A Gracefully Illustrated Epic"),
            ("ACharmingArchitectural Landscape", "The Magical Temple Town", "Kala Rasa · A Charming Architectural Landscape"),
            ("SecretsAmong the StonePathways", "Temple Garden Adventure", "Kala Rasa · Secrets Among the Stone Pathways"),
            ("EverydayMagicintheVillage", "South Indian Storybook Village", "Kala Rasa · Everyday Magic in the Village"),
            ("AJoyfulCulturalCelebration", "Festival in the Little Village", "Kala Rasa · A Joyful Cultural Celebration"),
            ("ADense,Breathing Rainforest", "Forest of the Western Ghats", "Kala Rasa · A Dense, Breathing Rainforest"),
            ("ALandscapeof MountainWonders", "Western Ghats Discovery", "Kala Rasa · A Landscape of Mountain Wonders"),
            ("HideandSeekintheOrchard", "Mango Grove Adventures", "Kala Rasa · Hide and Seek in the Orchard"),
            ("TheToweringTreeof Tales", "The Secret Mango Tree", "Kala Rasa · The Towering Tree of Tales"),
            ("Joyful SplashingintheBackwaters", "Kerala Monsoon Playground", "Kala Rasa · Joyful Splashing in the Backwaters"),
            ("AMicro-WorldofOversizedFlora", "Banana Leaf Wonderland", "Kala Rasa · A Micro-World of Oversized Flora"),
            ("The Midnight Tropics", "Indigo Botanica", "Kala Rasa · The Midnight Tropics")
        ]:
            if phrase[0] in name or phrase[0].lower() in name.lower():
                p['n'] = phrase[1]
                p['sub'] = phrase[2]

# Update VOLUMES counts
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

print(f"Updated data.js! KP Count: {kp_count}, KR Count: {kr_count}, Total: {len(filtered_plates)}")
