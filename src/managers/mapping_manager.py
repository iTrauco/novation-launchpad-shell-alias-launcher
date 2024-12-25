"""
🗺️ Mapping Manager Module
Manages relationships between buttons and shell aliases.
"""

import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from ..models.button import LaunchpadButton
from ..handlers.alias_handler import AliasHandler
from ..utils.constants import Colors

logger = logging.getLogger(__name__)

@dataclass
class ButtonMapping:
    """🔗 Represents button-to-alias mapping"""
    button: LaunchpadButton
    alias: str
    active: bool = True

class MappingManager:
    """Manages button-to-alias mappings and their states"""
    
    def __init__(self, alias_handler: Optional[AliasHandler] = None):
        self._mappings: Dict[Tuple[int, int], ButtonMapping] = {}
        self._alias_handler = alias_handler or AliasHandler()
        
    def create_mapping(self, x: int, y: int, color: int, alias: str) -> ButtonMapping:
        """
        ➕ Create new button mapping
        
        Args:
            x: X coordinate
            y: Y coordinate
            color: Button color
            alias: Shell alias to execute
        """
        button = LaunchpadButton(x=x, y=y, color=color)
        mapping = ButtonMapping(button=button, alias=alias)
        self._mappings[(x, y)] = mapping
        logger.info(f"✨ Created mapping: ({x}, {y}) -> {alias}")
        return mapping
    
    def get_mapping(self, x: int, y: int) -> Optional[ButtonMapping]:
        """📍 Get mapping for coordinates"""
        return self._mappings.get((x, y))
    
    def execute_mapping(self, x: int, y: int) -> bool:
        """
        🎯 Execute mapping's alias
        
        Returns:
            bool: True if execution successful
        """
        mapping = self.get_mapping(x, y)
        if mapping and mapping.active:
            logger.debug(f"🔄 Executing alias for button ({x}, {y})")
            return self._alias_handler.execute(mapping.alias)
        return False
    
    def toggle_mapping(self, x: int, y: int) -> bool:
        """🔄 Toggle mapping active state"""
        mapping = self.get_mapping(x, y)
        if mapping:
            mapping.active = not mapping.active
            status = "activated" if mapping.active else "deactivated"
            logger.info(f"{'🟢' if mapping.active else '🔴'} Mapping ({x}, {y}) {status}")
            return True
        return False
    
    def list_mappings(self) -> list:
        """📋 List all current mappings"""
        return [
            {
                'coordinates': (x, y),
                'alias': mapping.alias,
                'active': mapping.active
            }
            for (x, y), mapping in self._mappings.items()
        ]
