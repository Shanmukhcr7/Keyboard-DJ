import os
import wave
import math
import struct
import logging

logger = logging.getLogger(__name__)

# Base Frequency for Sa (C4)
BASE_FREQ = 261.63

# Frequencies for Indian Notes (using Just Intonation ratios for authentic sound)
INDIAN_NOTES = {
    'sa': BASE_FREQ * 1.0,        # 1/1
    're': BASE_FREQ * (9.0/8.0),  # 9/8
    'ga': BASE_FREQ * (5.0/4.0),  # 5/4
    'ma': BASE_FREQ * (4.0/3.0),  # 4/3
    'pa': BASE_FREQ * (3.0/2.0),  # 3/2
    'dha': BASE_FREQ * (5.0/3.0), # 5/3
    'ni': BASE_FREQ * (15.0/8.0), # 15/8
    'sa2': BASE_FREQ * 2.0        # 2/1
}

def generate_tone(filename, frequency, duration=1.5, volume=0.5, sample_rate=44100):
    """Generates a Piano-like tone and saves it as a WAV file."""
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            
            # Piano synthesis (Fundamental + decaying harmonics)
            # Higher harmonics decay faster
            val = (
                1.00 * math.sin(2.0 * math.pi * frequency * t) * math.exp(-1.5 * t) +
                0.50 * math.sin(2.0 * math.pi * (frequency * 2.01) * t) * math.exp(-3.0 * t) +
                0.25 * math.sin(2.0 * math.pi * (frequency * 3.02) * t) * math.exp(-4.5 * t) +
                0.10 * math.sin(2.0 * math.pi * (frequency * 4.03) * t) * math.exp(-6.0 * t)
            )
            val /= 1.85  # Normalize
            
            # Percussive Envelope for Piano (Sharp attack, exponential decay)
            attack = 0.01
            if t < attack:
                envelope = t / attack
            else:
                envelope = math.exp(-2.0 * (t - attack))
                
            value = int(volume * 32767.0 * val * envelope)
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)
            
def ensure_indian_piano_sounds():
    """Ensures that the Indian piano sound files exist."""
    dir_path = "assets/music/indian_piano"
    os.makedirs(dir_path, exist_ok=True)
    
    for note, freq in INDIAN_NOTES.items():
        filename = os.path.join(dir_path, f"{note}.wav")
        try:
            generate_tone(filename, freq)
        except Exception as e:
            logger.error(f"Failed to generate {filename}: {e}")
