import re

# 1. Update build-collection.mjs
with open('tools/build-collection.mjs', 'r', encoding='utf-8') as f:
    bjs = f.read()

# Replace body tag with class="page-collection"
bjs = bjs.replace('<body>', '<body class="page-collection">')

# Replace the hero and grid markup structure
hero_grid_replacement = """  <main id="main">
    <section class="coll-hero">
      <canvas class="coll-hero__fireworks" id="coll-fireworks-canvas" aria-hidden="true"></canvas>
      <div class="coll-hero__content">
        <div class="threshold" data-kolam="gate"><span class="rule"></span></div>
        <div class="headgroup">
          <h1 class="d2">The collection</h1>
          <p class="lead">${COLLECTION.length} master plates from the Wall Jewels volumes — every one recomposed, recoloured
            and printed to your wall's exact measure. No prices here by design: a wall deserves a conversation,
            and the conversation is free.</p>
        </div>
      </div>
    </section>

    <div class="coll-filters">
      <div class="coll-filters__in">
        <div class="fgroup" role="group" aria-label="Filter by volume">
          <button class="fchip is-active" type="button" data-filter="all" aria-pressed="true"><span class="mark"></span>All Volumes</button>
${volChips}
        </div>
        <div class="fgroup" role="group" aria-label="Filter by category">
${catChips}
        </div>
        <div class="fgroup" role="group" aria-label="Filter by space">
${spaceChips}
        </div>
        <span class="coll-count" data-coll-count>${COLLECTION.length} designs</span>
      </div>
    </div>

    <section class="coll-main-section" aria-label="All designs">
      <div class="coll-grid" data-coll-grid>
${plates}
      </div>
      <p class="coll-empty" style="display:none">Nothing answers that combination yet — loosen a filter, or
        <a href="https://wa.me/919677042903" rel="noopener">WhatsApp us</a>; if it exists, we can print it.</p>
    </section>"""

bjs = re.sub(r'  <main id="main">.*?    <section class="finale"', hero_grid_replacement + '\n\n    <section class="finale"', bjs, flags=re.DOTALL)

with open('tools/build-collection.mjs', 'w', encoding='utf-8') as f:
    f.write(bjs)

print("Updated build-collection.mjs with clean unboxed markup!")

# 2. Update styles.css with perfect full-width styling
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

coll_styles = """/* ==========================================================================
   COLLECTION PAGE ONLY (Full Width 7-Column Layout & Fireworks Behind Hero)
   ========================================================================== */

body.page-collection {
  --frame: 0px !important;
}

body.page-collection .coll-hero {
  position: relative;
  width: 100% !important;
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #05060a !important;
  overflow: hidden;
  padding: clamp(64px, 8vw, 110px) clamp(16px, 3vw, 40px) clamp(38px, 5vw, 64px);
  text-align: center;
  border-bottom: 1px solid var(--hairline);
  margin: 0 !important;
}

body.page-collection .coll-hero__fireworks {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  pointer-events: none !important;
  z-index: 1 !important;
}

body.page-collection .coll-hero__content {
  position: relative !important;
  z-index: 2 !important;
  max-width: 820px !important;
  margin-inline: auto !important;
  text-align: center !important;
  pointer-events: auto !important;
}

body.page-collection .coll-hero .d2 {
  font-family: var(--f-display);
  font-size: clamp(2.2rem, 4vw, 3.4rem);
  font-weight: 400;
  color: #ffffff;
  margin: 0 0 14px;
}

body.page-collection .coll-hero .lead {
  font-size: clamp(14px, 1.1vw, 16px);
  line-height: 1.55;
  color: var(--night-soft, #cfc9b8);
  max-width: 64ch;
  margin: 0 auto;
}

body.page-collection .coll-filters {
  position: sticky;
  top: var(--header-h);
  z-index: 80;
  width: 100% !important;
  background: rgba(20, 16, 12, 0.96) !important;
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
  border-block: 1px solid rgba(207, 161, 78, 0.22);
  padding: 12px clamp(16px, 2.5vw, 40px) !important;
  margin: 0 !important;
}

body.page-collection .coll-filters__in {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  width: 100% !important;
  max-width: 100% !important;
}

body.page-collection .coll-main-section {
  width: 100% !important;
  padding: 16px clamp(16px, 2.5vw, 40px) 60px !important;
  margin: 0 !important;
}

body.page-collection .coll-grid {
  display: grid !important;
  grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
  gap: clamp(8px, 1vw, 16px) !important;
  width: 100% !important;
  padding-block: 16px 36px !important;
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
    css = re.sub(r'/\* ===+\s*COLLECTION PAGE ONLY.*?(?=/\* ---------- 32\. Catalogue viewer)', coll_styles + '\n', css, flags=re.DOTALL)
else:
    css += "\n" + coll_styles

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated styles.css with body.page-collection scoped full-width rules!")
