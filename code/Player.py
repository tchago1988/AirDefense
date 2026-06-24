#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Entity import Entity
from code.Missile import Missile
from code.Cons import (
    WIN_WIDTH,
    PLAYER_KEY_ROTATE_LEFT,
    PLAYER_KEY_ROTATE_RIGHT,
    PLAYER_KEY_SHOOT,
    DIR_CENTER,
    MISSILE_ANGLES
)


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        self.direction = DIR_CENTER

        super().__init__(name, position)

        self.shoot_delay = 0
        self.rotate_delay = 0

        self.load_sprite()

        self.rect.centerx = WIN_WIDTH // 2
        self.rect.centery = 620

    def load_sprite(self):
        center = self.rect.center if hasattr(self, 'rect') else (WIN_WIDTH // 2, 620)

        self.surf = pygame.image.load(
            f'./asset/Player_{self.direction}.png'
        ).convert_alpha()

        self.surf = pygame.transform.scale(self.surf, (96, 96))
        self.rect = self.surf.get_rect(center=center)

    def move(self):
        keys = pygame.key.get_pressed()

        self.rotate_delay += 1

        if self.rotate_delay >= 10:
            if keys[PLAYER_KEY_ROTATE_LEFT]:
                if self.direction > 0:
                    self.direction -= 1
                    self.load_sprite()
                self.rotate_delay = 0

            elif keys[PLAYER_KEY_ROTATE_RIGHT]:
                if self.direction < 4:
                    self.direction += 1
                    self.load_sprite()
                self.rotate_delay = 0

        self.rect.centerx = WIN_WIDTH // 2
        self.rect.centery = 620

    def shoot(self):
        self.shoot_delay += 1
        keys = pygame.key.get_pressed()

        if keys[PLAYER_KEY_SHOOT] and self.shoot_delay >= 15:
            self.shoot_delay = 0

            angle = MISSILE_ANGLES[self.direction]

            missile_positions = {
                0: (self.rect.centerx - 34, self.rect.top + 28),
                1: (self.rect.centerx - 20, self.rect.top + 10),
                2: (self.rect.centerx, self.rect.top + 5),
                3: (self.rect.centerx + 20, self.rect.top + 10),
                4: (self.rect.centerx + 34, self.rect.top + 28),
            }

            return Missile(
                'Missile',
                missile_positions[self.direction],
                angle
            )

        return None