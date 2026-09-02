from gale import camera
import pygame
from gale.timer import Timer
from src.GameItem import GameItem
import settings

class SpecialBlock(GameItem):
    def __init__(self, x: float, y: float, game_level, frame_index: int) -> None:
        super().__init__(
            x=x,
            y=y,
            width=16,
            height=16,
            texture_id="assets",
            frame_index=frame_index,
            collidable=True,
            consumable=False,
        )
        self.game_level = game_level
        self.is_empty = False
        self.is_active = False
        self.active_frame = frame_index
        self.empty_frame = frame_index

        self.key = GameItem(
            self.x, 
            self.y, 
            16, 
            16, 
            "key",
            0,
            False,
            False
        )

    def reveal (self) -> None:
        if not self.is_active:
            self.is_active = True
            self.game_level.items.append(self.key)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def hit(self) -> None:
        if not self.is_empty:
            self.is_empty = True
            self.frame_index = self.empty_frame         
            self.spawn_key()

    def spawn_key(self) -> None:
      
        Timer.tween(
            0.5,
            [(self.key, {"y": self.y - 16})],
            on_finish=lambda: setattr(self.key, 'collidable', True)
        )

    def render(self, surface: pygame.Surface, camera) -> None:

        if not self.is_active:
            return

        super().render(surface, camera)