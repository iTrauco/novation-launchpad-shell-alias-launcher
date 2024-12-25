# Path: src/config/config_manager.py
"""
⚙️ Configuration Manager Module
Handles application settings, environment variables, and runtime configuration.

Flow:
1. Loads environment variables
2. Provides default configurations
3. Validates settings
4. Makes configuration accessible throughout the application
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

@dataclass
class LaunchpadConfig:
    """📝 Launchpad-specific configuration"""
    port_name: str
    debug_mode: bool
    grid_size: int = 8

@dataclass
class ShellConfig:
    """🐚 Shell-specific configuration"""
    shell_path: str
    timeout: int
    work_dir: Optional[str]

@dataclass
class AppConfig:
    """🔧 Complete application configuration"""
    launchpad: LaunchpadConfig
    shell: ShellConfig
    log_level: str

class ConfigManager:
    """
    🎛️ Manages application configuration
    """
    def __init__(self, env_file: str = '.env'):
        self._load_environment(env_file)
        self.config = self._initialize_config()
        
    def _load_environment(self, env_file: str) -> None:
        """📥 Load environment variables from file"""
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"✅ Loaded environment from {env_file}")
        else:
            logger.warning(f"⚠️ No {env_file} found, using defaults")
    
    def _initialize_config(self) -> AppConfig:
        """🏗️ Initialize configuration with defaults and env vars"""
        launchpad_config = LaunchpadConfig(
            port_name=os.getenv('LAUNCHPAD_PORT', 'Launchpad Mini MK3'),
            debug_mode=os.getenv('DEBUG_MODE', 'True').lower() == 'true',
            grid_size=int(os.getenv('GRID_SIZE', '8'))
        )
        
        shell_config = ShellConfig(
            shell_path=os.getenv('SHELL_PATH', '/bin/zsh'),
            timeout=int(os.getenv('SHELL_TIMEOUT', '5')),
            work_dir=os.getenv('WORK_DIR')
        )
        
        return AppConfig(
            launchpad=launchpad_config,
            shell=shell_config,
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )
    
    def get_config(self) -> AppConfig:
        """📋 Get current configuration"""
        return self.config
    
    def validate_config(self) -> bool:
        """
        ✅ Validate current configuration
        
        Returns:
            bool: True if configuration is valid
        """
        try:
            # Validate Launchpad settings
            if not self.config.launchpad.port_name:
                logger.error("❌ Launchpad port name not set")
                return False
            
            # Validate Shell settings
            shell_path = Path(self.config.shell.shell_path)
            if not shell_path.exists():
                logger.error(f"❌ Shell path not found: {shell_path}")
                return False
            
            # Validate working directory if set
            if self.config.shell.work_dir:
                work_dir = Path(self.config.shell.work_dir)
                if not work_dir.exists():
                    logger.error(f"❌ Working directory not found: {work_dir}")
                    return False
            
            logger.info("✅ Configuration validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration validation failed: {e}")
            return False