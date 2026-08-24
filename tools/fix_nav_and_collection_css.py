import re

with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Fix .nav a styles: clean, refined luxury typography
nav_old = r'''\.nav a \{
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: clamp\(96px, 6\.2vw, 114px\);
  height: 32px;
  padding: 0 4px;
  border-radius: 20px;
  font-size: 11\.5px;
  font-weight: 600;
  letter-spacing: \.03em;
  text-align: center;
  white-space: nowrap;
  text-decoration: none;
  background: linear-gradient\(135deg, #d4a753 0%, #b88628 100%\);
  border: 1px solid #e6c47f;
  color: #120e08 !important;
  box-shadow: 0 3px 12px rgba\(184, 134, 40, 0\.35\), inset 0 1px 1px rgba\(255, 255, 255, 0\.4\);
  transition: all 0\.25s cubic-bezier\(0\.19, 1, 0\.22, 1\);
\}
\.nav a:hover \{
  background: linear-gradient\(135deg, #e6be6a 0%, #c99632 100%\);
  border-color: #f7dda4;
  color: #0b0906 !important;
  transform: translateY\(-1\.5px\);
  box-shadow: 0 6px 18px rgba\(207, 161, 78, 0\.5\), 0 0 12px rgba\(230, 196, 127, 0\.35\);
\}
\.nav a\[aria-current="page"\] \{
  background: linear-gradient\(135deg, #f0c976 0%, #d4a13d 100%\);
  border: 1\.5px solid #fff2c4;
  color: #0b0906 !important;
  font-weight: 700;
  transform: translateY\(-1px\);
  box-shadow: 0 4px 16px rgba\(207, 161, 78, 0\.55\), inset 0 1px 2px rgba\(255, 255, 255, 0\.6\);
\}'''

nav_new = '''.nav a {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--ink-soft, #cfc9b8) !important;
  text-decoration: none;
  background: transparent;
  border: 1px solid transparent;
  box-shadow: none;
  transition: all 0.2s ease;
}
.nav a:hover {
  color: var(--gold-bright, #e6c47f) !important;
  background: rgba(207, 161, 78, 0.1);
  border-color: rgba(207, 161, 78, 0.25);
  transform: translateY(-1px);
}
.nav a[aria-current="page"] {
  color: var(--gold-bright, #e6c47f) !important;
  font-weight: 600;
  background: rgba(207, 161, 78, 0.15);
  border-color: var(--gold, #cfa14e);
}'''

css = re.sub(nav_old, nav_new, css)

# 2. Append collection styles if missing
coll_styles = '''
/* ---------- 29. Collection page & Filter Bar ---------- */
.coll-hero {
  position: relative;
  padding-block: clamp(48px, 6.5vw, 90px) clamp(28px, 3.5vw, 48px);
  background: radial-gradient(ellipse at 50% 30%, rgba(26, 20, 14, 0.95) 0%, rgba(14, 11, 8, 0.98) 100%);
  border-bottom: 1px solid var(--hairline);
  text-align: center;
}
.coll-hero .wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.coll-hero .headgroup {
  max-width: 680px;
  text-align: center;
  margin-inline: auto;
}

.coll-filters {
  position: sticky;
  top: calc(var(--header-h) + var(--bar-h));
  z-index: 80;
  background: rgba(18, 14, 10, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--hairline);
  padding-block: 12px;
}
.coll-filters__in {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
}
.fgroup {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}
.fgroup + .fgroup {
  margin-left: 14px;
  padding-left: 14px;
  border-left: 1px solid var(--hairline);
}
.fchip {
  font-family: var(--f-text);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--ink-soft, #cfc9b8);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--hairline-2);
  border-radius: 4px;
  padding: 6px 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all var(--beat) var(--ease);
}
.fchip .mark {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--gold);
  transform: scale(0);
  transition: transform var(--beat) var(--ease);
}
.fchip:hover {
  color: #ffffff;
  border-color: var(--gold-bright);
  background: rgba(207, 161, 78, 0.12);
}
.fchip.is-active,
.fchip[aria-pressed="true"] {
  color: #ffffff;
  border-color: var(--gold);
  background: rgba(207, 161, 78, 0.22);
  box-shadow: 0 0 12px rgba(207, 161, 78, 0.2);
}
.fchip.is-active .mark,
.fchip[aria-pressed="true"] .mark {
  transform: scale(1);
}
.coll-count {
  margin-left: auto;
  font-size: 12px;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--gold-bright, #e6c47f);
  font-weight: 600;
}

.coll-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: clamp(16px, 2vw, 28px);
  padding-block: clamp(36px, 4.5vw, 60px);
}
.coll-grid .plate {
  position: relative;
  background: rgba(22, 17, 12, 0.88);
  border: 1px solid var(--hairline);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform var(--beat) var(--ease), border-color var(--beat) var(--ease), box-shadow var(--beat) var(--ease);
}
.coll-grid .plate:hover {
  transform: translateY(-4px);
  border-color: rgba(207, 161, 78, 0.45);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(207, 161, 78, 0.15);
}
.coll-grid .plate__media {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #090806;
  overflow: hidden;
}
.coll-grid .plate__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform var(--beat-slow) var(--ease);
  cursor: zoom-in;
}
.coll-grid .plate:hover .plate__media img {
  transform: scale(1.04);
}
.plate__tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(14, 11, 8, 0.88);
  border: 1px solid rgba(207, 161, 78, 0.4);
  color: var(--gold-bright, #e6c47f);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 3px;
  backdrop-filter: blur(8px);
}
.plate__body {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.plate__vol {
  font-size: 10.5px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--gold, #cfa14e);
  font-weight: 600;
  margin-bottom: 4px;
}
.plate__name {
  font-family: var(--f-display);
  font-size: 1.15rem;
  color: #ffffff;
  margin-bottom: 4px;
  line-height: 1.25;
}
.plate__sub {
  font-size: 0.82rem;
  color: var(--gold-bright, #e6c47f);
  margin-bottom: 6px;
  font-weight: 500;
}
.plate__blurb {
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--ink-soft, #cfc9b8);
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}
.plate__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--hairline);
  padding-top: 12px;
  margin-top: auto;
}
.plate__view {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--gold-bright, #e6c47f);
  text-decoration: none;
  transition: color var(--beat) var(--ease);
}
.plate__view:hover {
  color: #ffffff;
}
.coll-empty {
  text-align: center;
  padding-block: 80px;
  color: var(--ink-dim);
  font-size: 1.1rem;
}
'''

if '.coll-hero' not in css:
    css += coll_styles

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated assets/css/styles.css with clean luxury nav and collection styling!")
