"""
🔧 Alias Handler Module
Handles the execution of shell aliases in a controlled environment.
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional
import os

logger = logging.getLogger(__name__)

class AliasHandler:
    """Handles shell alias execution and management"""
    
    def __init__(self, shell_path: str = '/bin/zsh'):
        self.home = str(Path.home())
        self.shell_path = shell_path
        
    def execute(self, alias_name: str) -> bool:
        """
        🚀 Execute a shell alias
        
        Args:
            alias_name: Name of the alias to execute
            
        Returns:
            bool: True if execution successful
        """
        try:
            command = f"{self.shell_path} -i -c '{alias_name}'"
            
            logger.debug(f"🔄 Executing: {alias_name}")
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable=self.shell_path,
                env=os.environ.copy(),
                start_new_session=True
            )
            
            stdout, stderr = process.communicate(timeout=5)
            
            if stdout:
                logger.debug(f"📤 Output: {stdout.decode().strip()}")
            if stderr:
                logger.warning(f"⚠️ Error: {stderr.decode().strip()}")
                
            success = process.returncode == 0
            if success:
                logger.info(f"✅ Successfully executed: {alias_name}")
            else:
                logger.error(f"❌ Failed to execute: {alias_name}")
                
            return success
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Timeout executing: {alias_name}")
            return False
        except Exception as e:
            logger.error(f"💥 Error executing {alias_name}: {e}")
            return False
