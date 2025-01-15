from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 280)

    def show_score(self):
        self.write(f"SCORE: {self.score}", move=False, align="center", font=('Arial', 11, 'normal'))

    def update_score(self):
        self.score += 1
