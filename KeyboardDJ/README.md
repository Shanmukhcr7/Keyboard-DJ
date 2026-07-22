# Keyboard DJ 🎵

Keyboard DJ is a fun, interactive desktop application that plays background music while you type. Whenever you press any key, the music starts. Stop typing, and the music pauses smoothly. It's designed to make long coding or writing sessions feel like a rhythm game!

![Keyboard DJ Screenshot](https://via.placeholder.com/800x500.png?text=Keyboard+DJ+Screenshot)

## Features 🚀

*   **Global Keyboard Detection**: Works in the background regardless of what application you are currently using (Chrome, VS Code, Word, etc.).
*   **Smart Music Engine**: Plays, pauses, and resumes exactly from where it left off. Never restarts the song abruptly.
*   **Typing Detection & Stats**: Real-time calculation of Words Per Minute (WPM) and total keys pressed.
*   **Modern GUI**: A sleek dark mode interface built with CustomTkinter.
*   **Fun Modes**:
    *   **DJ Mode**: Normal play/pause behavior.
    *   **Meme Mode**: Every key randomly plays a meme sound effect (add your sounds to `assets/music/memes/`).
    *   **Piano Mode**: Turns your keyboard into a piano. Keys correspond to specific notes.
    *   **Random Playlist**: Pick a new random song after 5 seconds of inactivity.
    *   **Typing Speed Mode**: Simulates changing playback speed by adjusting volume based on how fast you type.
*   **System Tray Integration**: Minimize to the system tray so it stays out of your way.
*   **Global Hotkeys**:
    *   `Ctrl+Alt+P` - Pause/Resume
    *   `Ctrl+Alt+S` - Stop
    *   `Ctrl+Alt+M` - Mute

## Project Structure 📁

```text
KeyboardDJ/
├── main.py                  # Entry point of the application
├── player.py                # Pygame music player wrapper and fun modes logic
├── keyboard_listener.py     # Global hook, WPM calculation, inactivity timeout
├── settings.py              # Configuration manager
├── gui.py                   # CustomTkinter interface
├── config.json              # Saved user settings
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── logs/
│   └── keyboarddj.log       # Application logs
└── assets/
    ├── icons/               # System tray icons
    └── music/
        ├── memes/           # Folder for Meme Mode sounds (.wav/.mp3)
        └── piano/           # Folder for Piano Mode sounds (A.wav, C.wav etc.)
```

## Requirements ⚙️

*   Python 3.11+
*   Windows OS (for global hooking best compatibility)

## Installation & Setup 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/KeyboardDJ.git
   cd KeyboardDJ
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage 🎧

1. Launch the application.
2. Click **Load Music** and select an `.mp3`, `.wav`, or `.ogg` file.
3. Start typing anywhere on your computer! The music will begin playing.
4. Stop typing, and after the configured timeout (default 300ms), the music will pause.
5. Adjust the **Timeout** and **Volume** sliders to your preference.
6. Select different **Fun Modes** from the dropdown to spice up your typing experience.

## How to Package into an EXE using PyInstaller 📦

If you want to distribute the app as a standalone executable without requiring users to install Python, you can use PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller to build the project. The `--noconsole` flag hides the terminal window, and `--onefile` packages it into a single EXE. We also need to include the `customtkinter` library assets:
   ```bash
   pyinstaller --noconsole --onefile --name "KeyboardDJ" --collect-all customtkinter main.py
   ```
   *(Note: You may also need to manually copy the `assets/` directory to the `dist/` folder next to your EXE so the app can find your music and icons).*

3. Your executable will be available in the `dist/` folder!

## Troubleshooting Guide 🔧

**1. Music isn't playing when I type:**
*   Check if you have loaded a music file.
*   Check the volume slider.
*   Look at `logs/keyboarddj.log` for any pygame initialization errors.

**2. Global hotkeys aren't working:**
*   Sometimes Windows security restricts global hooks. Try running the application or your IDE as an Administrator.

**3. "Missing module" errors on launch:**
*   Ensure you have installed all requirements: `pip install -r requirements.txt`.

**4. CPU Usage is high:**
*   The application is designed to stay under 2% CPU. If you see high usage, ensure you haven't modified the `time.sleep(0.05)` inside the monitoring loop in `keyboard_listener.py`.

## Future Enhancements 🔮

*   **Spotify/Apple Music Integration**: Instead of local MP3 files, integrate with Spotify API to control playback of your favorite playlists.
*   **Native Speed Control**: Implement an advanced audio processing library (like `pydub` or `soundfile`) to dynamically stretch/compress audio speed without altering pitch for the "Typing Speed Mode".
*   **Theme Customization**: Allow users to pick custom accent colors for the CustomTkinter UI.
*   **Mac/Linux Support**: Polish the global hooking and system tray integration for cross-platform support.

## License 📜

MIT License. See `LICENSE` for more details.
