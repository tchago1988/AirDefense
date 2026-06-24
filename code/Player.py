#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Entity import Entity
from code.Cons import WIN_WIDTH, WINDOW_HEIGHT, ENTITY_SPEED, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT
from code.Missile import Missile


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.surf = pygame.transform.scale(self.surf, (80, 80))
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.shoot_delay = 0

    def move(self):
        pressed_key = pygame.key.get_pressed()

        if pressed_key[PLAYER_KEY_LEFT] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]

        if pressed_key[PLAYER_KEY_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]

        self.rect.bottom = WINDOW_HEIGHT - 20

    def shoot(self):
        self.shoot_delay += 1

        pressed_key = pygame.key.get_pressed()

        if pressed_key[PLAYER_KEY_SHOOT] and self.shoot_delay >= 15:
            self.shoot_delay = 0
            return Missile('Missile', (self.rect.centerx - 8, self.rect.top - 20))

        return None