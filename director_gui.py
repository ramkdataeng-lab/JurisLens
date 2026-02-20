import tkinter as tk
from tkinter import ttk
import pygame
import os
import threading

AUDIO_DIR = "voiceovers"

# Mapping filenames to DETAILED instructions
SCRIPT_HINTS = {
    "01_Intro": "ACTION: Face camera. Confident opening. 'Web search reads, we enforce.'",
    "02_TheProblem": "ACTION: Show a generic ChatGPT/Grok window. Scroll a PDF manually. Look frustrated.",
    "03_TheBlindSpot": "ACTION: Point to a mock 'Bank Ledger' excel sheet (or just gesture). 'It's blind to state.'",
    "04_Solution": "ACTION: **SWITCH TAB** to JurisLens App. Point to 'Elasticsearch RAG' in sidebar.",
    "05_Demo_Ingest": "ACTION: Drag & Drop 'goliath_bank_internal_policy.pdf'. Click 'Process & Index'. Point to '✅ KB: 5 Chunks'.",
    "06_Demo_AskRule": "ACTION: Type: 'What is the limit for Zylaria?'. Hover over the [Relevance: 0.92] citation.",
    "07_Demo_AskAction": "ACTION: Type: 'My client wants to send $4,000 to Zylaria. Is this allowed?'.",
    "08_Demo_Result": "ACTION: WATCH SIDEBAR! Point to 'Scanning...' -> 'Calculating Risk...' -> '❌ BLOCKED'.",
    "09_Scenario2_Sanctions": "ACTION: Type: 'Can we onboard Ivan Drago?'.",
    "10_Scenario2_Result": "ACTION: Show Sidebar '🕵️‍♀️ Scanning Sanctions...'. Point to 'DENIED' result.",
    "11_Closing": "ACTION: **CLICK '🛠️ Architecture Pro' button in Sidebar.** Let the animated diagram play.",
    "12_Adoption": "ACTION: Final Close. 'Don't just chat, enforce.' Fade to Black."
}


class DirectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JurisLens Director")
        self.root.geometry("400x250")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg="#2c3e50")
        
        # Initialize Audio
        pygame.mixer.init()
        self.files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")])
        self.current_index = 0
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=('Segoe UI', 12, 'bold'), padding=10)
        
        # UI Elements
        self.lbl_title = tk.Label(root, text="Ready to Record", font=("Segoe UI", 14, "bold"), fg="white", bg="#2c3e50")
        self.lbl_title.pack(pady=(15, 5))
        
        self.lbl_hint = tk.Label(root, text="Press PLAY to start", font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50", wraplength=380)
        self.lbl_hint.pack(pady=5)
        
        self.progress = ttk.Progressbar(root, length=350, mode='determinate')
        self.progress.pack(pady=10)
        
        self.btn_action = ttk.Button(root, text="▶ PLAY CLIP 1", command=self.play_next)
        self.btn_action.pack(pady=10, fill='x', padx=20)
        
        self.lbl_status = tk.Label(root, text=f"Clip 0 / {len(self.files)}", fg="#7f8c8d", bg="#2c3e50")
        self.lbl_status.pack(side="bottom", pady=5)

    def play_next(self):
        if self.current_index >= len(self.files):
            self.lbl_title.config(text="🎉 DONE!", fg="#2ecc71")
            self.btn_action.config(state="disabled", text="Recording Finished")
            return

        filename = self.files[self.current_index]
        clip_key = os.path.splitext(filename)[0]
        
        # Load and Play
        filepath = os.path.join(AUDIO_DIR, filename)
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        
        # Update UI
        self.lbl_title.config(text=f"Playing: {clip_key}", fg="#3498db")
        instruction = SCRIPT_HINTS.get(clip_key, "No instruction")
        self.lbl_hint.config(text=instruction)
        
        self.current_index += 1
        
        next_text = "NEXT CLIP ▶" if self.current_index < len(self.files) else "FINISH"
        self.btn_action.config(text=next_text, state="disabled") # Disable until finished
        
        # Update Progress
        self.progress['value'] = (self.current_index / len(self.files)) * 100
        self.lbl_status.config(text=f"Clip {self.current_index} / {len(self.files)}")
        
        # Monitor playback in thread to re-enable button
        threading.Thread(target=self.monitor_playback, daemon=True).start()

    def monitor_playback(self):
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # When done
        self.root.after(0, lambda: self.btn_action.config(state="normal"))
        self.root.after(0, lambda: self.lbl_title.config(text="Paused (Ready)", fg="white"))

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectorApp(root)
    root.mainloop()
