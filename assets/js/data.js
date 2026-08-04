/* =============================================================
   Wall Jewels Wallpaper World — collection data
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

const W1 = 'assets/Wallpapers/wallpaper-collection-1.jpg';
const W2 = 'assets/Wallpapers/wallpaper-collection-2.jpg';
const W3 = 'assets/Wallpapers/wallpaper-collection-3.jpg';
const W4 = 'assets/Wallpapers/wallpaper-collection-4.jpg';

const COLLECTION = [
  // ---------- LIVING ROOM ----------
  { t: 'Calacatta Gold',        room: 'living',  theme: 'texture', blurb: 'Book-matched marble veining, printed seamless across the full wall.', img: W1, tone: ['#EDE6DA','#BFA46F'], tag: 'Bestseller' },
  { t: 'Ink & Gold Flow',       room: 'living',  theme: 'texture', blurb: 'Abstract alcohol-ink marbling with metallic gold rivers.',            img: W2, tone: ['#1B2436','#C9A24B'] },
  { t: 'Botanical Luxe',        room: 'living',  theme: 'floral',  blurb: 'Oversized banana leaf in deep emerald on a warm ground.',             img: W3, tone: ['#1E3A2B','#7FA86A'] },
  { t: 'Facet',                 room: 'living',  theme: '3d',      blurb: 'Low-poly relief that catches cove lighting from every angle.',        img: W4, tone: ['#D8D2C8','#8C8377'], tag: 'New' },
  { t: 'Raw Concrete',          room: 'living',  theme: 'texture', blurb: 'Micro-cement finish — the loft look without the loft.',               img: W1, tone: ['#B8B3AC','#6E6862'] },
  { t: 'Cherry Blossom Branch', room: 'living',  theme: 'floral',  blurb: 'Hand-painted chinoiserie, scaled to your exact wall.',                img: W3, tone: ['#F2E4DC','#C98897'] },
  { t: 'Noir Marquina',         room: 'living',  theme: 'texture', blurb: 'Black marble with lightning-white veins. Drama, controlled.',         img: W2, tone: ['#141312','#C9BFA8'] },
  { t: 'Highland Panorama',     room: 'living',  theme: 'nature',  blurb: 'A single continuous vista — no repeat, no seams.',                    img: W4, tone: ['#2E3B33','#9FB4A1'] },

  // ---------- BEDROOM ----------
  { t: 'Golden Eleaves',        room: 'bedroom', theme: 'floral',  blurb: 'Brushed-gold foliage on charcoal. Reads as art at night.',            img: W2, tone: ['#191A18','#C79A45'], tag: 'Bestseller' },
  { t: 'Soft Bloom Mural',      room: 'bedroom', theme: 'floral',  blurb: 'Watercolour peonies fading into bare plaster.',                       img: W3, tone: ['#F5E9E6','#D6A7AC'] },
  { t: 'Linen Weave',           room: 'bedroom', theme: 'texture', blurb: 'Real fabric scanned at 1200dpi. You can almost feel it.',             img: W1, tone: ['#E6DCCB','#A3907A'] },
  { t: 'Misty Ridge',           room: 'bedroom', theme: 'nature',  blurb: 'Layered hills in ten greys — the calmest wall we sell.',              img: W4, tone: ['#C6CCCB','#5C6A6B'] },
  { t: 'Nordic Fluting',        room: 'bedroom', theme: '3d',      blurb: 'Vertical reeded panel effect. Makes low ceilings taller.',            img: W1, tone: ['#E3D9CC','#9D8C79'] },
  { t: 'Indigo Terrazzo',       room: 'bedroom', theme: 'texture', blurb: 'Fine chip terrazzo, muted enough to sleep beside.',                   img: W2, tone: ['#2A3550','#B7BFCE'] },

  // ---------- POOJA ROOM ----------
  { t: 'Om Mandala',            room: 'pooja',   theme: 'deities', blurb: 'Fine-line mandala with a raised gold Om at the centre.',              img: W1, tone: ['#F3E7CE','#B08A3E'], tag: 'Bestseller' },
  { t: 'Krishna Bansuri',       room: 'pooja',   theme: 'deities', blurb: 'Line-art Krishna with peacock feather, on dark slate.',               img: W2, tone: ['#1C1A19','#CBA45C'] },
  { t: 'Lakshmi Kamal',         room: 'pooja',   theme: 'deities', blurb: 'Goddess Lakshmi on a lotus, framed by hanging bells.',                img: W3, tone: ['#F6EBD8','#C0863A'] },
  { t: 'Temple Arch',           room: 'pooja',   theme: '3d',      blurb: 'Carved sandstone arch that gives a flat niche real depth.',           img: W4, tone: ['#EFE3D2','#A78551'] },
  { t: 'Tulsi Vine',            room: 'pooja',   theme: 'floral',  blurb: 'Delicate trailing tulsi in gold leaf on ivory.',                      img: W3, tone: ['#F7F1E4','#9F8A4E'] },
  { t: 'Ganesha Relief',        room: 'pooja',   theme: 'deities', blurb: '3D stone-relief Ganesha, printed with true shadow depth.',            img: W4, tone: ['#E8DCC6','#94703C'] },

  // ---------- KIDS ----------
  { t: 'Wall-Break Superhero',  room: 'kids',    theme: 'heroes',  blurb: 'The famous smashed-through-the-wall effect. Kids lose their minds.',  img: W1, tone: ['#C6262E','#1B3A8C'], tag: 'Most requested' },
  { t: 'Rocket Bay',            room: 'kids',    theme: 'space',   blurb: 'Astronaut, shuttle and Earthrise across a full wall.',                img: W2, tone: ['#0B1533','#4C7BD1'] },
  { t: 'Jungle Friends',        room: 'kids',    theme: 'animal',  blurb: 'Soft-illustrated elephants, giraffes and monkeys.',                   img: W3, tone: ['#DDEAD1','#6E9A55'] },
  { t: 'Dinosaur Valley',       room: 'kids',    theme: 'animal',  blurb: 'Friendly dinos in a painterly prehistoric landscape.',                img: W4, tone: ['#D7E3C8','#5C7A44'] },
  { t: 'Solar System Chart',    room: 'kids',    theme: 'space',   blurb: 'Labelled planets — decoration that quietly teaches.',                 img: W2, tone: ['#0A1026','#D08A3C'] },
  { t: 'Racing Circuit',        room: 'kids',    theme: 'heroes',  blurb: 'Track lines and pit-lane graphics for a car-mad room.',               img: W1, tone: ['#1A1A1D','#D93A2B'] },

  // ---------- OFFICE ----------
  { t: 'Focus · Plan · Execute',room: 'office',  theme: 'custom',  blurb: 'Typographic wall in your brand colours and typeface.',                img: W1, tone: ['#111C2E','#D9A441'], tag: 'Custom' },
  { t: 'World Map, Line Drawn', room: 'office',  theme: 'custom',  blurb: 'Minimal continents — a boardroom classic done properly.',             img: W2, tone: ['#EDE7DB','#5B5347'] },
  { t: 'Circuit Grid',          room: 'office',  theme: '3d',      blurb: 'Backlit circuitry for tech floors and demo rooms.',                   img: W3, tone: ['#08151E','#2FA8C7'] },
  { t: 'Acoustic Felt Lines',   room: 'office',  theme: 'texture', blurb: 'Vertical felt-look battens. Warm, quiet, professional.',              img: W4, tone: ['#3A3B35','#9AA08D'] },
  { t: 'Reception Stone',       room: 'office',  theme: 'texture', blurb: 'Large-format travertine for the wall behind your logo.',              img: W1, tone: ['#E4D9C7','#9E8C72'] },

  // ---------- SCHOOL ----------
  { t: 'Alphabet Wall',         room: 'school',  theme: 'custom',  blurb: 'A–Z with illustrated objects, scaled for small eyes.',                img: W3, tone: ['#FDF6E8','#3E7CB1'] },
  { t: 'Multiplication Tables', room: 'school',  theme: 'custom',  blurb: 'Colour-coded tables 1–10. Permanent, wipe-clean revision.',           img: W2, tone: ['#F3F6FA','#C8574B'] },
  { t: 'The Scientific Method', room: 'school',  theme: 'custom',  blurb: 'Six-step process wall for labs and STEM rooms.',                      img: W4, tone: ['#EAF2F4','#2E7D8A'] },
  { t: 'World Map for Kids',    room: 'school',  theme: 'custom',  blurb: 'Animals, landmarks and oceans across the corridor.',                  img: W1, tone: ['#DFF0F4','#4E9AA8'] },
  { t: 'History Timeline',      room: 'school',  theme: 'custom',  blurb: 'From Indus Valley to today, along one long wall.',                    img: W2, tone: ['#F1EADC','#8A6A3A'] },

  // ---------- BALCONY ----------
  { t: 'Vertical Garden',       room: 'balcony', theme: 'nature',  blurb: 'Artificial green wall panels — no watering, no fading.',              img: W3, tone: ['#294B2E','#7CB262'], tag: 'Popular' },
  { t: 'Turf & Deck',           room: 'balcony', theme: 'nature',  blurb: 'Grass turf with interlocking wood tiles.',                            img: W4, tone: ['#3F6B35','#8B6239'] },
  { t: 'Sea Cave Vista',        room: 'balcony', theme: 'beach',   blurb: 'A framed ocean view where there isn\'t one.',                         img: W1, tone: ['#CFE4E8','#2E7C8E'] },
  { t: 'Weathered Teak',        room: 'balcony', theme: 'texture', blurb: 'Sun-bleached plank cladding, UV-stable print.',                       img: W2, tone: ['#C9B396','#7A6248'] },

  // ---------- FLOORING ----------
  { t: 'Pergo Oak Natural',     room: 'flooring',theme: 'texture', blurb: 'Authorised Pergo wooden flooring. Click-lock, 25-yr class.',          img: W1, tone: ['#D6B98C','#8A6740'], tag: 'Authorised dealer' },
  { t: 'SPC Stone Grey',        room: 'flooring',theme: 'texture', blurb: 'Rigid-core SPC — waterproof, kid-proof, quiet underfoot.',            img: W2, tone: ['#BFC0BC','#6C6E6B'] },
  { t: 'Vinyl Herringbone',     room: 'flooring',theme: 'texture', blurb: 'Classic parquet pattern in 2mm commercial vinyl.',                    img: W3, tone: ['#C6A57B','#7C5E3A'] },
  { t: 'Sports Court',          room: 'flooring',theme: 'custom',  blurb: 'Multi-game line marking for schools and clubs.',                      img: W4, tone: ['#B4562E','#2C4E7A'] }
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
