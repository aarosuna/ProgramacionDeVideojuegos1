The base game includes the scenery, physics, assets, sound, title, and start time. A pause mechanic was added, along with two game modes (normal and hard). In hard mode, the bird can move horizontally, some logs open and close, and a power-up allows the bird to fly through logs when collected. After the title screen, a menu was added to select the game mode. Upon death, another menu appears asking if the player wants to continue on the same level, change levels, or exit.

The keys added to the game are as follows:
"Left click" to jump
"A" to move the bird left
"D" to move the bird right
"Space" to pause and resume the game
"Enter" to select
"Esc" to exit the game
"Up" and "down" to navigate the menus

The following states were added:
GameOverState:
This state is activated when the player crashes. It displays the text "GAME OVER", the final score, and a menu to replay, change modes, or return to the main menu.
ModeSelectionState: This is the screen where the player can select the difficulty level. It allows the player to choose between "Normal Mode" and "Hard Mode" before transitioning to the game countdown.
PauseState: This state freezes the action. It temporarily stops the music and sound effects, displays the word "PAUSED" in the center of the screen, and returns the player to the countdown when the game resumes.

Modifications were made to the following states:
PlayingState: Now, "enter" receives the game mode and the ghost_timer, executes the selected game mode, manages power-up collection, and also transitions to the pause or Game Over states.
TitleScreenState: Includes an interactive menu that allows the player to use the up or down arrow keys to start the game or close the application.
CountDownState: Now, "enter" receives the game mode and the ghost_timer.
