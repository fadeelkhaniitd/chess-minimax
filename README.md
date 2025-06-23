# Python Chess Engine ♟️

A chess engine built in Python using Pygame for GUI and Minimax for AI.

## Features
- Minimax AI with Alpha-Beta Pruning
- Move ordering (MVV-LVA, checks, promotions)
- Quiescence search for stable evaluation
- Transposition table for fast search
- Enhanced evaluation (king safety, pawn structure, bishop pair, mobility, endgame detection)
- Time control (per side + increment, with real-time clocks)
- UCI protocol support (for automated testing and engine matches)
- 2-player simulator built from scratch
- GUI using Pygame with clocks on correct sides
- Takeback (undo move) feature
- PGN saving for completed games

## How to Run
Run the main engine (with GUI):
```bash
python Chess_Engine.py [--takeback] [--time SECONDS] [--inc SECONDS]
```
- `--takeback`: Enable undo move feature
- `--time SECONDS`: Total time per side (default: 300)
- `--inc SECONDS`: Increment per move (default: 0)

Run the 2-player simulator:
```bash
python Chess_Simulator.py
```

## UCI Engine
You can use the engine in UCI mode for automated matches with the included `uci_engine.exe` executable (no Python required).

### How to use the UCI engine

- Point your chess GUI (e.g. Arena, CuteChess, Scid vs PC, etc.) to `uci_engine.exe` as the engine binary.
- The engine supports standard UCI options and time controls.
- No installation or Python is required to use the executable.

If you want to run the engine from source (Python), you can still use `python Chess_Engine.py` for the GUI version.

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```
