import json, re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse collection items
# Each item has img, n, no, v, cat, sp, ideal, b
plates_raw = re.findall(r'\{\s*"id":\s*"([^"]+)",\s*"v":\s*"([^"]+)",\s*"n":\s*"([^"]+)",\s*"no":\s*"([^"]+)",\s*"sub":\s*"([^"]*)",\s*"b":\s*"([^"]*)",\s*"style":\s*"([^"]*)",\s*"palette":\s*"([^"]*)",\s*"ideal":\s*"([^"]*)",\s*"img":\s*"([^"]+)",\s*"sp":\s*"([^"]*)",\s*"cat":\s*"([^"]*)"\s*\}', text)

print(f"Total plates parsed: {len(plates_raw)}")

def match_plate(p, state):
    pid, v, name, no, sub, b, style, pal, ideal, img, sp, cat = p
    
    if state.get('v') and v != state['v']:
        return False
        
    # Category matching
    if state.get('c'):
        target_c = state['c']
        if target_c == 'kids':
            is_kids = cat == 'kids' or sp == 'kids' or any(k in (name + ' ' + b + ' ' + ideal).lower() for k in ['kids', 'nursery', 'child', 'playroom', 'whimsical', 'storybook', 'fairytale', 'baby', 'pastel forest', 'wonderland', 'meadows', 'enchanted'])
            if not is_kids:
                return False
        elif target_c != cat:
            return False

    # Space matching
    if state.get('s'):
        target_s = state['s']
        text_full = (sp + ' ' + ideal + ' ' + b + ' ' + name).lower()
        if target_s == 'temple':
            if sp != 'temple' and not any(k in text_full for k in ['temple', 'pooja', 'mandir', 'meditation', 'sanctuary', 'spiritual', 'prayer']):
                return False
        elif target_s == 'office':
            if sp != 'office' and not any(k in text_full for k in ['office', 'study', 'library', 'workspace', 'executive suite', 'boardroom']):
                return False
        elif target_s == 'dining':
            if sp != 'dining' and not any(k in text_full for k in ['dining']):
                return False
        elif target_s == 'bedroom':
            if sp != 'bedroom' and not any(k in text_full for k in ['bedroom', 'master suite', 'bed suite', 'nursery']):
                return False
        elif target_s == 'living':
            if sp != 'living' and not any(k in text_full for k in ['living', 'lounge', 'foyer', 'hospitality', 'salon', 'hall']):
                return False
        elif target_s != sp:
            return False

    return True

# Test all chips
chips = [
    ('all', {}),
    ('v:kala-parampara', {'v': 'kala-parampara'}),
    ('v:kala-rasa', {'v': 'kala-rasa'}),
    ('c:heritage', {'c': 'heritage'}),
    ('c:botanical', {'c': 'botanical'}),
    ('c:world', {'c': 'world'}),
    ('c:abstract', {'c': 'abstract'}),
    ('c:kids', {'c': 'kids'}),
    ('s:living', {'s': 'living'}),
    ('s:dining', {'s': 'dining'}),
    ('s:bedroom', {'s': 'bedroom'}),
    ('s:temple', {'s': 'temple'}),
    ('s:office', {'s': 'office'}),
]

for label, state in chips:
    matches = [p for p in plates_raw if match_plate(p, state)]
    print(f"Filter [{label}]: {len(matches)} matching plates")
