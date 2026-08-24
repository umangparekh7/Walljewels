import json
import re
import os

def clean_str(s):
    if not s:
        return ""
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def process_kp():
    with open('scratch/kp_full_raw_ocr.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
        
    items = []
    for p in pages:
        page_num = p['page']
        lines = [clean_str(l) for l in p['lines'] if clean_str(l)]
        img = f"assets/img/collection/kala-parampara/kp-plate-{page_num:02d}.jpg"
        
        code = None
        for l in lines:
            m = re.search(r'(WJWP-[A-Z]{3}-\d{3})', l)
            if m:
                code = m.group(1)
                break
                
        style = ""
        palette = ""
        ideal = ""
        
        for i, l in enumerate(lines):
            if re.search(r'STYLE\s*:', l, re.I):
                style = re.sub(r'STYLE\s*:\s*', '', l, flags=re.I).strip()
                if not style and i + 1 < len(lines):
                    style = lines[i+1]
            elif re.search(r'(COLOUR\s*)?PALETTE\s*:', l, re.I):
                palette = re.sub(r'(COLOUR\s*)?PALETTE\s*:\s*', '', l, flags=re.I).strip()
                if not palette and i + 1 < len(lines):
                    palette = lines[i+1]
            elif re.search(r'IDEAL\s*FOR\s*:', l, re.I):
                ideal = re.sub(r'IDEAL\s*FOR\s*:\s*', '', l, flags=re.I).strip()
                if not ideal and i + 1 < len(lines):
                    ideal = lines[i+1]

        # Extract title and subtitle
        content_lines = []
        for l in lines:
            if re.search(r'^(KALAPARAMPARA|COLLECTION|\d+|WJWP|DESIGN\s*NUMBER|STYLE|COLOUR|IDEAL|CUSTOM\s*SIZE)', l, re.I):
                continue
            content_lines.append(l)

        title = ""
        sub = ""
        desc_lines = []
        
        if content_lines:
            title = content_lines[0]
            idx = 1
            # Check if title continues
            if len(content_lines) > 1 and len(content_lines[0].split()) <= 2 and not content_lines[0].endswith('.'):
                if not any(k in content_lines[1].lower() for k in ['the ', 'stillness', 'a ', 'an ', 'capturing', 'rhythmic', 'devotion', 'right']):
                    title += " " + content_lines[1]
                    idx = 2
            
            if idx < len(content_lines):
                if len(content_lines[idx]) < 70 or content_lines[idx].endswith('.'):
                    sub = content_lines[idx]
                    idx += 1
                    
            for l in content_lines[idx:]:
                if any(k in l.upper() for k in ['DESIGN NUMBER', 'STYLE:', 'PALETTE:', 'IDEAL FOR:', 'CUSTOM SIZE', 'WJWP-']):
                    break
                desc_lines.append(l)

        desc = " ".join(desc_lines)
        if not desc:
            desc = f"Authentic handcrafted wallpaper plate from Kala Parampara (Volume I). Customized and printed to wall measure."

        sp = "living"
        il = ideal.lower()
        if "bed" in il: sp = "bedroom"
        elif "dining" in il: sp = "dining"
        elif "meditation" in il or "sanctuary" in il or "temple" in il or "pooja" in il or "spiritual" in il: sp = "temple"
        elif "office" in il or "study" in il or "executive" in il: sp = "office"
        elif "foyer" in il or "entrance" in il or "hotel" in il: sp = "hospitality"

        cat = "heritage"
        if code:
            if "BOT" in code: cat = "botanical"
            elif "WCS" in code: cat = "world"
            elif "CNT" in code: cat = "abstract"
            elif "SIH" in code or "DVN" in code: cat = "heritage"

        if not code:
            code = f"WJWP-KP-{page_num:03d}"
            
        items.append({
            "id": f"kp-{page_num:02d}",
            "v": "kala-parampara",
            "n": clean_str(title),
            "no": clean_str(code),
            "sub": clean_str(sub),
            "b": clean_str(desc),
            "style": clean_str(style),
            "palette": clean_str(palette),
            "ideal": clean_str(ideal),
            "img": img,
            "sp": sp,
            "cat": cat
        })
    return items

def process_kr():
    with open('scratch/kr_full_raw_ocr.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
        
    items = []
    for p in pages:
        page_num = p['page']
        lines = [clean_str(l) for l in p['lines'] if clean_str(l)]
        img = f"assets/img/collection/kala-rasa/kr-plate-{page_num:03d}.jpg"
        
        # 1. Code
        code = None
        for l in lines:
            m = re.search(r'(WJWP-[A-Z]{3}-\d{3})', l)
            if m:
                code = m.group(1)
                break
                
        # 2. Style, Palette, Ideal
        style = ""
        palette = ""
        ideal = ""
        for i, l in enumerate(lines):
            if re.search(r'^STYLE', l, re.I):
                s_val = re.sub(r'^STYLE\s*:?\s*', '', l, flags=re.I).strip()
                style = s_val if s_val else (lines[i+1] if i + 1 < len(lines) else "")
            elif re.search(r'^(COLOUR\s*)?PALETTE', l, re.I):
                p_val = re.sub(r'^(COLOUR\s*)?PALETTE\s*:?\s*', '', l, flags=re.I).strip()
                palette = p_val if p_val else (lines[i+1] if i + 1 < len(lines) else "")
            elif re.search(r'^IDEAL\s*FOR', l, re.I):
                i_val = re.sub(r'^IDEAL\s*FOR\s*:?\s*', '', l, flags=re.I).strip()
                ideal = i_val if i_val else (lines[i+1] if i + 1 < len(lines) else "")

        # 3. Title
        title = ""
        # Look for the line after WJWP-XXX-XXX
        for i, l in enumerate(lines):
            if 'WJWP-' in l:
                # next lines until STYLE/PALETTE/IDEAL
                t_parts = []
                for next_l in lines[i+1:]:
                    if any(k == next_l.upper() or next_l.upper().startswith(k + ' ') or next_l.upper().startswith(k + ':') for k in ['STYLE', 'PALETTE', 'IDEAL', 'IDEAL FOR', 'COLOUR']):
                        break
                    t_parts.append(next_l)
                title = " ".join(t_parts)
                break

        if not title:
            # Look before STYLE
            t_parts = []
            for l in lines:
                if any(k in l.upper() for k in ['DIVINE INDIA', 'SOUTHERN INDIA', 'PRAKRITI', 'WORLD', 'CONTEMPORARY', 'WJWP', 'KALARASA']):
                    continue
                if any(k == l.upper() or l.upper().startswith(k + ' ') or l.upper().startswith(k + ':') for k in ['STYLE', 'PALETTE', 'IDEAL', 'IDEAL FOR']):
                    break
                t_parts.append(l)
            title = " ".join(t_parts)

        # 4. Description
        desc_lines = []
        found_meta_end = False
        for l in lines:
            if any(k in l.upper() for k in ['IDEAL FOR', 'IDEALFOR']):
                found_meta_end = True
                continue
            if found_meta_end:
                if not any(k in l.upper() for k in ['STYLE', 'PALETTE', 'IDEAL', 'CUSTOM SIZE', 'WJWP-', 'COLLECTION', 'KALARASA']) and not l.isdigit():
                    desc_lines.append(l)

        desc = " ".join(desc_lines)
        if not desc:
            desc = f"Authentic handcrafted wallpaper plate from Kala Rasa (Volume II). Designed and custom scaled to wall measure in Chennai."

        sp = "living"
        il = ideal.lower()
        if "bed" in il: sp = "bedroom"
        elif "dining" in il: sp = "dining"
        elif "meditation" in il or "sanctuary" in il or "temple" in il or "pooja" in il or "spiritual" in il: sp = "temple"
        elif "office" in il or "study" in il or "creative" in il or "librar" in il: sp = "office"
        elif "child" in il or "nursery" in il or "kid" in il: sp = "kids"

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
            title = f"Kala Rasa Plate #{page_num:03d}"

        sub = f"Kala Rasa · {style}" if style else "Kala Rasa Masterpiece"

        items.append({
            "id": f"kr-{page_num:03d}",
            "v": "kala-rasa",
            "n": clean_str(title),
            "no": clean_str(code),
            "sub": clean_str(sub),
            "b": clean_str(desc),
            "style": clean_str(style),
            "palette": clean_str(palette),
            "ideal": clean_str(ideal),
            "img": img,
            "sp": sp,
            "cat": cat
        })
    return items

kp = process_kp()
kr = process_kr()

print(f"Total KP plates: {len(kp)}")
print(f"Total KR plates: {len(kr)}")
print(f"Total Combined: {len(kp) + len(kr)}")

# Print sample from both
print("\n--- SAMPLE KP (First 5) ---")
for d in kp[:5]:
    print(f"[{d['no']}] {d['n']} | sub: {d['sub']} | img: {d['img']}")

print("\n--- SAMPLE KR (First 5) ---")
for d in kr[:5]:
    print(f"[{d['no']}] {d['n']} | style: {d['style']} | img: {d['img']}")

with open('scratch/master_combined_plates.json', 'w', encoding='utf-8') as f:
    json.dump(kp + kr, f, indent=2, ensure_ascii=False)
