# TetrisGame

Clear 5 lines to move up a level. The game has 3 levels, and you win after clearing 15 lines.

## Run the game

On Windows, create the environment and run the game:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe Tetris\tetris2_run.py
```

In VS Code, select `.venv\Scripts\python.exe` as the Python interpreter before running `Tetris\tetris2_run.py`.

On Mac or Linux, run `sh run_pip.sh` to set up Python and pygame, then start the game. If you use uv, run `sh run_uv.sh` instead.

## Controls

- Left / right: move (hold to keep moving)
- Up: rotate
- Down: fall faster
- Space: drop the piece
- R: restart after winning or losing
- Esc or Q: quit
