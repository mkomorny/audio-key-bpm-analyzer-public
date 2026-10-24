# Audio Key, Scale, Pitch & BPM Analyzer

**Audio Key, Scale, Pitch & BPM Analyzer** (`audio-key-bpm-analyzer`) is a high-speed local musical intelligence tool and Windows Explorer context menu integration that analyzes any audio file (`.wav`, `.mp3`, `.flac`, `.m4a`, `.aiff`, `.ogg`) to extract Key, Scale, Camelot Wheel DJ code, BPM, Pitch Range, and tuning calibration without uploading data to external servers.

---

## ⚡ Extracted Metrics

| Metric | Algorithm / Methodology | Output Example |
| :--- | :--- | :--- |
| **Musical Key & Scale** | Krumhansl-Schmuckler chroma correlation on Librosa CQT profiles | `D Minor (Confidence: 89.4%)` |
| **Camelot Wheel Code** | 24-spoke harmonic mixing matrix for DJs | `7A` (D Minor) / `7B` (F Major) |
| **Relative Key** | Parallel harmonic counterpart calculation | `F Major` |
| **Tempo (BPM)** | Dynamic programming beat tracking on onset strength envelopes | `124.0 BPM` |
| **Pitch Range** | Spotify Basic Pitch neural note detection | `D3 to G5 (29 semitones)` |
| **Tuning Calibration** | Spectral peak centroid reference calculation | `440.0 Hz (Standard Concert Pitch)` |

---

## 🖱️ Windows Explorer Context Menu

You can analyze any audio file directly from your Windows desktop or file explorer with a single right-click:

1. Right-click any `.wav`, `.mp3`, `.flac`, `.m4a`, or `.ogg` file.
2. Select **"Analyze Key, Scale, Pitch & BPM (Basic Pitch)"**.
3. A terminal window launches immediately showing the formatted musical intelligence card.

### Installation & Removal
- **Install (Current User / HKCU — No Admin Needed)**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File "scripts/install_context_menu.ps1"
  ```
- **Uninstall**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File "scripts/uninstall_context_menu.ps1"
  ```

---

## 🚀 Usage

### In Chat (Prompts & Slash Commands)

- `/audio-key-bpm-analyzer "C:\Music\sample.wav"`
- *"Analyze the key, scale, and BPM of 'C:\Samples\bass_loop.wav'"*
- *"What is the Camelot code, tempo, and vocal pitch range of 'D:\Vocals\chorus_lead.mp3'?"*
- *"Run audio key analysis on 'C:\Audio\track.flac' and output JSON."*

### Command Line Interface (`scripts/analyze_audio.py`)

```powershell
# Formatted terminal summary card:
python scripts/analyze_audio.py "C:\Music\sample.wav"

# JSON output for automated music pipelines:
python scripts/analyze_audio.py "C:\Music\sample.wav" --json

# Pause console window after run (for batch/shortcut use):
python scripts/analyze_audio.py "C:\Music\sample.wav" --pause
```

---

## 📁 Repository Structure

```
audio-key-bpm-analyzer/
├── SKILL.md                    # Skill trigger and platform integration instructions
├── HOW_TO_USE.txt              # Quick-reference cheat sheet & prompt guide
├── IMPLEMENTATION_PLAN.md      # Multi-version roadmap and completed tasks
├── App Changes Tracker.html    # Permanent interactive HTML version changelog
├── README.md                   # This overview
└── scripts/
    ├── analyze_audio.py        # Musical intelligence analysis engine
    ├── install_context_menu.ps1   # Windows Explorer context menu installer
    └── uninstall_context_menu.ps1 # Context menu uninstaller
```

---

## 📜 Documentation & Lifecycle

- **Version History & Releases**: Tracked permanently in [App Changes Tracker.html](App%20Changes%20Tracker.html).
- **Roadmap & Completed Features**: Documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).
