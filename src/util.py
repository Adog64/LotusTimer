import os
from src.settings import *
import json
import configparser
import spotipy
from pyTwistyScrambler import scrambler222, scrambler333, scrambler444, \
scrambler555, scrambler666, scrambler777, skewbScrambler, \
squareOneScrambler, megaminxScrambler, pyraminxScrambler, clockScrambler
from spotipy.oauth2 import SpotifyOAuth
import statistics as stat
from math import ceil

class ScrambleGenerator:
    puzzle_types = {'2x2':scrambler222, '3x3':scrambler333,
            '4x4':scrambler444, '5x5':scrambler555, '6x6':scrambler666,
            '7x7':scrambler777, 'sqn':squareOneScrambler, 'skb':skewbScrambler,
            'mega':megaminxScrambler, 'pyra':pyraminxScrambler, 'clk':clockScrambler}

    def __init__(self, puzzle='3x3'):
        self.puzzle = puzzle
        # self.moves = self.get_moves(puzzle)
        # self.length = SCRAMBLE_LENGTHS[puzzle]
        # self.scramble = ""

    @classmethod
    def generate_scramble(cls, puzzle="3x3"):
        return cls.puzzle_types[puzzle].get_WCA_scramble().replace('/', ' / ')
        # gen = ScrambleGenerator(puzzle)
        # sets = []
        # for x in range(random.randint(gen.length[0], gen.length[1])):
        #     if puzzle in REG_SETS:
        #         new_set = random.sample(REG_SETS[puzzle], 1)[0]
        #         if len(sets) == 1:
        #             while new_set == sets[0]:
        #                 new_set = random.sample(REG_SETS[puzzle], 1)[0]
        #         elif len(sets) > 1:
        #             while new_set == sets[x-1] or new_set in gen.opposite_set(new_set):
        #                 new_set = random.sample(REG_SETS[puzzle], 1)[0]
        #         sets.append(new_set)
        #         gen.scramble += random.sample(new_set, 1)[0] + " "
        # return gen.scramble
        
    def get_moves(self, puzzle):
        # moves = []
        # if puzzle in REG_SETS:
        #     for set in REG_SETS[puzzle]:
        #         for move in set:
        #             moves.append(move)
        # elif puzzle == "Sq1":
        #     for move in SQ1_MOVES:
        #         moves.append(move)
        # return moves
        pass

    def opposite_set(self, set):
        # type = ALL_NxN_MOVES.index(set) % 3
        # opposites = []
        # for i in ALL_NxN_MOVES:
        #     if i != set and ALL_NxN_MOVES.index(i)%3 == type:
        #         opposites.append(i)
        # return opposites
        pass

class Session:
    def __init__(self, path, session=1, type='4x4'):
        self.session_number = session
        self.path = path
        self.best = None
        self.avg = None
        self.sdev = None
        self.data = None
        self.solve_rate = None
        self.ao5 = None
        self.ao12 = None
        self.ao100 = None
        self.ao1000 = None
        self.puzzle = type
        self.retrieve_data()

    def generate_scramble(self):
        return ScrambleGenerator.generate_scramble(self.puzzle)

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
            self.best = min(solved)
        if len(times) > 1:
            self.sdev = stat.stdev(solved)
        if len(times) >= 5:
            self.ao5 = self.get_WCA_AoN(n=5, penalties_times=times[:5])
        if len(times) >= 12:
            self.ao12 = self.get_WCA_AoN(n=12, penalties_times=times[:12])
        if len(times) >= 100:
            self.ao100 = self.get_WCA_AoN(n=100, penalties_times=times[:100])
        if len(times) >= 1000:
            self.ao1000 = self.get_WCA_AoN(n=1000, penalties_times=times[:1000])

    @classmethod
    def get_WCA_AoN(cls, n=5, penalties_times=[]):
        penalties = [item[0] for item in penalties_times]
        times = [item[0] + item[1] for item in penalties_times]
        dnfs = penalties.count(-1)
        buffer = ceil(0.05*len(times))

        #not correct number of times
        if len(times) != n:
            return ''
        
        #average is dnf if dnfs account for more than 5% of times
        elif dnfs > buffer:
            return -1
        
        else:
            removes = [item for item in range(len(penalties)) if penalties[item] == -1]
            for r in removes:
                del times[r]
            times = sorted(times, reverse=True)[buffer-dnfs:-buffer]
            return stat.mean(times)
    
    def get_scores(self):
        return [item[0] + item[1] for item in self.get_times() if item[0] != -1]

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
        self.data[f'session{self.session_number}'].append([time, scramble, '', timestamp])
        os.remove(self.path)
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
        self.retrieve_data()

    def remove_time(self, index):
        try:
            self.data[f'session{self.session_number}'].remove(index)
            os.remove(self.path)
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
        except IndexError:
            return
        self.retrieve_data()

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