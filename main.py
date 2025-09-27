import argparse
from pathlib import Path
from backend.transcriber import transcribe_audio
from backend.exporter import export_srt, export_premiere_xml, regroup_segments

def apply_duration_padding(segments, min_duration=0.0, padding=0.0):
    """Ensure each segment has at least min_duration and add optional padding."""
    adjusted = []
    for seg in segments:
        start = max(0, seg["start"] - padding)
        end = max(start, seg["end"] + padding)

        # enforce minimum duration
        if end - start < min_duration:
            end = start + min_duration

        adjusted.append({
            "start": start,
            "end": end,
            "text": seg["text"]
        })
    return adjusted

def main():
    parser = argparse.ArgumentParser(description="🎬 Subtitle Generator CLI")
    parser.add_argument("input_file", help="Path to audio/video file")
    parser.add_argument(
        "--break",
        dest="break_mode",
        choices=["sentence", "word", "nwords"],
        default="sentence",
        help="Break mode for subtitles (default: sentence)"
    )
    parser.add_argument(
        "--n",
        dest="nwords",
        type=int,
        default=5,
        help="Number of words per subtitle (only for nwords mode, default=5)"
    )
    parser.add_argument(
        "--lang",
        dest="language",
        default="en",
        help="Language code (default: en). Examples: en, hi, ur, mr"
    )
    parser.add_argument(
        "--min-duration",
        dest="min_duration",
        type=float,
        default=0.0,
        help="Minimum duration of each subtitle in seconds"
    )
    parser.add_argument(
        "--padding",
        dest="padding",
        type=float,
        default=0.0,
        help="Optional padding to add before/after each subtitle in seconds"
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return

    base_name = input_path.stem  # filename without extension

    print(f"📁 Input file: {input_path.name}")
    result = transcribe_audio(input_path, break_type=args.break_mode, language=args.language)

    # regroup if needed
    regrouped_segments = regroup_segments(result, args.break_mode, args.nwords)

    # apply user-defined min duration and padding
    regrouped_segments = apply_duration_padding(regrouped_segments, args.min_duration, args.padding)
    result["segments"] = regrouped_segments

    print("💾 Exporting .srt...")
    export_srt(result, output_dir="output", base_name=base_name)

    print("💾 Exporting .xml for Premiere...")
    export_premiere_xml(result, output_dir="output", base_name=base_name)

    print("✅ Subtitle files saved in 'output/' folder.")

if __name__ == "__main__":
    main()
