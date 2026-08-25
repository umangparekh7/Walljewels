from PIL import Image

replacements = {
    # 100: Mandala of Madurai
    'assets/img/collection/kala-rasa/kr-plate-046.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668213843.png",
    # 101: Chettinad Heritage
    'assets/img/collection/kala-rasa/kr-plate-047.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668246431.png",
    # 102: Mysore Palace Reverie
    'assets/img/collection/kala-rasa/kr-plate-048.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668271692.png",
    # 103: Hampi in the Monsoon
    'assets/img/collection/kala-rasa/kr-plate-049.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668293537.png",
    # 104: Deccan Palace Garden
    'assets/img/collection/kala-rasa/kr-plate-050.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787668315287.png"
}

for dest, src in replacements.items():
    img = Image.open(src).convert('RGB')
    img.save(dest, 'JPEG', quality=95)
    print(f"Replaced {dest} ({img.size})")

print("All 5 images (100-104) replaced successfully!")
