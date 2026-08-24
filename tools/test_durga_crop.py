from PIL import Image

img = Image.open('scratch/raw_kr_16.jpg')
w, h = img.size

# Durga and the niche is from x=280 to x=1660 in 2867 width
crop1 = img.crop((int(w * 0.18), 0, int(w * 0.60), h))
crop1.save('scratch/durga_test_crop.jpg')
print("Saved Durga test crop")
