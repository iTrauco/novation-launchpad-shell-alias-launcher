"""
🎼 MIDI Manager Module
Handles MIDI device connection and communication.
"""

import rtmidi
import logging
from typing import Callable, Optional, List, Dict
from ..utils.constants import MIDI_NOTE_ON, Colors

logger = logging.getLogger(__name__)

class MIDIManager:
    """Manages MIDI device connections and communications"""
    
    def __init__(self):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.port_name: Optional[str] = None
        self.callbacks: Dict[int, Callable] = {}
        
    def list_devices(self) -> List[str]:
        """📋 List available MIDI devices"""
        input_ports = self.midi_in.get_ports()
        logger.info("🔍 Available MIDI Ports:")
        for i, port in enumerate(input_ports):
            logger.info(f"  {i}: {port}")
        return input_ports
    
    def connect(self, port_name: str) -> bool:
        """
        🔌 Connect to MIDI device
        
        Args:
            port_name: Name of the MIDI port to connect to
        """
        try:
            in_ports = self.midi_in.get_ports()
            out_ports = self.midi_out.get_ports()
            
            in_port_idx = in_ports.index(port_name)
            out_port_idx = out_ports.index(port_name)
            
            self.midi_in.open_port(in_port_idx)
            self.midi_out.open_port(out_port_idx)
            self.port_name = port_name
            
            logger.info(f"✅ Connected to: {port_name}")
            return True
            
        except ValueError:
            logger.error(f"❌ Port not found: {port_name}")
            return False
        except Exception as e:
            logger.error(f"💥 Connection error: {e}")
            return False
    
    def set_callback(self, callback: Callable):
        """🎯 Set MIDI input callback"""
        if self.port_name:
            self.midi_in.set_callback(callback)
            logger.debug("✅ Callback set")
    
    def send_message(self, message: List[int]):
        """📤 Send MIDI message"""
        try:
            self.midi_out.send_message(message)
        except Exception as e:
            logger.error(f"❌ Failed to send MIDI message: {e}")
    
    def set_button_color(self, x: int, y: int, color: int):
        """🎨 Set button color"""
        note = x + (y * 10)
        self.send_message([MIDI_NOTE_ON, note, color])
    
    def reset_colors(self):
        """🧹 Reset all button colors"""
        for x in range(8):
            for y in range(8):
                self.set_button_color(x, y, Colors.OFF)
    
    def cleanup(self):
        """🧹 Clean up MIDI connections"""
        if self.port_name:
            self.reset_colors()
            self.midi_in.close_port()
            self.midi_out.close_port()
            logger.info("👋 MIDI connections closed")
