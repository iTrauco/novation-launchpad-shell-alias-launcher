# """
# 🎼 MIDI Manager Module
# Handles MIDI device connection and communication.
# """

# import rtmidi
# import logging
# from typing import Callable, Optional, List, Dict
# from ..utils.constants import MIDI_NOTE_ON, Colors

# logger = logging.getLogger(__name__)

# class MIDIManager:
#     def __init__(self):
#         self.midi_in = rtmidi.MidiIn()
#         self.midi_out = rtmidi.MidiOut()
#         self.port_name: Optional[str] = None
#         self.callbacks: Dict[int, Callable] = {}
        
#     def connect(self, port_name: str) -> bool:
#         """🔌 Connect to MIDI device"""
#         try:
#             in_ports = self.midi_in.get_ports()
#             out_ports = self.midi_out.get_ports()
            
#             logger.debug(f"Attempting to connect to {port_name}")
#             logger.debug(f"Available input ports: {in_ports}")
#             logger.debug(f"Available output ports: {out_ports}")
            
#             in_port_idx = in_ports.index(port_name)
#             out_port_idx = out_ports.index(port_name)
            
#             self.midi_in.open_port(in_port_idx)
#             self.midi_out.open_port(out_port_idx)
#             self.port_name = port_name
            
#             logger.info(f"✅ Connected to: {port_name}")
#             return True
            
#         except ValueError:
#             logger.error(f"❌ Port not found: {port_name}")
#             return False
#         except Exception as e:
#             logger.error(f"💥 Connection error: {e}")
#             return False
    
#     def set_button_color(self, x: int, y: int, color: int):
#         """🎨 Set button color with detailed logging"""
#         try:
#             note = x + (y * 10)
#             message = [MIDI_NOTE_ON, note, color]
#             logger.debug(f"Setting color: x={x}, y={y}, note={note}, color={color}")
#             logger.debug(f"Sending MIDI message: {message}")
#             self.midi_out.send_message(message)
#         except Exception as e:
#             logger.error(f"Failed to set button color: {e}")
    
#     def send_message(self, message: List[int]):
#         """📤 Send MIDI message with logging"""
#         try:
#             logger.debug(f"Sending raw MIDI message: {message}")
#             self.midi_out.send_message(message)
#         except Exception as e:
#             logger.error(f"Failed to send MIDI message: {e}")
# Path: src/managers/midi_manager.py
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
       
   def connect(self, port_name: str) -> bool:
       """🔌 Connect to MIDI device"""
       try:
           in_ports = self.midi_in.get_ports()
           out_ports = self.midi_out.get_ports()
           
           logger.debug(f"Attempting to connect to {port_name}")
           logger.debug(f"Available input ports: {in_ports}")
           logger.debug(f"Available output ports: {out_ports}")
           
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
       try:
           if self.port_name:
               self.midi_in.set_callback(callback)
               logger.debug("✅ MIDI callback set successfully")
           else:
               logger.error("❌ Cannot set callback - MIDI port not connected")
       except Exception as e:
           logger.error(f"❌ Failed to set callback: {e}")

   def set_button_color(self, x: int, y: int, color: int):
       """🎨 Set button color with detailed logging"""
       try:
           note = x + (y * 10)
           message = [MIDI_NOTE_ON, note, color]
           logger.debug(f"Setting color: x={x}, y={y}, note={note}, color={color}")
           logger.debug(f"Sending MIDI message: {message}")
           self.midi_out.send_message(message)
       except Exception as e:
           logger.error(f"Failed to set button color: {e}")
   
   def send_message(self, message: List[int]):
       """📤 Send MIDI message with logging"""
       try:
           logger.debug(f"Sending raw MIDI message: {message}")
           self.midi_out.send_message(message)
       except Exception as e:
           logger.error(f"Failed to send MIDI message: {e}")

   def reset_colors(self):
       """🧹 Reset all button colors to off"""
       try:
           for x in range(8):
               for y in range(8):
                   self.set_button_color(x, y, Colors.OFF)
           logger.debug("✨ Reset all button colors")
       except Exception as e:
           logger.error(f"Failed to reset colors: {e}")

   def cleanup(self):
       """🧹 Clean up MIDI connections"""
       try:
           if self.port_name:
               self.reset_colors()
               self.midi_in.close_port()
               self.midi_out.close_port()
               logger.info("👋 MIDI connections closed")
               self.port_name = None
       except Exception as e:
           logger.error(f"Error during cleanup: {e}")