import re

# 1. Update styles.css
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

coll_styles = """/* ==========================================================================
   COLLECTION PAGE ONLY (95% Screen Width, 7-Columns, Fireworks Behind Hero)
   ========================================================================== */

body.page-collection {
  --frame: 2.5vw !important;
}

body.page-collection .coll-hero {
  position: relative !important;
  width: min(95vw, 95%) !important;
  max-width: 95% !important;
  min-height: 380px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #05060a !important;
  overflow: hidden !important;
  padding: clamp(56px, 7vw, 96px) clamp(20px, 3vw, 48px) clamp(36px, 4.5vw, 60px) !important;
  text-align: center !important;
  border: 1px solid rgba(207, 161, 78, 0.35) !important;
  border-radius: 16px !important;
  margin: 18px auto 0 !important;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.75) !important;
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
  max-width: 780px !important;
  margin: 0 auto !important;
  text-align: center !important;
  pointer-events: auto !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  -webkit-backdrop-filter: none !important;
  backdrop-filter: none !important;
}

body.page-collection .coll-hero .d2 {
  font-family: var(--f-display) !important;
  font-size: clamp(2.2rem, 3.8vw, 3.2rem) !important;
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
  width: min(95vw, 95%) !important;
  max-width: 95% !important;
  margin: 16px auto !important;
  background: rgba(20, 16, 12, 0.96) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(207, 161, 78, 0.28) !important;
  border-radius: 12px !important;
  padding: 10px clamp(12px, 1.8vw, 24px) !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6) !important;
}

body.page-collection .coll-filters__in {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 10px !important;
  width: 100% !important;
  max-width: 100% !important;
}

body.page-collection .coll-main-section {
  width: min(95vw, 95%) !important;
  max-width: 95% !important;
  margin: 0 auto !important;
  padding: 0 0 60px 0 !important;
}

body.page-collection .coll-grid {
  display: grid !important;
  grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
  gap: clamp(8px, 1vw, 14px) !important;
  width: 100% !important;
  padding-block: 8px 36px !important;
  margin: 0 !important;
}

@media (max-width: 1180px) {
  body.page-collection .coll-grid {
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 820px) {
  body.page-collection .coll-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 520px) {
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

print("Updated styles.css with 95% width layout and fireworks direct overlay!")
