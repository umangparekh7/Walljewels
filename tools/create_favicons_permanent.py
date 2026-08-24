import os
import re
import base64
from PIL import Image

# 1. Read the apple touch icon (180x180) and 32x32
with open('apple-touch-icon.png', 'rb') as f:
    b64_180 = base64.b64encode(f.read()).decode('utf-8')

with open('favicon-32x32.png', 'rb') as f:
    b64_32 = base64.b64encode(f.read()).decode('utf-8')

# Create SVG favicon
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="180" height="180">
  <image href="data:image/png;base64,{b64_180}" x="0" y="0" width="180" height="180" />
</svg>'''

with open('favicon.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)
with open('assets/img/brand/favicon.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

# 2. Create webmanifest for Chrome/Android
manifest_content = '''{
  "name": "Wall Jewels Wallpaper World",
  "short_name": "Wall Jewels",
  "icons": [
    {
      "src": "/favicon-32x32.png",
      "sizes": "32x32",
      "type": "image/png"
    },
    {
      "src": "/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ],
  "theme_color": "#0b0d11",
  "background_color": "#0b0d11",
  "display": "standalone"
}
'''
with open('site.webmanifest', 'w', encoding='utf-8') as f:
    f.write(manifest_content)

# 3. Update all HTML files: place favicon tags at the TOP of <head> right after <title>
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and not f.startswith('webgl-preview'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                html = fh.read()
            
            is_sub = 'showrooms' in root
            rel = '../' if is_sub else ''
            v = '2026-08-24-wj'
            
            # Remove any existing favicon or manifest tags
            html = re.sub(r'\s*<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>', '', html)
            
            fav_block = (
                f'\n  <!-- Favicon & Brand Icons -->\n'
                f'  <link rel="icon" type="image/svg+xml" href="{rel}favicon.svg?v={v}">\n'
                f'  <link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32x32.png?v={v}">\n'
                f'  <link rel="icon" type="image/png" sizes="16x16" href="{rel}favicon-16x16.png?v={v}">\n'
                f'  <link rel="shortcut icon" type="image/x-icon" href="{rel}favicon.ico?v={v}">\n'
                f'  <link rel="apple-touch-icon" sizes="180x180" href="{rel}apple-touch-icon.png?v={v}">\n'
                f'  <link rel="manifest" href="{rel}site.webmanifest?v={v}">'
            )
            
            # Place right after </title>
            if '</title>' in html:
                html = html.replace('</title>', f'</title>{fav_block}')
            elif '<head>' in html:
                html = html.replace('<head>', f'<head>{fav_block}')
                
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(html)
            print(f'Placed top-level permanent favicons in {p}')

# 4. Update tools/build-collection.mjs
with open('tools/build-collection.mjs', 'r', encoding='utf-8') as fh:
    b_code = fh.read()

b_code = re.sub(r'\s*<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>', '', b_code)
fav_block_mjs = (
    '\n  <!-- Favicon & Brand Icons -->\n'
    '  <link rel="icon" type="image/svg+xml" href="favicon.svg?v=2026-08-24-wj">\n'
    '  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v=2026-08-24-wj">\n'
    '  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png?v=2026-08-24-wj">\n'
    '  <link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v=2026-08-24-wj">\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png?v=2026-08-24-wj">\n'
    '  <link rel="manifest" href="site.webmanifest?v=2026-08-24-wj">'
)
if '</title>' in b_code:
    b_code = b_code.replace('</title>', f'</title>{fav_block_mjs}')

with open('tools/build-collection.mjs', 'w', encoding='utf-8') as fh:
    fh.write(b_code)

print('Permanently updated build-collection.mjs!')
