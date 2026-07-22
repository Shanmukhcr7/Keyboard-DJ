import os
import sys
import logging
from pathlib import Path

# Create directories if they don't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("assets/music/memes", exist_ok=True)
os.makedirs("assets/music/piano", exist_ok=True)
os.makedirs("assets/icons", exist_ok=True)

# Configure logging
log_file = os.path.join("logs", "keyboarddj.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.info("="*40)
logger.info("Program Started: Keyboard DJ")
logger.info("="*40)

from settings import SettingsManager
from player import MusicPlayer
from keyboard_listener import KeyboardMonitor
from gui import AppGUI

class KeyboardDJApp:
    """Core controller for the Keyboard DJ application."""
    
    def __init__(self):
        logger.info("Initializing components...")
        self.settings = SettingsManager()
        self.player = MusicPlayer(self.settings)
        self.gui = None
        
        # Load previous music file if it exists
        music_file = self.settings.get("music_file", "")
        if music_file and os.path.exists(music_file):
            self.player.load_music(music_file)
            
        self.listener = KeyboardMonitor(
            self.player, 
            self.settings, 
            update_gui_callback=self.update_gui_status
        )

    def update_gui_status(self, typing=None, stats=None):
        """Callback passed to listener to update GUI."""
        if self.gui:
            if typing is not None:
                self.gui.update_status_gui(typing=typing)
            # Stats are updated via the GUI's own polling loop, 
            # but we could force an update here if needed.

    def run(self):
        """Starts the application."""
        try:
            # Prompt user for mode via terminal
            print("\n" + "="*57)
            print(r"""
  _  __          _                         _  ____  _ 
 | |/ /___ _   _| |__   ___   __ _ _ __ __| |/ ___|| |
 | ' // _ \ | | | '_ \ / _ \ / _` | '__/ _` | |  _ | |
 | . \  __/ |_| | |_) | (_) | (_| | | | (_| | |_| || |
 |_|\_\___|\__, |_.__/ \___/ \__,_|_|  \__,_|\____||_|
           |___/                                      
               by SHANMUKHCR7
""")
            print("="*57)
            print("1. Play the background 'Song' (DJ Mode)")
            print("2. Play Indian Piano 'Keys'")
            print("="*57)
            
            while True:
                choice = input("Enter your choice (1 or 2): ").strip()
                if choice == '1':
                    self.settings.set("fun_mode", "DJ Mode")
                    print("\n--> Selected: Song Mode")
                    
                    # Search for MP3s
                    search_dirs = [".", "assets/music"]
                    mp3_files = []
                    for d in search_dirs:
                        if os.path.exists(d):
                            for f in os.listdir(d):
                                if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                                    mp3_files.append(os.path.join(d, f))
                                    
                    if mp3_files:
                        print("\nAvailable Songs:")
                        for idx, f in enumerate(mp3_files):
                            print(f"{idx + 1}. {os.path.basename(f)}")
                        
                        while True:
                            song_choice = input(f"\nSelect a song (1-{len(mp3_files)}): ").strip()
                            try:
                                s_idx = int(song_choice) - 1
                                if 0 <= s_idx < len(mp3_files):
                                    selected_song = mp3_files[s_idx]
                                    self.settings.set("music_file", selected_song)
                                    self.player.load_music(selected_song)
                                    print(f"--> Loaded: {os.path.basename(selected_song)}")
                                    break
                                else:
                                    print("Invalid number.")
                            except ValueError:
                                print("Please enter a valid number.")
                    else:
                        print("\nNo songs found in current directory or assets/music/.")
                    break
                elif choice == '2':
                    self.settings.set("fun_mode", "Indian Piano Mode")
                    print("\n--> Selected: Indian Piano Keys Mode")
                    break
                else:
                    print("Invalid input. Please type 1 or 2.")
                    
            print("\n" + "★"*57)
            print(" 🎶  AWESOME! Minimize this window, start typing")
            print("     anywhere on your computer, and FEEL THE MUSIC!  🎶")
            print("★"*57 + "\n")
            
            self.listener.start()
            
            # Start GUI
            self.gui = AppGUI(self)
            
            # Check if should start minimized
            if self.settings.get("start_minimized", False):
                self.gui.hide_window()
                
            self.gui.mainloop()
            
        except Exception as e:
            logger.error(f"Application crashed: {e}", exc_info=True)
        finally:
            self.quit()

    def quit(self):
        """Cleans up and exits."""
        logger.info("Exiting application...")
        self.listener.stop()
        self.player.stop()
        self.settings.save_settings()
        logger.info("Program Ended.")

if __name__ == "__main__":
    app = KeyboardDJApp()
    app.run()
