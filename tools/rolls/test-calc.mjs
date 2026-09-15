// Unit tests for the pure half of assets/js/rolls.js (SPEC §3, §5).
// Run from the site root:  node --test tools/rolls/test-calc.mjs
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const rolls = require(path.join(here, '..', '..', 'assets', 'js', 'rolls.js'));
const { calculate, formatINR, formatArea, slugify, sortDesigns, matchesQuery, parseDimension } = rolls;

const ATHENIC = { id: 'athenic-india', slug: 'athenic-india', name: 'Athenic India', rollSize: 54, coverage: 45, pricePerSqFt: 55, rollPrice: 2970 };
const PLAIN = { id: 'plain', slug: 'plain', name: 'Plain', rollSize: 57, coverage: 50, pricePerSqFt: 25, rollPrice: 1425 };

describe('module shape', () => {
  test('exposes the five contract functions', () => {
    for (const fn of ['calculate', 'formatINR', 'slugify', 'sortDesigns', 'matchesQuery']) {
      assert.equal(typeof rolls[fn], 'function', `${fn} is exported`);
    }
  });
  test('does not touch the DOM when required in node', () => {
    assert.equal(typeof globalThis.document, 'undefined');
    assert.equal(typeof globalThis.WJRolls, 'object');
  });
});

describe('calculate — SPEC reference cases', () => {
  test('120 × 108 → 90 sq.ft', () => {
    const r = calculate(120, 108, ATHENIC);
    assert.equal(r.ok, true);
    assert.equal(r.area, 90);
  });
  test('120 × 108 Athenic → 2 rolls, ₹5,940', () => {
    const r = calculate(120, 108, ATHENIC);
    assert.equal(r.rolls, 2);
    assert.equal(r.cost, 5940);
    assert.equal(formatINR(r.cost), '₹5,940');
  });
  test('120 × 108 Plain → 2 rolls, ₹2,850', () => {
    const r = calculate(120, 108, PLAIN);
    assert.equal(r.rolls, 2);
    assert.equal(r.cost, 2850);
    assert.equal(formatINR(r.cost), '₹2,850');
  });
  test('100 sq.ft Athenic → 3 rolls, ₹8,910 (rounds up)', () => {
    const r = calculate(120, 120, ATHENIC); // 14400 / 144 = 100
    assert.equal(r.area, 100);
    assert.equal(r.rolls, 3);
    assert.equal(r.cost, 8910);
    assert.equal(formatINR(r.cost), '₹8,910');
  });
  test('135 × 48 Athenic (45 sq.ft) → exactly 1 roll', () => {
    const r = calculate(135, 48, ATHENIC);
    assert.equal(r.area, 45);
    assert.equal(r.rolls, 1);
    assert.equal(r.cost, 2970);
  });
});

describe('calculate — rounding and exact multiples', () => {
  test('90 / 45 = exactly 2 (no floating-point creep to 3)', () => {
    assert.equal(calculate(120, 108, ATHENIC).rolls, 2);
  });
  test('100 / 50 = exactly 2 for Plain', () => {
    assert.equal(calculate(120, 120, PLAIN).rolls, 2);
  });
  test('a hair over one roll rounds up to two', () => {
    const r = calculate(135.1, 48, ATHENIC); // 45.03 sq.ft
    assert.equal(r.rolls, 2);
  });
  test('exact multiple computed through non-terminating decimals stays exact', () => {
    // 0.3 sq.ft-ish increments: 36 in × 1.2 in = 43.2 sq.in = 0.3 sq.ft; coverage 0.3 → 1 roll
    const r = calculate(36, 1.2, { coverage: 0.3, rollPrice: 10 });
    assert.equal(r.rolls, 1);
  });
  test('accepts string inputs from form fields', () => {
    const r = calculate('120', '108', ATHENIC);
    assert.equal(r.ok, true);
    assert.equal(r.rolls, 2);
  });
  test('decimals: 120.5 × 108.25', () => {
    const r = calculate(120.5, 108.25, ATHENIC);
    assert.equal(r.ok, true);
    assert.ok(Math.abs(r.area - 90.5842) < 0.001);
    assert.equal(formatArea(r.area), '90.58');
    assert.equal(r.rolls, 3);
    assert.equal(r.cost, 8910);
  });
  test('cost uses rollPrice, never rollSize', () => {
    const r = calculate(120, 108, { ...ATHENIC, rollSize: 999 });
    assert.equal(r.rolls, 2);
    assert.equal(r.cost, 5940);
  });
});

describe('calculate — invalid input never yields a result', () => {
  const bad = [
    ['empty width', '', 108, 'width', 'Enter a wall width in inches'],
    ['empty height', 120, '', 'height', 'Enter a wall height in inches'],
    ['whitespace width', '   ', 108, 'width', 'Enter a wall width in inches'],
    ['undefined width', undefined, 108, 'width', 'Enter a wall width in inches'],
    ['null height', 120, null, 'height', 'Enter a wall height in inches'],
    ['zero', 0, 108, 'width', 'Enter a value between 1 and 2400'],
    ['negative', 120, -5, 'height', 'Enter a value between 1 and 2400'],
    ['NaN', NaN, 108, 'width', 'Enter a value between 1 and 2400'],
    ['text', 'abc', 108, 'width', 'Enter a value between 1 and 2400'],
    ['over 2400', 2401, 108, 'width', 'Enter a value between 1 and 2400'],
    ['Infinity', Infinity, 108, 'width', 'Enter a value between 1 and 2400']
  ];
  for (const [label, w, h, field, message] of bad) {
    test(`${label} → ok:false with a quiet message`, () => {
      const r = calculate(w, h, ATHENIC);
      assert.equal(r.ok, false);
      assert.equal(r.field, field);
      assert.equal(r.error, message);
      assert.equal('rolls' in r, false);
    });
  }
  test('2400 is the inclusive maximum', () => {
    assert.equal(calculate(2400, 2400, ATHENIC).ok, true);
  });
  test('missing or unusable collection → ok:false', () => {
    assert.equal(calculate(120, 108, null).ok, false);
    assert.equal(calculate(120, 108, {}).ok, false);
    assert.equal(calculate(120, 108, { coverage: 0, rollPrice: 100 }).ok, false);
    assert.equal(calculate(120, 108, { coverage: 45 }).ok, false);
    assert.equal(calculate(120, 108, null).error, 'Choose a collection');
  });
  test('parseDimension mirrors the field rules', () => {
    assert.equal(parseDimension('120.5', 'width').value, 120.5);
    assert.equal(parseDimension('', 'height').error, 'Enter a wall height in inches');
    assert.equal(parseDimension('0', 'height').error, 'Enter a value between 1 and 2400');
  });
});

describe('formatINR — en-IN grouping, no decimals', () => {
  test('₹5,940', () => assert.equal(formatINR(5940), '₹5,940'));
  test('₹2,970', () => assert.equal(formatINR(2970), '₹2,970'));
  test('₹1,42,500', () => assert.equal(formatINR(142500), '₹1,42,500'));
  test('₹55 (no grouping under 1,000)', () => assert.equal(formatINR(55), '₹55'));
  test('₹0', () => assert.equal(formatINR(0), '₹0'));
  test('₹10,00,000', () => assert.equal(formatINR(1000000), '₹10,00,000'));
  test('₹12,34,56,789', () => assert.equal(formatINR(123456789), '₹12,34,56,789'));
  test('rounds to whole rupees', () => assert.equal(formatINR(2849.6), '₹2,850'));
  test('accepts numeric strings', () => assert.equal(formatINR('1425'), '₹1,425'));
  test('never prints NaN', () => {
    assert.equal(formatINR(NaN).includes('NaN'), false);
    assert.equal(formatINR(undefined).includes('NaN'), false);
    assert.equal(formatINR('abc').includes('NaN'), false);
  });
});

describe('formatArea — up to two decimals', () => {
  test('90 → "90"', () => assert.equal(formatArea(90), '90'));
  test('90.0833 → "90.08"', () => assert.equal(formatArea(90.0833), '90.08'));
  test('45.5 → "45.5"', () => assert.equal(formatArea(45.5), '45.5'));
  test('NaN → "—"', () => assert.equal(formatArea(NaN), '—'));
});

describe('slugify', () => {
  test("'6877/2' → '6877-2'", () => assert.equal(slugify('6877/2'), '6877-2'));
  test("' 12 ' → '12'", () => assert.equal(slugify(' 12 '), '12'));
  test('lower-cases and collapses runs', () => assert.equal(slugify('ATHENIC  India / 2026'), 'athenic-india-2026'));
  test('trims leading and trailing dashes', () => assert.equal(slugify('--a--'), 'a'));
  test('tolerates non-strings', () => {
    assert.equal(slugify(12), '12');
    assert.equal(slugify(null), '');
    assert.equal(slugify(undefined), '');
  });
});

describe('sortDesigns — numeric-aware', () => {
  const d = (designNumber, id) => ({ designNumber, id: id || `x:${designNumber}` });
  test('2 sorts before 10', () => {
    const out = sortDesigns([d('10'), d('2'), d('1')]).map((x) => x.designNumber);
    assert.deepEqual(out, ['1', '2', '10']);
  });
  test("'5314/9' sorts before '5314/10'", () => {
    const out = sortDesigns([d('5314/10'), d('5314/9'), d('5314/1')]).map((x) => x.designNumber);
    assert.deepEqual(out, ['5314/1', '5314/9', '5314/10']);
  });
  test('mixed catalogue numbers', () => {
    const out = sortDesigns([d('14156'), d('6877/2'), d('11224'), d('6877/10'), d('12')]).map((x) => x.designNumber);
    assert.deepEqual(out, ['12', '6877/2', '6877/10', '11224', '14156']);
  });
  test('returns a new array and leaves the input untouched', () => {
    const input = [d('3'), d('1')];
    const out = sortDesigns(input);
    assert.notEqual(out, input);
    assert.deepEqual(input.map((x) => x.designNumber), ['3', '1']);
  });
  test('tolerates missing numbers and non-arrays', () => {
    assert.deepEqual(sortDesigns(null), []);
    assert.equal(sortDesigns([{ id: 'a' }, d('1')]).length, 2);
  });
});

describe('matchesQuery — normalisation and ranking', () => {
  const D = (n) => ({ designNumber: n });
  test("'6877-2' matches '6877/2'", () => assert.ok(matchesQuery(D('6877/2'), '6877-2')));
  test("'14 156' matches '14156'", () => assert.ok(matchesQuery(D('14156'), '14 156')));
  test("'6877.2' and ' 6877 / 2 ' match too", () => {
    assert.ok(matchesQuery(D('6877/2'), '6877.2'));
    assert.ok(matchesQuery(D('6877/2'), ' 6877 / 2 '));
  });
  test('case-insensitive', () => assert.ok(matchesQuery(D('AB12'), 'ab12')));
  test('no match is falsy', () => assert.equal(matchesQuery(D('14156'), '99'), 0));
  test('empty query matches everything', () => assert.ok(matchesQuery(D('12'), '')));
  test('exact ranks above prefix above contains', () => {
    const exact = matchesQuery(D('12'), '12');
    const prefix = matchesQuery(D('1234'), '12');
    const contains = matchesQuery(D('4125'), '12');
    assert.ok(exact > prefix, 'exact > prefix');
    assert.ok(prefix > contains, 'prefix > contains');
    assert.ok(contains > 0, 'contains matches');
  });
  test('tolerates missing designNumber', () => {
    assert.equal(matchesQuery({}, '12'), 0);
    assert.equal(matchesQuery(null, '12'), 0);
  });
});
