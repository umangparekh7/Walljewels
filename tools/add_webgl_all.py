import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and not f.startswith('webgl-preview'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                html = fh.read()
            
            if 'webgl-bg.js' not in html:
                is_sub = 'showrooms' in root
                rel_prefix = '../' if is_sub else ''
                webgl_tag = f'<script src="{rel_prefix}assets/js/webgl-bg.js?v=2026-08-24" defer></script>'
                
                if 'app.js' in html:
                    html = re.sub(r'(\s*)(<script[^>]*app\.js[^>]*></script>)', r'\1' + webgl_tag + r'\1\2', html)
                else:
                    html = html.replace('</body>', f'  {webgl_tag}\n</body>')
                    
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(html)
                print(f'Added WebGL to {p}')

print('All pages updated with WebGL!')
