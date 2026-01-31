# Space Invaders – Progressive Pygame Edition

A classic **Space Invaders–style arcade shooter** developed using **Python and Pygame**.  
The game features **progressive levels, smart alien shooting behavior, sound effects, explosions, and a persistent high-score system**.  

This project was **built by learning from [this YouTube tutorial series](https://youtube.com/playlist?list=PLjcN1EyupaQkAQyBCYKyf1jt1M1PiRJEp)**, and enhanced with **additional features** including:

- Scoring system with points for each alien
- Level system with increasing difficulty
- Countdown before gameplay starts
- Persistent highest score saved to file

---

## 🎮 Gameplay Features

- Player-controlled spaceship with smooth movement
- Shooting mechanics with cooldown control
- Smart alien shooting system (bottom-most alien per column)
- Progressive difficulty with each level
- Increasing alien speed, fire rate, and bullet count
- Health system with visual health bar
- Explosion animations and sound effects
- Countdown before gameplay starts
- Level completion and game-over screens

---

## 🕹️ Controls

| Key | Action |
|---|---|
| ← / → | Move left / right |
| ↑ / ↓ | Move up / down |
| Space | Shoot |
| Enter | Continue to next level |
| R | Restart (Game Over) |
| Q | Quit (Game Over) |

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Library:** Pygame
- **Audio:** Pygame Mixer
- **Assets:** Custom sprites, sound effects, and background
- **Platform:** Windows / Linux / macOS

---

## 📁 Project Structure

```
Space-Invaders/
│
├── assets/
│   ├── alien1.png
│   ├── alien2.png
│   ├── ...
│   ├── spaceship.png
│   ├── bullet.png
│   ├── alien_bullet.png
│   ├── explosion1.png
│   ├── explosion2.png
│   ├── ...
│   ├── background.jpg
│   ├── laser.wav
│   ├── explosion1.wav
│   ├── explosion2.wav
│   └── highestscore.txt
│
├── space_invaders.py
└── README.md
```

---

## ▶️ How to Run

### 1. Install Python (3.8+ recommended)
Download from: https://www.python.org

### 2. Install Pygame
```bash
pip install pygame
```

### 3. Run the Game
```bash
python space_invaders.py
```

---

## 💾 High Score System

* The highest score is stored in:
  ```
  assets/highestscore.txt
  ```
* The score persists between game sessions.
* Automatically updates when a new record is achieved.

---

## 🚀 Future Improvements (Optional Ideas)

* Main menu and pause system
* Power-ups and special weapons
* Boss levels
* Joystick / controller support
* Executable (.exe) distribution
* Settings menu (sound, difficulty)

---

## 📜 License

This project is open-source and free to use for learning and personal projects.
Feel free to modify, extend, or improve it.

---

## 👨‍💻 Author

Developed by **hamzza07x**

Built by learning from [this tutorial series](https://youtube.com/playlist?list=PLjcN1EyupaQkAQyBCYKyf1jt1M1PiRJEp) and enhanced with scoring and level features.

If you like the project, give it a ⭐ on GitHub.
