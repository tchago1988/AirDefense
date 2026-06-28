#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pygame
from code.Entity import Entity
from code.Cons import ENTITY_SPEED
from code.EnemyMissile import EnemyMissile


class Enemy(Entity):  # Initialize the base entity.
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Set the enemy movement speed.
        self.speed = ENTITY_SPEED[self.name]
        # Scale the sprite according to the enemy type.
        if self.name == 'Enemy1':
            self.surf = pygame.transform.scale(self.surf.convert_alpha(), (64, 64))
        elif self.name == 'Enemy2':
            self.surf = pygame.transform.scale(self.surf.convert_alpha(), (96, 96))
        # Position the enemy on the screen.
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        # Initialize the shooting timer.
        self.shoot_delay = random.randint(2000, 4000)
        self.last_shot = pygame.time.get_ticks()

    def move(self):  # Moves the enemy downward.
        self.rect.centery += self.speed

    def shoot(self, target_position):  # Launches a missile toward the target position.
        current_time = pygame.time.get_ticks()
        # Check whether the shooting delay has expired.
        if current_time - self.last_shot >= self.shoot_delay:
            # Reset the shooting timer.
            self.last_shot = current_time
            # Generate a new random delay for the next shot.
            self.shoot_delay = random.randint(2000, 4000)
            # Create and return a new enemy missile.
            return EnemyMissile(self.rect.center, target_position)
        # No missile was fired.
        return None
