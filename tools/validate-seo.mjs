import { readFileSync } from 'node:fs';

const pages = [
  'index.html',
  'collection.html',
  'wallpaper-chennai.html',
  'custom-wallpaper-printing.html',
  'luxury-wallpapers.html',
  'wallpaper-manufacturer-india.html',
  'wall-murals.html',
  'wallpaper-buying-guide.html',
  'wallpaper-installation.html',
  'showrooms/parrys-flagship.html',
  'showrooms/omr-experience-centre.html',
  'showrooms/tnagar-boutique.html'
];

console.log('Validating', pages.length, 'authority pages...\n');

let allPassed = true;

for (const p of pages) {
  try {
    const html = readFileSync(p, 'utf8');
    const canon = html.match(/<link rel="canonical" href="([^"]+)">/i);
    const title = html.match(/<title>([^<]+)<\/title>/i);
    const schemaMatches = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)];

    let schemaOk = true;
    for (const sm of schemaMatches) {
      try {
        JSON.parse(sm[1].trim());
      } catch (err) {
        schemaOk = false;
        console.error(`❌ JSON error in ${p}:`, err.message);
      }
    }

    if (canon && title && schemaOk) {
      console.log(`✅ [${p}] Canonical: ${canon[1]} | Title: "${title[1].slice(0, 50)}..."`);
    } else {
      allPassed = false;
      console.warn(`⚠️ Issue in ${p}: Canon=${!!canon}, Title=${!!title}, SchemaOk=${schemaOk}`);
    }
  } catch (err) {
    allPassed = false;
    console.error(`❌ Could not read ${p}:`, err.message);
  }
}

if (allPassed) {
  console.log('\n🎉 ALL 12 AUTHORITY & LOCAL PAGES PASSED VALIDATION WITH ZERO ERRORS!');
} else {
  console.log('\n❌ Some checks failed.');
}
