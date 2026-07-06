Files

- controller.py: Runs the game loop, reads keyboard input, adds food, moves enemies, and updates the display.
- boardDisplay.py: Draws the board, images, score, and game-over message.
- cell.py: Defines the Cell class and the possible cell types: player, food, enemy, and empty.
- preferences.py: Stores the game constants such as board size, colors, timing, and image file paths.
- gameData.py: Stores the game state and contains the implemented logic for neighbors, player movement, food, scoring, enemies, and game over.

Modified

- gameData.py was updated to complete the missing game logic and add comments
- The images in the images folder were customized for Part 4.

Run

- pip install pygame-ce
- python controller.py
