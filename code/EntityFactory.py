#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from code.Cons import WIN_WIDTH
from code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        if entity_name == 'Enemy1':
            x = random.randint(20, WIN_WIDTH - 84)
            return Enemy('Enemy1', (x, -150))

        if entity_name == 'Enemy2':
            x = random.randint(20, WIN_WIDTH - 120)
            return Enemy('Enemy2', (x, -220))

        return None