#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pygame

from code.Entity import Entity
from code.Cons import ENTITY_SPEED
from code.EnemyMissile import EnemyMissile


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.speed = ENTITY_SPEED[self.name]

        if self.name == 'Enemy1':
            self.surf = pygame.transform.scale(self.surf.convert_alpha(), (64, 64))

        elif self.name == 'Enemy2':
            self.surf = pygame.transform.scale(self.surf.convert_alpha(), (96, 96))

        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.shoot_delay = random.randint(2000, 4000)
        self.last_shot = pygame.time.get_ticks()

    def move(self):
        self.rect.centery += self.speed

    def shoot(self, target_position):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot >= self.shoot_delay:
            self.last_shot = current_time
            self.shoot_delay = random.randint(2000, 4000)

            return EnemyMissile(
                self.rect.center,
                target_position
            )

        return None