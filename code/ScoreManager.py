#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class ScoreManager:
    def __init__(self):
        self.save_dir = './save'
        self.save_file = f'{self.save_dir}/best_score.txt'
        # Create the save directory if it does not exist.
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def load_best_score(self):  # Loads the saved high score.
        # Return zero if no save file exists.
        if not os.path.exists(self.save_file):
            return 0
        try:
            # Read and return the saved score.
            with open(self.save_file, 'r', encoding='utf-8') as file:
                return int(file.read())
        # Return zero if the save file is invalid.
        except:
            return 0

    def save_best_score(self, score):  # Saves a new high score.
        with open(self.save_file, 'w', encoding='utf-8') as file:
            file.write(str(score))

    def update_best_score(self, score):  # Updates the high score if necessary.
        # Load the current high score.
        best_score = self.load_best_score()
        # Save the new score only if it is higher.
        if score > best_score:
            self.save_best_score(score)
            return True
        return False