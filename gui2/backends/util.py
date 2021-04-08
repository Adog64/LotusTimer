import os
from .settings import *
import json
import configparser
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth
#from twisties.scrambler import WCA_Scrambler
import statistics as stat
from math import ceil

class ScrambleGenerator:
    def __init__(self, puzzle='3x3'):
        self.puzzle = puzzle
        self.moves = self.get_moves(puzzle)
        self.length = SCRAMBLE_LENGTHS[puzzle]
        self.scramble = ""

    @classmethod
    def generate_scramble(cls, puzzle="3x3"):
        #return WCA_Scrambler().get_wca_scramble(puzzle)
        if puzzle != "3x3":
            return ''
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
        return gen.scramble.strip()
        
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
        #pass

    def opposite_set(self, set):
        type = ALL_NxN_MOVES.index(set) % 3
        opposites = []
        for i in ALL_NxN_MOVES:
            if i != set and ALL_NxN_MOVES.index(i)%3 == type:
                opposites.append(i)
        return opposites
        #pass

class Session:
    def __init__(self, path, session, type, scrambles):
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
        self.queue = []
        self.add_to_queue()
        self.retrieve_data()

    def get_scramble(self):
        self.queue_ready = True
        return self.queue.pop(0)

    
    def add_to_queue(self):
        self.queue.append(ScrambleGenerator.generate_scramble(self.puzzle))
        self.queue_ready = False

    def retrieve_data(self):
        self.data = json.load(open(self.path))
        times = self.get_times()
        self.entries = len(times)
        solved = []
        for t in times:
            if t[0] >=0:
                solved.append(t[1]+t[0])
        if len(solved) > 0:
            self.solve_rate = [solved, len(times)]
            self.avg = stat.mean(solved)
            self.best = min(solved)
        if len(solved) > 1:
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
            self.data[f'session{self.session_number}'].pop(index)
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

class SessionManager:
    def __init__(self, session_data):
        self.sessions = {
            '3x3': Session(session_data + 'session_data.json', 1, '3x3', f'{session_data}scrambles.json'),
            '2x2': Session(session_data + 'session_data.json', 1, '2x2', f'{session_data}scrambles.json'),
            '4x4': Session(session_data + 'session_data.json', 1, '4x4', f'{session_data}scrambles.json'),
            '5x5': Session(session_data + 'session_data.json', 1, '5x5', f'{session_data}scrambles.json'),
            '6x6': Session(session_data + 'session_data.json', 1, '6x6', f'{session_data}scrambles.json'),
            '7x7': Session(session_data + 'session_data.json', 1, '7x7', f'{session_data}scrambles.json'),
            'sqn': Session(session_data + 'session_data.json', 1, 'sqn', f'{session_data}scrambles.json'),
            'skb': Session(session_data + 'session_data.json', 1, 'skb', f'{session_data}scrambles.json'),
            'mgm': Session(session_data + 'session_data.json', 1, 'mgm', f'{session_data}scrambles.json'),
            'pyr': Session(session_data + 'session_data.json', 1, 'pyr', f'{session_data}scrambles.json'),
            'clk': Session(session_data + 'session_data.json', 1, 'clk', f'{session_data}scrambles.json')
        }
        self.current_session = '3x3'
    
    def get_session(self, puzzle=None):
        return self.sessions[puzzle or self.current_session]

    def get_puzzles(self):
        return self.sessions.keys()

class LotusTimeManager:
    def is_valid_time(self, time):
        formatted = ''
        if time[-2:] == '+2':
            time = time[:-2]
        elif time[-3:] == 'dnf':
            time = time[:-3]
        for c in time:
            if c.isnumeric():
                formatted += '0'
            else:
                formatted += c
        return formatted in VALID_TIME_FORMATS

    def time_ms(self, time):
        f = '00:00:00.00'
        if time[-2:] == '+2':
            time = time[:-2]
        elif time[-3:] == 'dnf':
            time = time[:-3]
        time = '00' + time + '00'
        dec = time.find('.')
        col = time.find(':')
        col2 = time.rfind(':')
        if '.' in time:
            f = f[:9] + time[dec+1:dec+3]
            f = f[:6] + time[dec-2:dec] + f[8:]
        if ':' in time:
            f = f[:6] + time[col2+1:col2+3] + f[8:]
            f = f[:3] + time[col2-2:col2] + f[5:]
        if col != col2:
             f = time[col-2:col] + f[2:]
        if dec == col:
            time = time[2:-2]
            while len(time) < 8:
                time = '0' + time
            f = time[:2] + ':' + time[2:4] + ':' + time[4:6] + '.' + time[6:]
        ms = 0
        mul = 10
        for c in f[::-1]:
            if c.isnumeric():
                ms += int(c) * mul
                mul*=10
            elif c == ':':
                mul*=6
                mul /= 10
        return int(ms)

    def format_time(self, time_ms):
        if time_ms == None or time_ms == '':
            return ''
        elif time_ms == -1:
            return 'DNF'
        hours = int(time_ms / H_MS)
        time_ms -= hours * H_MS
        minutes = int(time_ms / M_MS)
        time_ms -= minutes * M_MS
        seconds = time_ms / S_MS
        ts = ''
        seconds = "%.2f" % seconds
        if minutes != 0:
            minutes = (str(minutes).zfill(2) if hours != 0 else str(minutes)) + ':'
            seconds = seconds.zfill(5)
        elif hours == 0:
            minutes = ''
        if hours != 0:
            hours = str(hours) + ':'
            seconds = seconds.zfill(5)
            minutes = str(minutes).zfill(2) + ':' if type(minutes) != str else minutes
        else:
            hours = ''
        return hours + minutes + seconds


class SpotifyPlayer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        scope = "user-read-playback-state,user-modify-playback-state,streaming"

        auth = SpotifyOAuth(
                    client_id="2d0aa7b1e8e34e6db2bbcc9e35fd4db5",
                    client_secret="",
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