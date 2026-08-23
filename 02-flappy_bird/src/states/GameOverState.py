import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings

class GameOverState(BaseState):
    def enter(self, score: int = 0, world=None, bird=None, mode: str = "normal") -> None:
        self.score = score
        self.world = world
        self.bird = bird
        self.mode = mode
        self.selected_option = 0
        
        self.options = [
            "1. Jugar de nuevo ",
            "2. Cambiar Modo",
            "3. Salir al Menu"
        ]

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
    
        if self.world is not None:
            self.world.render(surface)
        if self.bird is not None:
            self.bird.render(surface)
            
        render_text(
            surface,
            "GAME OVER",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 4 - 20,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        
        render_text(
            surface,
            f"Puntuacion final: {self.score}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 4 + 40,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    
        for i, option in enumerate(self.options):
            color = settings.COLOR_WHITE if i == self.selected_option else (100, 100, 100)
            y_pos = settings.VIRTUAL_HEIGHT / 2 + (i * 30)
            
            render_text(
                surface,
                option,
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
                self.selected_option = (self.selected_option + 1) % 3
            elif input_id == "up":
                self.selected_option = (self.selected_option - 1) % 3
                
            elif input_id == "confirm":

                if self.selected_option == 0:
                    self.state_machine.change("count_down", mode=self.world.mode, score=0)
                elif self.selected_option == 1:
                    self.state_machine.change("mode_selection")
                elif self.selected_option == 2:
                    self.state_machine.change("title")