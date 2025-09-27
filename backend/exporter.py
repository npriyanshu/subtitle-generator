from pathlib import Path
import os
from datetime import datetime, timedelta

def export_srt(result, output_dir="output", base_name="output", pad_before=0.0, pad_after=0.0, min_duration=0.0):
    """Export Whisper result to a .srt subtitle file with optional padding and minimum duration."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    srt_path = output_dir / f"{base_name}_{now}_subtitles.srt"

    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    segments = result.get("segments", [])
    with srt_path.open("w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            # Apply optional padding
            start_sec = max(segment["start"] - pad_before, 0)
            end_sec = segment["end"] + pad_after

            # Ensure minimum duration
            if min_duration > 0 and (end_sec - start_sec) < min_duration:
                end_sec = start_sec + min_duration

            start = format_timestamp(start_sec)
            end = format_timestamp(end_sec)
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    print(f"✅ SRT saved to {srt_path}")


def export_premiere_xml(result, output_dir="output", base_name="output", pad_before=0.0, pad_after=0.0, min_duration=0.0):
    """Export Whisper result to Premiere Pro XML subtitle format with optional padding."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_path = output_dir / f"{base_name}_{now}_premiere.xml"

    segments = result.get("segments", [])

    def format_time(seconds):
        return f"{seconds:.3f}"

    with xml_path.open("w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<project>\n  <captions>\n')
        for seg in segments:
            start_sec = max(seg["start"] - pad_before, 0)
            end_sec = seg["end"] + pad_after
            if min_duration > 0 and (end_sec - start_sec) < min_duration:
                end_sec = start_sec + min_duration

            start = format_time(start_sec)
            end = format_time(end_sec)
            text = seg["text"].strip()
            f.write(f'    <caption start="{start}" end="{end}" text="{text}"/>\n')
        f.write('  </captions>\n</project>\n')

    print(f"✅ Premiere XML saved to {xml_path}")


def regroup_segments(result, break_mode="sentence", n=5):
    """Re-group transcription segments into word, sentence, or n-word chunks."""
    segments = result.get("segments", [])

    if break_mode == "sentence":
        return segments

    if break_mode == "word":
        words = []
        for seg in segments:
            if "words" in seg:
                for w in seg["words"]:
                    words.append({
                        "start": w["start"],
                        "end": w["end"],
                        "text": w["word"].strip()
                    })
        return words

    if break_mode == "nwords":
        words = []
        for seg in segments:
            if "words" in seg:
                for w in seg["words"]:
                    words.append(w)

        grouped = []
        for i in range(0, len(words), n):
            chunk = words[i:i+n]
            if not chunk:
                continue
            grouped.append({
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"],
                "text": " ".join([w["word"].strip() for w in chunk])
            })
        return grouped

    return segments
