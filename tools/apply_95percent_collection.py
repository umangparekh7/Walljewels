import re

# 1. Update styles.css
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

coll_styles = """/* ==========================================================================
   COLLECTION PAGE ONLY (Minimal Left/Right Padding, Strict 7-Columns, Hero Overlay)
   ========================================================================== */

body.page-collection {
  --frame: 0px !important;
}

body.page-collection #main {
  width: 100% !important;
  max-width: 100% !important;
  padding-inline: clamp(12px, 1.8vw, 28px) !important;
  box-sizing: border-box !important;
  margin: 0 auto !important;
}

body.page-collection .coll-hero {
  position: relative !important;
  width: 100% !important;
  max-width: 100% !important;
  min-height: 360px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #05060a !important;
  overflow: hidden !important;
  border: 1px solid rgba(207, 161, 78, 0.3) !important;
  border-radius: 12px !important;
  margin-top: 14px !important;
  margin-bottom: 0 !important;
  padding: clamp(48px, 6vw, 84px) 20px clamp(32px, 4vw, 56px) !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65) !important;
  text-align: center !important;
}

body.page-collection .coll-hero__fireworks {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  pointer-events: none !important;
  z-index: 1 !important;
}

body.page-collection .coll-hero__content {
  position: relative !important;
  z-index: 2 !important;
  max-width: 760px !important;
  margin: 0 auto !important;
  text-align: center !important;
  pointer-events: auto !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

body.page-collection .coll-hero .d2 {
  font-family: var(--f-display) !important;
  font-size: clamp(2.2rem, 3.6vw, 3.2rem) !important;
  font-weight: 400 !important;
  color: #ffffff !important;
  margin: 0 0 12px !important;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.8) !important;
}

body.page-collection .coll-hero .lead {
  font-size: clamp(13.5px, 1.1vw, 15.5px) !important;
  line-height: 1.55 !important;
  color: var(--night-soft, #cfc9b8) !important;
  max-width: 62ch !important;
  margin: 0 auto !important;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.85) !important;
}

body.page-collection .coll-filters {
  position: sticky !important;
  top: var(--header-h) !important;
  z-index: 80 !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 14px 0 !important;
  background: rgba(20, 16, 12, 0.96) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(207, 161, 78, 0.25) !important;
  border-radius: 10px !important;
  padding: 10px clamp(10px, 1.2vw, 18px) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
}

body.page-collection .coll-filters__in {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 8px !important;
  width: 100% !important;
}

body.page-collection .coll-main-section {
  width: 100% !important;
  max-width: 100% !important;
  padding: 0 0 60px 0 !important;
  margin: 0 !important;
}

body.page-collection .coll-grid {
  display: grid !important;
  grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
  gap: clamp(6px, 0.75vw, 12px) !important;
  width: 100% !important;
  padding-block: 6px 32px !important;
  margin: 0 !important;
}

@media (max-width: 1100px) {
  body.page-collection .coll-grid {
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 780px) {
  body.page-collection .coll-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 480px) {
  body.page-collection .coll-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 6px !important;
  }
}
"""

if "body.page-collection" in css:
    css = re.sub(r'/\* ===+\s*COLLECTION PAGE ONLY.*', coll_styles + '\n', css, flags=re.DOTALL)
else:
    css += "\n" + coll_styles

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated styles.css with minimal side padding on #main and 7-column layout!")
