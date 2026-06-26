#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from code.Cons import WIN_WIDTH
from code.Background import Background
from code.Player import Player
from code.Enemy import Enemy
from code.Explosion import Explosion


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:

            case 'Background':
                return [Background('Background', (0, 0))]

            case 'Background1':
                return [Background('Background1', (0, 0))]

            case 'Background2':
                return [Background('Background2', (0, 0))]

            case 'Background3':
                return [Background('Background3', (0, 0))]

            case 'Player1':
                return Player('Player1', (0, 0))

            case 'Player2':
                return Player('Player2', (0, 0))

            case 'Enemy1':
                x = random.randint(20, WIN_WIDTH - 84)
                return Enemy('Enemy1', (x, -150))

            case 'Enemy2':
                x = random.randint(20, WIN_WIDTH - 120)
                return Enemy('Enemy2', (x, -220))

            case 'Explosion':
                return Explosion('Explosion', (0, 0))

        return None