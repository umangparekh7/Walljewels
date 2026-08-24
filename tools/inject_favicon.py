import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and not f.startswith('webgl-preview'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                html = fh.read()
            
            is_sub = 'showrooms' in root
            rel = '../' if is_sub else ''
            
            # Remove any existing favicon tags to be clean
            html = re.sub(r'\s*<link rel="icon"[^>]*>', '', html)
            html = re.sub(r'\s*<link rel="shortcut icon"[^>]*>', '', html)
            html = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', '', html)
            
            fav_tags = (
                f'\n  <link rel="icon" type="image/x-icon" href="{rel}favicon.ico">\n'
                f'  <link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32x32.png">\n'
                f'  <link rel="icon" type="image/png" sizes="16x16" href="{rel}favicon-16x16.png">\n'
                f'  <link rel="apple-touch-icon" sizes="180x180" href="{rel}apple-touch-icon.png">'
            )
            
            # Insert right before </head> or after canonical
            if '</head>' in html:
                html = html.replace('</head>', f'{fav_tags}\n</head>')
            
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(html)
            print(f'Injected WJ favicon into {p}')

# Also update tools/build-collection.mjs template
with open('tools/build-collection.mjs', 'r', encoding='utf-8') as fh:
    b_code = fh.read()

fav_tags_mjs = (
    '  <link rel="icon" type="image/x-icon" href="favicon.ico">\n'
    '  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">\n'
    '  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">'
)

if 'favicon.ico' not in b_code:
    b_code = b_code.replace('</head>', f'{fav_tags_mjs}\n</head>')
    with open('tools/build-collection.mjs', 'w', encoding='utf-8') as fh:
        fh.write(b_code)
    print('Updated tools/build-collection.mjs with favicon tags!')

print('Favicon injection complete!')
