import json
import os
from PIL import Image

# 1. Update images for 71 and 73
f_ganesha = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666602723.png"
f_krishna = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666640681.png"

img_ganesha = Image.open(f_ganesha).convert('RGB')
img_krishna = Image.open(f_krishna).convert('RGB')

out_ganesha = "assets/img/collection/kala-rasa/kr-plate-008.jpg"
out_krishna = "assets/img/collection/kala-rasa/kr-plate-010.jpg"

img_ganesha.save(out_ganesha, "JPEG", quality=95)
img_krishna.save(out_krishna, "JPEG", quality=95)
print(f"Replaced image 71 -> {out_ganesha} ({img_ganesha.size})")
print(f"Replaced image 73 -> {out_krishna} ({img_krishna.size})")

# 2. Update data.js
with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# 66. Delete kp-73 (or any divider kp-73)
plates = [p for p in plates if p['id'] not in ['kp-73', 'kp-plate-73']]

for p in plates:
    # 54. Rename kp-61 as "Monolithic Colosseum"
    if p['id'] in ['kp-61', 'kp-plate-61']:
        p['n'] = 'Monolithic Colosseum'
        p['sub'] = 'Kala Parampara · The enduring geometry of the ancient world.'
        p['b'] = 'Command the room with the structured, classical majesty of Rome. Monolithic Colosseum arches and timeless travertine columns illustrated with archival precision.'
        
    # 55. Rename kp-62 as "Afternoon in Venice"
    if p['id'] in ['kp-62', 'kp-plate-62']:
        p['n'] = 'Afternoon in Venice'
        p['sub'] = 'Kala Parampara · The fluid romance of the floating city.'
        p['b'] = 'Surrender to the serene, aquatic poetry of Venice with gondolas gliding past Gothic palazzo facades and shimmering lagoon reflections.'

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

print(f"Updated data.js with {len(plates)} plates (KP: {kp_count}, KR: {kr_count})")
