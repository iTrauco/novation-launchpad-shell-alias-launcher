# Path: src/handlers/alias_handler.py
"""
🔧 Alias Handler Module
Handles the execution of shell aliases in a controlled environment.

Flow:
1. Imported by the main controller
2. Provides methods for executing shell aliases safely
3. Handles all shell-related operations and error management
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class AliasHandler:
    """
    🛠️ Handles shell alias execution and management
    """
    def __init__(self):
        # 🏠 Get user's home directory for shell config files
        self.home = str(Path.home())
        # 🐚 Default to zsh, but could be made configurable
        self.shell_path = '/bin/zsh'
    
    def execute(self, alias_name: str) -> bool:
        """
        🚀 Execute a shell alias in a controlled environment
        
        Args:
            alias_name (str): Name of the alias to execute
            
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            # Use login shell to ensure aliases are loaded
            command = f"{self.shell_path} -i -c '{alias_name}'"
            
            logger.debug(f"🔄 Executing alias: {alias_name}")
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable=self.shell_path,
                env=subprocess.os.environ.copy(),
                start_new_session=True  # Prevent keyboard interrupts from affecting parent
            )
            
            # Capture output but don't wait indefinitely
            stdout, stderr = process.communicate(timeout=5)
            
            if stdout:
                logger.debug(f"📤 Output: {stdout.decode().strip()}")
            if stderr:
                logger.warning(f"⚠️ Error: {stderr.decode().strip()}")
                
            return process.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Timeout while executing alias: {alias_name}")
            return False
        except Exception as e:
            logger.error(f"💥 Failed to execute alias {alias_name}: {e}")
            return False
        
        https://claude.ai/chat/b00befb3-b262-4e5e-b1c1-15cc3a9d272c