from src.GameObject import GameObject
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Projectile import Projectile

class Bow:
    def __init__(self) -> None:
        pass

    def fire(self, x: float, y: float, direction: str) -> Projectile:
        """
        Factory Pattern: Creates an 'arrow'-type GameObject, assigns it 
        its orientation, and wraps it in the Projectile class.
        """
        arrow_obj = GameObject(GAME_OBJECT_DEFS["arrow"], x, y)
        arrow_obj.state = direction
        
        return Projectile(arrow_obj, direction)