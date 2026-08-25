import re

def fix_spaced_letters(s):
    if not s:
        return ""
    # "T e r r a c o t t a   K o l a m" -> "Terracotta Kolam"
    # Join consecutive single letters separated by single space
    while re.search(r'(?<=\b[A-Za-z])\s(?=[A-Za-z]\b)', s):
        s = re.sub(r'(?<=\b[A-Za-z])\s(?=[A-Za-z]\b)', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

test = "T e r r a c o t t a   K o l a m   W a r m t h   i n   O r d e r"
print("Original:", test)
print("Fixed:", fix_spaced_letters(test))
