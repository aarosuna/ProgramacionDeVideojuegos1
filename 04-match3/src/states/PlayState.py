"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Tile import Tile


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]
        self.dragged_tile = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_shuffling = False


        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            # If the board is being reorganized, we exit the function.
            if getattr(self, "is_shuffling", False):
                return
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

        if getattr(self, 'dragged_tile', None):
            pos_x, pos_y = pygame.mouse.get_pos()
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            
            self.dragged_tile.x = pos_x - self.board.x - self.drag_offset_x
            self.dragged_tile.y = pos_y - self.board.y - self.drag_offset_y

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if getattr(self, 'dragged_tile', None):
            self.dragged_tile.render(surface, self.board.x, self.board.y)

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

        if getattr(self, "is_shuffling", False):
            #Draw a dark, semi-transparent rectangle over the board to darken the old pieces.
            overlay = pygame.Surface((settings.BOARD_WIDTH * settings.TILE_SIZE, settings.BOARD_HEIGHT * settings.TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 180), overlay.get_rect(), border_radius=7)
            surface.blit(overlay, (self.board.x, self.board.y))

            render_text(
                surface,
                "No possible moves!",
                settings.FONTS["medium"],
                self.board.x + 12,
                self.board.y + 100,
                (255,99,99),
                shadowed=True,
            )
            render_text(
                surface,
                "Shuffling...",
                settings.FONTS["medium"],
                self.board.x + 60,
                self.board.y + 130,
                (255,255,255),
                shadowed=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        pos_x, pos_y = input_data.position
        pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
        pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

        if input_id == "click" and input_data.pressed:
          
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE

            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                tile = self.board.tiles[i][j]
                if tile is not None:
                    self.dragged_tile = tile
                    self.dragged_tile.is_dragging = True
                    self.dragged_tile.orig_x = tile.x
                    self.dragged_tile.orig_y = tile.y
                    self.drag_offset_x = pos_x - (self.board.x + tile.x)
                    self.drag_offset_y = pos_y - (self.board.y + tile.y)

        elif input_id == "click" and not input_data.pressed:
            if getattr(self, 'dragged_tile', None):
                tile1 = self.dragged_tile
                tile1.is_dragging = False
                self.dragged_tile = None
                
                dest_i = (pos_y - self.board.y) // settings.TILE_SIZE
                dest_j = (pos_x - self.board.x) // settings.TILE_SIZE

                di = abs(dest_i - tile1.i)
                dj = abs(dest_j - tile1.j)

                if di == 0 and dj == 0 and (getattr(tile1, 'is_bomb', False) or getattr(tile1, 'is_color_bomb', False)):
                    self.active = False
                    tile1.force_explode = True
                    self._calculate_matches([tile1])
                    return

                if di <= 1 and dj <= 1 and di != dj and (0 <= dest_i < settings.BOARD_HEIGHT) and (0 <= dest_j < settings.BOARD_WIDTH):
                    self.active = False
                    tile2 = self.board.tiles[dest_i][dest_j]

                    def arrive():
                        (
                            self.board.tiles[tile1.i][tile1.j],
                            self.board.tiles[tile2.i][tile2.j],
                        ) = (
                            self.board.tiles[tile2.i][tile2.j],
                            self.board.tiles[tile1.i][tile1.j],
                        )
                        tile1.i, tile1.j, tile2.i, tile2.j = (
                            tile2.i, tile2.j, tile1.i, tile1.j,
                        )
                        
                        matches = self.board.calculate_matches_for([tile1, tile2])
                        
                        if matches is None:
                            settings.SOUNDS["error"].play()
                            (
                                self.board.tiles[tile1.i][tile1.j],
                                self.board.tiles[tile2.i][tile2.j],
                            ) = (
                                self.board.tiles[tile2.i][tile2.j],
                                self.board.tiles[tile1.i][tile1.j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                                tile2.i, tile2.j, tile1.i, tile1.j,
                            )
                            Timer.tween(
                                0.25,
                                [
                                    (tile1, {"x": tile1.j * settings.TILE_SIZE, "y": tile1.i * settings.TILE_SIZE}),
                                    (tile2, {"x": tile2.j * settings.TILE_SIZE, "y": tile2.i * settings.TILE_SIZE}),
                                ],
                                on_finish=lambda: setattr(self, 'active', True)
                            )
                        else:
                            self.board.matches = []
                            self._calculate_matches([tile1, tile2])

                    Timer.tween(
                        0.25,
                        [
                            (tile1, {"x": tile2.x, "y": tile2.y}),
                            (tile2, {"x": tile1.orig_x, "y": tile1.orig_y}),
                        ],
                        on_finish=arrive,
                    )
                else:
                    settings.SOUNDS["error"].play()
                    self.active = False
                    Timer.tween(
                        0.25,
                        [(tile1, {"x": tile1.orig_x, "y": tile1.orig_y})],
                        on_finish=lambda: setattr(self, 'active', True)
                    )

    def _calculate_matches(self, tiles: List) -> None:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            if not self.board.has_possible_moves():
                self.active = False
                settings.SOUNDS["error"].play()
                self.is_shuffling = True

                def do_reshuffle():
                    self.board.reshuffle()
                    self.is_shuffling = False
                    self.active = True

                Timer.after(1.5, do_reshuffle)
            else:
                self.active = True
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        # Look for 4-piece combinations to generate bombs.
        bombs_to_spawn = []
        for match in matches:
            self.score += len(match) * 50
            is_explosion = any(getattr(t, 'is_bomb', False) or getattr(t, 'is_color_bomb', False) for t in match)
            if len(match) >= 4 and not is_explosion:
                #Determine the type of pump.
                trigger = next((t for t in match if t in tiles), match[0])
                bomb_type = 'color_bomb' if len(match) >= 5 else 'line_bomb'
                bombs_to_spawn.append({
                    'i': trigger.i, 'j': trigger.j, 
                    'color': trigger.color, 'variety': trigger.variety, 
                    'type': bomb_type
                })

        self.board.remove_matches()

        for b in bombs_to_spawn:
            bomb = Tile(b['i'], b['j'], b['color'], b['variety'])

            if b['type'] == 'color_bomb':
                bomb.is_color_bomb = True
            else:
                bomb.is_bomb = True

            self.board.tiles[b['i']][b['j']] = bomb

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
