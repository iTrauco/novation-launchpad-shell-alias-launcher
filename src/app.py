# Path: src/app.py
"""
🎮 Main Application Module
Orchestrates all components and provides the main application interface.

Flow:
1. Entry point for the application
2. Initializes and connects all components
3. Manages application lifecycle
4. Handles shutdown and cleanup
"""

import logging
from typing import List, Tuple
import signal
from .config.config_manager import ConfigManager
from .managers.midi_manager import MIDIManager
from .managers.mapping_manager import MappingManager
from .handlers.button_handler import ButtonEventHandler

logger = logging.getLogger(__name__)

class LaunchpadApp:
    """
    🎯 Main application class
    """
    def __init__(self):
        # Initialize components
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        # Set up logging based on config
        logging.getLogger().setLevel(self.config.log_level)
        
        # Initialize managers
        self.midi_manager = MIDIManager()
        self.mapping_manager = MappingManager()
        self.button_handler = ButtonEventHandler(
            mapping_manager=self.mapping_manager,
            debug_mode=self.config.launchpad.debug_mode
        )
        
        # Setup signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        self._running = False
    
    def setup_midi_callback(self):
        """🎹 Setup MIDI event callback"""
        self.midi_manager.set_callback(
            lambda event, _: self.button_handler.handle_event(event[0])
        )
    
    def add_mapping(self, x: int, y: int, color: int, alias: str):
        """
        ➕ Add new button mapping and set button color
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            color (int): MIDI color code
            alias (str): Shell alias to execute
        """
        self.mapping_manager.add_mapping(x, y, color, alias)
        self.midi_manager.set_button_color(x, y, color)
        logger.info(f"✨ Added mapping: ({x}, {y}) -> {alias}")
    
    def start(self) -> bool:
        """
        🚀 Start the application
        
        Returns:
            bool: True if startup successful
        """
        try:
            # Validate configuration
            if not self.config_manager.validate_config():
                return False
                
            # Connect to Launchpad
            if not self.midi_manager.connect_launchpad(self.config.launchpad.port_name):
                return False
            
            # Setup MIDI callback
            self.setup_midi_callback()
            
            self._running = True
            logger.info("✅ Application started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start application: {e}")
            return False
    
    def _handle_shutdown(self, *args):
        """💫 Handle graceful shutdown"""
        logger.info("🔄 Shutting down...")
        self._running = False
        self.midi_manager.cleanup()
        logger.info("👋 Shutdown complete")
    
    def run(self):
        """🔄 Main application loop"""
        if not self.start():
            return
        
        logger.info("⌨️  Ready for input (Press Ctrl+C to exit)")
        
        try:
            while self._running:
                signal.pause()
        except KeyboardInterrupt:
            self._handle_shutdown()