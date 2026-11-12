import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Arial", 18, "bold")


def read_score(path):
    try:
        text = Path(path).read_text(encoding="utf-8").strip()
        return int(text) if text.isascii() and text.isdecimal() and len(text) <= 9 else 0
    except (OSError, UnicodeError):
        return 0


def save_best(path, score):
    """Keep displaying the session best if persistent storage is unavailable."""
    path = Path(path)
    best = max(score, read_score(path))
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="ascii", dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            output.write(str(best))
        os.replace(temporary, path)
    except OSError:
        pass
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
    return best


class Scoreboard(Turtle):
    def __init__(self, path=None):
        super().__init__()
        self.path = Path(path) if path is not None else Path(__file__).resolve().with_name("data.txt")
        self.score = 0
        self.high_score = read_score(self.path)
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 270)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"SCORE: {self.score} High Score: {self.high_score}", move=False, align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = save_best(self.path, self.score)
        self.score = 0
        self.update_scoreboard()
