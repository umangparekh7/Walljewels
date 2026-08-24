import os
import re
import base64

# 1. Read the 32x32 and 180x180 PNGs
with open('favicon-32x32.png', 'rb') as f:
    b64_32 = base64.b64encode(f.read()).decode('utf-8')
data_uri_32 = f'data:image/png;base64,{b64_32}'

with open('apple-touch-icon.png', 'rb') as f:
    b64_180 = base64.b64encode(f.read()).decode('utf-8')
data_uri_180 = f'data:image/png;base64,{b64_180}'

# 2. Inject into all HTML files
v_tag = '20260824d'

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and not f.startswith('webgl-preview'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                html = fh.read()
            
            is_sub = 'showrooms' in root
            rel = '../' if is_sub else ''
            
            # Remove any existing favicon or manifest tags
            html = re.sub(r'\s*<!-- Favicon.*?-->', '', html)
            html = re.sub(r'\s*<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>', '', html)
            
            fav_block = (
                f'\n  <!-- Favicon & Brand Icons (Embedded Data URI + Multi-Format Fallbacks) -->\n'
                f'  <link rel="icon" type="image/png" href="{data_uri_32}">\n'
                f'  <link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32x32.png?v={v_tag}">\n'
                f'  <link rel="icon" type="image/png" sizes="16x16" href="{rel}favicon-16x16.png?v={v_tag}">\n'
                f'  <link rel="shortcut icon" type="image/x-icon" href="{rel}favicon.ico?v={v_tag}">\n'
                f'  <link rel="apple-touch-icon" sizes="180x180" href="{rel}apple-touch-icon.png?v={v_tag}">\n'
                f'  <link rel="manifest" href="{rel}site.webmanifest?v={v_tag}">'
            )
            
            if '</title>' in html:
                html = html.replace('</title>', f'</title>{fav_block}')
            elif '<head>' in html:
                html = html.replace('<head>', f'<head>{fav_block}')
                
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(html)
            print(f'Updated permanent favicon in {p}')

# 3. Update build-collection.mjs
with open('tools/build-collection.mjs', 'r', encoding='utf-8') as fh:
    b_code = fh.read()

b_code = re.sub(r'\s*<!-- Favicon.*?-->', '', b_code)
b_code = re.sub(r'\s*<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>', '', b_code)

fav_block_mjs = (
    f'\n  <!-- Favicon & Brand Icons (Embedded Data URI + Multi-Format Fallbacks) -->\n'
    f'  <link rel="icon" type="image/png" href="{data_uri_32}">\n'
    f'  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v={v_tag}">\n'
    f'  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png?v={v_tag}">\n'
    f'  <link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v={v_tag}">\n'
    f'  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png?v={v_tag}">\n'
    f'  <link rel="manifest" href="site.webmanifest?v={v_tag}">'
)
if '</title>' in b_code:
    b_code = b_code.replace('</title>', f'</title>{fav_block_mjs}')

with open('tools/build-collection.mjs', 'w', encoding='utf-8') as fh:
    fh.write(b_code)

# 4. Inject runtime favicon lock in app.js
with open('assets/js/app.js', 'r', encoding='utf-8') as fh:
    app_js = fh.read()

runtime_fav_code = f'''  // Permanent WJ Diamond Favicon Lock
  (function lockWJFavicon() {{
    try {{
      const uri = "{data_uri_32}";
      let links = document.querySelectorAll("link[rel*='icon']");
      links.forEach(l => l.href = uri);
      if (links.length === 0) {{
        const l = document.createElement('link');
        l.rel = 'icon';
        l.type = 'image/png';
        l.href = uri;
        document.head.appendChild(l);
      }}
    }} catch (e) {{}}
  }})();
'''

if 'lockWJFavicon' not in app_js:
    app_js = re.sub(r'(\(function \(\) \{\s*[\'"]use strict[\'"];)', r'\1\n' + runtime_fav_code, app_js)
    with open('assets/js/app.js', 'w', encoding='utf-8') as fh:
        fh.write(app_js)
    print('Injected runtime favicon lock into app.js!')

print('Permanent favicon deployment script executed successfully!')
