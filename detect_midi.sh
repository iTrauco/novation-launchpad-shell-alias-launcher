# First, let's create and run the detection script
cat > detect_midi.py << 'EOL'
import rtmidi

def list_midi_ports():
    """List all available MIDI ports"""
    midi_in = rtmidi.MidiIn()
    midi_out = rtmidi.MidiOut()
    
    print("\n🎹 Available MIDI Ports:")
    print("\n📥 Input Ports:")
    ports = midi_in.get_ports()
    for i, port in enumerate(ports):
        print(f"  {i}: {port}")
        if "launchpad" in port.lower():
            print(f"  ✨ LAUNCHPAD DETECTED! Use this name in your .env file:")
            print(f"  LAUNCHPAD_PORT=\"{port}\"")
    
    print("\n📤 Output Ports:")
    ports = midi_out.get_ports()
    for i, port in enumerate(ports):
        print(f"  {i}: {port}")

if __name__ == "__main__":
    list_midi_ports()
EOL

# Run the detection script
python detect_midi.py