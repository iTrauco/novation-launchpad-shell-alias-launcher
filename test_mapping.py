"""
🧪 Test Mapping Script with Debug Logging
"""

from src.app import LaunchpadApp
from src.utils.constants import Colors
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Initializing Launchpad Test...")
    
    # Initialize app with debug mode
    app = LaunchpadApp()
    
    # Simple test mappings
    test_mappings = [
        # x, y, color, alias
        (0, 0, Colors.RED, "ls"),     # Top-left red button
        (1, 0, Colors.GREEN, "pwd"),   # Next to it, green button
        (0, 1, Colors.BLUE, "date")    # Below red button, blue
    ]
    
    # Register mappings
    for x, y, color, alias in test_mappings:
        print(f"🔧 Mapping button ({x}, {y}) to '{alias}'")
        app.add_mapping(x, y, color, alias)
        
    print("\n🎮 Test Configuration Active")
    print("===========================")
    print("Mapped Buttons:")
    for x, y, _, alias in test_mappings:
        print(f"  • ({x}, {y}) -> {alias}")
    print("\n📝 Press any button to see debug output")
    print("⌨️  Press Ctrl+C to exit\n")
    
    # Run the app
    app.run()

if __name__ == "__main__":
    main()
