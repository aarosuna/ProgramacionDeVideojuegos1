"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class TitleState.
"""

import random

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.rendering import render_table


class TitleState(BaseState):
    def enter(self, pong) -> None:
        self.pong = pong
        self.selected_mode = 0

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)
        render_text(
            surface,
            "Pong",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 4,
            settings.COLOR_WHITE,
            center=True,
        )
        modes = [
            "1. Human vs Human", 
            "2. Human (Left) vs AI", 
            "3. AI vs Human (Right)" , 
            "4. AI vs AI"
        ]

        for i, mode in enumerate(modes):
            color = settings.COLOR_WHITE if self.selected_mode == i else (100, 100, 100)
            y_pos = settings.VIRTUAL_HEIGHT / 2 + (i * 20)

            render_text(
                surface,
                mode,
                settings.FONTS["large"],
                settings.VIRTUAL_WIDTH / 2,
                y_pos,
                color,
                center=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_data.pressed:
            if input_id in ("p1_down", "p2_down"):
                self.selected_mode = (self.selected_mode + 1) % 4

            elif input_id in ("p1_up", "p2_up"):
                self.selected_mode = (self.selected_mode - 1) % 4
            
            if input_id == "confirm":

                if self.selected_mode == 0:
                    self.pong.player1.is_ai = False
                    self.pong.player2.is_ai = False
                elif self.selected_mode == 1:
                    self.pong.player1.is_ai = False
                    self.pong.player2.is_ai = True
                elif self.selected_mode == 2:
                    self.pong.player1.is_ai = True
                    self.pong.player2.is_ai = False
                elif self.selected_mode == 3:
                    self.pong.player1.is_ai = True
                    self.pong.player2.is_ai = True

                self.pong.serving_player = random.randint(1, 2)
                self.state_machine.change("serve", pong=self.pong)
