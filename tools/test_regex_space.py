import re

def remove_single_letter_spaces(s):
    # If more than 30% of words are single letters, it's a spaced string!
    tokens = s.split()
    single_count = sum(1 for t in tokens if len(t) == 1)
    if len(tokens) > 3 and single_count / len(tokens) > 0.4:
        # Reconstruct by joining single letters, preserving multiple spaces or word breaks
        # In the original string, two spaces or punctuation separated words
        # E.g. 'T e r r a c o t t a   K o l a m'
        # Let's replace '  ' with a special word break token '@@@', remove single spaces, then replace '@@@' with ' '
        # Or split by 2+ spaces
        words = re.split(r'\s{2,}', s)
        fixed_words = []
        for w in words:
            fixed_words.append(w.replace(' ', ''))
        return " ".join(fixed_words)
    return s

test1 = "T e r r a c o t t a  K o l a m  W a r m t h  i n  O r d e r"
test2 = "W a r m  t e r r a c o t t a  t o n e s  a n d  b o l d  s a c r e d  g e o m e t r i c"
print("Test 1:", remove_single_letter_spaces(test1))
print("Test 2:", remove_single_letter_spaces(test2))
