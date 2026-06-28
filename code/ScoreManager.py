#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class ScoreManager:
    def __init__(self):
        self.save_dir = './save'
        self.save_file = f'{self.save_dir}/best_score.txt'

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def load_best_score(self):
        if not os.path.exists(self.save_file):
            return 0

        try:
            with open(self.save_file, 'r', encoding='utf-8') as file:
                return int(file.read())
        except:
            return 0

    def save_best_score(self, score):
        with open(self.save_file, 'w', encoding='utf-8') as file:
            file.write(str(score))

    def update_best_score(self, score):
        best_score = self.load_best_score()

        if score > best_score:
            self.save_best_score(score)
            return True

        return False