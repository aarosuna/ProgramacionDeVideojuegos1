import random
from gale.factory import AbstractFactory

from src.powerups.TwoMoreBall import TwoMoreBall
from src.powerups.CatchPowerUp import CatchPowerUp
from src.powerups.EarthquakePowerUp import EarthquakePowerUp
from src.powerups.CannonsPowerUp import CannonsPowerUp

class PowerUpFactory(AbstractFactory):
    """
    GALE abstract factory for generating random power-ups.
    """
    def create(self, x: int, y: int):
        
        choice = random.choice(["two_more_ball", "catch", "earthquake", "cannon"])
        
        if choice == "two_more_ball":
            return TwoMoreBall(x, y)
        elif choice == "catch":
            return CatchPowerUp(x, y)
        elif choice == "earthquake":
            return EarthquakePowerUp(x,y)
        elif choice == "cannon":
            return CannonsPowerUp(x,y)
        
        return None