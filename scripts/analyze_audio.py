#!/usr/bin/env python3
"""
Audio Key, Scale, Pitch Range & BPM Analyzer
Powered by Librosa, Spotify Basic Pitch, and pretty_midi.

Provides instant musical intelligence on any audio file:
- Musical Key & Scale (Major / Minor with confidence score)
- Camelot Wheel Key (DJ harmonic mixing notation, e.g. 8A, 11B)
- Relative Musical Key
- Exact Tempo (BPM)
- Vocal / Instrument Pitch Range (Lowest Note, Highest Note, Vocal Register)
- Dominant Pitch Frequencies & Tuning Reference
"""

import os
import sys
import warnings
import logging
import argparse
import importlib.util
import subprocess
from pathlib import Path

# Suppress noisy library warnings from basic_pitch, librosa, and resampy
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch") or not importlib.util.find_spec("librosa"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import librosa
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

PITCHES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Krumhansl-Schmuckler harmonic key profiles
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

# Camelot Wheel Mapping (Root Pitch Index, Mode) -> Camelot Code
CAMELOT_MAP = {
    # Major (B)
    (0, "Major"): "8B",   # C
    (1, "Major"): "3B",   # Db/C#
    (2, "Major"): "10B",  # D
    (3, "Major"): "5B",   # Eb
    (4, "Major"): "12B",  # E
    (5, "Major"): "7B",   # F
    (6, "Major"): "2B",   # F#
    (7, "Major"): "9B",   # G
    (8, "Major"): "4B",   # Ab
    (9, "Major"): "11B",  # A
    (10, "Major"): "6B",  # Bb
    (11, "Major"): "1B",  # B
    # Minor (A)
    (0, "Minor"): "5A",   # C min
    (1, "Minor"): "12A",  # C# min
    (2, "Minor"): "7A",   # D min
    (3, "Minor"): "2A",   # Eb/D# min
    (4, "Minor"): "9A",   # E min
    (5, "Minor"): "4A",   # F min
    (6, "Minor"): "11A",  # F# min
    (7, "Minor"): "6A",   # G min
    (8, "Minor"): "1A",   # G# min
    (9, "Minor"): "8A",   # A min
    (10, "Minor"): "3A",  # Bb min
    (11, "Minor"): "10A", # B min
}


def midi_to_note_name(midi_number: int) -> str:
    octave = (midi_number // 12) - 1
    note = PITCHES[midi_number % 12]
    return f"{note}{octave}"


def analyze_audio_musical_profile(audio_path: str, fast_mode: bool = False) -> dict:
    audio_path = Path(audio_path).resolve()
    if not audio_path.exists():
        raise FileNotFoundError(f"File not found: {audio_path}")

    print(f"\n[*] Analyzing audio: {audio_path.name}")
    print(f"    - Running Librosa & Spotify Basic Pitch neural inference...")
    print(f"    - Extracting Key, Scale, Camelot, BPM, and Pitch Range (please wait)...")

    # Load audio (mono, 22050 Hz for fast chroma and beat analysis)
    y, sr = librosa.load(str(audio_path), sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    # 1. Key & Scale Detection
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    def correlate_profile(profile, chroma_vec):
        corrs = []
        for shift in range(12):
            shifted = np.roll(profile, shift)
            corr = np.corrcoef(shifted, chroma_vec)[0, 1]
            corrs.append(corr)
        return corrs

    maj_corrs = correlate_profile(MAJOR_PROFILE, chroma_mean)
    min_corrs = correlate_profile(MINOR_PROFILE, chroma_mean)

    best_maj_idx = int(np.argmax(maj_corrs))
    best_min_idx = int(np.argmax(min_corrs))

    if maj_corrs[best_maj_idx] >= min_corrs[best_min_idx]:
        root_idx = best_maj_idx
        mode = "Major"
        confidence = float(maj_corrs[best_maj_idx])
        rel_root_idx = (root_idx + 9) % 12
        rel_key = f"{PITCHES[rel_root_idx]} Minor"
    else:
        root_idx = best_min_idx
        mode = "Minor"
        confidence = float(min_corrs[best_min_idx])
        rel_root_idx = (root_idx + 3) % 12
        rel_key = f"{PITCHES[rel_root_idx]} Major"

    detected_key = f"{PITCHES[root_idx]} {mode}"
    camelot = CAMELOT_MAP.get((root_idx, mode), "N/A")

    # 2. BPM / Tempo Tracking
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo_val = float(np.atleast_1d(tempo)[0])

    # 3. Pitch Range & Discrete Notes (Basic Pitch)
    pitch_stats = {
        "min_note": "N/A",
        "max_note": "N/A",
        "pitch_span": "N/A",
        "dominant_notes": [],
        "note_count": 0
    }

    try:
        # Predict note events using Basic Pitch
        _, midi_data, note_events = predict(
            audio_path=str(audio_path),
            model_or_model_path=ICASSP_2022_MODEL_PATH,
            onset_threshold=0.55,
            frame_threshold=0.35,
            minimum_note_length=120.0
        )
        all_notes = []
        for inst in midi_data.instruments:
            all_notes.extend(inst.notes)

        if all_notes:
            pitches_list = [n.pitch for n in all_notes]
            min_p = min(pitches_list)
            max_p = max(pitches_list)
            pitch_stats["min_note"] = midi_to_note_name(min_p)
            pitch_stats["max_note"] = midi_to_note_name(max_p)
            pitch_stats["pitch_span"] = f"{max_p - min_p} semitones ({midi_to_note_name(min_p)} -> {midi_to_note_name(max_p)})"
            pitch_stats["note_count"] = len(all_notes)
    except Exception as e:
        pass

    # Top 4 pitch classes from chromagram
    top_indices = np.argsort(chroma_mean)[::-1][:4]
    pitch_stats["dominant_notes"] = [PITCHES[idx] for idx in top_indices]

    # Estimated tuning reference (A4 offset)
    tuning_offset = librosa.estimate_tuning(y=y, sr=sr)
    tuning_hz = 440.0 * (2.0 ** (tuning_offset / 12.0))

    return {
        "file_name": audio_path.name,
        "file_path": str(audio_path),
        "duration_seconds": round(duration, 2),
        "key": detected_key,
        "mode": mode,
        "camelot": camelot,
        "relative_key": rel_key,
        "confidence": round(max(0.0, min(1.0, confidence)) * 100, 1),
        "bpm": round(tempo_val, 1),
        "pitch_range": pitch_stats,
        "tuning_ref_hz": round(tuning_hz, 1)
    }


def print_musical_report(info: dict) -> None:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    width = 62
    border = "=" * width

    print(f"\n{CYAN}{border}{RESET}")
    print(f"{BOLD}{CYAN}  SPOTIFY BASIC PITCH & LIBROSA - MUSICAL ANALYSIS{RESET}")
    print(f"{CYAN}{border}{RESET}")
    print(f"  {BOLD}File:{RESET}     {info['file_name']}")
    print(f"  {BOLD}Length:{RESET}   {info['duration_seconds']}s ({int(info['duration_seconds']//60)}m {int(info['duration_seconds']%60)}s)")
    print(f"{CYAN}{'-' * width}{RESET}")
    print(f"  {BOLD}KEY / SCALE:{RESET}      {GREEN}{BOLD}{info['key']}{RESET}  {YELLOW}(Camelot: {info['camelot']}){RESET}")
    print(f"  {BOLD}Relative Key:{RESET}     {info['relative_key']}")
    print(f"  {BOLD}Confidence:{RESET}       {info['confidence']}%")
    print(f"{CYAN}{'-' * width}{RESET}")
    print(f"  {BOLD}TEMPO (BPM):{RESET}      {MAGENTA}{BOLD}{info['bpm']} BPM{RESET}")
    print(f"  {BOLD}Tuning Center:{RESET}    {info['tuning_ref_hz']} Hz (Standard: 440 Hz)")
    print(f"{CYAN}{'-' * width}{RESET}")
    print(f"  {BOLD}PITCH RANGE:{RESET}      {info['pitch_range']['min_note']}  -->  {info['pitch_range']['max_note']}")
    print(f"  {BOLD}Pitch Span:{RESET}       {info['pitch_range']['pitch_span']}")
    print(f"  {BOLD}Total Notes:{RESET}      {info['pitch_range']['note_count']} notes transcribed")
    print(f"  {BOLD}Prominent Notes:{RESET}  {', '.join(info['pitch_range']['dominant_notes'])}")
    print(f"{CYAN}{border}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Musical Key, Scale, Pitch & BPM Analyzer")
    parser.add_argument("audio_path", help="Path to audio file to analyze")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")
    parser.add_argument("--pause", action="store_true", help="Wait for user input before exiting (for Explorer context menu)")

    args = parser.parse_args()

    try:
        report = analyze_audio_musical_profile(args.audio_path)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_musical_report(report)
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}", file=sys.stderr)
    finally:
        if args.pause:
            try:
                input("Press [Enter] to close...")
            except Exception:
                pass


if __name__ == "__main__":
    main()
