import { readFileSync } from 'node:fs';

function checkFile(path) {
  console.log(`\n========================================\nChecking: ${path}\n========================================`);
  const content = readFileSync(path, 'utf8');

  // Check Schema
  const schemaRegex = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi;
  let match;
  let count = 0;
  while ((match = schemaRegex.exec(content)) !== null) {
    count++;
    try {
      const parsed = JSON.parse(match[1].trim());
      console.log(`✅ Schema Block ${count} JSON is valid!`);
      if (parsed['@graph']) {
        console.log(`   Found ${parsed['@graph'].length} graph nodes:`);
        parsed['@graph'].forEach((item) => {
          console.log(`     • ${item['@type']} -> ${item.name || item['@id'] || item.url || ''}`);
        });
      }
    } catch (e) {
      console.error(`❌ JSON Syntax Error in block ${count}:`, e.message);
    }
  }

  // Check Canonical
  const canon = content.match(/<link rel="canonical" href="([^"]+)">/i);
  console.log(`Canonical: ${canon ? '✅ ' + canon[1] : '❌ Missing'}`);

  // Check OG
  const ogTitle = content.match(/<meta property="og:title" content="([^"]+)">/i);
  console.log(`OG Title: ${ogTitle ? '✅ ' + ogTitle[1] : '❌ Missing'}`);

  // Check Twitter
  const twCard = content.match(/<meta name="twitter:card" content="([^"]+)">/i);
  console.log(`Twitter Card: ${twCard ? '✅ ' + twCard[1] : '❌ Missing'}`);
}

checkFile('index.html');
checkFile('collection.html');
console.log('\nAll SEO and JSON-LD checks finished successfully!');
