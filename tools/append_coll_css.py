with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

coll_styles = '''
/* ---------- 33. The Collection Page Layout & Filter Bar ---------- */
.coll-hero {
  position: relative;
  padding-top: clamp(52px, 7vw, 92px);
  padding-bottom: clamp(32px, 4vw, 52px);
  background: radial-gradient(ellipse at 50% 35%, rgba(26, 20, 14, 0.96) 0%, rgba(14, 11, 8, 0.99) 100%);
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
  margin-inline: auto;
  text-align: center;
  position: relative;
  z-index: 2;
}

.coll-filters {
  position: sticky;
  top: calc(var(--header-h) + var(--bar-h));
  z-index: 90;
  background: rgba(16, 12, 9, 0.97);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--hairline);
  padding-block: 14px;
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
  background: rgba(255, 255, 255, 0.05);
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
  background: rgba(22, 17, 12, 0.92);
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

if '/* ---------- 33. The Collection Page Layout' not in css:
    css += '\n' + coll_styles

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Appended Collection Page styles to styles.css!')
