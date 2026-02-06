# ScanTextOCR

A Python-based OCR tool that monitors a specific region of the screen for target text and sends notifications to Discord.

## Features
- Real-time screen monitoring using OCR (Tesseract).
- Custom scan area selection.
- Live vision preview.
- Discord notification with screenshots.
- Configurable interval and cooldown.
- Custom Discord message support.

## Prerequisites
- Python 3.x
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ScanTextOCR.git
   cd ScanTextOCR
   ```
2. Install dependencies:
   ```bash
   pip install requests pyautogui pytesseract pillow
   ```

## Usage
1. Run the script:
   ```bash
   python FruitNoti.py
   ```
2. Set the **Tesseract Path** to your local installation (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. Enter your **Discord Webhook URL**.
4. Use **Select Scan Area** to choose the region of the screen you want to monitor.
5. Click **START SCANNER**.

## Configuration
The application saves its settings to `config.json`. This file is ignored by Git to protect your private webhook URL.

## License
MIT
