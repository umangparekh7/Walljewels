import json
import os
import re
from PIL import Image

with open('scratch/kp_ocr_results.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Concordance mapping from Page 80 of Kala Parampara
# (page_idx, Title, Subtitle, Code, SecondaryCode, Category, Space, Description)
# Let's extract the exact text from each OCR page!

parsed_kp = []

# List of intro/index pages to skip
skip_pages = [0, 1, 2, 3, 4, 31, 52, 77, 78, 79, 80, 81]

for p in pages:
    idx = p['index']
    fn = p['file']
    lines = p['texts']
    
    if idx in skip_pages:
        continue
        
    # Extract Title, Subtitle, Description, Specs
    # Find specs section index
    spec_indices = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ['design number', 'style:', 'colour palette', 'palette:', 'ideal for', 'custom size', 'wjwp-']):
            spec_indices.append(i)
            
    first_spec = spec_indices[0] if spec_indices else len(lines)
    
    # Text before specs contains: Title (lines 0-1), Subtitle (lines 1-2), Description (remaining lines before first_spec)
    title = lines[0] if len(lines) > 0 else ''
    
    # If title is split in 2 lines (e.g. ['The Cosmic', 'Tandava'] or ['Metallic', 'Labyrinth'])
    desc_start = 1
    if len(lines) > 1 and len(lines[0].split()) <= 2 and lines[1][0].isupper() and not lines[1].endswith('.'):
        title = lines[0] + ' ' + lines[1]
        desc_start = 2
        
    subtitle = ''
    if desc_start < first_spec and (lines[desc_start].endswith('.') or len(lines[desc_start].split()) <= 8):
        subtitle = lines[desc_start]
        desc_start += 1
        
    # Description lines
    desc_lines = lines[desc_start:first_spec]
    desc_text = ' '.join(desc_lines).replace('- ', '').replace('  ', ' ').strip()
    
    # Specs
    code = ''
    style = ''
    palette = ''
    ideal_for = ''
    
    for line in lines[first_spec:]:
        m_code = re.search(r'(WJWP-[A-Z]+-\d+|WJ-[A-Z]+-\d+|DI-\d+|TH-\d+)', line)
        if m_code and not code:
            code = m_code.group(1)
        if 'Style:' in line or 'STYLE:' in line or 'Style :' in line:
            style = re.sub(r'^(?:Style|STYLE)\s*:\s*', '', line)
        if 'Colour Palette:' in line or 'Palette:' in line or 'PALETTE:' in line:
            palette = re.sub(r'^(?:Colour\s*Palette|Palette|PALETTE)\s*:\s*', '', line)
        if 'Ideal For:' in line or 'IDEAL FOR:' in line or 'IdealFor:' in line:
            ideal_for = re.sub(r'^(?:Ideal\s*For|IDEAL\s*FOR|IdealFor)\s*:\s*', '', line)
            
    # Also check bottom right code in lines (usually last 1-3 lines)
    for line in lines[-4:]:
        m_perm = re.search(r'(WJWP-[A-Z]+-\d+)', line)
        if m_perm:
            code = m_perm.group(1)
            
    # Assign category & space
    cat = 'heritage'
    if 'BOT' in code or 'BTS' in code or idx in range(44, 52):
        cat = 'botanical'
    elif 'WCS' in code or idx in range(53, 73):
        cat = 'world'
    elif 'CNT' in code or idx in range(73, 77):
        cat = 'abstract'
    elif 'SIH' in code or idx in range(32, 44):
        cat = 'heritage'
        
    space = 'living'
    ideal_lower = ideal_for.lower()
    if 'bedroom' in ideal_lower:
        space = 'bedroom'
    elif 'dining' in ideal_lower:
        space = 'dining'
    elif 'office' in ideal_lower or 'boardroom' in ideal_lower or 'study' in ideal_lower:
        space = 'office'
    elif 'pooja' in ideal_lower or 'temple' in ideal_lower or 'spiritual' in ideal_lower:
        space = 'temple'
    elif 'powder' in ideal_lower or 'bath' in ideal_lower:
        space = 'powder'
    elif 'hospitality' in ideal_lower or 'lobby' in ideal_lower or 'foyer' in ideal_lower:
        space = 'hospitality'
        
    img_name = f'kp-plate-{idx:02d}.jpg'
    img_path = f'assets/img/collection/kala-parampara/{img_name}'
    
    parsed_kp.append({
        'index': idx,
        'file': fn,
        'title': title,
        'subtitle': subtitle,
        'desc': desc_text,
        'code': code or f'WJWP-KP-{idx:03d}',
        'style': style,
        'palette': palette,
        'ideal_for': ideal_for,
        'category': cat,
        'space': space,
        'img': img_path
    })

print(f'Parsed {len(parsed_kp)} authentic Kala Parampara design plates!')

with open('scratch/kp_parsed_exact.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_kp, f, indent=2, ensure_ascii=False)
