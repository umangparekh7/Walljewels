from PIL import Image

f1 = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666602723.png"
f2 = r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666640681.png"

im1 = Image.open(f1)
im2 = Image.open(f2)

print(f"Image 1: format={im1.format}, size={im1.size}, mode={im1.mode}")
print(f"Image 2: format={im2.format}, size={im2.size}, mode={im2.mode}")
