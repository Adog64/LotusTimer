import os
import pygame
import random
from src.settings import *
import json
import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import statistics as stat

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

class Session:
    def __init__(self, path, session=1):
        self.session_number = session
        self.path = path
        self.best = None
        self.avg = None
        self.sdev = None
        self.data = None
        self.solve_rate = None

        self.retrieve_data()

    def retrieve_data(self):
        self.data = json.load(open(self.path))
        times = self.get_times()
        solved = []
        for t in times:
            if t[0] >=0:
                solved.append(t[1]+t[0])
        if len(times) > 0:
            self.solve_rate = [solved, len(times)]
            self.avg = stat.mean(solved)
            self.sdev = stat.stdev(solved)
            self.best = min(solved)

    @classmethod
    def get_WCA_AoN(cls, n=5, penalties_times=[]):
        penalties = [item[0] for item in penalties_times]
        times = [item[1] for item in penalties_times]

        if len(times) != n:
            return
        elif -1 in penalties and penalties.index(-1) != penalties[-1::-1]:
            return -1
        else:
            if -1 in penalties:
                dnf = penalties.index(-1)
                for i in range(len(times)):
                    times[i] = (penalties[i] + times[i], -1)[i == dnf]
            else:
                penalties = sorted(penalties)[1:-1]
        return stat.mean(times)


    @classmethod
    def parse_session_setting(cls):
        data = cls.session_settings[str(cls.session)]

        #decode puzzle from json
        type = '3x3'
        if data['opt'] != {}:
            cs_type = data['opt']['scrType'][:2]
            type = CUBE_PREFIXES[cs_type]
        return type

    def add_time(self, time, scramble, timestamp):
        self.data[f'session{self.session_number}'].append([time, scramble, timestamp])
        os.remove(self.path)
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def remove_time(self, index):
        try:
            self.data[f'session{self.session_number}'].remove(index)
            os.remove(self.path)
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
        except IndexError:
            return
        
    def get_times(self):
        s = self.data[f'session{self.session_number}']
        t = []
        idx = 1
        for i in s:
            t.append([i[0][0], i[0][1], idx])
            idx += 1
        return t
    
    def change_session(self, session=1):
        self.session_number = session

class SpotifyPlayer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        scope = "user-read-playback-state,user-modify-playback-state,streaming"

        auth = SpotifyOAuth(
                    client_id="2d0aa7b1e8e34e6db2bbcc9e35fd4db5",
                    client_secret="264330e29b1143f28800cc39b0ab8007",
                    redirect_uri="http://google.com/",
                    scope=scope)

        token = auth.get_access_token(as_dict=False)
        self.spotify = spotipy.Spotify(auth=token)

    def play_song(self, song_title):
        devices = self.spotify.devices()
        device_id = devices['devices'][0]['id']
        track = self.spotify.search(song_title)['tracks']['items'][0]['uri']
        #self.spotify.start_playback(uris=[track], device_id=device_id)
        self.spotify.shuffle(state=True)
        genres = self.spotify.recommendation_genre_seeds()
        queue = self.spotify.recommendations(seed_genres='reggae')
        self.spotify.add_to_queue(queue)