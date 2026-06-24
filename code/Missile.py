#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.Entity import Entity
from code.Cons import ENTITY_SPEED


class Missile(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.surf = pygame.transform.scale(self.surf, (16, 32))
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

    def move(self):
        self.rect.centery -= ENTITY_SPEED[self.name]