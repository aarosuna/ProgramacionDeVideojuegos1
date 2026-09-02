"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
import math
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        self.target_score = 250
        self.fade_alpha = 0
        self.objective_reached = False
        self.max_radius = math.hypot(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        self.transition_radius = 0
        self.is_transitioning = True
        Timer.tween(
            1.0,
            [(self, {"transition_radius": self.max_radius})],
            on_finish=lambda: setattr(self, 'is_transitioning', False)
        )
       
        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            # Resting exactly on the ground tile's surface (row 9, one tile
            # below the platform's top edge) rather than a few pixels into
            # it, so gale.tilemap's one-way platform collision (which
            # requires the entity to already be at/above the surface) picks
            # it up on the very first frame instead of falling through.
            spawn_y = 9 * self.tilemap.tile_height - 20
            self.player = Player(0, spawn_y, self.game_level)
            self.player.change_state("idle")

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.follow(self.player, rate=settings.CAMERA_FOLLOW_RATE)
            self.camera.bounds = self.game_level.get_rect()
            self.camera.x, self.camera.y = self.player.x, self.player.y
            self.camera.update(0)

        self.clock = enter_params.get("clock")

        if self.clock is None:
            self.clock = Clock(30)

            def countdown_timer():

                if getattr(self, "objective_reached", False):
                    return

                self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")

            Timer.every(1, countdown_timer)
        else:
            Timer.resume()

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)

        if self.player.y >= self.tilemap.pixel_height:
            self.player.change_state("dead")

        self.camera.update(dt)
        self.game_level.update(dt)

        player_rect = self.player.get_rect()

        for block in self.game_level.special_blocks:

            if self.player.score >= self.target_score and not block.is_active:
                block.reveal()
                self.objective_reached = True
                self.game_level.items = [
                    item for item in self.game_level.items 
                    if getattr(item, "texture_id", None) == "key" or getattr(item, "item_name", None) == "key"
                ]
                
                self.game_level.creatures.clear()

                pygame.mixer.music.stop()
                pygame.mixer.music.load(
                    settings.BASE_DIR / "assets" / "sounds" / "finish.mp3"
                )
                pygame.mixer.music.play(loops=-1)

                
            if not block.is_active:
                continue
            
            block_rect = block.get_rect()
            
            if player_rect.colliderect(block_rect):
                if self.player.vy > 0 and player_rect.bottom - self.player.vy * dt <= block_rect.top + 4:
                    self.player.y = block_rect.top - self.player.height
                    self.player.vy = 0
                    self.player.on_ground = True

                elif self.player.vy < 0 and player_rect.top - self.player.vy * dt >= block_rect.bottom - 4:
                    self.player.y = block_rect.bottom
                    self.player.vy = 0
                    block.hit() 
                
                elif self.player.vx > 0:
                    self.player.x = block_rect.left - self.player.width
                    self.player.vx = 0

                elif self.player.vx < 0:
                    self.player.x = block_rect.right
                    self.player.vx = 0

        for creature in self.game_level.creatures:
            if self.player.collides(creature):

                if self.player.vy > 0:
                    self.player.vy = -settings.JUMP_TAKEOFF_SPEED / 1.5
                    settings.SOUNDS["jump"].play()
                    if "fall" in creature.state_machine.states:
                        creature.change_state("fall")
                    else:
                        creature.is_dead = True
                else:
                    self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.active or not item.collidable:
                continue

            is_key = getattr(item, "texture_id", None) == "key" or getattr(item, "item_name", None) == "key"

            if getattr(self, "objective_reached", False) and not is_key:
                continue

            if self.player.collides(item):
                item.active = False

                if getattr(item, "texture_id", None) == "key" or getattr(item, "item_name", None) == "key":
                    settings.SOUNDS["pickup_coin"].play()
                    if not getattr(self, "is_transitioning", False):
                        self.is_transitioning = True
                        pygame.mixer.music.stop()
                        
                    def finish_level():
                        next_level = self.level + 1
                        if next_level > settings.NUM_LEVELS:
                            self.state_machine.change("start")
                        else:
                            self.state_machine.change("play", level=next_level)

                    self.transition_radius = self.max_radius
                    Timer.tween(
                        1.0,
                        [(self, {"transition_radius": 0})],
                        on_finish=finish_level
                    )
                else:
                    item.on_collide(self.player)
                    item.on_consume(self.player)

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        self.player.render(surface, self.camera)

        for item in self.game_level.items:
            if item.active:
                item.render(surface, self.camera)

        if self.transition_radius < self.max_radius:
            mask = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), 
                pygame.SRCALPHA
            )
            mask.fill((0, 0, 0))
            char_screen_x = int((self.player.x + self.player.width / 2) - self.camera.x)
            char_screen_y = int((self.player.y + self.player.height / 2) - self.camera.y)

            COLOR_KEY = (255, 0, 255)  # Magenta color for transparency
            pygame.draw.circle(
                mask, 
                COLOR_KEY, 
                (char_screen_x, char_screen_y), 
                int(self.transition_radius)
            )
            mask.set_colorkey(COLOR_KEY)
            surface.blit(mask, (0, 0))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)
