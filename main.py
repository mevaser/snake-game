import argparse
from pathlib import Path
from turtle import Screen, Terminator

from food import Food
from scoreboard import Scoreboard
from snake import Snake


def advance_round(snake, food, scoreboard):
    """Advance one tick and reset at most once when the round ends."""
    snake.move()
    if snake.head.distance(food) < 15:
        snake.grow()
        scoreboard.increase_score()
        food.refresh(snake.segments)

    outside = max(abs(snake.head.xcor()), abs(snake.head.ycor())) > 280
    hit_body = any(snake.head.distance(segment) < 10 for segment in snake.segments[1:])
    if outside or hit_body:
        scoreboard.reset()
        snake.reset()
        food.restart_demo(snake.segments)
        return "wall" if outside else "self"
    return None


def score_path(demo):
    return Path(__file__).resolve().with_name(".snake-demo-score.txt" if demo else "data.txt")


def main():
    parser = argparse.ArgumentParser(description="Play Snake using the arrow keys.")
    parser.add_argument("--demo", action="store_true",
                        help="Use a repeatable food layout and a separate practice high score.")
    args = parser.parse_args()

    screen = Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("black")
    screen.title("Snake — practice" if args.demo else "My Snake Game")
    screen.tracer(0)

    snake = Snake()
    food = Food(demo=args.demo)
    scoreboard = Scoreboard(score_path(args.demo))
    for name, turn in (("Up", snake.up), ("Down", snake.down), ("Left", snake.left), ("Right", snake.right)):
        screen.onkey(turn, name)
    screen.listen()

    def tick():
        try:
            advance_round(snake, food, scoreboard)
            screen.update()
            screen.ontimer(tick, 100)
        except Terminator:
            pass

    screen.update()
    screen.ontimer(tick, 100)
    screen.mainloop()


if __name__ == "__main__":
    main()
