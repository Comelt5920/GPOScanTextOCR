import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import json
import os
import requests
import pyautogui
import pytesseract
from PIL import Image, ImageTk
import io

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

class SelectionOverlay:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.5)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="cross")
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='#00FF00', width=3)

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(self.start_x - end_x)
        height = abs(self.start_y - end_y)
        
        self.root.destroy()
        if width > 5 and height > 5:
            self.callback((left, top, width, height))

class FruitNotiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FruitNoti OCR Bot")
        self.geometry("500x800")
        self.resizable(False, False)
        
        self.is_running = False
        self.scan_thread = None
        self.show_vision = tk.BooleanVar(value=True)
        self.vision_img = None
        self.last_notification_time = 0
        self.always_on_top_var = tk.BooleanVar(value=False)
        
        # Default Config
        self.config = {
            "tesseract_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            "webhook_url": "",
            "scan_region": [0, 0, 500, 200],
            "target_text": "has spawned",
            "interval": 2.0,
            "cooldown": 60,
            "always_on_top": False,
            "custom_message": "<@[uridhere]>"
        }
        self.load_config()
        
        self.create_widgets()
        pytesseract.pytesseract.tesseract_cmd = self.config["tesseract_path"]

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Styling for the buttons
        style = ttk.Style()
        style.configure("Start.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        style.configure("Stop.TButton", font=("Segoe UI", 12, "bold"), padding=10)

        # Buttons (Pack first to dock at bottom)
        self.btn_toggle = ttk.Button(main_frame, text="▶ START SCANNER", command=self.toggle_scanner, style="Start.TButton")
        self.btn_toggle.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Tesseract Path
        ttk.Label(main_frame, text="Tesseract Path:").pack(anchor="w")
        self.tess_entry = ttk.Entry(main_frame, width=60)
        self.tess_entry.insert(0, self.config["tesseract_path"])
        self.tess_entry.pack(fill="x", pady=(0, 10))
        
        # Webhook URL
        ttk.Label(main_frame, text="Discord Webhook URL:").pack(anchor="w")
        self.webhook_entry = ttk.Entry(main_frame, width=60)
        self.webhook_entry.insert(0, self.config["webhook_url"])
        self.webhook_entry.pack(fill="x", pady=(0, 10))
        
        # Target Text
        ttk.Label(main_frame, text="Target Text to Find:").pack(anchor="w")
        self.target_entry = ttk.Entry(main_frame, width=60)
        self.target_entry.insert(0, self.config["target_text"])
        self.target_entry.pack(fill="x", pady=(0, 10))

        # Custom Message
        ttk.Label(main_frame, text="Discord Message Text:").pack(anchor="w")
        self.message_entry = ttk.Entry(main_frame, width=60)
        self.message_entry.insert(0, self.config.get("custom_message", "🚨 **Detection Alert!**"))
        self.message_entry.pack(fill="x", pady=(0, 10))
        
        # Region info
        ttk.Label(main_frame, text="Scan Region (x, y, w, h):").pack(anchor="w")
        self.region_label = ttk.Label(main_frame, text=str(self.config["scan_region"]), foreground="blue")
        self.region_label.pack(anchor="w", pady=(0, 5))
        
        ttk.Button(main_frame, text="Select Scan Area", command=self.select_area).pack(pady=(0, 10))
        
        # Vision Area
        vision_frame = ttk.LabelFrame(main_frame, text="Vision Preview")
        vision_frame.pack(fill="x", pady=(0, 10))
        
        self.vision_canvas = tk.Canvas(vision_frame, height=100, bg="black", highlightthickness=0)
        self.vision_canvas.pack(fill="x", padx=5, pady=5)
        
        self.vision_toggle = ttk.Checkbutton(vision_frame, text="Show Live Vision", variable=self.show_vision)
        self.vision_toggle.pack(anchor="w", padx=5, pady=(0, 5))
        
        # Settings (Interval/Cooldown)
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill="x", pady=10)
        
        ttk.Label(settings_frame, text="Interval (s):").grid(row=0, column=0, sticky="w")
        self.interval_entry = ttk.Entry(settings_frame, width=10)
        self.interval_entry.insert(0, str(self.config["interval"]))
        self.interval_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(settings_frame, text="Cooldown (s):").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.cooldown_entry = ttk.Entry(settings_frame, width=10)
        self.cooldown_entry.insert(0, str(self.config["cooldown"]))
        self.cooldown_entry.grid(row=0, column=3, padx=5)
        
        self.topmost_check = ttk.Checkbutton(settings_frame, text="Always on Top", 
                                             variable=self.always_on_top_var, command=self.update_topmost)
        self.topmost_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
        
        # Status Log
        ttk.Label(main_frame, text="Log:").pack(anchor="w", pady=(10, 0))
        self.log_text = tk.Text(main_frame, height=12, state="disabled", font=("Consolas", 9), bg="#f0f0f0")
        self.log_text.pack(fill="both", expand=True, pady=5)
        
        

    def log(self, message):
        self.log_text.config(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_text.insert("end", timestamp + message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def select_area(self):
        self.withdraw()
        # Small delay to ensure main window is hidden before selection starts
        self.after(200, lambda: SelectionOverlay(self.on_area_selected))

    def on_area_selected(self, region):
        self.config["scan_region"] = region
        self.region_label.config(text=f"X: {region[0]}, Y: {region[1]}, W: {region[2]}, H: {region[3]}")
        self.deiconify()
        self.log(f"New scan area set: {region}")
        # Clear previous vision preview
        self.vision_canvas.delete("all")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config.update(json.load(f))
            except Exception as e:
                self.log(f"[!] Error loading config: {e}")
        
        # Apply loaded settings
        self.always_on_top_var.set(self.config.get("always_on_top", False))
        self.update_topmost()

    def save_config(self):
        try:
            self.config["tesseract_path"] = self.tess_entry.get()
            self.config["webhook_url"] = self.webhook_entry.get()
            self.config["target_text"] = self.target_entry.get()
            self.config["custom_message"] = self.message_entry.get()
            self.config["interval"] = float(self.interval_entry.get())
            self.config["cooldown"] = int(self.cooldown_entry.get())
            self.config["always_on_top"] = self.always_on_top_var.get()
            
            # Validate Tesseract path
            if self.config["tesseract_path"] and not os.path.exists(self.config["tesseract_path"]):
                messagebox.showwarning("Warning", f"Tesseract not found at: {self.config['tesseract_path']}")
            
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=4)
            
            pytesseract.pytesseract.tesseract_cmd = self.config["tesseract_path"]
            self.log("Config saved successfully.")
        except ValueError as e:
            messagebox.showerror("Error", f"Interval and Cooldown must be numbers. Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def send_to_discord(self, image, text_found):
        try:
            if not self.config["webhook_url"]:
                self.log("[!] Discord webhook URL is empty")
                return
                
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            msg = self.config.get("custom_message", "🚨 **Detection Alert!**")
            payload = {"content": f"{msg}\nDetected: `{text_found}`"}
            files = {"file": ("screenshot.png", img_byte_arr, "image/png")}
            response = requests.post(self.config["webhook_url"], data=payload, files=files, timeout=10)
            if response.status_code == 204:
                self.log("[✓] Notification sent to Discord!")
            else:
                self.log(f"[!] Discord returned status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.log(f"[!] Network Error: {e}")
        except Exception as e:
            self.log(f"[!] Discord Error: {type(e).__name__}: {e}")

    def scanner_loop(self):
        while self.is_running:
            try:
                region = self.config["scan_region"]
                screenshot = pyautogui.screenshot(region=region)
                gray = screenshot.convert('L')
                
                try:
                    extracted = pytesseract.image_to_string(gray).lower()
                except Exception as ocr_error:
                    self.log(f"[!] OCR Error: {ocr_error}")
                    time.sleep(self.config["interval"])
                    continue
                
                target = self.config["target_text"].lower()
                if target in extracted:
                    self.log(f"MATCH FOUND: '{target}'")
                    
                    elapsed = time.time() - self.last_notification_time
                    if elapsed >= self.config["cooldown"]:
                        self.send_to_discord(screenshot, target)
                        self.last_notification_time = time.time()
                    else:
                        remaining = int(self.config["cooldown"] - elapsed)
                        self.log(f"Cooldown active: {remaining}s remaining")
                
                # Update Vision UI
                if self.show_vision.get():
                    try:
                        self.update_vision_preview(screenshot)
                    except Exception as e:
                        self.log(f"[!] Vision preview error: {e}")
                
                time.sleep(self.config["interval"])
            except Exception as e:
                self.log(f"[!] Scanner error: {type(e).__name__}: {e}")
                time.sleep(2)

    def update_vision_preview(self, pil_img):
        # Resize to fit canvas while maintaining aspect ratio
        canvas_w = self.vision_canvas.winfo_width()
        canvas_h = self.vision_canvas.winfo_height()
        
        if canvas_w < 10: canvas_w = 460 # Default approx width
        
        img_w, img_h = pil_img.size
        ratio = min(canvas_w/img_w, 100/img_h)
        new_size = (int(img_w * ratio), int(img_h * ratio))
        
        if new_size[0] > 0 and new_size[1] > 0:
            resized = pil_img.resize(new_size, Image.Resampling.LANCZOS)
            self.vision_img = ImageTk.PhotoImage(resized)
            
            # Use .after to update UI safely from thread
            self.after(0, self._set_canvas_image)

    def _set_canvas_image(self):
        self.vision_canvas.delete("all")
        self.vision_canvas.create_image(
            self.vision_canvas.winfo_width() // 2, 
            self.vision_canvas.winfo_height() // 2, 
            image=self.vision_img, 
            anchor="center"
        )

    def update_topmost(self):
        self.attributes('-topmost', self.always_on_top_var.get())

    def toggle_scanner(self):
        if not self.is_running:
            try:
                self.save_config()
                
                # Validation checks
                if not self.config["webhook_url"]:
                    messagebox.showerror("Error", "Please provide a Discord Webhook URL.")
                    return
                
                if not self.config["target_text"]:
                    messagebox.showerror("Error", "Please provide Target Text to find.")
                    return
                
                if self.config["interval"] <= 0 or self.config["cooldown"] < 0:
                    messagebox.showerror("Error", "Interval must be positive and Cooldown non-negative.")
                    return
                
                self.is_running = True
                self.btn_toggle.config(text="■ STOP SCANNER")
                self.scan_thread = threading.Thread(target=self.scanner_loop, daemon=True)
                self.last_notification_time = 0 # Reset cooldown on start
                self.scan_thread.start()
                self.log("Scanner started.")
            except Exception as e:
                self.is_running = False
                self.btn_toggle.config(text="▶ START SCANNER")
                messagebox.showerror("Error", f"Failed to start: {e}")
        else:
            self.is_running = False
            self.btn_toggle.config(text="▶ START SCANNER")
            self.log("Scanner stopped.")

if __name__ == "__main__":
    print("Launching FruitNoti GUI...")
    app = FruitNotiApp()
    app.mainloop()
