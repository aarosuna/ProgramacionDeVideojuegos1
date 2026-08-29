"""
This file contains the specialization of PowerUp to catch the ball.
"""
from typing import TypeVar


from src.powerups.PowerUp import PowerUp

class CatchPowerUp(PowerUp):
    """
    Power-up that allows the paddle to catch the ball.
    """
    def __init__(self, x: int, y: int) -> None:
       
        super().__init__(x, y, 7)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.can_catch = True

        paddle.catches_left = len(play_state.balls)

        for ball in play_state.balls:
            ball.already_caught = False
        
        self.active = False