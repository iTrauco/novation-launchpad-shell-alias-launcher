
# 🚀 Quick Start

Building this as a way to use the Novation LaunchPads as Linux macro keyboard for shell aliases, I ran out of hotkey command launches years ago...

Building this to solve that problem.

## Prerequisites
- Python 3.8+
- Novation Launchpad Mini MK3
- Virtual environment tool (`venv`)

---

## Installation

### Clone the repository and create a virtual environment:

```bash
# Clone repository
git clone [your-repo-url]
cd launchpad-shell

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### Install dependencies:

```bash
pip install --upgrade pip
pip install python-rtmidi python-dotenv cryptography rich logging
pip freeze > requirements.txt
```

### Detect your Launchpad port:

```bash
# Run the detection script
python detect_midi.py

# Example output:
🎹 Available MIDI Ports:
📥 Input Ports:
  0: Midi Through:Midi Through Port-0 14:0
  1: Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 20:0
  2: Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1
```

---

## Create Your Configuration

```bash
# Copy example config
cp config/default_config.env .env

# Edit .env with your Launchpad port name
LAUNCHPAD_PORT="Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1"
```

---

## 🎮 Testing Button Coordinates

Before setting up your commands, you can use the test script to verify button coordinates:

```bash
# Run the test script
python test_mapping.py
```

### This will:
- Light up some test buttons with different colors
- Show coordinates of any button you press in the debug output
- Help you plan your button layout

**Example output when pressing buttons:**
```plaintext
🔔 Button Event: (0, 0) - Pressed [Note: 0, Velocity: 127]
🔔 Button Event: (1, 0) - Pressed [Note: 1, Velocity: 127]
```

---

## 📍 Button Grid Layout

The Launchpad uses a coordinate system where `(0, 0)` is the top-left button:

```plaintext
     0  1  2  3  4  5  6  7   (x-coordinates →)
  0  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  1  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  2  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  3  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  4  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  5  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  6  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
  7  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
      (y-coordinates ↓)
```

---

## 🎨 Available Colors

Use these color constants in your mappings:

```python
Colors.OFF = 0      # No light
Colors.RED = 5      # 🔴
Colors.GREEN = 21   # 💚
Colors.YELLOW = 13  # 💛
Colors.BLUE = 45    # 💙
Colors.PURPLE = 53  # 💜
Colors.CYAN = 37    # 💠
Colors.WHITE = 3    # ⚪
```

---

## 🔍 Debugging

If you're having issues:

### Check MIDI connection:

```bash
python detect_midi.py
```

### Run test script with debug output:

```bash
python test_mapping.py
```

### Verify your .env configuration:

```bash
cat .env
```

---

## 🛠️ Next Steps

After confirming your button coordinates work:
- Plan your button layout
- Create shell aliases you want to trigger
- Map buttons to your aliases
