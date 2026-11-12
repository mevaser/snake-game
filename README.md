🐍 Snake Game

A complete and engaging implementation of the classic Snake Game using Python's turtle module. This project demonstrates modular design and the application of Object-Oriented Programming (OOP) principles.

📜 Description

The Snake Game is a timeless arcade game where the player controls a snake to collect food while avoiding collisions with itself and the screen boundaries. As the snake eats, it grows longer, making the game progressively more challenging.

This project features a modular design with separate classes for the snake, food, and scoreboard, ensuring clean and maintainable code.

🚀 Features

Dynamic Gameplay: The snake grows longer as it eats.
Score Tracking: Displays the current score and high score.
Collision Detection: A wall or body collision saves the round best and immediately starts a new round in the center.
Modular Design: Organized code with Snake, Food, and Scoreboard classes.
Customizable: Easily modify colors, speed, and screen size.

📂 Project Structure
snake-game/
│
├── main.py         # Main game logic
├── snake.py        # Snake class implementation
├── food.py         # Food class implementation
├── scoreboard.py   # Scoreboard class implementation
├── README.md       # Project description

🛠️ Requirements
Python 3.x
Python's turtle module, Tk support, and a graphical display. Run `python -m tkinter` to check that Tk is available.

▶️ How to Run
Clone the repository:

git clone https://github.com/mevaser/snake-game.git
cd snake-game

Run the main.py file:
python main.py

🎮 Controls
Arrow Keys: Move the snake up, down, left, or right.

### Repeatable local practice

Run `python main.py --demo`. The opening food is two moves to the right. Leave the snake facing right to see one pickup and one extra segment. Continuing straight reaches the wall, returns the snake to its initial length, and starts a fresh round automatically. To keep playing after the first pickup, steer up toward the next food. Arrow input accepts one turn per movement tick and ignores a direct reversal.

Normal play uses the existing `data.txt` beside the script. Practice uses its own ignored `.snake-demo-score.txt` in the same directory. Missing or malformed scores start at zero; if the game cannot write its file it keeps the best for the current session. Launching from a different working directory still uses the same score location.

Run the headless gameplay and score-storage checks with `python -m unittest discover -s tests`.

📜 Disclaimer
This project was created as part of the "100 Days of Code: The Complete Python Pro Bootcamp" course on Udemy. The code is shared for educational purposes and to document my learning journey. Full solutions and rights are owned by the course instructor.
