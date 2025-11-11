import json
import os
import sys
import time
from datetime import datetime
from pynput import keyboard


class InputLogger:
    def __init__(self, tracked_keys: set = None):
        self.inputs = []
        self.start_time = None
        self.is_recording = False
        self.tracked_keys = tracked_keys or {"w", "a", "s", "d", "space"}
        self.timestamp_format = "%d/%m/%Y %H:%M:%S.%f"

    def start_recording(self):
        """Start recording inputs"""
        self.inputs = []
        self.start_time = time.time()
        self.is_recording = True
        print("\n🔴 RECORDING STARTED")
        print("Playing your game now! Press ESC to stop recording.\n")

    def stop_recording(self):
        """Stop recording and save to file"""
        if not self.is_recording:
            return

        self.is_recording = False
        filename = f"gameplay_inputs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Save to JSON
        output_data = {
            "session_info": {
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "duration_seconds": time.time() - self.start_time,
                "total_inputs": len(self.inputs),
                "tracked_keys": list(self.tracked_keys),
            },
            "inputs": self.inputs,
        }

        with open(filename, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✅ Recording stopped!")
        print(f"📁 Saved to: {filename}")
        print(f"📂 Location: {os.path.abspath(filename)}")
        print(f"📊 Total inputs recorded: {len(self.inputs)}")
        print(
            f"⏱️  Duration: {output_data['session_info']['duration_seconds']:.2f} seconds"
        )

    def on_press(self, key):
        """Called when a key is pressed"""
        if not self.is_recording:
            return

        try:
            key_name = key.char.lower() if hasattr(key, "char") else key.name.lower()
        except:
            key_name = str(key).replace("Key.", "").lower()

        timestamp = datetime.now().strftime(self.timestamp_format)[:-3]

        if key_name in self.tracked_keys:
            self.inputs.append(
                {
                    "timestamp": timestamp,
                    "key": key_name,
                    "action": "press",
                    "tracked": key_name in self.tracked_keys,
                }
            )
            print(f"⌨️  [{timestamp}] {key_name.upper()} pressed")

    def on_release(self, key):
        """Called when a key is released"""
        # ESC to stop recording
        if key == keyboard.Key.esc:
            self.stop_recording()
            return False  # Stop listener

        if not self.is_recording:
            return

        try:
            key_name = key.char.lower() if hasattr(key, "char") else key.name.lower()
        except:
            key_name = str(key).replace("Key.", "").lower()

        timestamp = datetime.now().strftime(self.timestamp_format)[:-3]

        if key_name in self.tracked_keys:
            self.inputs.append(
                {
                    "timestamp": timestamp,
                    "key": key_name,
                    "action": "release",
                    "tracked": key_name in self.tracked_keys,
                }
            )
            print(f"⌨️  [{timestamp}] {key_name.upper()} released")

    def run(self):
        """Main run loop"""
        print("=" * 50)
        print("🎮 GAMEPLAY INPUT LOGGER")
        print("=" * 50)
        print("\nTracking keys: W, A, S, D, SPACE")
        print("\nPress ENTER to start recording...")
        input()

        self.start_recording()

        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()

        print("\n👋 Logger closed. Your file is in the GameLogger folder!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tracked_keys = set(sys.argv[1:])
        logger = InputLogger(tracked_keys=tracked_keys)
    else:
        logger = InputLogger()
    logger.run()
