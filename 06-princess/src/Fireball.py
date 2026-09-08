import math
import pygame
import settings

class Fireball:
    def __init__(self, x: float, y: float, target_x: float, target_y: float) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.dead = False
        

        self.is_enemy_projectile = True 

        speed = 90.0
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = 0
            self.vy = speed

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, target) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

        if (self.x < 0 or self.x > settings.VIRTUAL_WIDTH or 
            self.y < 0 or self.y > settings.VIRTUAL_HEIGHT):
            self.dead = True

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        cx = int(self.x + offset_x + self.width / 2)
        cy = int(self.y + offset_y + self.height / 2)
        
        pygame.draw.circle(surface, (255, 80, 0), (cx, cy), 5)
        pygame.draw.circle(surface, (255, 200, 0), (cx, cy), 3)