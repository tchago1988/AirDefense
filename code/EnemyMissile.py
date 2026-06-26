#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import pygame

from code.Cons import ENTITY_SPEED, ENTITY_DAMAGE, ENTITY_HEALTH


class EnemyMissile:
    def __init__(self, position: tuple, target_position: tuple):
        self.name = 'EnemyMissile'
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.speed = ENTITY_SPEED[self.name]

        self.surf = pygame.image.load('./asset/Missile.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (22, 44))

        dx = target_position[0] - position[0]
        dy = target_position[1] - position[1]

        distance = math.hypot(dx, dy)

        if distance == 0:
            distance = 1

        self.x_speed = (dx / distance) * self.speed
        self.y_speed = (dy / distance) * self.speed

        # Calcula o ângulo do míssil inimigo
        angle = math.degrees(math.atan2(-dy, dx))

        # Rotaciona o sprite para apontar na direção do player
        self.surf = pygame.transform.rotate(
            self.surf,
            angle - 90
        )

        self.rect = self.surf.get_rect(center=position)

        self.x_float = float(self.rect.centerx)
        self.y_float = float(self.rect.centery)

    def move(self):
        self.x_float += self.x_speed
        self.y_float += self.y_speed

        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)