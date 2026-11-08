"""GameState: keeps the game data (state, score, level, lines, sound flag).

It does not draw, play sound or read the keyboard (single responsibility).
It does not import pygame, so it can be unit tested without a window.
"""

MAX_LEVEL = 3
LINES_PER_LEVEL = 5
VALID_STATES = ("start", "paused", "gameover", "won")


class GameState:
    def __init__(self, sound_on=True):
        # The sound flag is set once here. reset() does not touch it,
        # because a restart should keep the player's mute choice.
        self._sound_on = sound_on
        self.reset()

    def reset(self):
        self._state = "start"
        self._score = 0
        self._lines = 0
        self._level = 1

    # Read-only access (encapsulation: other code cannot set these directly)
    @property
    def state(self):
        return self._state

    @property
    def score(self):
        return self._score

    @property
    def lines(self):
        return self._lines

    @property
    def level(self):
        return self._level

    @property
    def sound_on(self):
        return self._sound_on

    # Changes go through methods
    def set_state(self, new_state):
        if new_state not in VALID_STATES:
            raise ValueError(f"Unknown state: {new_state}")
        self._state = new_state

    def toggle_pause(self):
        # Same rule as the P key: only works while playing or paused.
        if self._state == "start":
            self._state = "paused"
        elif self._state == "paused":
            self._state = "start"

    def toggle_sound(self):
        self._sound_on = not self._sound_on

    def add_cleared_lines(self, cleared):
        # Same rules as break_lines() in tetris2_run.py
        self._score += cleared ** 2
        self._lines += cleared
        self._level = min(self._lines // LINES_PER_LEVEL + 1, MAX_LEVEL)
        if self._lines >= MAX_LEVEL * LINES_PER_LEVEL:
            self._state = "won"
            