# 🎵 Keyboard DJ by SHANMUKHCR7 🎵

Have you ever wanted to feel like a DJ or a Pianist while typing an essay, coding, or writing an email? 
Welcome to **Keyboard DJ**! 

Whenever you type anywhere on your computer (Notepad, Word, Chrome, VS Code), the music starts playing. As soon as you stop typing, the music pauses seamlessly. It turns your boring typing tasks into an interactive rhythm game!

---

## 🌟 The Ultimate Tutorial

Follow this step-by-step guide to get Keyboard DJ running perfectly on your computer!

### Step 1: Download the Project
Click the green **"Code"** button at the top of this repository and select **"Download ZIP"**. Extract the downloaded folder somewhere on your computer.

### Step 2: Install Python
If you don't already have Python installed, you need it! 
* Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version.
* **Important for Windows:** During installation, make sure to check the box that says **"Add Python to PATH"**.

### Step 3: Install the Requirements
Open your **Terminal** (Mac) or **Command Prompt** (Windows), navigate to the folder where you extracted the project, and install the required background libraries:
```bash
pip install -r requirements.txt
```

---

## 🚀 Step 4: Running the App (Windows vs Mac)

Because Windows and Mac handle security differently, there is a specific way to run the app depending on your device!

### 🪟 For Windows Users
1. Open your Command Prompt inside the main folder.
2. Run the application:
   ```bash
   python main.py
   ```
3. You will see the epic SHANMUKHCR7 logo! Choose your mode, minimize the terminal, and start typing anywhere!

### 🍎 For MacBook Users
Apple has strict security that prevents background apps from listening to your keyboard by default.
1. Open your Terminal inside the `KeyboardDJ_Mac` folder.
2. Run the application:
   ```bash
   python main.py
   ```
3. **CRITICAL STEP:** If the music doesn't play when you type, you must give your Terminal permission to read your keyboard.
   * Go to **System Settings** ➔ **Privacy & Security** ➔ **Accessibility**.
   * Toggle the switch **ON** for your Terminal (or VS Code, depending on where you ran the command).
   * Restart your terminal and run the command again. It will now work perfectly!

---

## 🎧 Step 5: How to Add Your Own Favorite Songs!

By default, the project comes with a few awesome tracks, but the best part is that you can add **any song you want**!

1. Download your favorite song as an `.mp3`, `.wav`, or `.ogg` file.
2. Open the project folder and navigate into the `assets/music/` directory.
3. Paste your song file right there!
4. The next time you run `python main.py` and select **Option 1 (DJ Mode)**, your song will automatically appear in the list. Just type its number and start jamming while you type!

---

## 🎹 The Two Epic Modes

When you start the app, you get to choose between:
1.  🎧 **DJ Mode (Song)**: Plays your selected background track. It plays while you type and pauses when you stop. Perfect for long coding or writing sessions!
2.  🎹 **Indian Piano Mode (Keys)**: Your keyboard turns into a physical Piano! The middle row keys (`A, S, D, F, G, H, J, K`) play authentic Just-Intonation Indian Piano notes (*Sa, Re, Ga, Ma, Pa, Dha, Ni, Sa*).

---

## ⚙️ Advanced Settings (Hidden UI)
Want to change the volume or adjust how fast the music pauses after you stop typing? 
Look at your **System Tray** (the bottom right corner of your screen on Windows, or top right on Mac). You will see a small green Keyboard DJ icon. **Double-click it** to open the hidden control panel!

### Global Hotkeys
You don't even need to open the app to control it. Use these shortcuts from anywhere:
*   `Ctrl+Alt+P` - Pause/Resume manually
*   `Ctrl+Alt+S` - Stop completely
*   `Ctrl+Alt+M` - Mute

---

*Created by **SHANMUKHCR7**. Feel free to fork, share, and enjoy the music!*
