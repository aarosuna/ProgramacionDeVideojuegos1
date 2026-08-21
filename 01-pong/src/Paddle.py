"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Paddle.
"""

import pygame

import settings


class Paddle:
    def __init__(self, x: float, y: float, width: float, height: float, is_ai: bool = False) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.is_ai: bool = is_ai

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float, ball=None) -> None:
        if self.is_ai and ball is not None: 
            paddle_center = self.y + self.height / 2
            is_left_paddle = self.x < settings.VIRTUAL_WIDTH / 2
            ball_heading_towards = (is_left_paddle and ball.vx < 0) or (not is_left_paddle and ball.vx > 0)

            if ball_heading_towards:
                deadzone = self.height / 4

                if paddle_center < ball.y - deadzone:
                    self.vy = settings.PADDLE_SPEED
                elif paddle_center > ball.y + deadzone:
                    self.vy = -settings.PADDLE_SPEED
                else:
                    self.vy = 0.0
            else:
                self.vy = 0.0

        self.y += self.vy * dt
        self.y = max(0, min(settings.VIRTUAL_HEIGHT - self.height, self.y))

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, settings.COLOR_WHITE, self.get_rect())
