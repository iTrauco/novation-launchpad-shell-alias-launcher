# Path: src/handlers/button_handler.py
"""
🎹 Button Event Handler Module
Processes MIDI events from the Launchpad and manages button states.

Flow:
1. Receives raw MIDI events from controller
2. Processes button press/release events
3. Manages button states and feedback
4. Triggers appropriate mapping executions
"""

import logging
from typing import Callable, Dict, Optional
from dataclasses import dataclass
from ..managers.mapping_manager import MappingManager
from ..utils.constants import MIDI_NOTE_ON, MIDI_NOTE_OFF

logger = logging.getLogger(__name__)

@dataclass
class ButtonState:
    """📊 Tracks the state of a button"""
    is_pressed: bool = False
    last_velocity: int = 0
    press_count: int = 0

class ButtonEventHandler:
    """
    🎛️ Handles MIDI button events and manages button states
    """
    def __init__(self, mapping_manager: MappingManager, debug_mode: bool = False):
        self._mapping_manager = mapping_manager
        self._button_states: Dict[int, ButtonState] = {}
        self.debug_mode = debug_mode
        
    def _get_xy_from_note(self, note: int) -> tuple[int, int]:
        """🧮 Convert MIDI note to x,y coordinates"""
        x = note % 10
        y = note // 10
        return x, y
    
    def handle_event(self, message: list) -> None:
        """
        🎯 Process incoming MIDI message
        
        Args:
            message (list): [status_byte, note, velocity]
        """
        if len(message) != 3:
            return
            
        status, note, velocity = message
        x, y = self._get_xy_from_note(note)
        
        # 🔍 Debug mode output
        if self.debug_mode:
            logger.info(f"🔔 Button Event: ({x}, {y}) - "
                       f"{'Pressed' if velocity > 0 else 'Released'} "
                       f"[Note: {note}, Velocity: {velocity}]")
        
        # Track button state
        if note not in self._button_states:
            self._button_states[note] = ButtonState()
            
        state = self._button_states[note]
        
        if velocity > 0:  # Button Press
            if not state.is_pressed:  # Avoid repeated presses
                state.is_pressed = True
                state.press_count += 1
                self._handle_press(x, y)
        else:  # Button Release
            state.is_pressed = False
            self._handle_release(x, y)
            
        state.last_velocity = velocity
    
    def _handle_press(self, x: int, y: int) -> None:
        """🔽 Handle button press event"""
        self._mapping_manager.execute_mapping(x, y)
    
    def _handle_release(self, x: int, y: int) -> None:
        """🔼 Handle button release event"""
        # Could be used for long-press detection or other features
        pass
    
    def get_button_info(self, note: int) -> Optional[dict]:
        """ℹ️ Get debug information about a button"""
        if note in self._button_states:
            x, y = self._get_xy_from_note(note)
            state = self._button_states[note]
            return {
                'coordinates': (x, y),
                'press_count': state.press_count,
                'is_pressed': state.is_pressed,
                'has_mapping': bool(self._mapping_manager.get_mapping(x, y))
            }
        return None