"""
🎮 Launchpad Alias Controller
Maps Launchpad buttons to system aliases with visual feedback.
"""

from src.app import LaunchpadApp
from src.utils.constants import Colors
import logging

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Initializing Launchpad Alias Controller...")
    
    # Initialize app with debug mode
    app = LaunchpadApp()
    
    # Map your existing aliases with meaningful colors
    alias_mappings = [
        # x, y, color, alias
        # Claude instances in the top row
        (0, 0, Colors.PURPLE, "claude1"),  # Purple for AI
        (1, 0, Colors.BLUE, "claude2"),    # Different shade for each instance
        (2, 0, Colors.CYAN, "claude3"),
        (3, 0, Colors.GREEN, "claude4"),
        
        # Utility commands in the second row
        (0, 1, Colors.YELLOW, "gifme"),    # Yellow for utility
    ]
    
    # Register mappings
    for x, y, color, alias in alias_mappings:
        print(f"🔧 Mapping button ({x}, {y}) to alias '{alias}'")
        app.add_mapping(x, y, color, alias)
        
    print("\n🎮 Alias Controller Active")
    print("=========================")
    print("Mapped Aliases:")
    for x, y, _, alias in alias_mappings:
        print(f"  • ({x}, {y}) -> {alias}")
    print("\n💡 Top Row: Claude Instances (Purple -> Green)")
    print("💡 Second Row: Utilities (Yellow)")
    print("\n📝 Debug mode active - all button presses will be logged")
    print("⌨️  Press Ctrl+C to exit\n")
    
    # Run the app
    app.run()

if __name__ == "__main__":
    main()
