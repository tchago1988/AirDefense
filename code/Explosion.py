#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Entity import Entity


class Explosion(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, (0, 0))

        self.surf = pygame.transform.scale(self.surf, (80, 80))
        self.rect = self.surf.get_rect(center=position)

        self.life_time = 20

    def move(self):
        self.life_time -= 1

        if self.life_time <= 0:
            self.health = 0