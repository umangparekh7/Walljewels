from PIL import Image

replacements = {
    # 93: Chola Temple Chronicles
    'assets/img/collection/kala-rasa/kr-plate-039.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668028041.png",
    # 94: Gopuram Grandeur
    'assets/img/collection/kala-rasa/kr-plate-040.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668053989.png",
    # 95: Bronze and Lotus
    'assets/img/collection/kala-rasa/kr-plate-041.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668075023.png",
    # 96: Thanjavur Golden Garden
    'assets/img/collection/kala-rasa/kr-plate-042.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668099319.png",
    # 98: Dravidian Stone Stories
    'assets/img/collection/kala-rasa/kr-plate-044.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668128091.png"
}

for dest, src in replacements.items():
    img = Image.open(src).convert('RGB')
    img.save(dest, 'JPEG', quality=95)
    print(f"Replaced {dest} ({img.size})")

print("All 5 images replaced successfully!")
