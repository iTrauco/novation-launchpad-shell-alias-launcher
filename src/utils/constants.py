"""
🎨 Constants Module
Define MIDI constants and color codes.
"""

# MIDI message types
MIDI_NOTE_ON = 0x90
MIDI_NOTE_OFF = 0x80

class Colors:
    """🎨 Color constants for Launchpad buttons"""
    OFF = 0
    RED = 5        # 🔴
    GREEN = 21     # 💚
    YELLOW = 13    # 💛
    BLUE = 45      # 💙
    PURPLE = 53    # 💜
    CYAN = 37      # 💠
    WHITE = 3      # ⚪

    # Brightness variants
    RED_DIM = 7
    GREEN_DIM = 17
    BLUE_DIM = 41

# Grid configuration
GRID_SIZE = 8
MAX_VELOCITY = 127
