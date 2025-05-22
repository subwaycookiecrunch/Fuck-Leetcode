# Study Assistant Tool

A Python application designed to help with algorithm study and problem-solving practice.

## Features

- Organize algorithm patterns by category
- Store and retrieve common algorithm templates
- Integrated screen analysis tools for learning from examples
- Discreet operation for focused study sessions

## Setup

1. Install Python 3.8+ if not already installed
2. Install Tesseract OCR:
   - Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - The default installation path should be `C:\Program Files\Tesseract-OCR\`

3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Add your Claude API key:
   - Open `src/stealth_capture.py`
   - Replace `YOUR_CLAUDE_API_KEY` with your actual API key
   - If you don't have one, visit [Anthropic](https://console.anthropic.com/) to obtain a key

## Usage

### Regular Mode
Run the application in standard mode:
```
python src/main.py
```

### Study Mode
For distraction-free study sessions, run:
```
pythonw stealth_launcher.pyw
```

### Hotkeys
- `Ctrl+Alt+L`: Capture the current screen for analysis
- `Ctrl+Alt+P`: Insert previously analyzed code example

## Tips for Effective Study

1. Use the tool to analyze and learn from algorithm examples
2. Practice implementing solutions based on the templates provided
3. Compare your solutions with the analyzed examples
4. For best learning results, try to solve problems yourself before reviewing solutions

## Privacy & Data Storage

- All study session data is stored locally
- Analysis results are saved temporarily and automatically cleared after 30 minutes
- No data is sent to third parties except for API requests to Claude for algorithm analysis 