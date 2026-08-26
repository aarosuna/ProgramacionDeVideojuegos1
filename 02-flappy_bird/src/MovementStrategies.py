import pygame
import settings

class NormalMovement:
    def update(self, bird, dt: float) -> None:

        bird.vy += settings.GRAVITY * dt

        if bird.jumping:
            settings.SOUNDS["jump"].play()
            bird.vy = -settings.JUMP_TAKEOFF_SPEED
            bird.jumping = False

        bird.y += bird.vy * dt

class HardMovement:
    def update(self, bird, dt: float) -> None:

        bird.vy += settings.GRAVITY * dt

        if bird.jumping:
            settings.SOUNDS["jump"].play()
            bird.vy = -settings.JUMP_TAKEOFF_SPEED
            bird.jumping = False

        bird.y += bird.vy * dt
        
        keys = pygame.key.get_pressed()
        move_speed = 150  
        
        if keys[pygame.K_a]:
            bird.x -= move_speed * dt
        if keys[pygame.K_d]:
            bird.x += move_speed * dt

        bird.x = max(0, min(bird.x, settings.VIRTUAL_WIDTH - bird.width))