import pygame
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
import settings

class PauseState(BaseState):
    def enter(self, mode, world, bird, score) -> None:
        self.world = world
        self.bird = bird
        self.score = score
        self.mode = mode
        pygame.mixer.music.pause()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        
        render_text(
            surface,
            "PAUSED",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            pygame.mixer.music.unpause()
            self.state_machine.change("count_down", mode=self.mode, world=self.world, bird=self.bird, score=self.score)