#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.Entity import Entity
from code.Cons import ENTITY_SPEED


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        if self.name == 'Enemy1':
            self.surf = self.surf.convert_alpha()
            self.surf = __import__('pygame').transform.scale(self.surf, (64, 64))

        elif self.name == 'Enemy2':
            self.surf = self.surf.convert_alpha()
            self.surf = __import__('pygame').transform.scale(self.surf, (96, 96))

        self.rect = self.surf.get_rect(left=position[0], top=position[1])

    def move(self):
        self.rect.centery += ENTITY_SPEED[self.name]