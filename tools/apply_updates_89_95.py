import json
from PIL import Image

# 1. Image Replacements
f_shiva = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787667423447.png"
f_kartikeya = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787667456942.png"
f_narayana = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787667490682.png"

Image.open(f_shiva).convert('RGB').save("assets/img/collection/kala-rasa/kr-plate-028.jpg", "JPEG", quality=95)
Image.open(f_kartikeya).convert('RGB').save("assets/img/collection/kala-rasa/kr-plate-029.jpg", "JPEG", quality=95)
Image.open(f_narayana).convert('RGB').save("assets/img/collection/kala-rasa/kr-plate-030.jpg", "JPEG", quality=95)

print("Saved new images for 89, 90, 91!")

# 2. Delete 92 to 95 from data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

to_delete = ['kr-031', 'kr-032', 'kr-033', 'kr-034', 'kr-plate-031', 'kr-plate-032', 'kr-plate-033', 'kr-plate-034']
plates = [p for p in plates if p['id'] not in to_delete]

kp_count = len([p for p in plates if p['v'] == 'kala-parampara'])
kr_count = len([p for p in plates if p['v'] == 'kala-rasa'])

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

const COLLECTION = {json.dumps(plates, indent=2, ensure_ascii=False)};
'''

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print(f"Updated data.js! Total plates: {len(plates)} (KP: {kp_count}, KR: {kr_count})")
