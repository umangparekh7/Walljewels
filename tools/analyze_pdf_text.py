import pymupdf
import json

kr_pdf = r'C:\Users\Chintan Kamani\Desktop\WJWP\Kala Rasa_Volume-II.pdf'
doc = pymupdf.open(kr_pdf)

def analyze_page(pnum):
    page = doc[pnum - 1]
    # Check text blocks in PDF
    text_blocks = page.get_text("blocks")
    rect = page.rect
    w, h = rect.width, rect.height
    print(f"\n--- PAGE {pnum} (w={w}, h={h}) ---")
    for b in text_blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        cleaned = text.replace('\n', ' ').strip()
        if cleaned:
            rel_x = x0 / w
            print(f"  [x={rel_x:.2f} ({x0:.0f}..{x1:.0f}), y={y0:.0f}..{y1:.0f}]: {cleaned[:100]}")

# Analyze some key pages
for p in [16, 33, 34, 35, 36, 37, 39, 40, 44, 50, 121, 122, 133, 137, 159, 160, 167]:
    analyze_page(p)
