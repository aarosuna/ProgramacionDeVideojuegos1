# Match-3 Study Case

This project is a Match-3 puzzle game developed using Python, `pygame`, and the `gale` engine. It features a fully playable core game loop with drag-and-drop mechanics, special bomb tiles, a dynamic hint system, and level progression

---

## Key Features

* **Drag and Drop Controls:** Players can click and drag a tile to swap it with an adjacent one.
* **Invalid Move Reversal:** If a swap does not result in a match, the game plays an error sound and the tiles return to their original positions.
* **Auto-Shuffling:** The board automatically detects if there are no possible moves left. If none are found, a "Shuffling..." message appears and the board is repainted with new colors (keeping bombs intact) to guarantee a valid move.
* **Dynamic Hint System:** If the player is idle for a certain amount of time, a possible move is highlighted with a pulsing yellow surface. The delay before a hint appears scales with the current level.

---

## Power-Ups & Bombs

Matching larger sets of tiles generates special bombs that can clear massive sections of the board. Bombs can also be manually detonated by clicking directly on them without swapping.

* **Line Bomb:** 
  * **How to get:** Created by matching exactly 4 tiles.
  * **Effect:** Explodes in a cross shape, clearing the entire row and column.
  * **Appearance:** Identified by red and white circles drawn over the tile.
* **Color Bomb:** 
  * **How to get:** Created by matching 5 or more tiles.
  * **Effect:** Destroys all tiles on the board that share the same color as the trigger tile.
  * **Appearance:** Identified by gold and bright white circles.

---

## File Structure & Architecture

The game's logic is divided into four main classes:

### `Match3.py`
* Serves as the main game entry point, inheriting from the Gale engine's `Game` class.
* Sets up a custom image cursor (or defaults to the system hand cursor if it fails).
* Manages the continuous background scrolling effect.

### `PlayState.py`
* Processes mouse inputs (`click` and `drag`) to swap tiles.
* Triggers tween animations for swapping pieces and making new tiles fall.

### `Board.py`
* Uses a recursive algorithm to calculate horizontal and vertical matches.
* Implements a Breadth-First Search (BFS) algorithm to expand explosions triggered by Line Bombs and Color Bombs.
* Contains the logic for simulating swaps to detect if there are any valid moves left on the board (`has_possible_moves`).

### `Tile.py`
* Contains boolean flags to define its state, such as `is_dragging`, `is_bomb`, and `is_color_bomb`.
* Handles its own rendering logic, including the drawing of the specific graphical indicators for bombs.