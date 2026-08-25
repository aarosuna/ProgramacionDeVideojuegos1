"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair
from src.PowerUp import PowerUp

class World:
    def __init__(self, generate_logs: bool = False, mode: str = "normal") -> None:
        self.generate_logs: bool = generate_logs
        self.mode: str = mode
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        self.logs: List[LogPair] = []
        self.logs_spawn_timer: float = 1.5
        self.time_to_next_spawn : float = random.uniform(1.5, 2.0)
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.log_pair_factory: Factory = Factory(LogPair)
        self.powerups = []
        self.powerup_factory: Factory = Factory(PowerUp)
        self.powerup_timer = 0.0

    def reset(self, generate_logs: bool, mode: str = "normal") -> None:
        self.generate_logs = generate_logs
        self.mode = mode

    def collides(self, rect: pygame.Rect, is_ghost: bool = False) -> bool:
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True
        if is_ghost:
            return False

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def update(self, dt: float) -> None:
        if self.generate_logs:
            self.logs_spawn_timer += dt
            self.powerup_timer += dt

            if self.powerup_timer > 15.0:
                time_to_next = self.time_to_next_spawn - self.logs_spawn_timer
                if self.logs_spawn_timer > 0.6 and time_to_next > 0.6:
                    self.powerup_timer = 0.0
                    if self.mode == "hard" and random.random() < 1.0:
                        valid_spawn = False
                        attempts = 0
                        py = 0
                        while not valid_spawn and attempts < 10:
                            py = random.randint(50, settings.VIRTUAL_HEIGHT - 100)
                            temp_rect = pygame.Rect(settings.VIRTUAL_WIDTH, py, 39, 28)

                            collision = any(log_pair.collides(temp_rect) for log_pair in self.logs)
                            if not collision:
                                valid_spawn = True

                            attempts += 1
                        if valid_spawn:
                            self.powerups.append(self.powerup_factory.create(settings.VIRTUAL_WIDTH, py))

            if self.logs_spawn_timer >= self.time_to_next_spawn:
                self.logs_spawn_timer = 0.0

                if self.mode == "hard":
                    self.time_to_next_spawn = random.uniform(1.2, 2.5)
                    gap_size = random.randint(70, 105)

                    is_moving = random.random() < 0.3
                    is_symmetrical = random.random() < 0.5 if is_moving else False
                    max_y_shift = int(60 * self.time_to_next_spawn)
                    
                else:
                    self.time_to_next_spawn = random.uniform(1.5, 2.0)
                    gap_size = random.randint(85, 130)
                    is_moving = False
                    is_symmetrical = False
                    max_y_shift = int(25 * (self.time_to_next_spawn / 1.5))

                y = max(
                    -settings.LOG_HEIGHT + 20,
                    min(
                        self.last_log_y + random.randint(-max_y_shift, max_y_shift),
                        settings.VIRTUAL_HEIGHT - gap_size - settings.LOG_HEIGHT - 30,
                    ),
                )
                self.last_log_y = y
                self.logs.append(
                    self.log_pair_factory.create(
                        settings.VIRTUAL_WIDTH, 
                        y,
                        {"gap_size": gap_size, "is_moving": is_moving, "is_symmetrical": is_symmetrical}
                    )
                )

        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        for log_pair in self.logs:
            log_pair.update(dt)

        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]

        for p in self.powerups:
            p.update(dt)
        self.powerups = [p for p in self.powerups if not p.to_remove]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        for p in self.powerups:
            p.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
