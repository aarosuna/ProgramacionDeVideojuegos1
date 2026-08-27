import pygame
import settings

class Projectile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 4
        self.height = 12
        self.vy = -300 
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, obj) -> bool:
        return self.get_collision_rect().colliderect(obj.get_collision_rect())

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        if self.y < 0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 50, 50), self.get_collision_rect())