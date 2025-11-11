# Gameplay Input Logger 🎮

Simple Python script to log WASD + Space key inputs with timestamps for AI training.

## Setup (5 minutes)

1. **Install Python** (if you don't have it)
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Install the required library**
   ```bash
   pip install pynput
   ```
   
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. **Start the logger**
   ```bash
   python input_logger.py
   ```

2. **Press ENTER** when you're ready to start recording

3. **Play your game!** The logger will track:
   - W, A, S, D keys
   - Spacebar
   - Both presses AND releases

4. **Press ESC** when you're done playing to stop recording

5. **Find your file** in the `outputs` folder - it'll be named like:
   `gameplay_inputs_20241107_143052.json`

## Output Format

The JSON file contains:
```json
{
  "session_info": {
    "start_time": "2024-11-07T14:30:52",
    "duration_seconds": 45.3,
    "total_inputs": 127
  },
  "inputs": [
    {"timestamp": 0.0234, "key": "w", "action": "press"},
    {"timestamp": 0.1567, "key": "w", "action": "release"},
    {"timestamp": 0.2012, "key": "space", "action": "press"},
    ...
  ]
}
```

## Tips

- Start the logger BEFORE you start your game recording (OBS, etc.)
- The timestamps are in seconds, starting from when you pressed ENTER
- Each input logs both press and release for precise timing
- You can run multiple sessions - each gets a unique timestamped filename

## Troubleshooting

**"Module not found" error?**
- Make sure you ran: `pip install pynput`

**Permission errors on Mac/Linux?**
- You may need to grant accessibility permissions to Terminal/Python

**Want to track more keys?**
- Edit line 10 in `input_logger.py` and add more keys to the list
