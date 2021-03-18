from os import path
import pygame as pg
import sys
from pygame.locals import *
from random import randint
from settings import *
from components import *
from util import *
import json
import time

class App:
    def __init__(self):
        pg.display.init()
        pg.font.init()
        self.APP_DIR = path.split(path.dirname(__file__))[0]
        self.assets = self.APP_DIR + '/assets/'
        self.window = pg.display.set_mode(DEFAULT_WINDOW_SIZE, pg.FULLSCREEN)
        self.logo = pg.image.load(self.assets + logo)
        pg.display.set_caption(TITLE)
        pg.display.set_icon(self.logo)
        self.themes = open(path.join(self.APP_DIR, 'assets/themes') + '/themes.txt', 'r').readlines()
        self.theme = self.APP_DIR + '/assets/themes/' + self.themes[0][6:-1] + '/'
        self.theme_init(self.theme + 'options.json')
        self.title_font = pg.font.Font(self.assets + title_font, SCRAMBLE_SIZE)
        self.subtitle_font = pg.font.Font(self.theme + text_font, 35)
        self.text_font = pg.font.Font(self.theme + text_font, 25)
        self.init_sessions()
        self.running = True
        self.screens()
        

    def process_inputs(self):
        for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP and event:
                    self.screen.clicks(pygame.mouse.get_pos())
                if event.type == VIDEORESIZE:
                    self.window = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                if event.type == pg.KEYDOWN:
                    if 'Time' in self.screen.get_selected():
                        if event.unicode in TIME_CHARS:
                            self.screen.components['Time'].enter(event.unicode)
                        elif event.key == K_RETURN and self.screen.components['Time'].valid():
                            self.publish_time(self.screen.components['Time'].text, self.screen.components['Scramble'].text)
                            self.screen.components['Time'].clear()
                            self.screen.components['Scramble'].text = ScrambleGenerator.generate_scramble()
                        elif event.key == K_BACKSPACE:
                            self.screen.components['Time'].backspace()

    def screens(self):
        timer_screen = {
        'Panel': Box((94, DEFAULT_WINDOW_HEIGHT/2), (188, DEFAULT_WINDOW_HEIGHT+14), visible=True, fill_color=box_fill_color),
        'Scramble': Label(((DEFAULT_WINDOW_WIDTH+188)/2, 200), (DEFAULT_WINDOW_WIDTH/2, DEFAULT_WINDOW_HEIGHT/3),self.text_font, text_color, text=ScrambleGenerator.generate_scramble("3x3"), enabled=True),
        'Time': TextBox(self.subtitle_font, text_color, center=((DEFAULT_WINDOW_WIDTH+188)/2, 260), size=(600,90), enterable=True, bordered=True, is_valid_entry=self.valid_time),
        'Logo': Image((94, 64), (128, 128), self.logo),
        'LogoText': TextBox(self.title_font, (122, 28, 255), (94, 128), (128, 48), text='Lotus'),
        'TimeBox': Box((188 + 305, DEFAULT_WINDOW_HEIGHT-220), (450, 400), visible=True),
        'QuickStatsBox': Box((DEFAULT_WINDOW_WIDTH - 425, DEFAULT_WINDOW_HEIGHT - 220), (750, 400), visible=True),
        'Quit': Button((100, DEFAULT_WINDOW_WIDTH-100), (75, 75), enabled=True, text='X', when_pressed=self.end, text_font=self.text_font)
        }
        self.screen = Screen(((DEFAULT_WINDOW_WIDTH+188)/2, DEFAULT_WINDOW_HEIGHT/2), DEFAULT_WINDOW_SIZE, True, timer_screen)

    def draw(self):
        self.window.fill(background_color)

        #render components
        self.screen.render(self.window)
        pg.display.update()

    def test_button(self):
        print('pressed')

    def theme_init(self, path):
        global background_color, text_color, border_color, box_fill_color
        opts = json.loads(open(path).read())
        background_color = tuple(opts['BACKGROUND_COLOR'])
        text_color = tuple(opts['TEXT_COLOR'])
        border_color = text_color
        box_fill_color = tuple(opts['BOX_FILL_COLOR'])

    def init_sessions(self):
        sessions = []
        for i in range(10):
            sessions.append(SessionManager( self.APP_DIR + '/assets/session_data.json', i+1))
        self.sessions = sessions
        self.session = sessions[0]

    def publish_time(self, score, scramble):
        penalty = 0
        model = '00:00:00.00'
        if score[-2:] == '+2':
            penalty = 2000
            score = score[:-2]
        elif score[-3:] == 'dnf':
            penalty = -1
            score = score[:-3]
        score = self.time_ms(score)
        timestamp = int(time.time())
        print([penalty, score], scramble, timestamp)
        self.session.add_time([penalty, score], scramble, timestamp)

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
        for c in f[-1::-1]:
            if c.isnumeric():
                ms += int(c) * mul
                mul*=10
            elif c == ':':
                mul*=60
        return ms                

    def valid_time(self, time):
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
    
    def end(self):
        self.running = False

if __name__ == '__main__':
    a = App()
    while a.running:
        a.process_inputs()
        a.draw()