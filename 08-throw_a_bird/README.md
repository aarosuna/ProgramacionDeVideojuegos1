# Throw a Bird

A 2D physics video game (*Angry Birds* style) developed in Python. This project utilizes the GALE engine and its physics wrapper (`gale.physics` / `pymunk`) to simulate realistic collisions, gravity, momentum conservation, and procedural structure destruction.

## Implemented Features

### 1. Split Ability ("The Blues" Split)
A special mechanic was integrated allowing the bird to multiply mid-flight to maximize destruction:
* **Tactical Activation:** By pressing the spacebar after launching the bird from the slingshot, it spawns two dynamic clones.
* **Trajectory Vectors:** The central bird keeps its original velocity and angle intact. The two clones dynamically calculate new trajectories based on the velocity vector of the exact moment of the split (deviating 15 degrees upwards and downwards, respectively).
* **Visual Indicator (Randomness):** Every time a bird appears on the slingshot, it has a 50% chance of inheriting this ability. Birds with the split power are automatically tinted blue so the player can plan their strategy.

### 2. Collision Condition (Single Use)
The split ability requires precision and reflexes from the player:
* The cloning power is strictly restricted to the free-flight phase.
* If the bird collides with the ground, a structure, or an enemy, the ability is irreversibly disabled for that turn, forcing the player to trigger the split before impact.

### 3. Score Control and Collective Turn End
The turn system was redesigned to support multiple simultaneous entities:
* **Absolute Rest Evaluation:** The turn does not end when the first bird stops. The engine tracks the complete list of birds (original and clones) and only resets the slingshot when **all** entities have linear and angular velocities below the rest threshold.

---

## Implementation Details

To achieve a robust physics system, the following code and architecture modifications were made:

* **Vector Mathematics (`Bird.py`):** The calculation of divergent trajectories was solved using two-dimensional rotation matrices. Leveraging `pygame.Vector2.rotate()`, the rigid body's current linear velocity is extracted and the $X$ and $Y$ components of the clones are calculated in real-time, ensuring the momentum feels natural regardless of the launch arc.
* **Non-Destructive Color Processing:** To visually indicate which bird has the power, a `pygame.transform.grayscale` filter was applied to the base texture and subsequently filled with a bright blue using the `BLEND_RGB_MULT` flag. This allows tinting the sprite dynamically without losing the shadows or volume of the original artwork.
* **Memory and Collision Management (`PlayState.py`):**
  * The static reference to the main bird was migrated to a dynamic list (`self.birds`) to orchestrate the rendering and physical evaluation of multiple simultaneous instances.
  * A subscription to the physics simulator's `on_collision_begin` callback was implemented. This allows intercepting any body contact and turning off the `can_split` boolean flag in constant time $O(1)$.
  * Once absolute rest is confirmed and the turn ends, the code not only resets the list but actively calls `self.world.destroy_body(bird.body)` on the clones to purge them from the physics engine and prevent memory leaks or ghost collisions in subsequent turns.