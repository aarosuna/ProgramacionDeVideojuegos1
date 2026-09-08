# Ultimate Fantasy (RPG)

A 2D Role-Playing Game (RPG) developed in Python. This project utilizes the stack-based state architecture (State Stack) of the GALE engine and features classic JRPG mechanics, open-world exploration (procedural generation), and a strategic real-time combat system.

## Implemented Features

### 1. Graphical User Interface (GUI) and Status Menu
The out-of-combat user experience was redesigned to provide detailed information and tactical control over the party:
* **Individual Status Panel:** Graphical interface displaying each party member's information in independent boxes, including Level, Experience Points (EXP), Hit Points (HP), and base stats (Magic, Attack, and Defense).
* **Visual Action Management:** Intelligent rendering of the menu with *Alpha* (transparency) values for inactive elements, visually highlighting available abilities (such as healing) and darkening disabled ones.
* **Integrated Healing System:** 
  * *Single Target Healing:* Allows dynamically selecting the allied target to heal from the world menu.
  * *Global Healing:* Execution of Area of Effect (AoE) spells to restore the entire party's HP simultaneously, directly from the main menu.

### 2. Active Time Battle (ATB) System
Traditional turn-based combat was replaced by a dynamic system based on Rest Time, providing greater fluidity and strategy:
* **Individual Timers:** Each entity (players and enemies) possesses a base recovery time that must be met after executing an action.
* **Orchestrated System:** Time management and initiative decision-making occur dynamically instead of relying on a static list of predefined turns.

---

## Implementation Details

To achieve the described mechanics, deep architectural modifications were made to the base engine while adhering to the principles of high cohesion and low coupling:

* **Time Attribute Injection:** The base battle entity class (`BattleEntity`) was extended to incorporate the `base_rest_time` and `current_rest_time` properties, initializing the latter with a random value to prevent exact ties at the start of each combat.
* **Master Clock Refactoring (`BattleState.py`):** The `update(dt)` method of the battle state was rewritten to act as the world clock. It now iterates over all active combatants, reducing their timers based on `dt` (Delta Time).
* **Ephemeral States (`TakeTurnState.py`):** The old recursive logic that iterated over fixed indices was eliminated. Now, when `BattleState` detects that a timer has reached zero, it pushes a `TakeTurnState` "ephemerally," passing only the entity that needs to act. Once the weapon or spell is executed, the state performs a `pop()`, returning control to the master clock so time can continue running freely.