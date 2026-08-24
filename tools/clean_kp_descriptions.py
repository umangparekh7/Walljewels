import json
import re

with open('assets/js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Common word boundary fixes for OCR text
fixes = [
    (r'deepmeditation', 'deep meditation'),
    (r'inspirationfrom', 'inspiration from'),
    (r'cinematicrealism', 'cinematic realism'),
    (r'therugged', 'the rugged'),
    (r'Renderedindeep', 'Rendered in deep'),
    (r'atmospherictones', 'atmospheric tones'),
    (r'overwhelmingthemoderninterior', 'overwhelming the modern interior'),
    (r'iconographythrough', 'iconography through'),
    (r'contemporarylens', 'contemporary lens'),
    (r'dancingShivawithina', 'dancing Shiva within a'),
    (r'swirling,abstractcosmic', 'swirling, abstract cosmic'),
    (r'geometry,the', 'geometry, the'),
    (r'celestialtheatre', 'celestial theatre'),
    (r'throughsweepingcelestialcurves', 'through sweeping celestial curves'),
    (r'motion\.The', 'motion. The'),
    (r'backdropallowstheexplosivecopperand', 'backdrop allows the explosive copper and'),
    (r'saffronmetallictexturestovisuallyleapfrom', 'saffron metallic textures to visually leap from'),
    (r'designedforspacesthatdemand', 'designed for spaces that demand'),
    (r'drawinginspirationfrom', 'drawing inspiration from'),
    (r'sacredgeometry', 'sacred geometry'),
    (r'bas-relief', 'bas-relief'),
    (r'architecturaldepth', 'architectural depth'),
    (r'photorealistictextures', 'photorealistic textures'),
    (r'visualabsorbing', 'visually absorbing'),
    (r'deeplysophisticated', 'deeply sophisticated'),
    (r'theevokes', 'it evokes'),
    (r'Theartwork', 'The artwork'),
    (r'thepiecetransformsthe', 'the piece transforms the'),
    (r'windowlooking', 'window looking'),
    (r'timeless,idyllic', 'timeless, idyllic'),
    (r'restfulspaces', 'restful spaces'),
    (r'modernarchitecture', 'modern architecture'),
    (r'Thisintricate3Ddesignconstructsavisual', 'This intricate 3D design constructs a visual'),
    (r'interlocking,angular', 'interlocking, angular'),
    (r'polished antiquebrassplay', 'polished antique brass play'),
    (r'youmovethrough', 'you move through'),
    (r'Thishyper-realistic3Dwallpaper', 'This hyper-realistic 3D wallpaper'),
    (r'createsanastonishingoptical', 'creates an astonishing optical'),
    (r'flowing sculptural', 'flowing sculptural'),
    (r'carveddirectlyinto', 'carved directly into'),
    (r'mattestonetextures,combinedwithperfectly', 'matte stone textures, combined with perfectly'),
    (r'Abreathtaking,gallery-level', 'A breathtaking, gallery-level'),
    (r'3Drenderingtechniquestocreatethe', '3D rendering techniques to create the'),
    (r'sophisticatedtaste\.An', 'sophisticated taste. An')
]

for orig, repl in fixes:
    content = re.sub(orig, repl, content)

with open('assets/js/data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Polished all description texts in data.js!")
