from os import path
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
import sys
from pygame.locals import *
from random import randint
from src.settings import *
from src.components import *
from src.util import *
import json
import time

class App:
    def __init__(self):
        global window_width, window_height
        pg.display.init()
        pg.font.init()
        self.APP_DIR = path.dirname(__file__)
        self.assets = self.APP_DIR + '/assets/'
        self.window = pg.display.set_mode(DEFAULT_WINDOW_SIZE)
        self.logo = pg.image.load(f"{self.assets}{logo}")
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(f"{self.assets}lotus_round.png"))
        window_width, window_height = self.window.get_size()
        self.themes = open(path.join(self.APP_DIR, 'assets/themes') + '/themes.txt', 'r').readlines()
        self.theme = self.APP_DIR + '/assets/themes/' + self.themes[0][6:-1] + '/'
        self.theme_init(self.theme + 'options.json')
        self.title_font = pg.font.Font(self.assets + title_font, SCRAMBLE_SIZE)
        self.subtitle_font = pg.font.Font(self.theme + text_font, 30)
        self.text_font = pg.font.Font(self.theme + text_font, 25)
        self.init_sessions()
        self.running = True
        self.timec = len(self.session.get_times())
        self.screens()
        

    def process_inputs(self):
        for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
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
                if event.type == pg.MOUSEWHEEL:
                    if event.y > 0 and 'Times' in self.screen.get_selected():
                        self.screen.components['Times'].scroll_up()
                    if event.y < 0 and 'Times' in self.screen.get_selected():
                        self.screen.components['Times'].scroll_down()
                    

    def screens(self):
        self.timer_screen = {
        'ControlPanel': Box(control_panel_center, control_panel_size, visible=True, fill_color=box_fill_color),
        'Scramble': Label(scramble_center, scramble_size,self.text_font, text_color, text=ScrambleGenerator.generate_scramble("3x3"), enabled=True),
        'Time': TextBox(self.subtitle_font, text_color, center=time_center, size=time_size, enterable=True, bordered=True, is_valid_entry=self.valid_time),
        'Logo': Image(logo_center, logo_size, self.logo),
        'LogoText': Label((500,500), logo_text_size, self.title_font, (122, 28, 255), text='Lotus'),
        'Quit': Button((94, window_height-40), (100, 75), enabled=True, text='Quit', when_pressed=self.end, text_font=self.text_font, text_color=text_color)
        }
        if self.timec > 0:
            self.timer_screen['TimeBox'] = Box((188 + 305, window_height-220), (450, 400), visible=True)
            self.timer_screen['QuickStatsBox'] = Box((window_width - 425, window_height - 220), (750, 400), visible=True)
            self.timer_screen['Times'] = ScrollBox((188 + 325, window_height-220), (450, 400), True, items=self.get_time_elements(), scroll_speed=25)
            self.timer_screen['QuickStats'] = Panel((window_width - 405, window_height - 220), (750, 400), items=self.stat_labels(), columns=2, column_width=310)
        self.screen = Screen(((window_width+188)/2, window_height/2), DEFAULT_WINDOW_SIZE, True, self.timer_screen)

    def draw(self):
        self.window.fill(background_color)

        #render components
        self.screen.render(self.window)
        pg.display.update()

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
            sessions.append(Session( self.APP_DIR + '/assets/session_data.json', i+1))
        self.sessions = sessions
        self.session = sessions[0]

    def get_time_elements(self):
        times = self.session.get_times()
        elelments = []
        if len(times) > 0:
            for t in times:
                penalty = t[0]
                time_ms = t[1]
                idx = t[2]
                if penalty > 0:
                    time_ms += penalty
                ts = self.format_time(time_ms)
                if penalty == 2000:
                    ts += ' (+2)'
                if penalty == -1:
                    ts = 'DNF'
                elelments.append([
                    Label((100, 40), (200, 80), self.text_font, text_color, str(idx) + '.   ' + ts, just='l')])
                    #Button((300, 40), (100, 80), text_font=self.text_font, text='Delete', toggle=False, when_pressed=self.delete_time_button_press, wp_arg=idx)])
        elelments = elelments[-1::-1]
        return elelments
    
    def delete_time_button_press(self, index):
        self.session.remove_time(index)

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
        if self.timec == 0:
            self.timer_screen['TimeBox'] = Box((188 + 305, window_height-220), (450, 400), visible=True)
            self.timer_screen['QuickStatsBox'] = Box((window_width - 425, window_height - 220), (750, 400), visible=True)
            self.timer_screen['Times'] = ScrollBox((188 + 325, window_height-220), (450, 400), True, items=self.get_time_labels(), scroll_speed=25)
            self.timer_screen['QuickStats'] = Panel((window_width - 405, window_height - 220), (750, 400), items=self.stat_labels(), columns=2, column_width=310)
        self.timec += 1
        if score > 0  or penalty == -1:
            timestamp = int(time.time())
            self.session.add_time([penalty, score], scramble, timestamp)
            self.screen.components['Times'].items = self.get_time_elements()
            self.screen.components['QuickStats'].items = self.stat_labels()

    def format_time(self, time_ms):
        hours = int(time_ms / H_MS)
        time_ms -= hours * H_MS
        minutes = int(time_ms / M_MS)
        time_ms -= minutes * M_MS
        seconds = time_ms / S_MS
        ts = ''
        if hours != 0:
            ts = str(hours) + ':' + str(minutes) + ':'
        elif minutes != 0:
            ts = str(minutes) + ':'
        ts = (ts + "%.2f" % seconds)
        return ts

    def stat_labels(self):
        times = self.session.get_times()
        times = times[-1::-1]
        solved = []
        best = ''
        solve_rate = ''
        sdev = ''
        avg = ''
        ao5 = ''
        ao12 = ''
        for t in times:
            if t[0] >=0:
                solved.append(t[1]+t[0])
        if len(times) > 0:
            solve_rate = f'{solved}/{len(times)}'
            avg = self.format_time(stat.mean(solved))
            sdev = self.format_time(stat.stdev(solved))
            best = self.format_time(min(solved))
        # if len(times) >= 5:
        #     ao5 = stat.mean(sorted(ao5)[1:-1])
        #     ao5 = self.format_time(ao5)
        # else:
        #     ao5 = ''
        # if len(times) >= 12:
        #     ao12 = stat.mean(sorted(ao12)[1:-1])
        #     ao12 = self.format_time(ao12)
        else:
            ao12 = ''
        labels = [
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Best:   {best}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Ao5:   {ao5}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Ao12:    {ao12}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Mean:   {avg}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'S Dev:   {sdev}', just='l')]
            #Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Solved:   {solve_rate}', just='l')]
        return labels           

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