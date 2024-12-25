# Path: src/models/button.py
"""
🎛️ Button Model Module
Defines the core button mapping structure for the Launchpad controller.

Flow:
1. This is a base model that will be used by other modules
2. Represents a single Launchpad button with its properties
3. Used for type safety and data validation
"""

from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class LaunchpadButton:
    # 📍 Physical properties
    x: int  # X coordinate on the grid
    y: int  # Y coordinate on the grid
    
    # 🎨 Visual properties
    color: int  # MIDI color code
    
    # 🔧 Functional properties
    note: Optional[int] = None  # MIDI note number (calculated from x,y)
    
    def __post_init__(self):
        """
        🧮 Automatically calculate MIDI note number from x,y coordinates
        Formula: note = x + (y * 10)
        """
        self.note = self.x + (y * 10)