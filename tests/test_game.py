import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from food import Food, practice_food
from main import advance_round, score_path
from scoreboard import Scoreboard, read_score, save_best
from snake import Snake


class Sprite:
    """A Turtle-shaped coordinate store for tests without a Tk display."""

    def __init__(self, *args, **kwargs):
        self.x, self.y, self.angle = 0, 0, 0

    def color(self, *args):
        pass

    def penup(self):
        pass

    def goto(self, x, y=None):
        self.x, self.y = x if y is None else (x, y)

    def position(self):
        return self.x, self.y

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def heading(self):
        return self.angle

    def setheading(self, heading):
        self.angle = heading

    def forward(self, distance):
        dx, dy = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}[self.angle]
        self.goto(self.x + distance * dx, self.y + distance * dy)

    def distance(self, other):
        return math.dist(self.position(), other.position())


class PracticePellet(Sprite):
    refresh = Food.refresh
    restart_demo = Food.restart_demo

    def __init__(self):
        super().__init__()
        self.index, self.demo = 0, True
        self.refresh()


class SnakeTests(unittest.TestCase):
    def setUp(self):
        stub = patch("snake.Turtle", Sprite)
        stub.start()
        self.addCleanup(stub.stop)
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.snake = Snake()
        self.food = PracticePellet()
        self.scoreboard = Scoreboard.__new__(Scoreboard)
        self.scoreboard.path = self.root / "demo-score.txt"
        self.scoreboard.score, self.scoreboard.high_score = 0, 0
        self.scoreboard.update_scoreboard = Mock()

    def tick(self):
        return advance_round(self.snake, self.food, self.scoreboard)

    def test_score_survives_restart_and_rejects_bad_content(self):
        path = self.root / "score.txt"
        self.assertEqual(read_score(path), 0)
        for content in (b"", b"NaN", b"-2", b"\xff", b"1234567890"):
            path.write_bytes(content)
            self.assertEqual(read_score(path), 0)
        self.assertEqual(save_best(path, 3), 3)
        self.assertEqual(read_score(path), 3)
        self.assertEqual(save_best(path, 2), 3)
        self.assertEqual(save_best(self.root / "missing" / "score.txt", 2), 2)

    def test_demo_uses_repeatable_food_and_separate_persistent_score(self):
        with patch("main.__file__", str(self.root / "main.py")):
            normal, demo = score_path(False), score_path(True)
        normal.write_text("12", encoding="ascii")
        self.scoreboard.path = demo
        self.assertEqual(self.food.position(), (40, 0))
        self.assertIsNone(self.tick())
        self.assertIsNone(self.tick())
        self.assertEqual((self.scoreboard.score, len(self.snake.segments)), (1, 4))
        self.assertEqual(self.food.position(), (40, 40))
        events = [self.tick() for _ in range(13)]
        self.assertEqual(events.count("wall"), 1)
        self.assertEqual(self.snake.head.position(), (0, 0))
        self.assertEqual((self.scoreboard.score, len(self.snake.segments)), (0, 3))
        self.assertEqual(read_score(demo), 1)
        self.assertEqual(normal.read_text(), "12")
        self.assertEqual(self.food.position(), (40, 0))

    def test_direction_cannot_reverse_or_double_turn_before_a_tick(self):
        self.snake.left()
        self.tick()
        self.assertEqual(self.snake.head.position(), (20, 0))
        self.snake.up()
        self.snake.left()
        self.tick()
        self.assertEqual(self.snake.head.position(), (20, 20))
        self.snake.down()
        self.tick()
        self.assertEqual(self.snake.head.position(), (20, 40))

    def test_body_collision_resets_exactly_once(self):
        for _ in range(2):
            self.snake.grow()
        for segment, position in zip(self.snake.segments, [(0, 0), (0, 20), (20, 20), (20, 0), (40, 0)]):
            segment.goto(position)
        self.food.goto(-100, -100)
        self.scoreboard.score = 2
        self.assertEqual(self.tick(), "self")
        self.assertEqual(len(self.snake.segments), 3)
        self.assertEqual(self.scoreboard.high_score, 2)
        self.scoreboard.update_scoreboard.assert_called_once()

    def test_practice_food_excludes_occupied_tiles(self):
        self.assertNotEqual(practice_food(0, {(40, 0)}), (40, 0))


if __name__ == "__main__":
    unittest.main()
