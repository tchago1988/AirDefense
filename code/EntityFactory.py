#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.Cons import WIN_WIDTH, WINDOW_HEIGHT
from code.Player import Player
from code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        if entity_name == 'Player':
            return Player('Player', (WIN_WIDTH // 2 - 40, WINDOW_HEIGHT - 100))

        if entity_name == 'Enemy1':
            x = random.randint(20, WIN_WIDTH - 80)
            return Enemy('Enemy1', (x, -80))

        if entity_name == 'Enemy2':
            x = random.randint(20, WIN_WIDTH - 120)
            return Enemy('Enemy2', (x, -120))

        return None