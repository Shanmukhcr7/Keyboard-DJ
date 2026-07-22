import os
import time
import threading
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import pystray

import logging
logger = logging.getLogger(__name__)

class AppGUI(ctk.CTk):
    """The main GUI for Keyboard DJ using CustomTkinter."""

    def __init__(self, app_core):
        super().__init__()
        self.app_core = app_core
        self.player = app_core.player
        self.settings = app_core.settings
        self.listener = app_core.listener

        self.title("Keyboard DJ")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.start_time = time.time()
        self.tray_icon = None

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Periodic GUI update
        self.after(100, self.update_stats)

    def _build_ui(self):
        """Constructs the UI elements."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Sidebar (Controls)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Keyboard DJ 🎵", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.load_btn = ctk.CTkButton(self.sidebar_frame, text="Load Music", command=self.load_music)
        self.load_btn.grid(row=1, column=0, padx=20, pady=10)

        self.play_btn = ctk.CTkButton(self.sidebar_frame, text="Play", command=self.player.play)
        self.play_btn.grid(row=2, column=0, padx=20, pady=10)

        self.pause_btn = ctk.CTkButton(self.sidebar_frame, text="Pause", command=self.player.pause)
        self.pause_btn.grid(row=3, column=0, padx=20, pady=10)

        self.stop_btn = ctk.CTkButton(self.sidebar_frame, text="Stop", command=self.player.stop)
        self.stop_btn.grid(row=4, column=0, padx=20, pady=10)

        self.fun_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Fun Mode:")
        self.fun_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))
        
        self.fun_mode_var = ctk.StringVar(value=self.settings.get("fun_mode", "DJ Mode"))
        self.fun_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["DJ Mode", "Meme Mode", "Piano Mode", "Random Playlist", "Typing Speed Mode"],
                                               command=self.change_fun_mode, variable=self.fun_mode_var)
        self.fun_mode_menu.grid(row=6, column=0, padx=20, pady=(0, 10))

        self.exit_btn = ctk.CTkButton(self.sidebar_frame, text="Exit", command=self.quit_app, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.exit_btn.grid(row=9, column=0, padx=20, pady=20)

        # Right Area (Stats and Sliders)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Status Indicators
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.play_status_label = ctk.CTkLabel(self.status_frame, text="Idle", text_color="gray", font=ctk.CTkFont(weight="bold"))
        self.play_status_label.pack(side="left", padx=10)
        
        self.type_status_label = ctk.CTkLabel(self.status_frame, text="Inactive", text_color="gray")
        self.type_status_label.pack(side="right", padx=10)

        # Current Song
        current_song = self.settings.get("music_file", "None")
        song_name = os.path.basename(current_song) if current_song else "None"
        self.song_label = ctk.CTkLabel(self.main_frame, text=f"Song: {song_name}", font=ctk.CTkFont(size=14, weight="bold"), wraplength=300)
        self.song_label.grid(row=1, column=0, sticky="w", pady=10)

        # Stats Area
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)

        self.wpm_label = ctk.CTkLabel(self.stats_frame, text="WPM: 0")
        self.wpm_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.keys_label = ctk.CTkLabel(self.stats_frame, text="Total Keys: 0")
        self.keys_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.time_label = ctk.CTkLabel(self.stats_frame, text="Session Time: 00:00")
        self.time_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.pos_label = ctk.CTkLabel(self.stats_frame, text="Music Pos: 0:00")
        self.pos_label.grid(row=1, column=1, padx=10, pady=5)

        # Sliders
        self.slider_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.slider_frame.grid(row=3, column=0, sticky="ew", pady=20)

        # Volume
        self.vol_label = ctk.CTkLabel(self.slider_frame, text="Volume")
        self.vol_label.grid(row=0, column=0, sticky="w")
        self.vol_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=1, command=self.change_volume)
        self.vol_slider.grid(row=0, column=1, sticky="ew", padx=10)
        self.vol_slider.set(self.settings.get("volume", 0.8))

        # Timeout
        self.timeout_label = ctk.CTkLabel(self.slider_frame, text="Timeout (ms)")
        self.timeout_label.grid(row=1, column=0, sticky="w", pady=(20, 0))
        self.timeout_slider = ctk.CTkSlider(self.slider_frame, from_=100, to=2000, number_of_steps=19, command=self.change_timeout)
        self.timeout_slider.grid(row=1, column=1, sticky="ew", padx=10, pady=(20, 0))
        self.timeout_slider.set(self.settings.get("timeout", 300))
        self.timeout_val_label = ctk.CTkLabel(self.slider_frame, text=f"{self.settings.get('timeout', 300)} ms")
        self.timeout_val_label.grid(row=1, column=2, pady=(20, 0))

    def load_music(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        if file_path:
            if self.player.load_music(file_path):
                self.song_label.configure(text=f"Song: {os.path.basename(file_path)}")

    def change_volume(self, value):
        self.player.set_volume(float(value))

    def change_timeout(self, value):
        ms = int(value)
        self.settings.set("timeout", ms)
        self.timeout_val_label.configure(text=f"{ms} ms")
        
    def change_fun_mode(self, value):
        self.settings.set("fun_mode", value)

    def update_status_gui(self, typing=None):
        """Callback to update indicator labels based on typing events."""
        if typing is not None:
            if typing:
                self.type_status_label.configure(text="Typing...", text_color="cyan")
            else:
                self.type_status_label.configure(text="Inactive", text_color="gray")

    def update_stats(self):
        """Periodically updates the stats labels."""
        try:
            # Play Status
            if self.player.is_playing:
                if self.player.is_paused:
                    self.play_status_label.configure(text="Paused", text_color="yellow")
                else:
                    self.play_status_label.configure(text="Playing", text_color="green")
            else:
                self.play_status_label.configure(text="Stopped", text_color="gray")

            # Keyboard Stats
            stats = self.listener.get_stats()
            self.wpm_label.configure(text=f"WPM: {stats['wpm']}")
            self.keys_label.configure(text=f"Total Keys: {stats['total_keys']}")

            # Session Time
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.time_label.configure(text=f"Session Time: {mins:02d}:{secs:02d}")

            # Music Pos
            pos_ms = self.player.get_position()
            if pos_ms > 0:
                pos_s = pos_ms // 1000
                pmins, psecs = divmod(pos_s, 60)
                self.pos_label.configure(text=f"Music Pos: {pmins:02d}:{psecs:02d}")
            else:
                self.pos_label.configure(text="Music Pos: 0:00")
                
            # If playing, the type status is green, otherwise gray or cyan based on `inactive_notified`
            if not self.listener.inactive_notified:
                self.type_status_label.configure(text="Typing...", text_color="cyan")
            else:
                self.type_status_label.configure(text="Inactive", text_color="gray")

        except Exception as e:
            logger.error(f"Error updating stats: {e}")

        # Re-schedule
        self.after(200, self.update_stats)

    # System Tray Logic
    def create_image(self):
        """Create a simple icon for the system tray."""
        image = Image.new('RGB', (64, 64), color=(0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (16, 16, 48, 48),
            fill=(40, 200, 100)
        )
        return image

    def hide_window(self):
        """Hides the window and creates the system tray icon."""
        self.withdraw()
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem('Show', self.show_window),
            pystray.MenuItem('Exit', self.quit_app)
        )
        self.tray_icon = pystray.Icon("KeyboardDJ", image, "Keyboard DJ", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon=None, item=None):
        """Restores the window from the system tray."""
        if self.tray_icon:
            self.tray_icon.stop()
        self.after(0, self.deiconify)

    def quit_app(self, icon=None, item=None):
        """Exits the application completely."""
        if self.tray_icon:
            self.tray_icon.stop()
        self.app_core.quit()
        self.destroy()
