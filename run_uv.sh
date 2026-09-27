#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec uv run --python 3.12 --with pygame==2.6.1 Tetris/tetris2_run.py
