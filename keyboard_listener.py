import time
import logging
import threading
from pynput import keyboard
from collections import deque

logger = logging.getLogger(__name__)

class KeyboardMonitor:
    """Monitors global keystrokes and controls music playback based on typing activity."""

    def __init__(self, player, settings_manager, update_gui_callback=None):
        self.player = player
        self.settings = settings_manager
        self.update_gui = update_gui_callback
        
        self.last_keypress_time = time.time()
        self.is_typing = False
        self.total_keys_pressed = 0
        self.keys_history = deque()  # Store timestamps of recent keys to calculate WPM
        
        self.listener = None
        self.hotkey_listener = None
        self.monitor_thread = None
        self.running = False
        self.inactive_notified = True  # Start assuming inactive
        self.last_pause_time = 0

    def start(self):
        """Starts the keyboard listener and monitor threads."""
        if self.running:
            return
            
        self.running = True
        
        # Start pynput listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()
        logger.info("Keyboard listener started.")
        
        # Start hotkey listener
        hotkeys = {
            '<ctrl>+<alt>+p': self.hotkey_pause,
            '<ctrl>+<alt>+s': self.hotkey_stop,
            '<ctrl>+<alt>+m': self.hotkey_mute
        }
        self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
        self.hotkey_listener.daemon = True
        self.hotkey_listener.start()
        logger.info("Global hotkeys registered.")

        # Start background monitor thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop(self):
        """Stops the monitoring threads."""
        self.running = False
        if self.listener:
            self.listener.stop()
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        logger.info("Keyboard listener stopped.")

    def on_press(self, key):
        """Callback for every key press."""
        current_time = time.time()
        self.last_keypress_time = current_time
        self.total_keys_pressed += 1
        self.keys_history.append(current_time)
        
        # Remove timestamps older than 60 seconds for accurate WPM
        while self.keys_history and current_time - self.keys_history[0] > 60:
            self.keys_history.popleft()

        mode = self.settings.get("fun_mode", "DJ Mode")

        # Resume or start music if we were inactive
        if not self.is_typing:
            self.is_typing = True
            self.inactive_notified = False
            
            # Only resume background track if we are in a mode that uses it
            song_modes = ["DJ Mode", "Random Playlist", "Typing Speed Mode"]
            
            if mode in song_modes:
                # Handle Random Playlist mode logic (5 seconds inactivity -> new song)
                if mode == "Random Playlist":
                    if self.last_pause_time and (current_time - self.last_pause_time) > 5.0:
                        self.player.handle_random_playlist("assets/music")
                    else:
                        self.player.resume()
                else:
                    self.player.resume()
                    
            if self.update_gui:
                self.update_gui(typing=True)

        # Handle specific fun modes on key press
        if mode == "Meme Mode":
            self.player.play_random_meme()
        elif mode == "Piano Mode":
            try:
                char = key.char.lower()
                self.player.play_piano_note(char)
            except AttributeError:
                pass  # Special keys don't have .char
        elif mode == "Indian Piano Mode":
            try:
                char = key.char.lower()
                self.player.play_indian_piano_note(char)
            except AttributeError:
                pass
        elif mode == "Typing Speed Mode":
            wpm = self.calculate_wpm()
            self.player.simulate_speed(wpm)

    def on_release(self, key):
        """Callback for key release (unused currently but required by listener)."""
        pass
        
    def _monitor_loop(self):
        """Background thread that checks for inactivity."""
        while self.running:
            current_time = time.time()
            timeout_sec = self.settings.get("timeout", 300) / 1000.0
            
            # Check for inactivity
            if self.is_typing and (current_time - self.last_keypress_time > timeout_sec):
                self.is_typing = False
                self.last_pause_time = current_time
                if not self.inactive_notified:
                    self.player.pause()
                    self.inactive_notified = True
                    if self.update_gui:
                        self.update_gui(typing=False)
            
            # Update GUI stats periodically
            if self.update_gui:
                self.update_gui(stats=True)
                
            time.sleep(0.05)  # Run 20 times a second to keep CPU low

    def calculate_wpm(self) -> int:
        """Calculates approximate Words Per Minute."""
        # 1 word ~ 5 characters. keys_history stores keys in last 60 seconds.
        keys_in_last_min = len(self.keys_history)
        wpm = keys_in_last_min // 5
        return wpm
        
    def get_stats(self) -> dict:
        """Returns current typing statistics."""
        current_time = time.time()
        # Clean up history before counting
        while self.keys_history and current_time - self.keys_history[0] > 60:
            self.keys_history.popleft()
            
        keys_in_last_min = len(self.keys_history)
        wpm = keys_in_last_min // 5
        
        return {
            "wpm": wpm,
            "kpm": keys_in_last_min,
            "total_keys": self.total_keys_pressed,
            "is_typing": self.is_typing
        }

    # Hotkey Callbacks
    def hotkey_pause(self):
        logger.info("Global hotkey: Pause/Resume")
        if self.player.is_playing:
            if self.player.is_paused:
                self.player.resume()
            else:
                self.player.pause()

    def hotkey_stop(self):
        logger.info("Global hotkey: Stop")
        self.player.stop()

    def hotkey_mute(self):
        logger.info("Global hotkey: Mute")
        # Toggle volume between 0 and previous setting
        current_vol = self.settings.get("volume", 0.8)
        if current_vol > 0:
            self.settings.set("volume", 0)
            self.player.set_volume(0)
        else:
            self.settings.set("volume", 0.8)  # default back if 0
            self.player.set_volume(0.8)
