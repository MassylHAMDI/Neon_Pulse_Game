# 🌟 Neon Pulse - A Modern Arkanoid Clone

## 📝 Description
Neon Pulse is a modern take on the classic Arkanoid game.

## 🎬 Demo
https://github.com/user-attachments/assets/ff553bdb-0659-41f9-af80-9623f3039a59

### 🔄 Game States
- Main Menu with animated elements
- In-game state with pause functionality
- Game Over screen
- Victory screen with level progression
- High score display

## 💻 Technical Requirements
- Python 3.9
- Pygame library
- Required folder structure:
  ```
  assets/
    ├── images/
    │   ├── bg_menu.jpg
    │   └── bg_game.jpg
    └── sounds/
        ├── paddle.wav
        ├── brick.wav
        └── wall.wav
  ```

## 🚀 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd neon-pulse
```

2. Install the required dependencies:
```bash
pip install pygame
```

3. Ensure all assets are in place in the assets directory

4. Run the game:
```bash
python main.py
```

## 📁 Project Structure
```
src/
├── __init__.py
├── ball.py         # Ball physics and behavior
├── bonus_malus.py  # Power-ups system
├── brick.py        # Brick properties and behavior
├── constants.py    # Game constants and configurations
├── game.py         # Main game logic
├── menu.py         # Menu system
├── player.py       # Player paddle controls
└── score_display.py # Score and UI display
```
## 📄 License
This project is released under the MIT License.
