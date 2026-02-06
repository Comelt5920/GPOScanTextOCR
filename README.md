# ScanTextOCR

A Python-based OCR tool that monitors a specific region of the screen for target text and sends notifications to Discord.

## Features

- **Real-time monitoring:** Uses OCR (Tesseract) to scan screen areas.
- **Easy Selection:** Custom scan area selection tool built-in.
- **Visual Feedback:** Live vision preview in the GUI.
- **Discord Alerts:** Sends notifications with screenshots and character matches.
- **Customizable:** Adjustable intervals, cooldowns, and message text.

## Prerequisites

- **Python 3.x**
- **Tesseract OCR:** Must be installed on your system. [Download here](https://github.com/tesseract-ocr/tesseract).

## Installation

### Option 1: Download ZIP (easiest for non-Git users)
1. Download the code as a ZIP file from: [Click here to download](https://github.com/Comelt5920/GPOScanTextOCR/archive/refs/heads/main.zip)
2. Extract the ZIP file to a folder on your computer.
3. Open a terminal (CMD or PowerShell) in that folder.

### Option 2: Using Git
```bash
git clone https://github.com/Comelt5920/GPOScanTextOCR.git
cd GPOScanTextOCR
```

## Setup & Dependencies

1. **Install dependencies:**
   ```bash
   pip install requests pyautogui pytesseract pillow
   ```

2. **Run the script:**
   ```bash
   python FruitNoti.py
   ```

## Usage

1. **Setup Tesseract:** Point the "Tesseract Path" to your `tesseract.exe` (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`).
2. **Setup Discord:** Enter your **Discord Webhook URL**.
3. **Choose Area:** Click **Select Scan Area** to highlight the part of the screen to monitor.
4. **Start:** Click **START SCANNER**.

## Configuration

The application saves settings to `config.json`. 
> [!NOTE]
> `config.json` is ignored by Git to prevent leaking your private Webhook URLs.

## License

MIT