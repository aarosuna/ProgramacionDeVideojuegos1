import pygame
from gale.stencil import Stencil
import settings
from src.Entity import Entity
from src.Fireball import Fireball

class Boss(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_health = self.health
        self.is_immune = True
        self.immunity_timer = 0.0
        self.fireball_timer = 1.0

    def damage(self, dmg: int, source: str = "unknown") -> None:
        if self.invulnerable:
            return
        
        if self.is_immune and source != "arrow":
            settings.SOUNDS["pot-wall"].play()
            return

        if source == "arrow":
            self.is_immune = False
            self.immunity_timer = 4.0
            return
        super().damage(dmg)
        self.go_invulnerable(0.5)

    def update(self, dt: float) -> None:
        super().update(dt)
        if not self.is_immune:
            self.immunity_timer -= dt
            if self.immunity_timer <= 0:
                self.is_immune = True

    def process_ai(self, room, dt: float) -> None:
        super().process_ai(room, dt)
        if not self.is_immune:
            return
        self.fireball_timer -= dt

        if self.fireball_timer <= 0:
            self.fireball_timer = 2.0
            target_x = room.player.x + room.player.width / 2
            target_y = room.player.y + room.player.height / 2
            start_x = self.x + self.width / 2 - 4
            start_y = self.y + self.height / 2 - 4
            fireball = Fireball(start_x, start_y, target_x, target_y)
            room.projectiles.append(fireball)

    def render_sprite(
        self, surface: pygame.Surface, texture_id: str, frame_index: int
    ) -> None:
        texture = settings.TEXTURES[texture_id]
        frame = settings.frame(texture_id, frame_index)
        image = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        image.blit(texture, (0, 0), frame)

        if not self.is_immune:
            image.fill((100, 150, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)

        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            image.set_alpha(64)

        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)

        sprite_x = round(self.x - self.offset_x)
        sprite_y = round(self.y - self.offset_y)

        if self.visibility_clip_rect is not None:
            sprite_rect = pygame.Rect(sprite_x, sprite_y, frame.width, frame.height)
            visible = self.visibility_clip_rect.clip(sprite_rect)
            visible.move_ip(-sprite_x, -sprite_y)

            stencil = Stencil((frame.width, frame.height))
            stencil.draw(lambda mask: mask.fill((255, 255, 255, 255), visible))
            stencil.apply(image)

        surface.blit(image, (sprite_x, sprite_y))