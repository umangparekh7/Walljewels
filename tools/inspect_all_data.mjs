import { readFileSync } from 'node:fs';

const dataSrc = readFileSync('assets/js/data.js', 'utf8');
const ctx = {};
new Function(`${dataSrc}; this.VOLUMES=VOLUMES; this.COLLECTION=COLLECTION;`).call(ctx);
const { COLLECTION } = ctx;

console.log(`Total items in COLLECTION: ${COLLECTION.length}`);
const kp = COLLECTION.filter(d => d.v === 'kala-parampara');
const kr = COLLECTION.filter(d => d.v === 'kala-rasa');

console.log(`\n=== KALA PARAMPARA (${kp.length} items) ===`);
kp.forEach((d, i) => {
  console.log(`${i+1}. [${d.id}] ${d.no} | "${d.n}" | sub: "${d.sub || ''}" | img: ${d.img}`);
});

console.log(`\n=== KALA RASA (${kr.length} items) ===`);
kr.forEach((d, i) => {
  console.log(`${i+1}. [${d.id}] ${d.no} | "${d.n}" | sub: "${d.sub || ''}" | img: ${d.img}`);
});
