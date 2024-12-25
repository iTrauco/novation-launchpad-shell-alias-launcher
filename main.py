# Path: main.py
"""
🚀 Main Entry Point
Demonstrates how to use the LaunchpadApp with example mappings.

Flow:
1. Load application
2. Define button mappings
3. Start the application
4. Keep running until interrupted
"""

import logging
from src.app import LaunchpadApp
from src.utils.constants import Colors

# Example mapping structure
BUTTON_MAPPINGS = [
    # Format: (x, y, color, alias)
    # Top Row (Quick Actions)
    (0, 0, Colors.RED, "open_chrome"),     # 🔴 Opens Chrome
    (1, 0, Colors.GREEN, "code_editor"),    # 💚 Opens VS Code
    
    # Second Row (Development Tools)
    (0, 1, Colors.BLUE, "run_tests"),      # 💙 Runs test suite
    (1, 1, Colors.YELLOW, "git_status"),   # 💛 Shows git status
    
    # Third Row (Custom Scripts)
    (0, 2, Colors.RED, "deploy_app"),      # 🔴 Deploy application
    (1, 2, Colors.GREEN, "backup_db"),     # 💚 Backup database
]

def main():
    """🎯 Main application entry point"""
    try:
        # Initialize application
        app = LaunchpadApp()
        
        # Register all mappings
        for x, y, color, alias in BUTTON_MAPPINGS:
            app.add_mapping(x, y, color, alias)
            
        # Print startup message
        print("\n🎹 Launchpad Shell Controller")
        print("=============================")
        print("🔵 Debug Mode:", "Enabled" if app.config.launchpad.debug_mode else "Disabled")
        print("\n📍 Mapped Buttons:")
        for x, y, _, alias in BUTTON_MAPPINGS:
            print(f"  • ({x}, {y}): {alias}")
        print("\n⌨️  Press any unmapped button to see its coordinates")
        print("👋 Press Ctrl+C to exit\n")
        
        # Run the application
        app.run()
        
    except Exception as e:
        logging.error(f"💥 Application error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())