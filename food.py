import random
from turtle import Turtle


PRACTICE_POSITIONS = ((40, 0), (40, 40), (0, 40), (0, 0))


def practice_food(index, occupied):
    if index < len(PRACTICE_POSITIONS):
        x, y = PRACTICE_POSITIONS[index]
        first = ((280 - y) // 20) * 29 + ((x + 280) // 20)
    else:
        first = (index * 127 + 53) % (29 * 29)
    for offset in range(29 * 29):
        cell = (first + offset) % (29 * 29)
        position = (20 * (cell % 29) - 280, 280 - 20 * (cell // 29))
        if position not in occupied:
            return position
    return None


class Food(Turtle):
    def __init__(self, demo=False):
        super().__init__()
        self.demo = demo
        self.index = 0
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self, segments=()):
        if self.demo:
            occupied = {tuple(segment.position()) for segment in segments}
            position = practice_food(self.index, occupied)
            self.index += 1
            if position is None:
                self.goto(1000, 1000)
                return
        else:
            position = (random.randint(-270, 270), random.randint(-270, 270))
        self.goto(position)

    def restart_demo(self, segments):
        if self.demo:
            self.index = 0
            self.refresh(segments)
