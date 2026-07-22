import os
import random
import logging
import pygame
from pathlib import Path

logger = logging.getLogger(__name__)

class MusicPlayer:
    """Handles background music playing, pausing, and fun modes using pygame."""

    def __init__(self, settings_manager):
        self.settings = settings_manager
        self.is_playing = False
        self.is_paused = False
        self.current_song = None
        self.playlist = []
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            logger.info("Pygame mixer initialized successfully.")
        except pygame.error as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            
        self.set_volume(self.settings.get("volume", 0.8))
        
        # Load resources for Fun Modes
        self.meme_sounds = self._load_sounds_from_dir("assets/music/memes")
        self.piano_sounds = self._load_piano_sounds()
        self.indian_piano_sounds = self._load_indian_piano_sounds()
        self.base_speed = 1.0

    def _load_sounds_from_dir(self, directory: str) -> list:
        """Loads all valid audio files from a directory into Sound objects."""
        sounds = []
        if not os.path.exists(directory):
            return sounds
            
        for file in os.listdir(directory):
            if file.endswith(('.wav', '.ogg', '.mp3')):
                try:
                    sound = pygame.mixer.Sound(os.path.join(directory, file))
                    sounds.append(sound)
                except Exception as e:
                    logger.warning(f"Failed to load sound {file}: {e}")
        return sounds
        
    def _load_piano_sounds(self) -> dict:
        """Loads specific notes for piano mode (placeholders or actual if present)."""
        piano_dir = "assets/music/piano"
        piano_map = {}
        # Mapping letters to generic note files if they exist
        notes = {'a': 'C.wav', 's': 'D.wav', 'd': 'E.wav', 'f': 'F.wav', 'g': 'G.wav', 'h': 'A.wav', 'j': 'B.wav', 'k': 'C2.wav'}
        if os.path.exists(piano_dir):
            for key, filename in notes.items():
                path = os.path.join(piano_dir, filename)
                if os.path.exists(path):
                    try:
                        piano_map[key] = pygame.mixer.Sound(path)
                    except Exception:
                        pass
        return piano_map

    def _load_indian_piano_sounds(self) -> dict:
        """Loads Indian notes (Sa, Re, Ga, etc.)."""
        from generate_sounds import ensure_indian_piano_sounds
        ensure_indian_piano_sounds()
        
        indian_dir = "assets/music/indian_piano"
        indian_map = {}
        # Mapping standard keyboard row to Indian notes
        notes = {'a': 'sa.wav', 's': 're.wav', 'd': 'ga.wav', 'f': 'ma.wav', 
                 'g': 'pa.wav', 'h': 'dha.wav', 'j': 'ni.wav', 'k': 'sa2.wav'}
        if os.path.exists(indian_dir):
            for key, filename in notes.items():
                path = os.path.join(indian_dir, filename)
                if os.path.exists(path):
                    try:
                        indian_map[key] = pygame.mixer.Sound(path)
                    except Exception as e:
                        logger.warning(f"Failed to load indian note {filename}: {e}")
        return indian_map

    def load_music(self, filepath: str) -> bool:
        """Loads a music file into the mixer."""
        if not filepath or not os.path.exists(filepath):
            logger.error(f"Music file not found: {filepath}")
            return False
            
        try:
            pygame.mixer.music.load(filepath)
            self.current_song = filepath
            self.settings.set("music_file", filepath)
            logger.info(f"Loaded music: {filepath}")
            return True
        except pygame.error as e:
            logger.error(f"Error loading music {filepath}: {e}")
            return False

    def play(self):
        """Starts playing the loaded music."""
        if not self.current_song:
            logger.warning("Tried to play, but no song loaded.")
            return

        try:
            loops = -1 if self.settings.get("loop_music", True) else 0
            pygame.mixer.music.play(loops=loops)
            self.is_playing = True
            self.is_paused = False
            logger.info("Playback started.")
        except pygame.error as e:
            logger.error(f"Error playing music: {e}")

    def pause(self):
        """Pauses the music."""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            logger.info("Playback paused.")

    def resume(self):
        """Resumes the paused music or starts it if not playing."""
        if not self.is_playing:
            self.play()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            logger.info("Playback resumed.")

    def stop(self):
        """Stops the music entirely."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            logger.info("Playback stopped.")

    def set_volume(self, volume: float):
        """Sets the volume (0.0 to 1.0)."""
        pygame.mixer.music.set_volume(volume)
        self.settings.set("volume", volume)

    def get_position(self) -> int:
        """Returns the current playback position in milliseconds."""
        if self.is_playing:
            return pygame.mixer.music.get_pos()
        return 0
        
    def play_random_meme(self):
        """Plays a random meme sound."""
        if self.meme_sounds:
            sound = random.choice(self.meme_sounds)
            sound.play()
            
    def play_piano_note(self, key_char: str):
        """Plays a piano note corresponding to the key."""
        if key_char in self.piano_sounds:
            self.piano_sounds[key_char].play()
            
    def play_indian_piano_note(self, key_char: str):
        """Plays an Indian piano note corresponding to the key."""
        if key_char in self.indian_piano_sounds:
            self.indian_piano_sounds[key_char].play()

    def simulate_speed(self, wpm: int):
        """
        Simulates playback speed changes since pygame doesn't natively support it.
        We adjust volume based on WPM to give a sense of intensity.
        """
        base_vol = self.settings.get("volume", 0.8)
        if wpm < 20:
            target_vol = max(0.1, base_vol - 0.3)
        elif wpm > 80:
            target_vol = min(1.0, base_vol + 0.2)
        else:
            target_vol = base_vol
            
        pygame.mixer.music.set_volume(target_vol)

    def handle_random_playlist(self, directory: str):
        """Mode 4: Load a random song from a directory."""
        if not os.path.exists(directory):
            return
            
        songs = [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav', '.ogg'))]
        if songs:
            random_song = random.choice(songs)
            path = os.path.join(directory, random_song)
            self.load_music(path)
            self.play()
            logger.info(f"Random Playlist Mode: Loaded {random_song}")
