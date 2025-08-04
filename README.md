# 🚀 Space Shooter Game (Python + Pygame)

A fully functional **2D Space Shooter game** developed using **Python** and **Pygame**, as part of my [UNEC] coursework (Nov–Dec 2024). The game features smooth player movement, dynamic difficulty scaling, interactive menus, and frame rate-independent performance.

## 🎮 Features

### 🕹️ Gameplay Mechanics
- Smooth directional movement using normalized vectors
- Real-time laser shooting with cooldown
- Collision detection using pixel-perfect masks
- Dynamic meteor spawn rate based on player score
- Procedural star placement with overlap prevention

### 🧠 Advanced Logic
- Scaled explosion animations by meteor size
- Delta time implementation for frame rate independence
- Laser-to-meteor and player-to-meteor collision systems

### 📊 Performance Optimizations
- Efficient rendering using sprite groups
- Maintains consistent 60 FPS across systems

### 🖱️ UI/UX
- Main menu with:
  - Play
  - Settings (volume control and mute)
  - How to Play
  - Exit
- Game over screen with restart or exit options

## 🧱 Project Structure
```
├── README.md
├── LICENSE.txt
├── .gitignore
├── requirements.txt
├── images/           # Game sprites, stars, explosion frames, fonts
├── audio/            # Sound effects and background music
└── main.py
```

## 🗺️ Controls

| Action                | Key(s)                |
|-----------------------|-----------------------|
| Move                  | W/A/S/D or Arrow Keys |
| Shoot Laser           | Spacebar              |
| Restart (after death) | R                     |
| Quit Game             | Esc or Exit button    |

## 🔊 Settings Menu
- Volume slider (10 levels)
- Mute toggle
- Back button to return to main menu

## 🧠 How to Play
1. Avoid incoming meteors.
2. Shoot them to survive longer and earn points.
3. Each second survived = +1 point.

## 🛠️ Technologies Used

- **Python 3.x**
- **Pygame**
- Pixel-perfect collision (`pygame.mask`)
- Delta time and event-driven spawning

## 📚 Coursework Context

Developed as part of my **UNEC** Programming Coursework in Fall 2024.

## ✅ To Run the Game

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/space-shooter-pygame.git
   cd space-shooter-pygame

2. Make sure you have pygame installed:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python main.py
