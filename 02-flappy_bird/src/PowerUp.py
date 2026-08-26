import pygame
import settings

class PowerUp:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.width = 39 
        self.height = 28
        self.to_remove = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt
        if self.x < -self.width:
            self.to_remove = True

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["power_up"], self.get_rect())