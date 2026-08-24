import json
import re
import os

def clean_text(t):
    if not t:
        return ""
    # remove weird symbols
    t = re.sub(r'^[\.\,\-\s\•]+', '', t)
    t = re.sub(r'[]+', '', t)
    # Fix common spacing issues
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def parse_kp():
    with open('scratch/kp_full_raw_ocr.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
        
    items = []
    for p in pages:
        lines = [clean_text(l) for l in p['lines'] if clean_text(l)]
        page_num = p['page']
        img = f"assets/img/collection/kala-parampara/kp-plate-{page_num:02d}.jpg"
        
        # Find code
        code = None
        for l in lines:
            m = re.search(r'(WJWP-[A-Z]{3}-\d{3})', l)
            if m:
                code = m.group(1)
                break
                
        # Find design number (e.g. DI-001, TH-002, etc.)
        d_num = None
        for l in lines:
            m = re.search(r'DESIGN\s*NUMBER\s*:\s*([A-Z0-9\-]+)', l, re.I)
            if m:
                d_num = m.group(1).upper().replace('O', '0')
                break

        # Find style
        style = ""
        for i, l in enumerate(lines):
            if re.search(r'STYLE\s*:', l, re.I):
                style = clean_text(re.sub(r'STYLE\s*:\s*', '', l, flags=re.I))
                if not style and i + 1 < len(lines):
                    style = lines[i+1]
                break

        # Find palette
        palette = ""
        for i, l in enumerate(lines):
            if re.search(r'COLOUR\s*PALETTE\s*:', l, re.I) or re.search(r'PALETTE\s*:', l, re.I):
                palette = clean_text(re.sub(r'(COLOUR\s*)?PALETTE\s*:\s*', '', l, flags=re.I))
                if not palette and i + 1 < len(lines):
                    palette = lines[i+1]
                break

        # Find ideal for
        ideal = ""
        for i, l in enumerate(lines):
            if re.search(r'IDEAL\s*FOR\s*:', l, re.I):
                ideal = clean_text(re.sub(r'IDEAL\s*FOR\s*:\s*', '', l, flags=re.I))
                if not ideal and i + 1 < len(lines):
                    ideal = lines[i+1]
                break

        # Extract title and subtitle
        # Title is typically the first 1 or 2 lines
        title_lines = []
        sub = ""
        desc_lines = []
        
        # Filter out headers
        body_lines = []
        for l in lines:
            if re.search(r'^(KALAPARAMPARA|COLLECTION|\d+|WJWP|DESIGN NUMBER|STYLE|COLOUR|IDEAL|CUSTOM SIZE)', l, re.I):
                continue
            body_lines.append(l)

        if len(body_lines) >= 1:
            title = body_lines[0]
            # Check if title was split across 2 lines
            idx = 1
            if len(body_lines) > 1 and len(body_lines[0].split()) <= 2 and not body_lines[0].endswith('.'):
                if not any(k in body_lines[1].lower() for k in ['the ', 'stillness', 'a ', 'an ', 'capturing']):
                    title += " " + body_lines[1]
                    idx = 2
                    
            if idx < len(body_lines):
                # Subtitle is often in quotes or a short sentence
                if len(body_lines[idx]) < 65 or body_lines[idx].endswith('.'):
                    sub = body_lines[idx]
                    idx += 1
                    
            # Remaining lines form the description paragraph
            for l in body_lines[idx:]:
                if any(k in l.upper() for k in ['DESIGN NUMBER', 'STYLE:', 'COLOUR PALETTE:', 'IDEAL FOR:', 'CUSTOM SIZE', 'WJWP-']):
                    break
                desc_lines.append(l)
                
        desc = " ".join(desc_lines)
        
        # Space category mapping
        sp = "living"
        ideal_lower = ideal.lower()
        if "bed" in ideal_lower: sp = "bedroom"
        elif "dining" in ideal_lower: sp = "dining"
        elif "meditation" in ideal_lower or "sanctuary" in ideal_lower or "temple" in ideal_lower or "pooja" in ideal_lower or "spiritual" in ideal_lower: sp = "temple"
        elif "office" in ideal_lower or "study" in ideal_lower or "executive" in ideal_lower: sp = "office"
        elif "hotel" in ideal_lower or "foyer" in ideal_lower or "entrance" in ideal_lower: sp = "hospitality"

        cat = "heritage"
        if code:
            if "BOT" in code: cat = "botanical"
            elif "WCS" in code: cat = "world"
            elif "CNT" in code: cat = "abstract"
            elif "SIH" in code or "DVN" in code: cat = "heritage"

        # Fallback default code if missing
        if not code:
            code = f"WJWP-KP-{page_num:03d}"

        items.append({
            "id": f"kp-{page_num:02d}",
            "v": "kala-parampara",
            "n": title,
            "no": code,
            "sub": sub,
            "b": desc,
            "style": style,
            "palette": palette,
            "ideal": ideal,
            "img": img,
            "sp": sp,
            "cat": cat
        })
        
    return items

def parse_kr():
    with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
        
    items = []
    for p in pages:
        lines = [clean_text(l) for l in p['lines'] if clean_text(l)]
        page_num = p['page']
        img = f"assets/img/collection/kala-rasa/kr-plate-{page_num:03d}.jpg"
        
        # Find code (e.g. WJWP-DVN-027, WJWP-SIH-013, WJWP-KOL-001, etc.)
        code = None
        for l in lines:
            m = re.search(r'(WJWP-[A-Z]{3}-\d{3})', l)
            if m:
                code = m.group(1)
                break
                
        # Find style
        style = ""
        for i, l in enumerate(lines):
            if l.upper() == 'STYLE' and i + 1 < len(lines):
                style = lines[i+1]
                break
            elif re.search(r'STYLE\s*:', l, re.I):
                style = clean_text(re.sub(r'STYLE\s*:\s*', '', l, flags=re.I))
                break

        # Find palette
        palette = ""
        for i, l in enumerate(lines):
            if l.upper() == 'PALETTE' and i + 1 < len(lines):
                palette = lines[i+1]
                break
            elif re.search(r'PALETTE\s*:', l, re.I):
                palette = clean_text(re.sub(r'PALETTE\s*:\s*', '', l, flags=re.I))
                break

        # Find ideal for
        ideal = ""
        for i, l in enumerate(lines):
            if (l.upper() == 'IDEAL FOR' or l.upper() == 'IDEALFOR') and i + 1 < len(lines):
                ideal = lines[i+1]
                break
            elif re.search(r'IDEAL\s*FOR\s*:', l, re.I):
                ideal = clean_text(re.sub(r'IDEAL\s*FOR\s*:\s*', '', l, flags=re.I))
                break

        # In Kala Rasa, lines often look like:
        # DIVINE INDIA | WJWP-DVN-027 | Ganesha: The Auspicious Beginning | STYLE | Contemporary Sacred Art ...
        title = ""
        desc_lines = []
        
        # Extract title from lines
        for i, l in enumerate(lines):
            if 'WJWP-' in l:
                # Next line is usually title
                if i + 1 < len(lines) and lines[i+1].upper() not in ['STYLE', 'PALETTE', 'IDEAL FOR', 'COLOUR']:
                    title = lines[i+1]
                    # If title wrapped
                    if i + 2 < len(lines) and lines[i+2].upper() not in ['STYLE', 'PALETTE', 'IDEAL FOR']:
                        title += " " + lines[i+2]
                break
                
        if not title:
            # Fallback scan for first non-header line
            for l in lines:
                if not re.search(r'^(KALARASA|COLLECTION|\d+|WJWP|STYLE|PALETTE|IDEAL|DIVINE|SOUTHERN|PRAKRITI)', l, re.I):
                    title = l
                    break

        # Description is usually after ideal for or at bottom
        found_meta = False
        for l in lines:
            if any(k in l.upper() for k in ['IDEAL FOR', 'IDEALFOR']):
                found_meta = True
                continue
            if found_meta:
                if not re.search(r'^(STYLE|PALETTE|IDEAL|CUSTOM SIZE|\d+$)', l, re.I):
                    desc_lines.append(l)

        desc = " ".join(desc_lines)
        if not desc:
            desc = f"Authentic handcrafted wallpaper plate from Kala Rasa (Volume II). Customized and printed to wall measure."

        sp = "living"
        ideal_lower = ideal.lower()
        if "bed" in ideal_lower: sp = "bedroom"
        elif "dining" in ideal_lower: sp = "dining"
        elif "meditation" in ideal_lower or "sanctuary" in ideal_lower or "temple" in ideal_lower or "pooja" in ideal_lower or "spiritual" in ideal_lower: sp = "temple"
        elif "office" in ideal_lower or "study" in ideal_lower or "creative" in ideal_lower or "librar" in ideal_lower: sp = "office"
        elif "child" in ideal_lower or "nursery" in ideal_lower: sp = "kids"

        cat = "heritage"
        if code:
            if "BOT" in code: cat = "botanical"
            elif "WCS" in code or "WLD" in code: cat = "world"
            elif "CNT" in code or "MOD" in code: cat = "abstract"
            elif "KID" in code: cat = "kids"
            elif "SIH" in code or "DVN" in code: cat = "heritage"

        if not code:
            code = f"WJWP-KR-{page_num:03d}"

        if not title:
            title = f"Plate #{page_num:03d}"

        items.append({
            "id": f"kr-{page_num:03d}",
            "v": "kala-rasa",
            "n": title,
            "no": code,
            "sub": f"Kala Rasa · {style}" if style else "Kala Rasa Masterpiece",
            "b": desc,
            "style": style,
            "palette": palette,
            "ideal": ideal,
            "img": img,
            "sp": sp,
            "cat": cat
        })
        
    return items

if __name__ == '__main__':
    kp = parse_kp()
    print(f"Parsed KP items: {len(kp)}")
    if os.path.exists('scratch/kr_full_raw_ocr.json'):
        kr = parse_kr()
        print(f"Parsed KR items: {len(kr)}")
        
        total = kp + kr
        print(f"Total Combined Master Plates: {len(total)}")
        with open('scratch/master_combined_plates.json', 'w', encoding='utf-8') as f:
            json.dump(total, f, indent=2, ensure_ascii=False)
