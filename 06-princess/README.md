# The Legend of the Princess - Boss Update

A 2D Action RPG (ARPG) video game developed in Python using the Pygame library and the Gale framework. This version expands upon classic procedural dungeon generation by adding advanced combat mechanics (bow and arrow) and boss fights.

## New Features Implemented

### Chest and Bow System (Dynamic Inventory)
* **Unique and Random Generation:** The room generation engine ensures that a single chest appears randomly throughout the player's run.
* **Environmental Interaction:** The chest responds to the player's proximity and direction, opening to grant the Bow.
* **Firing Mechanics (Factory Pattern):** A `Bow` class was integrated, exposing a `fire` method. This method acts as a factory (Factory Pattern) to instantiate projectiles (`Projectile`) in real-time, calculating direction vectors based on the player's orientation.

### Boss Encounter (Demon Boss Room)
The combat experience reaches its climax when facing a boss designed with complex states and asymmetrical difficulty balancing.

* **Arena Architecture (Boss Room):** 
  * Conditional procedural access: There is a mathematical probability of entering the boss room upon crossing a door, *only* if the player already has the bow in their inventory.
  * The room overrides the base engine's item generation: it spawns without minor enemies, pots, or switches, and blocks all exits except the entrance door, which remains locked.
* **Invulnerability and Stun Mechanics:**
  * The boss is strictly immune to melee attacks (sword).
  * Projectile impacts (arrows) break its immunity (blue visual feedback), creating a time-limited window of vulnerability where the sword can reduce its hit points.
* **Artificial Intelligence and Attacks:**
  * The boss fires magical projectiles (fireballs) that calculate and target the exact position the player had at the moment of firing.
* **Extreme Lethality Balancing:**
  * Being hit by a fireball results in **Instant Death** (Insta-kill).
  * Physical contact with the boss's *hitbox* penalizes the player by subtracting a full heart (2 damage points), demanding strict spatial control.

## Architecture and Highlighted Patterns
* **Finite State Machines (FSM):** Smooth management of animations and logic between walking, attacking, and taking damage.
* **Inheritance and Polymorphism:** Classes like `BossRoom` and `Boss` extend the base behavior of engine rooms and entities.
* **Separation of Concerns:** Total independence between physics calculations (collisions), artificial intelligence, and on-screen rendering (e.g., software mirroring effect for sprites).

## Controls
* **Arrow Keys:** Character movement.
* **Space:** Sword Attack (Melee) / Interact.
* **F Key:** Fire Bow (Once unlocked).