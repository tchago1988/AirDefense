#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Entity import Entity


class Missile(Entity):

    def __init__(self, name: str, position: tuple, angle: tuple):

        super().__init__(name, position)

        self.surf = pygame.transform.scale(self.surf,(72, 120))

        self.rect = self.surf.get_rect(center=position)

        self.x_speed = angle[0]
        self.y_speed = angle[1]

    def move(self):

        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed