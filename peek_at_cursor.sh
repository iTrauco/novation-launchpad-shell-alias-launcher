#!/bin/bash

# 🎥 Peek Launcher Script
# 🛠️  Usage:
#   1️⃣ Install dependencies: `sudo apt install peek xdotool x11-utils`
#   2️⃣ Save this script as `peek_at_cursor.sh` and make it executable.
#      Example: `chmod +x ~/scripts/peek_at_cursor.sh`
#   3️⃣ Run the script: `~/scripts/peek_at_cursor.sh`
#   4️⃣ Peek will open at your cursor's position and stay open for multiple recordings.

# Close any existing Peek windows
PEEK_WINDOWS=$(xdotool search --name "Peek")
if [ -n "$PEEK_WINDOWS" ]; then
    echo "Closing existing Peek windows..."
    for WINDOW in $PEEK_WINDOWS; do
        xdotool windowclose "$WINDOW"
    done
    sleep 1  # Allow time for the windows to close
fi

# Launch Peek
peek &

# Wait for Peek to open
sleep 2

# Get cursor position
CURSOR_POS=$(xdotool getmouselocation --shell)
CURSOR_X=$(echo "$CURSOR_POS" | grep "X=" | cut -d '=' -f2)
CURSOR_Y=$(echo "$CURSOR_POS" | grep "Y=" | cut -d '=' -f2)

# Get monitor information using xrandr
MONITORS=$(xrandr | grep " connected")

TARGET_X=0
TARGET_Y=0
FOUND=false

while IFS= read -r MONITOR; do
    # Extract monitor geometry
    GEOMETRY=$(echo "$MONITOR" | grep -oP "\d+x\d+\+\d+\+\d+")
    WIDTH=$(echo "$GEOMETRY" | cut -d'x' -f1)
    HEIGHT=$(echo "$GEOMETRY" | cut -d'x' -f2 | cut -d'+' -f1)
    X_POS=$(echo "$GEOMETRY" | cut -d'+' -f2)
    Y_POS=$(echo "$GEOMETRY" | cut -d'+' -f3)

    # Check if cursor is within monitor bounds
    if (( CURSOR_X >= X_POS && CURSOR_X < (X_POS + WIDTH) &&
          CURSOR_Y >= Y_POS && CURSOR_Y < (Y_POS + HEIGHT) )); then
        TARGET_X=$X_POS
        TARGET_Y=$Y_POS
        FOUND=true
        break
    fi
done <<< "$MONITORS"

if [ "$FOUND" = false ]; then
    echo "Error: Could not determine the monitor for the cursor."
    exit 1
fi

echo "Cursor is on monitor with geometry: $TARGET_X, $TARGET_Y"

# Get the new Peek window ID
PEEK_WINDOW=$(xdotool search --name "Peek" | tail -1)

if [ -z "$PEEK_WINDOW" ]; then
    echo "Error: Peek window not found."
    exit 1
fi

# Move Peek window to the cursor's display
xdotool windowmove "$PEEK_WINDOW" "$CURSOR_X" "$CURSOR_Y"

echo "Peek launched and moved to cursor position ($CURSOR_X, $CURSOR_Y) on monitor."

# Monitor Peek process and close it after recording
PEEK_PID=$(pgrep -n peek)  # Get the most recent Peek process ID

if [ -z "$PEEK_PID" ]; then
    echo "Error: Peek process not found."
    exit 1
fi

echo "Monitoring Peek process (PID: $PEEK_PID)..."

# Wait for Peek to exit
while kill -0 "$PEEK_PID" 2>/dev/null; do
    sleep 1  # Check every second
done

echo "Peek process has exited. Closing the Peek window (if still open)."

# Ensure the Peek window is closed
PEEK_WINDOWS=$(xdotool search --name "Peek")
if [ -n "$PEEK_WINDOWS" ]; then
    for WINDOW in $PEEK_WINDOWS; do
        xdotool windowclose "$WINDOW"
    done
fi

echo "Peek has been closed."

