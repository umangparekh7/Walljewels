import re
import time

timestamp = f"v{int(time.time())}"

# 1. Add -webkit-backdrop-filter in styles.css
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add -webkit-backdrop-filter before any backdrop-filter that lacks it
def add_webkit_bf(match):
    full = match.group(0)
    if '-webkit-backdrop-filter' in full:
        return full
    val = match.group(1).strip()
    return f"-webkit-backdrop-filter: {val};\n  backdrop-filter: {val};"

css = re.sub(r'(?<!-webkit-)backdrop-filter:\s*([^;]+);', add_webkit_bf, css)

# Add iOS Safari touch scrolling and dvh units for lightbox on mobile
mobile_lightbox_enhancements = """
/* iOS Safari specific optimizations */
@supports (-webkit-touch-callout: none) {
  .lightbox__dialog {
    max-height: min(88dvh, 88vh);
    -webkit-overflow-scrolling: touch;
  }
  .lightbox__content {
    -webkit-overflow-scrolling: touch;
  }
}
"""

if "/* iOS Safari specific optimizations */" not in css:
    css += mobile_lightbox_enhancements

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated styles.css with -webkit-backdrop-filter and iOS Safari touch optimizations!")

# 2. Update cache busters in collection.html & all html files
import glob

for html_file in glob.glob('*.html') + glob.glob('showrooms/*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace ?v=... on styles.css and js files
    content = re.sub(r'\?v=[0-9A-Za-z._-]+', f'?v={timestamp}', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated all HTML cache-busters to ?v={timestamp}!")
