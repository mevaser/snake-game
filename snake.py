from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180


class Snake:
    def __init__(self):
        self.segments = []
        self.pending_heading = None
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            new_segment = Turtle(shape="square")
            new_segment.penup()
            new_segment.goto(position)
            new_segment.color("white")
            self.segments.append(new_segment)

    def grow(self):
        new_segment = Turtle(shape="square")
        new_segment.penup()
        new_segment.goto(self.segments[-1].position())
        new_segment.color("white")
        self.segments.append(new_segment)

    def reset(self):
        self.pending_heading = None
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    def move(self):
        if self.pending_heading is not None:
            self.head.setheading(self.pending_heading)
            self.pending_heading = None
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def queue_turn(self, heading):
        current = self.head.heading()
        if self.pending_heading is None and heading != current and heading != (current + 180) % 360:
            self.pending_heading = heading

    def up(self):
        self.queue_turn(UP)

    def down(self):
        self.queue_turn(DOWN)

    def right(self):
        self.queue_turn(RIGHT)

    def left(self):
        self.queue_turn(LEFT)
