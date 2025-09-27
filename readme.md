# 🎬 Subtitle Generator CLI

A simple Python CLI tool to generate subtitles for audio or video files using Whisper.  
It supports multiple languages, flexible subtitle break modes, and exports both `.srt` and Adobe Premiere `.xml` files.

---

## ✨ Features
- 🎤 Transcribe audio/video to text
- ✂️ Break subtitles by sentence, word, or fixed number of words
- 🌍 Multiple languages supported (English, Hindi, Urdu, Marathi, etc.)
- 📂 Export `.srt` (standard subtitles) and `.xml` (Adobe Premiere)
- ⏱ Optional padding and minimum duration control

---

## ⚙️ Prerequisites

Before installing, make sure you have these installed:

1. **Python**  
   - Version **3.10+** (works with 3.10, 3.11; avoid 3.12/3.13 with Whisper issues on Windows)  
   - Download: [python.org/downloads](https://www.python.org/downloads/)

2. **FFmpeg** (required by Whisper to handle audio/video)  
   - [Download FFmpeg](https://ffmpeg.org/download.html)  
   - On Windows, add FFmpeg’s `bin/` folder to your **PATH**  
   - Test it:  
     ```bash
     ffmpeg -version
     ```

3. **PyTorch** (for Whisper model execution)  
   - Install CPU or GPU version depending on your system:  
     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
     ```
   - For CUDA (NVIDIA GPU):  
     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
     ```

---

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/subtitle-generator.git
   cd subtitle-generator
Create a virtual environment

bash
Copy code
python -m venv venv
Activate the virtual environment

Windows (PowerShell):

powershell
Copy code
.\venv\Scripts\activate
macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
🚀 Usage
Basic command:

bash
Copy code
python main.py path/to/your/file.mp4
Optional Arguments
Argument	Description	Default
--break	Subtitle break mode: sentence, word, nwords	sentence
--n	Number of words per subtitle (for nwords mode)	5
--lang	Language code (en, hi, ur, mr, etc.)	en
--min-duration	Minimum subtitle duration in seconds	0.0
--padding	Padding (delay) in seconds before/after subtitle	0.0

💡 Examples
bash
Copy code
# Basic usage, sentence breaks, English (default)
python main.py myvideo.mp4

# Break subtitles every 3 words, Hindi
python main.py myaudio.wav --break nwords --n 3 --lang hi

# One subtitle per word, Urdu
python main.py myaudio.wav --break word --lang ur

# Add minimum duration 1s and padding 0.5s
python main.py myvideo.mp4 --min-duration 1.0 --padding 0.5

# Combine options: Marathi, 7 words per subtitle, with padding
python main.py movie.mkv --lang mr --break nwords --n 7 --padding 0.3

📂 Output
All results are saved in the output/ folder:

filename.srt → Standard subtitle file

filename.xml → Adobe Premiere XML for editing

⚠️ Notes
Ensure FFmpeg is installed and on PATH. Without it, Whisper cannot load media files.

Running on CPU will be slower. Use GPU (CUDA) if available for faster transcription.

Large video/audio files will take more time.

If you encounter llvmlite / numba errors, downgrade Python to 3.10 or 3.11.

📜 License
MIT License. Feel free to use, modify, and distribute.