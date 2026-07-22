import json
import os
import logging

CONFIG_FILE = "config.json"

DEFAULT_SETTINGS = {
    "timeout": 300,
    "volume": 0.8,
    "start_minimized": False,
    "loop_music": True,
    "launch_on_startup": False,
    "music_file": "",
    "fun_mode": "DJ Mode"
}

logger = logging.getLogger(__name__)

class SettingsManager:
    """Manages reading and writing application settings."""

    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.settings = DEFAULT_SETTINGS.copy()
        self.load_settings()

    def load_settings(self):
        """Loads settings from the JSON file, creating it if it doesn't exist."""
        if not os.path.exists(self.config_path):
            logger.info("Config file not found. Creating default config.")
            self.save_settings()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_settings = json.load(f)
                # Merge loaded settings with defaults to ensure all keys exist
                self.settings.update(loaded_settings)
            logger.info("Settings loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            logger.info("Using default settings.")

    def save_settings(self):
        """Saves current settings to the JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully.")
        except Exception as e:
            logger.error(f"Error saving config file: {e}")

    def get(self, key: str, default=None):
        """Gets a setting value."""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Sets a setting value and saves the configuration."""
        self.settings[key] = value
        self.save_settings()
