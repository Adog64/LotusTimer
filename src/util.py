from os import times
import pygame
import random
from settings import *
import json

class ScrambleGenerator:
    def __init__(self, puzzle='3x3'):
        self.moves = self.get_moves(puzzle)
        self.length = SCRAMBLE_LENGTHS[puzzle]
        self.scramble = ""

    @classmethod
    def generate_scramble(cls, puzzle="3x3"):
        gen = ScrambleGenerator(puzzle)
        sets = []
        for x in range(random.randint(gen.length[0], gen.length[1])):
            if puzzle in REG_SETS:
                new_set = random.sample(REG_SETS[puzzle], 1)[0]
                if len(sets) == 1:
                    while new_set == sets[0]:
                        new_set = random.sample(REG_SETS[puzzle], 1)[0]
                elif len(sets) > 1:
                    while new_set == sets[x-1] or new_set in gen.opposite_set(new_set):
                        new_set = random.sample(REG_SETS[puzzle], 1)[0]
                sets.append(new_set)
                gen.scramble += random.sample(new_set, 1)[0] + " "
        return gen.scramble

    def get_moves(self, puzzle):
        moves = []
        if puzzle in REG_SETS:
            for set in REG_SETS[puzzle]:
                for move in set:
                    moves.append(move)
        elif puzzle == "Sq1":
            for move in SQ1_MOVES:
                moves.append(move)
        return moves

    def opposite_set(self, set):
        type = ALL_NxN_MOVES.index(set) % 3
        opposites = []
        for i in ALL_NxN_MOVES:
            if i != set and ALL_NxN_MOVES.index(i)%3 == type:
                opposites.append(i)
        return opposites

class SessionManager:
    def __init__(self, path, session=1):
        self.session_number = session
        self.path = path
        self.retrieve_session_data()

    def retrieve_session_data(self):
        data = json.loads(open(self.path).read())
        self.times = data['session' + str(self.session_number)]
        self.settings = json.loads(data['properties']['sessionData'])
    
    def parse_session_setting(self):
        data = self.session_settings[str(self.session)]

        #decode puzzle from json
        type = '3x3'
        if data['opt'] != {}:
            cs_type = data['opt']['scrType'][:2]
            type = CUBE_PREFIXES[cs_type]
        self.puzzle = type

    def add_time(self, time, scramble, timestamp):
        self.times.append([time, scramble, timestamp])
    
    def change_session(self, session=1):
        self.session_number = session
        retrieve
        

if __name__ == '__main__':
    s = SessionManager()
    s.add_time()