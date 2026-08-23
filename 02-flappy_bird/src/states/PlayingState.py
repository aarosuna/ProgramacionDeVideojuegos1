"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World

from src.MovementStrategies import NormalMovement, HardMovement

class PlayingState(BaseState):
    def enter(self, world: Optional[World] = None, bird: Optional[Bird] = None, score: int = 0, mode: str = "normal", ghost_timer: float = 0.0) -> None:
        self.world = world if world is not None else World()
        self.mode = mode

        if bird is not None:
            self.bird = bird
            self.score = score
            self.ghost_timer = ghost_timer
        else:
            self.ghost_timer = 0.0
            self.world.reset(True, self.mode)

            if self.mode == "normal":
                strategy = NormalMovement()
            elif self.mode == "hard":
                strategy = HardMovement()

            self.bird = Bird(
                settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
                settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
                settings.BIRD_WIDTH,
                settings.BIRD_HEIGHT,
                strategy
            )    
            self.score = 0

    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt)

        if getattr(self.bird, 'is_ghost', False):
            self.ghost_timer -= dt
    
            if 0 < self.ghost_timer <= 2.0 and not getattr(self, 'warning_played', False):
                settings.SOUNDS["finished_power_up"].play()
                self.warning_played = True
                
            if self.ghost_timer <= 0:
                self.bird.is_ghost = False
                settings.SOUNDS["finish_power_up"].play()
                settings.SOUNDS["back_power_up"].stop()
                pygame.mixer.music.unpause()
              

        for p in self.world.powerups:
            if p.collides(self.bird.get_rect()):
                p.to_remove = True 
                self.bird.is_ghost = True
                self.ghost_timer = 7.0
                self.warning_played = False
                settings.SOUNDS["power_up"].play()
                pygame.mixer.music.pause()
                settings.SOUNDS["back_power_up"].play(loops=-1)

        if self.world.collides(self.bird.get_rect(), getattr(self.bird, 'is_ghost', False)):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            settings.SOUNDS["back_power_up"].stop()
            pygame.mixer.music.unpause()
            self.state_machine.change("game_over", score=self.score, world=self.world, bird=self.bird)
            return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()

        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change("pause", mode=self.mode, world=self.world, bird=self.bird, score=self.score, ghost_timer=self.ghost_timer)
