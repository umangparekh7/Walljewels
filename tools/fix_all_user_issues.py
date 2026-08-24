import json
import re
import pymupdf
from PIL import Image

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

import io

# 1. Re-crop Durga: The Protector (KR Page 16)
pix_kr16 = doc_kr[15].get_pixmap(dpi=200)
img_kr16 = Image.open(io.BytesIO(pix_kr16.tobytes('png')))
w, h = img_kr16.size
crop_durga = img_kr16.crop((int(w * 0.18), 0, int(w * 0.60), h))
crop_durga.save('assets/img/collection/kala-rasa/kr-plate-016.jpg', quality=95)
print("Re-cropped Durga: The Protector (kr-plate-016.jpg) perfectly centered!")

# 2. Re-crop The Sanjeevani Flight (KP Page 15)
pix_kp15 = doc_kp[14].get_pixmap(dpi=200)
img_kp15 = Image.open(io.BytesIO(pix_kp15.tobytes('png')))
w, h = img_kp15.size
crop_sanj = img_kp15.crop((0, 0, int(w * 0.56), h))
crop_sanj.save('assets/img/collection/kala-parampara/kp-plate-15.jpg', quality=95)
print("Re-cropped The Sanjeevani Flight (kp-plate-15.jpg) cleanly!")

# 3. Load data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Filter out divider section pages
filtered_plates = []
for p in plates:
    if p['id'] in ['kp-32', 'kr-038', 'kr-117']:
        print(f"Removed section header divider page: {p['id']} ({p['n']})")
        continue
    if "CONTINUES" in p['n'].upper() or "CONTINUES" in p['sub'].upper():
        print(f"Removed section header divider page: {p['id']} ({p['n']})")
        continue
    filtered_plates.append(p)

# Clean specific plates
for p in filtered_plates:
    # Pages 32, 33, 34
    if p['id'] == 'kr-032':
        p['n'] = "Divine India: Sacred Harmony"
        p['sub'] = "Kala Rasa · Contemporary Masterpiece (The Magnum Opus)"
        p['style'] = "Contemporary Masterpiece"
        p['ideal'] = "Galleries, Feature Walls, Collector Spaces"
        p['b'] = "The magnum opus. A deeply sophisticated contemporary masterpiece interweaving the symbolic elements of Ganesha, Shiva, Krishna, Lakshmi, Saraswati, and Durga in harmonious sacred balance without overcrowding. A true collector's wall statement."
        
    elif p['id'] == 'kr-033':
        p['n'] = "Pichwai: Divine Companions"
        p['sub'] = "Kala Rasa · Traditional Pichwai Art"
        p['style'] = "Traditional Pichwai"
        p['ideal'] = "Pooja Rooms, Formal Living, Heritage Interiors"
        p['b'] = "A celebration of the sacred bond between cow and calf, inspired by the traditional Pichwai art of Nathdwara and Rajasthan. Blends lush foliage, lotus-filled waters, and intricate detailing to bring peace, prosperity, and divine grace into living spaces."

    elif p['id'] == 'kr-034':
        p['n'] = "Pichwai: Eternal Melody"
        p['sub'] = "Kala Rasa · Traditional Pichwai Heritage"
        p['style'] = "Traditional Pichwai"
        p['ideal'] = "Pooja Rooms, Formal Living, Heritage Interiors"
        p['b'] = "Inspired by the sacred Pichwai art of Nathdwara, this design reflects the eternal melody of devotion and nature. Krishna at the heart surrounded by cows, lotuses, peacocks, and temple charm — a timeless tribute to love, harmony, and heritage."

    # Split merged titles & subtitles
    elif p['id'] == 'kr-035' or "Rama of the Forest Arches" in p['n']:
        p['n'] = "Rama of the Forest Arches"
        p['sub'] = "Kala Rasa · Sovereign in the Sacred Grove"
        p['style'] = "Ornamental Storybook Mural"
        p['ideal'] = "Entrance Halls, Pooja Rooms, Formal Living"
        p['b'] = "Lord Rama stands at the centre of a carved triple arch, the forest and its rivers opening behind him. Ornamental sandstone framing gives the composition an architectural weight that lets a devotional subject sit comfortably in a contemporary room."

    elif p['id'] == 'kr-037' or "Ganesha Enthroned" in p['n']:
        p['n'] = "Ganesha Enthroned"
        p['sub'] = "Kala Rasa · The Vertical Sanctum"
        p['style'] = "Ornamental Portrait Mural"
        p['ideal'] = "Grand Entrances, Pooja Rooms, Feature Columns"
        p['b'] = "Lord Ganesha seated in divine grandeur beneath ornate temple arches. The vertical orientation and rich jewel tones create a monumental spiritual focal point for grand entries and sacred sanctums."

    elif p['id'] == 'kr-039' or "Chola Temple Chronicles" in p['n']:
        p['n'] = "Chola Temple Chronicles"
        p['sub'] = "Kala Rasa · Epic Narratives in Stone"
        p['style'] = "Classical Storytelling Mural"
        p['ideal'] = "Grand Living, Corridors, Heritage Suites"
        p['b'] = "Monumental stone carvings and friezes celebrating the timeless architectural genius of the Chola dynasty. Warm granite textures and lifelike bas-relief shadows create depth and historic dignity."

    elif p['id'] == 'kr-040' or "Gopuram Grandeur" in p['n']:
        p['n'] = "Gopuram Grandeur"
        p['sub'] = "Kala Rasa · Monumental Elegance"
        p['style'] = "Architectural Illustration"
        p['ideal'] = "Double Height Walls, Staircases, Grand Foyers"
        p['b'] = "Towering Dravidian gopuram silhouettes rendered in gold, sandstone, and warm terracotta. Captures the majestic verticality and spiritual aura of ancient South Indian temples."

    elif p['id'] == 'kr-041' or "Bronze and Lotus" in p['n']:
        p['n'] = "Bronze and Lotus"
        p['sub'] = "Kala Rasa · Sacred Flora"
        p['style'] = "Painterly Botanical"
        p['ideal'] = "Dining Rooms, Living Suites, Master Bedrooms"
        p['b'] = "Lustrous antique bronze sculptural forms intertwined with delicate, hand-painted South Indian temple lotuses against a rich, atmospheric patina backdrop."

    elif p['id'] == 'kr-042' or "Thanjavur Golden Garden" in p['n']:
        p['n'] = "Thanjavur Golden Garden"
        p['sub'] = "Kala Rasa · Ornamental Heritage"
        p['style'] = "Engraved Artwork"
        p['ideal'] = "Dining Halls, Formal Reception, Master Suites"
        p['b'] = "Inspired by Thanjavur gold-foil traditions, featuring intricate botanical tendrils, stylized birds, and classical South Indian ornamentation on an aged metallic canvas."

    elif p['id'] == 'kr-043' or "Temple Corridor Tales" in p['n']:
        p['n'] = "Temple Corridor Tales"
        p['sub'] = "Kala Rasa · Pathways of Antiquity"
        p['style'] = "Architectural Illustration"
        p['ideal'] = "Long Hallways, Corridors, Gallery Passages"
        p['b'] = "A breathtaking perspective through a thousand-pillared temple corridor with dramatic light filtering through stone colonnades, creating immense architectural depth."

    # General cleanup for any trailing design tags in names
    if " " in p['n']:
        parts = p['n'].split()
        if len(parts) > 4 and any(w in p['n'] for w in ["Monumental", "Sovereign", "Epic", "Ornamental", "Pathways", "Sacred"]):
            # Split if joined
            for kw in ["Sovereign in", "Epic Narratives", "Monumental Elegance", "Sacred Flora", "Ornamental Heritage", "Pathways of"]:
                if kw in p['n']:
                    t, s = p['n'].split(kw, 1)
                    p['n'] = t.strip()
                    p['sub'] = f"Kala Rasa · {kw} {s}".strip()

# Update VOLUMES counts
kp_count = len([p for p in filtered_plates if p['v'] == 'kala-parampara'])
kr_count = len([p for p in filtered_plates if p['v'] == 'kala-rasa'])

data_js = f'''// Wall Jewels Wallpaper World — Canonical Catalogue Dataset
// Synchronized directly from Kala Parampara (Volume I) & Kala Rasa (Volume II)

const VOLUMES = [
  {{ id: 'kala-parampara', name: 'Kala Parampara', no: 'Volume I', desc: '82 master plates of classical sacred iconography, southern heritage, and world architectures.', count: {kp_count} }},
  {{ id: 'kala-rasa', name: 'Kala Rasa', no: 'Volume II', desc: '178 plates of divine devotion, Pichwai traditions, lush tropicals, modern abstractions, and serene landscapes.', count: {kr_count} }}
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
