import pymupdf

kp_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Parampara_Volume-I.pdf'
kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'

doc_kp = pymupdf.open(kp_pdf)
doc_kr = pymupdf.open(kr_pdf)

print("--- Testing PyMuPDF text block extraction on KP ---")
for p in range(6, 26):
    page = doc_kp[p - 1]
    rect = page.rect
    w, h = rect.width, rect.height
    blocks = page.get_text("blocks")
    
    left_chars = sum(len(b[4]) for b in blocks if (b[0] + b[2]) / 2 < 0.5 * w)
    right_chars = sum(len(b[4]) for b in blocks if (b[0] + b[2]) / 2 >= 0.5 * w)
    
    print(f"KP Page {p:02d} -> Rect: {w}x{h}, LeftText={left_chars}, RightText={right_chars}")
