Let's create the mapping manager module that will handle the relationships between buttons and aliases:
pythonCopy# Path: src/managers/mapping_manager.py
"""
🗺️ Mapping Manager Module
Manages the relationships between Launchpad buttons and shell aliases.

Flow:
1. Imported by the main controller
2. Stores and manages button-to-alias mappings
3. Provides interface for adding and retrieving mappings
4. Validates mapping configurations
"""

import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from ..models.button import LaunchpadButton
from ..handlers.alias_handler import AliasHandler

logger = logging.getLogger(__name__)

@dataclass
class ButtonMapping:
    """🔗 Represents a mapping between a button and an alias"""
    button: LaunchpadButton
    alias: str
    is_active: bool = True

class MappingManager:
    """
    🎮 Manages button-to-alias mappings and their states
    """
    def __init__(self):
        self._mappings: Dict[Tuple[int, int], ButtonMapping] = {}
        self._alias_handler = AliasHandler()
        
    def add_mapping(self, x: int, y: int, color: int, alias: str) -> ButtonMapping:
        """
        ➕ Create a new button-to-alias mapping
        
        Args:
            x (int): X coordinate on Launchpad
            y (int): Y coordinate on Launchpad
            color (int): MIDI color code
            alias (str): Shell alias to execute
            
        Returns:
            ButtonMapping: The created mapping
        """
        button = LaunchpadButton(x=x, y=y, color=color)
        mapping = ButtonMapping(button=button, alias=alias)
        self._mappings[(x, y)] = mapping
        logger.info(f"🔵 Created mapping: ({x}, {y}) -> {alias}")
        return mapping
    
    def get_mapping(self, x: int, y: int) -> Optional[ButtonMapping]:
        """📍 Get mapping for specific coordinates"""
        return self._mappings.get((x, y))
    
    def execute_mapping(self, x: int, y: int) -> bool:
        """
        🎯 Execute the alias associated with given coordinates
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        mapping = self.get_mapping(x, y)
        if mapping and mapping.is_active:
            logger.debug(f"🎲 Triggering alias for button ({x}, {y})")
            return self._alias_handler.execute(mapping.alias)
        return False
    
    def toggle_mapping(self, x: int, y: int) -> bool:
        """🔄 Toggle the active state of a mapping"""
        mapping = self.get_mapping(x, y)
        if mapping:
            mapping.is_active = not mapping.is_active
            logger.info(f"{'🟢' if mapping.is_active else '🔴'} "
                       f"Mapping ({x}, {y}) -> {mapping.alias} "
                       f"{'activated' if mapping.is_active else 'deactivated'}")
            return True
        return False