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
    def get_entity(entity_name: str):  # Creates and returns the requested game entity.
        match entity_name:
            # Create the default background.
            case 'Background':
                return [Background('Background', (0, 0))]
            # Create the Level 1 background.
            case 'Background1':
                return [Background('Background1', (0, 0))]
            # Create the Level 2 background.
            case 'Background2':
                return [Background('Background2', (0, 0))]
            # Create the Level 3 background.
            case 'Background3':
                return [Background('Background3', (0, 0))]
            # Create Player 1.
            case 'Player1':
                return Player('Player1', (0, 0))
            # Create Player 2.
            case 'Player2':
                return Player('Player2', (0, 0))
            # Create Enemy 1 at a random horizontal position.
            case 'Enemy1':
                x = random.randint(20, WIN_WIDTH - 84)
                return Enemy('Enemy1', (x, -150))
            # Create Enemy 2 at a random horizontal position.
            case 'Enemy2':
                x = random.randint(20, WIN_WIDTH - 120)
                return Enemy('Enemy2', (x, -220))
            # Create an explosion effect.
            case 'Explosion':
                return Explosion('Explosion', (0, 0))
        # Return None if the requested entity does not exist.
        return None
