---
name: audio-key-bpm-analyzer
description: Instant audio musical intelligence tool and Windows Explorer context menu. Analyzes any local audio file to extract musical Key & Scale (Major/Minor), Camelot Wheel key code (e.g. 8A, 11B), Relative Key, Tempo (BPM), Pitch Range (min/max/span), and tuning frequency calibration.
---

# Audio Key, Scale, Pitch & BPM Analyzer

Fast local musical analyzer powered by Librosa and Spotify Basic Pitch. Extracts essential musical attributes from any audio file (`.wav`, `.mp3`, `.flac`, `.m4a`, `.aiff`, `.ogg`) without uploading data to external servers.

## Metrics Extracted

- **Key & Scale**: Krumhansl-Schmuckler harmonic chroma correlation (identifies tonic, mode, and confidence score).
- **Camelot Code**: Standard DJ harmonic mixing wheel notation (e.g., `8B` for C Major, `8A` for A Minor).
- **Relative Key**: Identifies the parallel harmonic counterpart.
- **BPM (Tempo)**: Dynamic programming beat tracking and tempo estimation.
- **Pitch Range**: Lowest note (e.g., `E2`), Highest note (e.g., `G5`), pitch semitone span, and total discrete notes transcribed.
- **Tuning Calibration**: Detects microtonal master tuning frequency (e.g., 440.0 Hz vs 432.0 Hz or 442.0 Hz).

---

## Windows Explorer Context Menu

You can analyze any audio file directly by right-clicking it in Windows Explorer:

1. Right-click any `.wav`, `.mp3`, `.flac`, `.m4a`, or `.ogg` file.
2. Click **"Analyze Key, Scale, Pitch & BPM (Basic Pitch)"**.
3. A terminal window opens instantly displaying the musical analysis summary card.

### Installation & Removal
- **Install**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File "C:\Users\<you>\.agents\skills\audio-key-bpm-analyzer\scripts\install_context_menu.ps1"
  ```
- **Uninstall**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File "C:\Users\<you>\.agents\skills\audio-key-bpm-analyzer\scripts\uninstall_context_menu.ps1"
  ```

---

## Command Line Usage

```bash
# Pretty terminal display:
python "C:\Users\<you>\.agents\skills\audio-key-bpm-analyzer\scripts\analyze_audio.py" "C:\Music\sample.wav"

# JSON output for automated scripting / pipelines:
python "C:\Users\<you>\.agents\skills\audio-key-bpm-analyzer\scripts\analyze_audio.py" "C:\Music\sample.wav" --json
```
