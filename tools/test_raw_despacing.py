import re
import json

def despacing_text(s):
    if not s or not isinstance(s, str):
        return ""
    # Standardize
    s = s.replace('\ufffd', ' ').replace('', ' ')
    s = s.replace('\u2014', '—').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # Check if this string is letter-spaced:
    # Look for 3+ consecutive single-character words: e.g. "S o v e r e i g n"
    # A word is spaced if we have sequences like 'X y z' or 'X Y Z'
    # In 'S o v e r e i g n  o f  t h e  C o s m o s', words are separated by 2 or more spaces, or punctuation
    # If the string contains single letters separated by single space:
    def join_chars(match):
        return match.group(0).replace(' ', '')

    # Match sequences of single letters separated by space: e.g. "S o v e r e i g n" -> "Sovereign"
    # Specifically: single letter followed by (space single letter)+
    # But do NOT join single-letter English words like 'a' or 'I' across real words if the real words are normal words.
    # To do that, if the entire string is mostly single-letter tokens:
    tokens = s.split()
    single_tokens = [t for t in tokens if len(t) == 1 and t.isalnum()]
    if len(tokens) >= 3 and len(single_tokens) / len(tokens) > 0.35:
        # The string is character-spaced!
        # First protect actual spaces between words (which are 2+ spaces, or after punctuation)
        # In Python:
        # Split by 2+ spaces or punctuation
        parts = re.split(r'(\s{2,}|[,\.\?!:;\(\)—\-])', s)
        fixed_parts = []
        for part in parts:
            if re.match(r'(\s{2,}|[,\.\?!:;\(\)—\-])', part):
                fixed_parts.append(part)
            else:
                # Remove single space between single characters
                # e.g. "S o v e r e i g n o f t h e" -> "Sovereign of the"
                # Wait, if "o f" was separated from "Sovereign" by 1 space,
                # let's see how they were separated in the raw OCR!
                # Let's inspect raw OCR for kp-08
                fixed_parts.append(re.sub(r'(?<=[A-Za-z0-9]) (?=[A-Za-z0-9])', '', part))
        s = "".join(fixed_parts)

    # Strip OCR junk
    for j in [r'\bCUSTOM\s*SIZE\s*AVAILABLE\b', r'\bCUSTOM\s*SIZE\b', r'\bCUSTOM\b', r'\bAVAILABLE\b', r'\bCUST\b', r'\bBLE\b', r'\bAVAI\b', r'\bYeS\b', r'\bYES\b']:
        s = re.sub(j, '', s, flags=re.IGNORECASE)

    # Split camelCase
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r',([^\s])', r', \1', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,-·')
    return s

with open('scratch/master_combined_plates.json', 'r', encoding='utf-8') as f:
    raw_kp = json.load(f)

for p in raw_kp[:10]:
    print("BEFORE:", p['id'], p.get('n'))
    print("AFTER: ", p['id'], despacing_text(p.get('n')))
    print("BLURB AFTER:", despacing_text(p.get('b'))[:100])
    print("-" * 50)
