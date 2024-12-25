"""
🎮 Button Handler Module
Processes MIDI button events and manages button states.
"""

import logging
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from ..models.button import LaunchpadButton
from ..utils.constants import MIDI_NOTE_ON, MIDI_NOTE_OFF

logger = logging.getLogger(__name__)

@dataclass
class ButtonState:
    """📊 Tracks button state"""
    is_pressed: bool = False
    press_count: int = 0
    last_velocity: int = 0

class ButtonHandler:
    def __init__(self, debug_mode: bool = False):
        self.button_states: Dict[int, ButtonState] = {}
        self.callbacks: Dict[int, Callable] = {}
        self.debug_mode = debug_mode
        
    def _get_xy(self, note: int) -> tuple[int, int]:
        """🧮 Convert MIDI note to x,y coordinates"""
        x = note % 10
        y = note // 10
        return x, y
    
    def register_callback(self, note: int, callback: Callable):
        """🎯 Register callback for button"""
        self.callbacks[note] = callback
        
    def handle_event(self, message: list):
        """
        🎯 Process MIDI message
        
        Args:
            message: [status_byte, note, velocity]
        """
        if len(message) != 3:
            return
            
        status, note, velocity = message
        x, y = self._get_xy(note)
        
        # Initialize button state if needed
        if note not in self.button_states:
            self.button_states[note] = ButtonState()
        
        state = self.button_states[note]
        
        # Debug output
        if self.debug_mode:
            logger.info(
                f"🔔 Button Event: ({x}, {y}) - "
                f"{'Pressed' if velocity > 0 else 'Released'} "
                f"[Note: {note}, Velocity: {velocity}]"
            )
        
        # Handle button press/release
        if velocity > 0:  # Button Press
            if not state.is_pressed:  # Avoid repeat triggers
                state.is_pressed = True
                state.press_count += 1
                if note in self.callbacks:
                    self.callbacks[note]()
        else:  # Button Release
            state.is_pressed = False
        
        state.last_velocity = velocity
    
    def get_button_info(self, note: int) -> Optional[dict]:
        """ℹ️ Get debug information about button"""
        if note in self.button_states:
            x, y = self._get_xy(note)
            state = self.button_states[note]
            return {
                'coordinates': (x, y),
                'press_count': state.press_count,
                'is_pressed': state.is_pressed,
                'has_callback': note in self.callbacks
            }
        return None
