# Super Martian (Platformer)

A 2D side-scrolling platformer developed in Python using `pygame` and the `gale` game framework. Control Martian, navigate platforms, jump on enemies, collect coins to reach the score target, and unlock the exit key to clear each level

---

## Gameplay & Core Mechanics

* **Objective & Key System:** 
  * The player must collect coins to reach a target score (**250 points**).
  * Once reached, all remaining coins and regular creatures disappear, the music switches to a victory fanfare, and the **Special Block** is activated.
  * Hitting the Special Block from below pops out a **Key**. Collecting this key triggers a circular wipe transition to advance to the next level.
* **Time Limit:** A countdown timer is active (**30s**). If the timer hits 0, Martian runs out of time and dies. The timer stops once the score objective is reached.
* **Transitions:** Smooth circular iris/vignette animations open when entering a level and close down focused on the player upon collecting the key.
* **Combat & Collision:**
  * Stomping enemies from above bounces Martian upward and either triggers their falling/stunned state or defeats them.
  * Colliding with creatures from the side or bottom defeats the player.
  * Falling out of the map boundary results in immediate death.

---

## Items & Score Values

Coins dynamically respawn after a short duration using random timers:

| Item | Base Points | Respawn Interval | Notes |
| :--- | :---: | :---: | :--- |
| **Green Coin** | 1 pt | 2.0s – 4.0s | Common coin scattered across paths. |
| **Blue Coin** | 5 pts | 5.0s – 8.0s | Uncommon coin. |
| **Red Coin** | 20 pts | 10.0s – 18.0s | High-value coin. |
| **Yellow Coin** | 50 pts | 20.0s – 25.0s | Rare, high-yield coin. |
| **Level Key** | — | Single use | Spawns from the Special Block upon hit; finishes the level. |

---

## Creatures & Enemies

Enemies feature specific movement speeds, animation frame configurations, and state routines:

* **Ground Creatures (Snails/Walkers):**
  * **Slime (grey) & Snail (blue):** Standard walkers moving at speed 15.
  * **Slime (red):** Walker variant moving at speed 15.
  * **Snail (yellow):** Slower ground walker moving at speed 10.
* **Hovering / Fly Creatures:**
  * **Bee:** Static/flying creature maintaining altitude at horizontal speed 40.
* **Dynamic Flying Spawners:**
  * Spawns intermittently from screen edges across open air rows.
  * Variations vary in flight speeds (35 to 50 px/s) and use distinct flapping and falling/stun animations.

---

## Level Design & Tilemap Architecture

Level2 is designed in **Tiled** (orthographic projection, 16x16 px tiles, 48x20 grid dimensions):

* **Layers:**
  1. `background`: Non-collidable scenery and parallax backdrop art.
  2. `ground`: Main platform geometry (`solid` and one-way `platform` collision tiles).
  3. `decorations`: Foliage, pillars, and foreground accents.
  4. `creatures`: Pre-placed object positions for enemies and walkers.
  5. `coins`: Position markers for collectible coins and the hidden Special Block.

---

## Source File Breakdown

| File | Type | Description |
| :--- | :--- | :--- |
| **`PlayState.py`** | Game State | Controls the active gameplay loop, camera tracking, HUD text rendering, circular transitions, win/loss evaluation, and entity collision checks. |
| **`GameLevel.py`** | Level Manager | Loads Tiled `.json` maps, parses object groups (coins, creatures, special blocks), and schedules flying creature spawns. |
| **`SpecialBlock.py`** | Entity / Block | Hidden objective block activated upon reaching the score goal. Tweens out the level key upward when struck from below. |
| **`GameEntity.py`** | Base Class | Inherits drawable, collidable, and animated mixins. Implements gravity, velocity, map bounds, and tile collision via `move_and_collide`. |
| **`Creature.py`** | Base Enemy | Extends `GameEntity` to bind specific creature state machines, walking/flying speeds, and spritesheet configurations. |
| **`creatures.py`** | Definitions | Data dictionary specifying spritesheet frames, speeds, and state machine mappings for ground and flying enemies. |
| **`items.py`** | Definitions | Logic and point tables for collectibles, sound playback, player counters, and coin respawn timers. |
| **`map_level.json`** | Tilemap Asset | Orthogonal 48x20 Tiled map definition storing layers, collision metadata, and item/creature spawn locations. |