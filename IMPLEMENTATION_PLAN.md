# Implementation Plan: Audio Key, Scale, Pitch & BPM Analyzer

This document tracks planned, in-progress, and completed work for the **Audio Key, Scale, Pitch & BPM Analyzer** skill. It persists across all version passes.

---

## Completed Work

### v1.0.0 — Initial Release (2026-09-24)
- [x] **Harmonic Key & Scale Engine (`scripts/analyze_audio.py`)**: Implemented Krumhansl-Schmuckler chroma correlation using Librosa CQT/Chroma profiles to determine root pitch, mode (Major/Minor), and confidence percentage. (✅ done in v1.0.0)
- [x] **Camelot Wheel & Relative Key Mapping**: Full 24-spoke harmonic mixing matrix mapping musical keys directly to DJ Camelot codes (`1A`-`12A`, `1B`-`12B`) and relative key counterparts. (✅ done in v1.0.0)
- [x] **Dynamic Programming Beat Tracking**: Integrated Librosa beat tracking and onset strength envelope analysis for accurate BPM estimation. (✅ done in v1.0.0)
- [x] **Pitch Range & Note Span Extraction**: Leveraged Spotify Basic Pitch neural model to transcribe active notes, determining lowest note (e.g. `E2`), highest note (e.g. `G5`), semitone span, and note counts. (✅ done in v1.0.0)
- [x] **Microtonal Tuning Calibration**: Spectral centroid estimation calculating master tuning deviation (e.g. 440 Hz standard vs 432 Hz alternate). (✅ done in v1.0.0)
- [x] **Windows Explorer Context Menu**: Built `scripts/install_context_menu.ps1` and `uninstall_context_menu.ps1` to register right-click "Analyze Key, Scale, Pitch & BPM" actions in HKCU without requiring administrator privileges. (✅ done in v1.0.0)
- [x] **Dual Terminal & JSON Output**: Supports both ANSI terminal summary cards and `--json` serialized output for CLI pipelines. (✅ done in v1.0.0)
- [x] **Automatic Runtime Delegation**: Transparent execution through dedicated `basic-pitch` uv Python environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`). (✅ done in v1.0.0)
- [x] **Tri-Platform Deployment**: Established canonical skill in `.agents/skills/audio-key-bpm-analyzer` with NTFS directory junctions to `.claude/skills`, `.grok/skills`, and `.gemini/config/skills`. (✅ done in v1.0.0)
- [x] **Documentation & Versioning**: Authored `SKILL.md`, standardized `HOW_TO_USE.txt`, `README.md`, and permanent `App Changes Tracker.html`. (✅ done in v1.0.0)

---

## Planned Future Work

- [ ] **Batch Folder Audio Profiler**: Support scanning entire sample libraries or DJ playlist folders and outputting a consolidated CSV/Excel catalog.
- [ ] **Energy & Danceability Scoring**: Add spectral flux and dynamic range loudness profiling (RMS/LUFS) to score track energy.
- [ ] **Automatic Ableton Clip Tagging**: Write detected Key and BPM into Ableton `.asd` clip analysis sidecar files.
