/* =============================================================
   Wall Jewels Wallpaper World — collection data
   -------------------------------------------------------------
   PHASE 2: replace `img` with your own photographs.
   Drop files into  assets/img/collection/  and set e.g.
   img: 'assets/img/collection/buddha-3d.jpg'
   Everything else on the site updates automatically.
   `tone` drives the woven fallback swatch if an image is missing.
   ============================================================= */

/* `in` is the grammatical form used in headings: "<Theme> for <in>" */
const ROOMS = [
  { id: 'living',   label: 'Living Room',      in: 'the living room',      note: 'Statement walls for the room everyone sees.' },
  { id: 'bedroom',  label: 'Bedroom',          in: 'the bedroom',          note: 'Quiet texture, soft light, restful colour.' },
  { id: 'pooja',    label: 'Pooja Room',       in: 'the pooja room',       note: 'Divine motifs, brass tones, gentle glow.' },
  { id: 'kids',     label: 'Kids & Nursery',   in: 'kids’ rooms',          note: 'Superheroes, space, jungle — safe inks.' },
  { id: 'office',   label: 'Office',           in: 'the office',           note: 'Brand walls and quiet focus zones.' },
  { id: 'school',   label: 'School & Campus',  in: 'schools & campuses',   note: 'Learning walls that teach all day.' },
  { id: 'balcony',  label: 'Balcony & Outdoor',in: 'balconies & outdoors', note: 'Vertical gardens, turf, weatherable finishes.' },
  { id: 'flooring', label: 'Flooring',         in: 'flooring',             note: 'Vinyl, wooden, SPC and sports surfaces.' }
];

const THEMES = [
  { id: '3d',       label: '3D & Depth' },
  { id: 'deities',  label: 'Indian Deities' },
  { id: 'nature',   label: 'Nature & Landscape' },
  { id: 'animal',   label: 'Animal Kingdom' },
  { id: 'beach',    label: 'Beach & Coastal' },
  { id: 'space',    label: 'Outer Space' },
  { id: 'texture',  label: 'Marble & Texture' },
  { id: 'floral',   label: 'Floral & Botanical' },
  { id: 'heroes',   label: 'Superheroes & Cartoons' },
  { id: 'custom',   label: 'Your Own Photograph' }
];

const U = (id, w) => `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${w || 900}&q=72`;

const COLLECTION = [
  // ---------- LIVING ROOM ----------
  { t: 'Calacatta Gold',        room: 'living',  theme: 'texture', blurb: 'Book-matched marble veining, printed seamless across the full wall.', img: U('1615874959474-d609969a20ed'), tone: ['#EDE6DA','#BFA46F'], tag: 'Bestseller' },
  { t: 'Ink & Gold Flow',       room: 'living',  theme: 'texture', blurb: 'Abstract alcohol-ink marbling with metallic gold rivers.',            img: U('1618221195710-dd6b41faaea6'), tone: ['#1B2436','#C9A24B'] },
  { t: 'Botanical Luxe',        room: 'living',  theme: 'floral',  blurb: 'Oversized banana leaf in deep emerald on a warm ground.',             img: U('1512428813834-c702c7702b78'), tone: ['#1E3A2B','#7FA86A'] },
  { t: 'Facet',                 room: 'living',  theme: '3d',      blurb: 'Low-poly relief that catches cove lighting from every angle.',        img: U('1618220179428-22790b461013'), tone: ['#D8D2C8','#8C8377'], tag: 'New' },
  { t: 'Raw Concrete',          room: 'living',  theme: 'texture', blurb: 'Micro-cement finish — the loft look without the loft.',               img: U('1600607687939-ce8a6c25118c'), tone: ['#B8B3AC','#6E6862'] },
  { t: 'Cherry Blossom Branch', room: 'living',  theme: 'floral',  blurb: 'Hand-painted chinoiserie, scaled to your exact wall.',                img: U('1616486338812-3dadae4b4ace'), tone: ['#F2E4DC','#C98897'] },
  { t: 'Noir Marquina',         room: 'living',  theme: 'texture', blurb: 'Black marble with lightning-white veins. Drama, controlled.',         img: U('1600566753086-00f18fb6b3ea'), tone: ['#141312','#C9BFA8'] },
  { t: 'Highland Panorama',     room: 'living',  theme: 'nature',  blurb: 'A single continuous vista — no repeat, no seams.',                    img: U('1441974231531-c6227db76b6e'), tone: ['#2E3B33','#9FB4A1'] },

  // ---------- BEDROOM ----------
  { t: 'Golden Eleaves',        room: 'bedroom', theme: 'floral',  blurb: 'Brushed-gold foliage on charcoal. Reads as art at night.',            img: U('1616594039964-ae9021a400a0'), tone: ['#191A18','#C79A45'], tag: 'Bestseller' },
  { t: 'Soft Bloom Mural',      room: 'bedroom', theme: 'floral',  blurb: 'Watercolour peonies fading into bare plaster.',                       img: U('1522708323590-d24dbb6b0267'), tone: ['#F5E9E6','#D6A7AC'] },
  { t: 'Linen Weave',           room: 'bedroom', theme: 'texture', blurb: 'Real fabric scanned at 1200dpi. You can almost feel it.',             img: U('1505693416388-ac5ce068fe85'), tone: ['#E6DCCB','#A3907A'] },
  { t: 'Misty Ridge',           room: 'bedroom', theme: 'nature',  blurb: 'Layered hills in ten greys — the calmest wall we sell.',              img: U('1470071459604-3b5ec3a7fe05'), tone: ['#C6CCCB','#5C6A6B'] },
  { t: 'Nordic Fluting',        room: 'bedroom', theme: '3d',      blurb: 'Vertical reeded panel effect. Makes low ceilings taller.',            img: U('1615529182904-14819c35db37'), tone: ['#E3D9CC','#9D8C79'] },
  { t: 'Indigo Terrazzo',       room: 'bedroom', theme: 'texture', blurb: 'Fine chip terrazzo, muted enough to sleep beside.',                   img: U('1567016432779-094069958ea5'), tone: ['#2A3550','#B7BFCE'] },

  // ---------- POOJA ROOM ----------
  { t: 'Om Mandala',            room: 'pooja',   theme: 'deities', blurb: 'Fine-line mandala with a raised gold Om at the centre.',              img: null, tone: ['#F3E7CE','#B08A3E'], tag: 'Bestseller' },
  { t: 'Krishna Bansuri',       room: 'pooja',   theme: 'deities', blurb: 'Line-art Krishna with peacock feather, on dark slate.',               img: U('1609619385002-f40f1df9b7eb'), tone: ['#1C1A19','#CBA45C'] },
  { t: 'Lakshmi Kamal',         room: 'pooja',   theme: 'deities', blurb: 'Goddess Lakshmi on a lotus, framed by hanging bells.',                img: null, tone: ['#F6EBD8','#C0863A'] },
  { t: 'Temple Arch',           room: 'pooja',   theme: '3d',      blurb: 'Carved sandstone arch that gives a flat niche real depth.',           img: U('1590077428593-a55bb07c4665'), tone: ['#EFE3D2','#A78551'] },
  { t: 'Tulsi Vine',            room: 'pooja',   theme: 'floral',  blurb: 'Delicate trailing tulsi in gold leaf on ivory.',                      img: U('1519681393784-d120267933ba'), tone: ['#F7F1E4','#9F8A4E'] },
  { t: 'Ganesha Relief',        room: 'pooja',   theme: 'deities', blurb: '3D stone-relief Ganesha, printed with true shadow depth.',            img: null, tone: ['#E8DCC6','#94703C'] },

  // ---------- KIDS ----------
  { t: 'Wall-Break Superhero',  room: 'kids',    theme: 'heroes',  blurb: 'The famous smashed-through-the-wall effect. Kids lose their minds.',  img: U('1608889175123-8ee362201f81'), tone: ['#C6262E','#1B3A8C'], tag: 'Most requested' },
  { t: 'Rocket Bay',            room: 'kids',    theme: 'space',   blurb: 'Astronaut, shuttle and Earthrise across a full wall.',                img: U('1446776877081-d282a0f896e2'), tone: ['#0B1533','#4C7BD1'] },
  { t: 'Jungle Friends',        room: 'kids',    theme: 'animal',  blurb: 'Soft-illustrated elephants, giraffes and monkeys.',                   img: U('1503919545889-aef636e10ad4'), tone: ['#DDEAD1','#6E9A55'] },
  { t: 'Dinosaur Valley',       room: 'kids',    theme: 'animal',  blurb: 'Friendly dinos in a painterly prehistoric landscape.',                img: U('1519659528534-7fd733a832a0'), tone: ['#D7E3C8','#5C7A44'] },
  { t: 'Solar System Chart',    room: 'kids',    theme: 'space',   blurb: 'Labelled planets — decoration that quietly teaches.',                 img: U('1451187580459-43490279c0fa'), tone: ['#0A1026','#D08A3C'] },
  { t: 'Racing Circuit',        room: 'kids',    theme: 'heroes',  blurb: 'Track lines and pit-lane graphics for a car-mad room.',               img: U('1503376780353-7e6692767b70'), tone: ['#1A1A1D','#D93A2B'] },

  // ---------- OFFICE ----------
  { t: 'Focus · Plan · Execute',room: 'office',  theme: 'custom',  blurb: 'Typographic wall in your brand colours and typeface.',                img: U('1497366216548-37526070297c'), tone: ['#111C2E','#D9A441'], tag: 'Custom' },
  { t: 'World Map, Line Drawn', room: 'office',  theme: 'custom',  blurb: 'Minimal continents — a boardroom classic done properly.',             img: U('1524661135-423995f22d0b'), tone: ['#EDE7DB','#5B5347'] },
  { t: 'Circuit Grid',          room: 'office',  theme: '3d',      blurb: 'Backlit circuitry for tech floors and demo rooms.',                   img: U('1518770660439-4636190af475'), tone: ['#08151E','#2FA8C7'] },
  { t: 'Acoustic Felt Lines',   room: 'office',  theme: 'texture', blurb: 'Vertical felt-look battens. Warm, quiet, professional.',              img: U('1497215728101-856f4ea42174'), tone: ['#3A3B35','#9AA08D'] },
  { t: 'Reception Stone',       room: 'office',  theme: 'texture', blurb: 'Large-format travertine for the wall behind your logo.',              img: U('1524758631624-e2822e304c36'), tone: ['#E4D9C7','#9E8C72'] },

  // ---------- SCHOOL ----------
  { t: 'Alphabet Wall',         room: 'school',  theme: 'custom',  blurb: 'A–Z with illustrated objects, scaled for small eyes.',                img: U('1503676260728-1c00da094a0b'), tone: ['#FDF6E8','#3E7CB1'] },
  { t: 'Multiplication Tables', room: 'school',  theme: 'custom',  blurb: 'Colour-coded tables 1–10. Permanent, wipe-clean revision.',           img: U('1509062522246-3755977927d7'), tone: ['#F3F6FA','#C8574B'] },
  { t: 'The Scientific Method', room: 'school',  theme: 'custom',  blurb: 'Six-step process wall for labs and STEM rooms.',                      img: U('1532094349884-543bc11b234d'), tone: ['#EAF2F4','#2E7D8A'] },
  { t: 'World Map for Kids',    room: 'school',  theme: 'custom',  blurb: 'Animals, landmarks and oceans across the corridor.',                  img: U('1526778548025-fa2f459cd5c1'), tone: ['#DFF0F4','#4E9AA8'] },
  { t: 'History Timeline',      room: 'school',  theme: 'custom',  blurb: 'From Indus Valley to today, along one long wall.',                    img: U('1461360370896-922624d12aa1'), tone: ['#F1EADC','#8A6A3A'] },

  // ---------- BALCONY ----------
  { t: 'Vertical Garden',       room: 'balcony', theme: 'nature',  blurb: 'Artificial green wall panels — no watering, no fading.',              img: U('1466692476868-aef1dfb1e735'), tone: ['#294B2E','#7CB262'], tag: 'Popular' },
  { t: 'Turf & Deck',           room: 'balcony', theme: 'nature',  blurb: 'Grass turf with interlocking wood tiles.',                            img: U('1416879595882-3373a0480b5b'), tone: ['#3F6B35','#8B6239'] },
  { t: 'Sea Cave Vista',        room: 'balcony', theme: 'beach',   blurb: 'A framed ocean view where there isn\'t one.',                         img: U('1507525428034-b723cf961d3e'), tone: ['#CFE4E8','#2E7C8E'] },
  { t: 'Weathered Teak',        room: 'balcony', theme: 'texture', blurb: 'Sun-bleached plank cladding, UV-stable print.',                       img: U('1503387762-592deb58ef4e'), tone: ['#C9B396','#7A6248'] },

  // ---------- FLOORING ----------
  { t: 'Pergo Oak Natural',     room: 'flooring',theme: 'texture', blurb: 'Authorised Pergo wooden flooring. Click-lock, 25-yr class.',          img: U('1595428774223-ef52624120d2'), tone: ['#D6B98C','#8A6740'], tag: 'Authorised dealer' },
  { t: 'SPC Stone Grey',        room: 'flooring',theme: 'texture', blurb: 'Rigid-core SPC — waterproof, kid-proof, quiet underfoot.',            img: U('1493809842364-78817add7ffb'), tone: ['#BFC0BC','#6C6E6B'] },
  { t: 'Vinyl Herringbone',     room: 'flooring',theme: 'texture', blurb: 'Classic parquet pattern in 2mm commercial vinyl.',                    img: U('1615529162924-f8605388461d'), tone: ['#C6A57B','#7C5E3A'] },
  { t: 'Sports Court',          room: 'flooring',theme: 'custom',  blurb: 'Multi-game line marking for schools and clubs.',                      img: U('1546519638-68e109498ffc'), tone: ['#B4562E','#2C4E7A'] }
];

/* Marquee clients — straight from the company profile */
const CLIENTS = [
  'Superstar Rajinikanth’s Residence', 'Apollo Hospitals', 'Indian Railways',
  'Palazzo · Vijaya Forum Mall', 'Express Avenue Mall', 'DLF Commander’s Court',
  'Casa Grande Corporate Office', 'MGR Engineering College', 'Ashpra Interiors',
  'Design DNA Architects', 'Soul Garden Bistro', 'Lotus Service Apartments',
  'Jeppiaar Engineering College', 'ACS Medical College', 'Akshayah International School'
];

const MYTHS = [
  { m: 'Wallpaper doesn’t last.',              f: 'Ours comfortably runs 10 years and beyond. We have walls from 2012 still on our books.' },
  { m: 'It’s impossible to keep clean.',       f: 'Stain marks wipe off with a damp cloth. Most of our range is scrubbable vinyl.' },
  { m: 'Wallpaper is expensive.',              f: 'Rates start at ₹22 per sq.ft — materials and fixing included.' },
  { m: 'Installation takes days.',             f: 'Four hours. That’s 400 sq.ft, cleared and finished, by a two-man crew.' },
  { m: 'It won’t stick on damp walls.',        f: 'It will — provided there is no active leakage. We check before we quote.' },
  { m: 'Wallpaper is a fire risk.',            f: 'Our materials are fire-retardant grade, which is why hospitals and malls use them.' }
];
