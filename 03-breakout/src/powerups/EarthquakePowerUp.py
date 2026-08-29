from typing import TypeVar
from src.powerups.PowerUp import PowerUp
from src.Brick import COLOR_PALETTE
import settings

class EarthquakePowerUp(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 1) 

    def take(self, play_state: TypeVar("PlayState")) -> None:

        settings.SOUNDS["brick_hit_2"].play()
        
        for brick in play_state.brickset.bricks.values():
            if not brick.broken:

                play_state.score += brick.score()
                r, g, b = COLOR_PALETTE[brick.color]
                brick.particle_system.set_colors([(r, g, b, 10), (r, g, b, 50)])
                brick.particle_system.generate()
                if brick.tier == 0:
                    if brick.color == 0:
                        brick.broken = True
                    else:
                        brick.tier = 3
                        brick.color -= 1
                else:
                    brick.tier -= 1
        

        play_state.shake_timer = 0.5 
        self.active = False