# FruitNoti OCR Bot 🍎

A simple and powerful tool that watches your screen and sends a Discord notification whenever specific text (like "has spawned") appears.

---

## ✨ Features
- **Smart Screen Watcher**: Tell it where to look, and it will scan that area.
- **Discord Integration**: Sends a screenshot and the detected text directly to your channel.
- **Easy to Use**: Simple GUI for selecting scan areas and setting cooldowns.
- **Privacy Focus**: Your Discord webhooks are stored safely on your machine.

---

## 🚀 How to Use

1. **Install Tesseract OCR**:
   - Download: [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
   - Install it to the default path: `C:\Program Files\Tesseract-OCR`

2. **Run the Program**:
   - Open `FruitNoti.py` (or run the EXE if you have one).

3. **Setup on Screen**:
   - **Tesseract Path**: Make sure it points to `tesseract.exe`.
   - **Webhook URL**: Paste your Discord Webhook URL.
   - **Select Area**: Click "Select Scan Area" and draw a box over the text you want to watch.
   - **Target Text**: Type the text you are looking for (e.g., `spawned`).

4. **Start**: Click **▶ START SCANNER**.

---

## 📦 Building your own EXE (Bundled)

> [!TIP]
> **Recommended:** Download the pre-built version from the **[Releases](https://github.com/Comelt5920/GPOScanTextOCR/releases)** section. It is already optimized and has a much smaller file size.

If you want to create your own EXE (Note: The file might be very large unless you manually clean the Tesseract-OCR folder as I have):

1. Copy your `C:\Program Files\Tesseract-OCR` folder into this project folder.
2. Open your terminal in this folder.
3. Run this command:
   ```bash
   pyinstaller FruitNoti.spec
   ```
4. Find your ready-to-use program in the `dist` folder!

---

## ⚠️ Privacy & Security
- **`config.json`**: This file contains your private Discord Webhook. It is excluded from Git to keep your information safe.
- **`config.json.template`**: A sample file showing how the settings look.

---

## License
MIT