import json
import time
import os
from pynput import keyboard
from datetime import datetime
import threading


class InputLogger:
    def __init__(self):
        self.inputs = []
        self.start_time = None
        self.is_recording = False
        self.tracked_keys = {"w", "a", "s", "d", "space"}

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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gameplay_inputs_{timestamp}.json"

        # Save to JSON
        output_data = {
            "session_info": {
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "duration_seconds": time.time() - self.start_time,
                "total_inputs": len(self.inputs),
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

        # Only log tracked keys
        if key_name in self.tracked_keys:
            relative_time = time.time() - self.start_time
            self.inputs.append(
                {
                    "timestamp": round(relative_time, 4),
                    "key": key_name,
                    "action": "press",
                }
            )
            print(f"⌨️  [{relative_time:.3f}s] {key_name.upper()} pressed")

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

        # Only log tracked keys
        if key_name in self.tracked_keys:
            relative_time = time.time() - self.start_time
            self.inputs.append(
                {
                    "timestamp": round(relative_time, 4),
                    "key": key_name,
                    "action": "release",
                }
            )

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
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()

        print("\n👋 Logger closed. Your file is in the GameLogger folder!")


if __name__ == "__main__":
    logger = InputLogger()
    logger.run()
