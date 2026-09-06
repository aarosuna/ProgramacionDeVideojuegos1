from typing import TypeVar
import pygame
from gale.state import StateMachine
import settings
from src.states.entity.BaseEntityState import BaseEntityState

class PlayerShootState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.shoot_timer = 0.0

    def enter(self) -> None:
        
        self.entity.change_animation(f"idle-{self.entity.direction}")
        

        arrow_x = self.entity.x
        arrow_y = self.entity.y + self.entity.height / 2 - 8
        
        if self.entity.direction == "left":
            arrow_x -= 8
        elif self.entity.direction == "right":
            arrow_x += self.entity.width
        elif self.entity.direction == "up":
            arrow_y -= 8
        elif self.entity.direction == "down":
            arrow_y += self.entity.height


        if hasattr(self.entity, "bow") and self.entity.bow is not None:
            new_arrow = self.entity.bow.fire(arrow_x, arrow_y, self.entity.direction)
            self.dungeon.current_room.projectiles.append(new_arrow)
            settings.SOUNDS["arrow"].play()
        self.entity.current_animation.reset()
        self.shoot_timer = 0.2

    def update(self, dt: float) -> None:
        self.entity.interact_requested = False
        self.entity.sword_requested = False

        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
        bow_texture = settings.TEXTURES["bow"]
        bow_rect = settings.frame("bow", 1)
        bow_image = bow_texture.subsurface(bow_rect)
        player_center_x = self.entity.x + self.entity.width / 2
        player_center_y = self.entity.y + self.entity.height / 2

        #Adjustments to fit the bow to the hands
        if self.entity.direction == "left":
            bow_x = self.entity.x - 6
            bow_y = player_center_y - 8
            bow_image = pygame.transform.flip(bow_image, True, False)

        elif self.entity.direction == "right":
            bow_x = self.entity.x + 2
            bow_y = player_center_y - 8

        elif self.entity.direction == "up":
            bow_x = player_center_x - 8
            bow_y = self.entity.y - 4
            bow_image = pygame.transform.rotate(bow_image, 90)
        elif self.entity.direction == "down":
            bow_x = player_center_x - 8
            bow_y = self.entity.y + 6
            bow_image = pygame.transform.rotate(bow_image, -90)

        surface.blit(
            bow_image,
            (round(bow_x), round(bow_y))
        )