import shutil
from PIL import Image

src = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\8f6b1326-946c-4c7a-9e67-edec7a411650\ganesha_geometry_living_room_1787591041830.jpg"
dst = r"c:\Users\Chintan Kamani\Desktop\WJWP New Website-Table\walljewels-site\assets\img\collection\kala-rasa\kr-plate-023.jpg"

img = Image.open(src)
img.save(dst, quality=95)
print("Updated kr-plate-023.jpg with luxury living room render!")
