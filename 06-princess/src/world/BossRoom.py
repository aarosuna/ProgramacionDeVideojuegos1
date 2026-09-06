import pygame
import settings
from src.world.Room import Room
from src.Boss import Boss
from src.definitions.entity import ENTITY_DEFS
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState

class BossRoom(Room):
    def __init__(self, dungeon, player, on_game_over) -> None:
        self.entrance_direction = player.direction
        super().__init__(dungeon, player, on_game_over)

        opposite_doors = {
            "up": "bottom",
            "down": "top",
            "left": "right",
            "right": "left"
        }
        entrance_door = opposite_doors[self.entrance_direction]
        self.doorways = [door for door in self.doorways if door.direction == entrance_door]
        self.cleared = False

    def _generate_entities(self) -> None:

        """
        Instead of multiple random enemies, it spawns a single boss.
        """

        definition = ENTITY_DEFS["boss"]
        boss_x = settings.VIRTUAL_WIDTH / 2 - 16
        boss_y = settings.VIRTUAL_HEIGHT / 2 - 16

        if self.entrance_direction == "up":
            boss_y = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE * 2
        elif self.entrance_direction == "down":
            boss_y = settings.MAP_RENDER_OFFSET_Y + (settings.MAP_HEIGHT - 5) * settings.TILE_SIZE
        elif self.entrance_direction == "left":
            boss_x = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE * 2
        elif self.entrance_direction == "right":
            boss_x = settings.MAP_RENDER_OFFSET_X + (settings.MAP_WIDTH - 5) * settings.TILE_SIZE
        
        boss = Boss(
            x=boss_x,
            y=boss_y,
            width=32,
            height=48,
            walk_speed=definition.get("walk_speed", 20),
            health=5,
            animation_defs=definition["animations"],
            states={},
        )

        boss.state_machine.states = {
            "walk": lambda sm, e=boss: EntityWalkState(e, sm),
            "idle": lambda sm, e=boss: EntityIdleState(e, sm),
        }
        boss.change_state("walk")
        self.entities.append(boss)

    def update(self, dt: float) -> None:
        super().update(dt)
        if not self.cleared and len(self.entities) == 0:
            self.cleared = True
            for doorway in self.doorways:
                doorway.open = True
            settings.SOUNDS["door"].play()

    def _generate_objects(self) -> None:
        pass

    def render(self, surface: pygame.Surface, camera_offset_x: float = 0, camera_offset_y: float = 0) -> None:
        super().render(surface, camera_offset_x, camera_offset_y)

        for entity in self.entities:
            if isinstance(entity, Boss) and not entity.dead:
                bar_width = 120
                bar_height = 10
                x = (settings.VIRTUAL_WIDTH - bar_width) // 2
                health_pct = max(0, entity.health / entity.max_health)
                y = 15
                pygame.draw.rect(surface, settings.COLOR_TITLE_SHADOW, pygame.Rect(x, 10, bar_width, bar_height))
                pygame.draw.rect(surface, settings.COLOR_TITLE, pygame.Rect(x, y, int(bar_width * health_pct), bar_height))
                pygame.draw.rect(surface, settings.COLOR_WHITE, pygame.Rect(x, y, bar_width, bar_height), 1)
                font = settings.FONTS["princess-little"]
                text = font.render("DEMON", True, settings.COLOR_WHITE)
                text_health = font.render(f"{entity.health}/{entity.max_health}", True, settings.COLOR_WHITE)
                text_rect = text.get_rect(center=(settings.VIRTUAL_WIDTH // 2, y + bar_height + 5))
                surface.blit(text, text_rect)
                surface.blit(text_health, text_health.get_rect(center=(settings.VIRTUAL_WIDTH // 2, y + bar_height + 15)))
                break
