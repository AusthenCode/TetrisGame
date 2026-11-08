import unittest

from game_state import GameState


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()

    def test_starts_with_default_values(self):
        self.assertEqual(self.gs.state, "start")
        self.assertEqual(self.gs.score, 0)
        self.assertEqual(self.gs.lines, 0)
        self.assertEqual(self.gs.level, 1)
        self.assertTrue(self.gs.sound_on)

    def test_score_is_cleared_lines_squared(self):
        self.gs.add_cleared_lines(1)
        self.assertEqual(self.gs.score, 1)
        self.gs.add_cleared_lines(3)
        self.assertEqual(self.gs.score, 10)

    def test_zero_lines_changes_nothing(self):
        self.gs.add_cleared_lines(0)
        self.assertEqual(self.gs.score, 0)
        self.assertEqual(self.gs.lines, 0)
        self.assertEqual(self.gs.state, "start")

    def test_level_goes_up_every_five_lines(self):
        self.gs.add_cleared_lines(4)
        self.assertEqual(self.gs.level, 1)
        self.gs.add_cleared_lines(1)
        self.assertEqual(self.gs.level, 2)
        self.gs.add_cleared_lines(5)
        self.assertEqual(self.gs.level, 3)

    def test_win_at_fifteen_lines(self):
        self.gs.add_cleared_lines(14)
        self.assertEqual(self.gs.state, "start")
        self.gs.add_cleared_lines(1)
        self.assertEqual(self.gs.state, "won")
        self.assertEqual(self.gs.level, 3)

    def test_toggle_pause(self):
        self.gs.toggle_pause()
        self.assertEqual(self.gs.state, "paused")
        self.gs.toggle_pause()
        self.assertEqual(self.gs.state, "start")

    def test_pause_does_nothing_after_game_over(self):
        self.gs.set_state("gameover")
        self.gs.toggle_pause()
        self.assertEqual(self.gs.state, "gameover")

    def test_toggle_sound(self):
        self.gs.toggle_sound()
        self.assertFalse(self.gs.sound_on)
        self.gs.toggle_sound()
        self.assertTrue(self.gs.sound_on)

    def test_reset_clears_progress_but_keeps_sound_choice(self):
        self.gs.add_cleared_lines(15)
        self.gs.toggle_sound()
        self.gs.reset()
        self.assertEqual(self.gs.state, "start")
        self.assertEqual(self.gs.score, 0)
        self.assertEqual(self.gs.lines, 0)
        self.assertEqual(self.gs.level, 1)
        self.assertFalse(self.gs.sound_on)

    def test_set_state_rejects_unknown_state(self):
        with self.assertRaises(ValueError):
            self.gs.set_state("banana")

    def test_can_start_with_sound_off(self):
        self.assertFalse(GameState(sound_on=False).sound_on)


if __name__ == "__main__":
    unittest.main()
    