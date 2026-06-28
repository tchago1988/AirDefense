#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.Entity import Entity
from code.Missile import Missile
from code.Cons import (DIR_CENTER, MISSILE_ANGLES, ENTITY_HEALTH, ENTITY_SHOT_DELAY, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT,
                       PLAYER_KEY_SHOOT, )

class Player(Entity): # Player identifier (Player1 or Player2).
    def __init__(self, name: str, position: tuple):
        self.name = name
        # Initial cannon direction (center position).
        self.direction = DIR_CENTER
        # Player health defined in Cons.py.
        self.health = ENTITY_HEALTH[self.name]
        # Controls the fire rate.
        self.shoot_delay = 0
        # Controls the cannon rotation speed.
        self.rotate_delay = 0
        # Load the initial player sprite.
        self.load_sprite()
        # Set the initial player position.
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def load_sprite(self):  # Loads the sprite according to the current cannon direction.
        center = self.rect.center if hasattr(self, 'rect') else (0, 0)
        # Load the sprite corresponding to the current direction.
        self.surf = pygame.image.load(
            f'./asset/{self.name}_{self.direction}.png').convert_alpha()
        # Scale the sprite to the desired size.
        self.surf = pygame.transform.scale(self.surf, (72, 72))
        # Recreate the collision rectangle while preserving the position.
        self.rect = self.surf.get_rect(center=center)

    def move(self):  # Rotates the player's cannon according to keyboard input.
        keys = pygame.key.get_pressed()
        # Update the rotation timer.
        self.rotate_delay += 1
        # Rotate only after the delay expires.
        if self.rotate_delay >= 10:
            # Rotate to the left.
            if keys[PLAYER_KEY_LEFT[self.name]]:
                if self.direction > 0:
                    self.direction -= 1
                    self.load_sprite()
                self.rotate_delay = 0
            # Rotate to the right.
            elif keys[PLAYER_KEY_RIGHT[self.name]]:
                if self.direction < 4:
                    self.direction += 1
                    self.load_sprite()
                self.rotate_delay = 0

    def shoot(self):  # Creates a missile using the current cannon direction.
        self.shoot_delay += 1
        keys = pygame.key.get_pressed()
        # Fire only when the shoot key is pressed.
        if keys[PLAYER_KEY_SHOOT[self.name]]:
            # Respect the configured shooting delay.
            if self.shoot_delay >= ENTITY_SHOT_DELAY[self.name]:
                self.shoot_delay = 0
                # Get the missile angle for the current direction.
                angle = MISSILE_ANGLES[self.direction]
                # Spawn position for each cannon direction.
                missile_positions = {
                    0: (self.rect.centerx - 34, self.rect.top + 28),
                    1: (self.rect.centerx - 20, self.rect.top + 10),
                    2: (self.rect.centerx, self.rect.top + 5),
                    3: (self.rect.centerx + 20, self.rect.top + 10),
                    4: (self.rect.centerx + 34, self.rect.top + 28),}
                # Create and return the missile.
                return Missile('Missile',missile_positions[self.direction],angle,self.name)
        # No missile was fired.
        return None
