#!/bin/bash

# Paths to scripts (adjust to your directory)
MAIN_APP="$HOME/Desktop/Crosshair V3/Crosshair_v5_tkinter.py"
TOGGLE_SCRIPT="$HOME/Desktop/Crosshair V3/Red_dot_toggle.py"
LOG_FILE="$HOME/Desktop/Crosshair V3/Red_dot_toggle.log"

# Ensure absolute paths
MAIN_APP=$(realpath "$MAIN_APP")
TOGGLE_SCRIPT=$(realpath "$TOGGLE_SCRIPT")
LOG_FILE=$(realpath "$LOG_FILE" 2>/dev/null || echo "$HOME/red_dot_crosshair/toggle_red_dot.log")

# Clear the log file
if [ -f "$LOG_FILE" ]; then
    : > "$LOG_FILE"  # Truncate to zero length
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleared log file" >> "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Error: Failed to clear log file" >> "/tmp/toggle_red_dot_fallback.log"
        exit 1
    fi
else
    touch "$LOG_FILE"  # Create if it doesn't exist
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Created log file" >> "$LOG_FILE"
fi

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if log file is writable
if ! touch "$LOG_FILE" 2>/dev/null; then
    log "Error: Cannot write to log file $LOG_FILE"
    exit 1
fi

log "Starting toggle_red_dot.sh"

# Check if Python is available
if ! command -v python3 &>/dev/null; then
    log "Error: python3 not found"
    exit 1
fi

# Check if scripts exist
if [ ! -f "$MAIN_APP" ]; then
    log "Error: Main app not found at $MAIN_APP"
    exit 1
fi
if [ ! -f "$TOGGLE_SCRIPT" ]; then
    log "Error: Toggle script not found at $TOGGLE_SCRIPT"
    exit 1
fi

# Check if main application is running (avoid matching this script or grep)
if ! pgrep -f "python3 $MAIN_APP" &>/dev/null; then
    log "Starting red dot application"
    python3 "$MAIN_APP" &
    sleep 1  # Wait for initialization
    if pgrep -f "python3 $MAIN_APP" &>/dev/null; then
        log "Red dot application started successfully"
    else
        log "Error: Failed to start red dot application"
        exit 1
    fi
else
    log "Red dot application already running"
fi

# Run toggle script
log "Triggering toggle script"
python3 "$TOGGLE_SCRIPT" >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    log "Toggle script executed successfully"
else
    log "Error: Toggle script failed"
    exit 1
fi