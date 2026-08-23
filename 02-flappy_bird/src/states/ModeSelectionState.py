import pygame
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
import settings
from src.World import World

class ModeSelectionState(BaseState):
    def enter(self) -> None:
        self.world = World(generate_logs=False)
        self.selected_mode = 0
        self.modes = [
            "1. Normal Mode",
            "2. Hard Mode"
        ]

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        
        render_text(
            surface,
            "Elige un Modo",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

        for i, mode in enumerate(self.modes):
            color = settings.COLOR_WHITE if i == self.selected_mode else (100, 100, 100)
            y_pos = settings.VIRTUAL_HEIGHT / 2 + (i * 30)

            render_text(
                surface,
                mode,
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH / 2,
                y_pos,
                color,
                center=True,
                shadowed=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_data.pressed:
            if input_id == "down":
                self.selected_mode = (self.selected_mode + 1) % 2
            elif input_id == "up":
                self.selected_mode = (self.selected_mode - 1) % 2    
            elif input_id == "confirm":
                selected_mode_str = "normal" if self.selected_mode == 0 else "hard"
                self.state_machine.change("count_down", mode=selected_mode_str)