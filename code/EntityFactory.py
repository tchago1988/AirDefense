#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.Cons import WIN_WIDTH
from code.Player import Player
from code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        if entity_name == 'Player':
            player = Player('Player', (0, 0))
            player.rect.centerx = WIN_WIDTH // 2
            player.rect.centery = 640
            return player

        if entity_name == 'Enemy1':
            x = random.randint(20, WIN_WIDTH - 70)
            return Enemy('Enemy1', (x, -150))

        if entity_name == 'Enemy2':
            x = random.randint(20, WIN_WIDTH - 100)
            return Enemy('Enemy2', (x, -220))

        return None