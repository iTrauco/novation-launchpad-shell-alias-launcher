# # Path: debug_colors.py
# """
# 🔍 Comprehensive Color Testing Script
# Tests multiple approaches to controlling Launchpad lights
# """

# import rtmidi
# import time
# import logging
# from src.utils.constants import Colors, MIDI_NOTE_ON
# from src.app import LaunchpadApp

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# logger = logging.getLogger(__name__)

# def test_suite():
#     tests = [
#         # Test 1: Direct MIDI messaging
#         {
#             'name': "Direct MIDI Output",
#             'description': """
#             Attempts to send color messages directly via MIDI out.
#             Will try to turn top-left button red.
#             """,
#             'code': direct_midi_test
#         },
        
#         # Test 2: Through LaunchpadApp
#         {
#             'name': "LaunchpadApp Integration",
#             'description': """
#             Uses our LaunchpadApp class to set colors.
#             Should set first row of buttons to different colors.
#             """,
#             'code': app_test
#         },
        
#         # Test 3: Raw MIDI messages
#         {
#             'name': "Raw MIDI Messages",
#             'description': """
#             Sends raw MIDI messages in different formats.
#             Tests various message structures.
#             """,
#             'code': raw_midi_test
#         },
        
#         # Test 4: Channel cycling
#         {
#             'name': "MIDI Channel Cycling",
#             'description': """
#             Tests sending messages on different MIDI channels.
#             Cycles through channels 0-15.
#             """,
#             'code': channel_cycle_test
#         },
        
#         # Test 5: Velocity variation
#         {
#             'name': "Velocity Testing",
#             'description': """
#             Tests different velocity values for color intensity.
#             Ranges from 0-127 on one button.
#             """,
#             'code': velocity_test
#         }
#     ]
    
#     for i, test in enumerate(tests, 1):
#         print(f"\n{'='*50}")
#         print(f"Test {i}: {test['name']}")
#         print(f"{'='*50}")
#         print(test['description'])
#         input("\nPress Enter to run this test...")
        
#         try:
#             test['code']()
#             result = input("\nDid you see any lights change? (y/n): ").lower()
#             print(f"Test {i} Result: {'✅ WORKED' if result == 'y' else '❌ FAILED'}")
#         except Exception as e:
#             print(f"❌ Test failed with error: {e}")
        
#         input("\nPress Enter for next test...")

# def direct_midi_test():
#     midi_out = rtmidi.MidiOut()
#     port_name = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1"
#     ports = midi_out.get_ports()
#     port_idx = ports.index(port_name)
#     midi_out.open_port(port_idx)
    
#     # Try top-left button
#     midi_out.send_message([MIDI_NOTE_ON, 0, Colors.RED])
#     time.sleep(0.5)
#     midi_out.close_port()

# def app_test():
#     app = LaunchpadApp()
#     colors = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW]
#     for i, color in enumerate(colors):
#         app.midi_manager.set_button_color(i, 0, color)
#         time.sleep(0.2)

# def raw_midi_test():
#     midi_out = rtmidi.MidiOut()
#     port_name = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1"
#     port_idx = midi_out.get_ports().index(port_name)
#     midi_out.open_port(port_idx)
    
#     # Test different message formats
#     messages = [
#         [0x90, 0, Colors.RED],  # Note On
#         [0x90, 1, Colors.GREEN],  # Different note
#         [144, 2, Colors.BLUE],  # Note On in decimal
#         [146, 3, Colors.YELLOW]  # Channel 2
#     ]
    
#     for msg in messages:
#         print(f"Sending message: {msg}")
#         midi_out.send_message(msg)
#         time.sleep(0.5)
    
#     midi_out.close_port()

# def channel_cycle_test():
#     midi_out = rtmidi.MidiOut()
#     port_name = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1"
#     port_idx = midi_out.get_ports().index(port_name)
#     midi_out.open_port(port_idx)
    
#     # Try each channel
#     for channel in range(16):
#         status = 0x90 + channel
#         print(f"Testing channel {channel} (status: {status})")
#         midi_out.send_message([status, 0, Colors.RED])
#         time.sleep(0.3)
    
#     midi_out.close_port()

# def velocity_test():
#     midi_out = rtmidi.MidiOut()
#     port_name = "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 20:1"
#     port_idx = midi_out.get_ports().index(port_name)
#     midi_out.open_port(port_idx)
    
#     # Test velocity ranges
#     for velocity in range(0, 128, 16):
#         print(f"Testing velocity: {velocity}")
#         midi_out.send_message([MIDI_NOTE_ON, 0, velocity])
#         time.sleep(0.3)
    
#     midi_out.close_port()

# if __name__ == "__main__":
#     print("🎨 Launchpad Color Debug Suite")
#     print("Testing multiple approaches to controlling Launchpad lights")
#     input("Press Enter to begin testing...")
#     test_suite()

# Path: color_test.py
"""
🎨 Launchpad Color Test Script
Tests basic button color functionality.
"""

from src.app import LaunchpadApp
from src.utils.constants import Colors
import logging
import time

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🎨 Starting Color Test...")
    app = LaunchpadApp()
    
    # Create simple color pattern
    color_pattern = [
        # Top row
        (6, 0, Colors.RED),    # Red
        (1, 0, Colors.GREEN),  # Green
        (2, 0, Colors.BLUE),   # Blue
        (3, 0, Colors.YELLOW)  # Yellow
    ]
    
    # Light up buttons
    for x, y, color in color_pattern:
        print(f"Setting button ({x}, {y}) to color value: {color}")
        app.midi_manager.set_button_color(x, y, color)
        time.sleep(0.1)  # Small delay between settings
    
    print("\n🔍 Color Test Active")
    print("===================")
    print("Colors set for:")
    for x, y, color in color_pattern:
        print(f"  • ({x}, {y}) - Color Value: {color}")
    print("\nCheck if you see the colors on your Launchpad")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()