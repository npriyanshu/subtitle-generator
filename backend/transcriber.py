import whisper
import ffmpeg
from pathlib import Path
import tempfile

def extract_audio(input_path, output_audio_path):
    (
        ffmpeg
        .input(str(input_path))
        .output(str(output_audio_path), format='wav', acodec='pcm_s16le', ac=1, ar='16k')
        .run(quiet=True)
    )

def transcribe_audio(input_path: Path, break_type="sentence", language="en"):
    print("🤖 Transcribing using Whisper...")
    model = whisper.load_model("small")  # You can switch to "tiny" for faster testing

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_audio = Path(tmpdir) / "temp.wav"
        extract_audio(input_path, temp_audio)

        result = model.transcribe(
            str(temp_audio),
            language=language,
            # 👇 FIX: enable for both 'word' and 'nwords'
            word_timestamps=(break_type in ["word", "nwords"])
        )

    print(f"🌐 Detected language (Whisper): {result.get('language', 'unknown')}")
    return result
