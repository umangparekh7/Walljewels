import glob
import os

GA_SNIPPET = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y6B7GHF42V"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-Y6B7GHF42V');
  </script>
"""

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = glob.glob(os.path.join(root, '**/*.html'), recursive=True)
    
    updated = []
    for fpath in sorted(html_files):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'G-Y6B7GHF42V' in content:
            print(f"Skipping (already contains gtag): {os.path.relpath(fpath, root)}")
            continue
        
        if '<head>' in content:
            new_content = content.replace('<head>\n', '<head>\n' + GA_SNIPPET, 1)
            if new_content == content:
                new_content = content.replace('<head>', '<head>\n' + GA_SNIPPET, 1)
            
            with open(fpath, 'w', encoding='utf-8', newline='') as f:
                f.write(new_content)
            updated.append(os.path.relpath(fpath, root))
    
    print(f"Updated {len(updated)} files with Google Analytics gtag.js:")
    for u in updated:
        print(f"  + {u}")

if __name__ == '__main__':
    main()
