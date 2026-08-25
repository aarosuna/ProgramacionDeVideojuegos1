"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame

import settings


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float, movement_strategy) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.movement_strategy = movement_strategy
        self.jumping: bool = False
        self.is_ghost: bool = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float) -> None:
        self.movement_strategy.update(self, dt)

        if self.y < 0 :
            self.y = 0
            self.vy = 0

    def render(self, surface: pygame.Surface) -> None:
        texture_key = "bird_ghost" if self.is_ghost else "bird"
        surface.blit(settings.TEXTURES[texture_key], self.get_rect())
