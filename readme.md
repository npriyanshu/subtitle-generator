# 🎬 Subtitle Generator CLI

A simple Python CLI tool to generate subtitles for audio or video files using Whisper. It supports multiple languages, flexible subtitle break modes, and exports both `.srt` and Adobe Premiere `.xml` files.

---

## Features

- Transcribe audio/video to text.
- Break subtitles by sentence, word, or a fixed number of words.
- Support for multiple languages (English, Hindi, Urdu, Marathi, etc.).
- Export `.srt` and `.xml` files for video editing.
- Optional padding/delay control.

---

## Requirements

- Python 3.10+  
- Virtual environment (recommended)
- Dependencies in `requirements.txt` (Whisper, NumPy, etc.)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/subtitle-generator.git
cd subtitle-generator
````

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

* **Windows (PowerShell):**

```powershell
.\venv\Scripts\activate
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Usage

Run the CLI with your input audio/video file:

```bash
python main.py path/to/your/file.mp4
```

### Optional Arguments

| Argument  | Description                                                     | Default    |
| --------- | --------------------------------------------------------------- | ---------- |
| `--break` | Break mode for subtitles. Options: `sentence`, `word`, `nwords` | `sentence` |
| `--n`     | Number of words per subtitle (only for `nwords` mode)           | `5`        |
| `--lang`  | Language code (e.g., `en`, `hi`, `ur`, `mr`)                    | `en`       |

### How to Use Your Script (with Examples)

```bash
# Basic usage, sentence breaks, English (default)
python main.py myvideo.mp4

# Break subtitles every 3 words, Hindi language
python main.py myaudio.wav --break nwords --n 3 --lang hi

# One subtitle per word, Urdu language
python main.py myaudio.wav --break word --lang ur

# Add minimum duration 1.0 seconds and padding 0.5 seconds
python main.py myvideo.mp4 --min-duration 1.0 --padding 0.5

# Combine options: Marathi language, 7 words per subtitle, with padding
python main.py movie.mkv --lang mr --break nwords --n 7 --padding 0.3
```

---

## Output

* Subtitle files will be saved in the `output/` folder:

  * `filename.srt` → Standard subtitle file
  * `filename.xml` → Adobe Premiere XML for editing

---

## Notes

* Make sure your input file exists and is a valid audio/video file.
* Padding between subtitles is automatically handled. You can configure it in the code if needed.
* For large videos, transcription may take time depending on your CPU/GPU.

---

