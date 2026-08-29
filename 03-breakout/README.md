# 03-Breakout

This document describes the functionality of the files related to *power-up* mechanics, the operation of the main game state (`PlayState`), and projectiles within the Breakout case study.

---

## File Descriptions

The game's architecture utilizes specialized modules to handle projectiles and power-up behaviors:

| File | Description | Action / Key |
| :--- | :--- | :--- |
| **`Projectile.py`** | Defines the `Projectile` class for player shots. Manages upward vertical movement, `pygame.Rect` collision logic, and rendering (red rectangle). | Automatic |
| **`CannonsPowerUp.py`** | Modifies the player's state by activating the `has_cannons` property on the paddle, granting the ability to fire projectiles. | Press **`F`** to use |
| **`CatchPowerUp.py`** | Allows the paddle to catch the ball upon contact. Calculates remaining catches based on active balls and resets the capture state for each. | Press **`Space`** to use |
| **`EarthquakePowerUp.py`** | Triggers a global event. Reduces resistance/destroys all blocks, adds points, emits particles, plays sounds, and generates a 0.5s screen shake. | Automatic |
| **`PowerUpFactory.py`** | Inherits from the Gale engine's `AbstractFactory`. Randomly instantiates power-ups to fall toward the player from specified coordinates. | Background System |

---

## PlayState.py Overview

The `PlayState.py` file contains the class responsible for the game's main loop. It actively handles:
* Updating and rendering the paddle, balls, projectiles, and bricks.
* Managing the user interface (displaying lives and score).
* Processing collisions and block destruction.
* Handling paddle growth (based on accumulated points) and the system for earning extra lives.

### Power-Up System and Management
During gameplay, there is a **30% chance** of randomly spawning a *power-up* whenever a block is destroyed. The class implements the following logic:

* **TwoMoreBall:** Integrated via the Abstract Factory pattern, this represents the most likely option (weight of 60) when selecting which *power-up* to spawn.
* **CatchPowerUp:** When the paddle possesses the `can_catch` ability, colliding balls become "stuck" to it. The paddle tracks the remaining catches; once exhausted, the ability is lost.
* **CannonsPowerUp:** Enables the `has_cannons` attribute. Firing launches two projectiles upward from the paddle's ends to destroy blocks. This is a single-use item and deactivates immediately after use.
* **EarthquakePowerUp:** Adds a camera-shake effect using a `shake_timer` and random `shake_offset` applied to the game world surface. **Restrictions:** It can only spawn from Level 3 onwards and is strictly limited to a maximum of 3 appearances during the game state.

### Cleanup and Transition Upon Level Completion
This file manages victory and defeat conditions, ensuring the player state is cleaned up and reset accordingly to prevent abilities from remaining active improperly.

When transitioning to the **Victory** state (all valid bricks destroyed), or whenever all balls leave the screen and the player loses a life (returning to the **Serve** state or triggering **Game Over**), a mandatory cleanup process takes place. The paddle's attributes are explicitly reset:

* The cannons are removed: `self.paddle.has_cannons = False`
* The ball-catching ability is disabled: `self.paddle.can_catch = False`