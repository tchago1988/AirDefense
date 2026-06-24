#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import pygame

from code.Entity import Entity


class Missile(Entity):
    def __init__(self, name: str, position: tuple, angle_degrees: int):
        super().__init__(name, position)

        self.speed = 10
        self.angle_degrees = angle_degrees

        self.surf = pygame.transform.scale(self.surf, (24, 48))

        # Rotaciona a imagem do míssil para apontar na direção correta
        self.surf = pygame.transform.rotate(
            self.surf,
            self.angle_degrees - 90
        )

        self.rect = self.surf.get_rect(center=position)

        angle_radians = math.radians(self.angle_degrees)

        self.x_speed = math.cos(angle_radians) * self.speed
        self.y_speed = -math.sin(angle_radians) * self.speed

        self.x_float = float(self.rect.centerx)
        self.y_float = float(self.rect.centery)

    def move(self):
        self.x_float += self.x_speed
        self.y_float += self.y_speed

        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)