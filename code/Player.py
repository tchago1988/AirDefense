#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Entity import Entity
from code.Missile import Missile
from code.Cons import (
    DIR_CENTER,
    MISSILE_ANGLES,
    ENTITY_HEALTH,
    ENTITY_SHOT_DELAY,
    PLAYER_KEY_LEFT,
    PLAYER_KEY_RIGHT,
    PLAYER_KEY_SHOOT,
)


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.direction = DIR_CENTER
        self.health = ENTITY_HEALTH[self.name]

        self.shoot_delay = 0
        self.rotate_delay = 0

        self.load_sprite()

        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def load_sprite(self):
        center = self.rect.center if hasattr(self, 'rect') else (0, 0)

        self.surf = pygame.image.load(
            f'./asset/{self.name}_{self.direction}.png'
        ).convert_alpha()

        self.surf = pygame.transform.scale(self.surf, (72, 72))
        self.rect = self.surf.get_rect(center=center)

    def move(self):
        keys = pygame.key.get_pressed()
        self.rotate_delay += 1

        if self.rotate_delay >= 10:
            if keys[PLAYER_KEY_LEFT[self.name]]:
                if self.direction > 0:
                    self.direction -= 1
                    self.load_sprite()
                self.rotate_delay = 0

            elif keys[PLAYER_KEY_RIGHT[self.name]]:
                if self.direction < 4:
                    self.direction += 1
                    self.load_sprite()
                self.rotate_delay = 0

    def shoot(self):
        self.shoot_delay += 1
        keys = pygame.key.get_pressed()

        if keys[PLAYER_KEY_SHOOT[self.name]]:
            if self.shoot_delay >= ENTITY_SHOT_DELAY[self.name]:
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
                    angle,
                    self.name
                )

        return None
