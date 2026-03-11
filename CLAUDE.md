# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

このディレクトリ (`~/myCLAUDE`) はClaude Codeの作業ベースです。
ホームディレクトリ配下にある複数の独立したプロジェクトを管理・参照します。

## Projects

### myAG — Personal Landing Page (`~/myAG/`)
Static site with no build step. Open `index.html` directly in a browser.
- Vanilla HTML/CSS/JS (no frameworks, no package manager)
- Japanese/English multilingual content
- Uses Google Fonts (Noto Sans JP, Noto Serif JP) via CDN

### OCR Project (`~/Documents/OCR_Project/`)
Python script for batch PDF-to-text extraction with Japanese OCR support.

```bash
cd ~/Documents/OCR_Project
python ocr_pdf.py
```

Dependencies: `pdf2image`, `pytesseract`, `Pillow`, `tqdm`
System requirement: Tesseract with `jpn` and `eng` language packs (`brew install tesseract tesseract-lang`)

Output: one `.txt` file per PDF page in `output_text/`

### Whisper Environment (`~/whisper-env/`)
Python venv for audio transcription (OpenAI Whisper). Activate with:
```bash
source ~/whisper-env/bin/activate
```
