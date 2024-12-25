# Path: src/managers/midi_manager.py
"""
🎼 MIDI Connection Manager Module
Handles MIDI device connection, port management, and communication.

Flow:
1. Discovers available MIDI devices
2. Manages connections to Launchpad
3. Handles MIDI I/O operations
4. Provides device status monitoring
"""

import rtmidi
import logging
from typing import Callable, Optional, List, Tuple
from dataclasses import dataclass
from ..utils.constants import MIDI_NOTE_ON

logger = logging.getLogger(__name__)

@dataclass
class MIDIPort:
    """📍 Represents a MIDI port connection"""
    name: str
    port_number: int
    is_input: bool

class MIDIManager:
    """
    🎹 Manages MIDI device connections and communications
    """
    def __init__(self):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.current_input_port: Optional[MIDIPort] = None
        self.current_output_port: Optional[MIDIPort] = None
        
    def list_devices(self) -> Tuple[List[str], List[str]]:
        """📋 Get lists of available input and output ports"""
        input_ports = self.midi_in.get_ports()
        output_ports = self.midi_out.get_ports()
        
        logger.info("🔍 Available MIDI Ports:")
        logger.info("📥 Inputs:")
        for i, port in enumerate(input_ports):
            logger.info(f"  {i}: {port}")
        logger.info("📤 Outputs:")
        for i, port in enumerate(output_ports):
            logger.info(f"  {i}: {port}")
            
        return input_ports, output_ports
    
    def connect_launchpad(self, port_name: str) -> bool:
        """
        🔌 Connect to Launchpad input and output ports
        
        Args:
            port_name (str): Name of the Launchpad MIDI port
            
        Returns:
            bool: True if connection successful
        """
        try:
            input_ports = self.midi_in.get_ports()
            output_ports = self.midi_out.get_ports()
            
            # Find port indices
            in_port_idx = input_ports.index(port_name)
            out_port_idx = output_ports.index(port_name)
            
            # Open ports
            self.midi_in.open_port(in_port_idx)
            self.midi_out.open_port(out_port_idx)
            
            # Store port info
            self.current_input_port = MIDIPort(port_name, in_port_idx, True)
            self.current_output_port = MIDIPort(port_name, out_port_idx, False)
            
            logger.info(f"🟢 Connected to Launchpad: {port_name}")
            return True
            
        except ValueError:
            logger.error(f"❌ Could not find Launchpad port: {port_name}")
            return False
        except Exception as e:
            logger.error(f"💥 Connection error: {e}")
            return False
    
    def set_callback(self, callback: Callable) -> None:
        """🎯 Set MIDI input callback function"""
        if self.current_input_port:
            self.midi_in.set_callback(callback)
            logger.debug("✅ MIDI callback set")
    
    def send_message(self, message: List[int]) -> None:
        """
        📤 Send MIDI message to device
        
        Args:
            message (List[int]): [status_byte, note, velocity]
        """
        if self.current_output_port:
            try:
                self.midi_out.send_message(message)
            except Exception as e:
                logger.error(f"❌ Failed to send MIDI message: {e}")
    
    def set_button_color(self, x: int, y: int, color: int) -> None:
        """
        🎨 Set color of specific button
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            color (int): MIDI color code
        """
        note = x + (y * 10)
        self.send_message([MIDI_NOTE_ON, note, color])
    
    def cleanup(self) -> None:
        """🧹 Clean up MIDI connections"""
        self.midi_in.close_port()
        self.midi_out.close_port()
        logger.info("🔌 MIDI connections closed")