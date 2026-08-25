import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

json_str = text.split('const COLLECTION = ')[1].rsplit(';', 1)[0].strip()
plates = json.loads(json_str)

# Specific exact updates requested by user and comprehensive audits
exact_updates = {
    # 30th image: kp-36 (WJWP-SIH-004)
    'kp-36': {
        'n': 'Shadows of the Gopurams',
        'sub': 'Kala Parampara · South Indian Temple Silhouettes in Mustard and Sage',
        'b': 'South Indian temple silhouettes in mustard and sage. A monumental tribute to the skyline of Southern India.'
    },
    # 48th image: kp-54 (WJWP-WCS-001)
    'kp-54': {
        'n': 'Gotham Deco',
        'sub': 'Kala Parampara · The electric ambition of a timeless metropolis.',
        'b': 'Capture the relentless energy of the Manhattan skyline with this bold, geometric tribute to 1930s Art Deco architecture. Deep charcoal and burnished gold leaf create a commanding statement wall.'
    },
    # 49th image: kp-55 (WJWP-WCS-002)
    'kp-55': {
        'n': 'Manhattan Matrix',
        'sub': 'Kala Parampara · The pure geometry of vertical ambition.',
        'b': 'Experience the metropolis stripped of literal detail and rebuilt as pure, architectural abstraction. Crisp grid lines and contrasting monotone values lend soaring height to contemporary spaces.'
    },
    # 50th image: kp-56 (WJWP-WCS-003)
    'kp-56': {
        'n': 'Hollywood Glow',
        'sub': 'Kala Parampara · The golden hour of the West Coast.',
        'b': 'Bask in the perpetual golden hour of the American West. This sun-drenched architectural silhouette captures palm-lined boulevards and hillside modernist villas in warm amber radiance.'
    },
    # 51st image: kp-57 (WJWP-WCS-004)
    'kp-57': {
        'n': 'Christ the Redeemer',
        'sub': 'Kala Parampara · The breathless rhythm of the tropical coast.',
        'b': 'Energize your space with the unrivaled vibrancy of Rio de Janeiro. Featuring the iconic Christ the Redeemer statue overlooking the dramatic mountain peaks and sweeping bays of the Brazilian coast.'
    },
    # Fix all other World Cities titles and spacing
    'kp-58': {
        'n': 'Thames Heritage',
        'sub': 'Kala Parampara · Historic elegance along the waterfront.',
        'b': 'Step into the refined history of the British capital with the classic silhouette of the Palace of Westminster and Big Ben reflecting over misty twilight waters.'
    },
    'kp-59': {
        'n': 'Twilight over Haussmann',
        'sub': 'Kala Parampara · The romance of a Parisian evening.',
        'b': 'Experience the delicate charm of a romantic evening in Paris with ornate wrought-iron balconies and grand Haussmannian boulevard facades bathed in soft evening light.'
    },
    'kp-60': {
        'n': 'Liffey Tales',
        'sub': 'Kala Parampara · The soulful charm of a literary capital.',
        'b': 'Embrace the captivating, moody atmosphere of Dublin with stone bridges arching over the River Liffey and historic Georgian brickwork.'
    },
    'kp-61': {
        'n': 'Eternal Stones',
        'sub': 'Kala Parampara · The enduring geometry of the ancient world.',
        'b': 'Command the room with the structured, classical majesty of Rome. Monolithic Colosseum arches and timeless travertine columns illustrated with archival precision.'
    },
    'kp-62': {
        'n': 'Canal Reflections',
        'sub': 'Kala Parampara · The fluid romance of the floating city.',
        'b': 'Surrender to the serene, aquatic poetry of Venice with gondolas gliding past Gothic palazzo facades and shimmering lagoon reflections.'
    },
    'kp-63': {
        'n': 'Bosphorus Splendour',
        'sub': 'Kala Parampara · The supreme opulence of a city across two worlds.',
        'b': 'Majestic domes and minarets of Istanbul rising above the Bosphorus strait in luxurious black, gold, and deep burgundy tones.'
    },
    'kp-64': {
        'n': 'Desert Mirage',
        'sub': 'Kala Parampara · Where ancient sands meet futuristic skylines.',
        'b': 'Sweeping desert dunes transitioning into the gleaming futuristic architecture and soaring spires of Dubai in crisp silver and cobalt.'
    },
    'kp-65': {
        'n': 'Nile Silhouette',
        'sub': 'Kala Parampara · Millennia of history in a single line.',
        'b': 'Minimalist architectural line-work tracing ancient pyramids and the flowing Cairo skyline along the legendary Nile in warm desert tones.'
    },
    'kp-66': {
        'n': 'Imperial Echoes',
        'sub': 'Kala Parampara · Where rich heritage meets contemporary momentum.',
        'b': 'The monumental grandeur of India Gate juxtaposed with modern New Delhi architecture in warm terracotta, beige, and gold.'
    },
    'kp-67': {
        'n': 'Arabian Dusk',
        'sub': "Kala Parampara · The dramatic sweep of the Queen's Necklace.",
        'b': "The glowing curve of Marine Drive and the Gateway of India set against a fiery sunset and deep Arabian Sea waters in Mumbai."
    },
    'kp-68': {
        'n': 'Shibuya Shadows',
        'sub': 'Kala Parampara · The cinematic pulse of the neon metropolis.',
        'b': 'Moody nocturnal skyline capturing Tokyo Tower and Shibuya with restrained jewel-toned urban glows on deep navy.'
    },
    'kp-69': {
        'n': 'Victoria Mist',
        'sub': 'Kala Parampara · Vertical ambition wrapped in harbor fog.',
        'b': 'Skyscrapers rising from Victoria Harbour into mist-shrouded mountain peaks in monochromatic charcoal and silver.'
    },
    'kp-70': {
        'n': 'Botanic Horizon',
        'sub': 'Kala Parampara · The apex of modern tropical architecture.',
        'b': 'Singapore skyline in fluid watercolour, blending Marina Bay Sands curves with lush Gardens by the Bay canopies in emerald and ivory.'
    },
    'kp-71': {
        'n': 'Harbour Brilliance',
        'sub': 'Kala Parampara · The crystalline clarity of coastal modernism.',
        'b': 'Sydney Opera House and Harbour Bridge bathed in crisp oceanic sunlight and coastal modern clarity.'
    },
    'kp-72': {
        'n': 'World Metropolis',
        'sub': 'Kala Parampara · The ultimate global panorama.',
        'b': 'A grand panoramic mural weaving the most iconic silhouettes of major world cities into a seamless, sophisticated architectural landscape.'
    }
}

for p in plates:
    pid = p['id']
    if pid in exact_updates:
        for k, v in exact_updates[pid].items():
            p[k] = v

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

print("Updated exact titles and blurbs in data.js!")
