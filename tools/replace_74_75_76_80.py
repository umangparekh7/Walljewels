from PIL import Image

uploads = {
    # 74: Rama and Sita
    'assets/img/collection/kala-rasa/kr-plate-012.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666693613.png",
    # 75: Lakshmi Abundance
    'assets/img/collection/kala-rasa/kr-plate-013.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666727362.png",
    # 76: Saraswati Wisdom and Art
    'assets/img/collection/kala-rasa/kr-plate-014.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666757115.png",
    # 80: Hanuman Unyielding Devotion
    'assets/img/collection/kala-rasa/kr-plate-018.jpg': r"C:\Users\Chintan Kamani\.gemini\antigravity-ide\brain\99a8f198-e31a-4099-b444-928a9a1ef591\.user_uploaded\media_1787666923452.png"
}

for dest, src in uploads.items():
    img = Image.open(src).convert('RGB')
    img.save(dest, 'JPEG', quality=95)
    print(f"Saved {dest} from {src} ({img.size})")

print("All 4 images replaced successfully!")
