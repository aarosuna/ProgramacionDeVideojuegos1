# 02-flappy_bird (Extended Version)

This project is an extended version of a base game. It builds upon the core mechanics by introducing new game modes, menus, power-ups, and a more complex state machine architecture to enhance the player's experience.

---

## Features

### Base Game Features
* Scenery and environment rendering
* Core physics and collision detection
* Assets (sprites, graphics)
* Sound effects and music
* Title screen and start time tracking

### New Additions
* **Pause Mechanic:** Ability to freeze the game and mute audio temporarily.
* **Interactive Menus:** Added navigation for the Title Screen, Game Mode selection, and Game Over screens.
* **Power-ups:** A collectible power-up that grants the bird the ability to fly through logs/pipes unharmed.
* **Advanced Mechanics (Hard Mode):** Moving obstacles (logs that open and close) and horizontal player movement.

---

## Game Modes

Players can choose between two distinct difficulties before starting a run:

1. **Normal Mode:** The standard gameplay experience.
2. **Hard Mode:** 
   * The bird can be moved horizontally.
   * Logs (obstacles) dynamically open and close.
   * Special power-up spawn, allowing the bird to temporarily phase through logs when collected.---

## Controls

| Key / Input | Action |
| :--- | :--- |
| **Left Click** | Jump / Flap |
| **A** | Move bird left *(Hard Mode only)* |
| **D** | Move bird right *(Hard Mode only)* |
| **Space** | Pause and resume the game |
| **Enter** | Select menu options |
| **Esc** | Exit the game |
| **Up / Down Arrows** | Navigate through menus |

---

## State Machine Architecture

To implement these new features, the game's state machine was heavily updated.

### New States Added

* **`ModeSelectionState`**
  * **Function:** Screen where the player selects the difficulty level.
  * **Behavior:** Allows the player to choose between "Normal Mode" and "Hard Mode" before transitioning to the game countdown.
* **`PauseState`**
  * **Function:** Freezes the active gameplay.
  * **Behavior:** Temporarily stops the music and sound effects, displays the word "PAUSED" in the center of the screen, and returns the player to the countdown when the game is resumed.
* **`GameOverState`**
  * **Function:** Activated when the player crashes.
  * **Behavior:** Displays "GAME OVER" and the final score. Presents a menu asking if the player wants to continue on the same level (replay), change game modes, or return to the main menu.

### Modified States
* **`TitleScreenState`**
  * Now includes an interactive menu that allows the player to use the up/down arrow keys to start the game or close the application.
* **`CountDownState`**
  * The `enter` function now receives the selected game mode and the `ghost_timer` to pass them along to the gameplay state.
* **`PlayingState`**
  * The `enter` function now receives the game mode and `ghost_timer`.
  * Executes specific logic depending on the selected game mode.
  * Manages power-up spawning and collection.
  * Handles transitions to both the `PauseState` and the new `GameOverState`.