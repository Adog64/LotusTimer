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
        self.window = pg.display.set_mode(DEFAULT_WINDOW_SIZE, pg.RESIZABLE)
        self.logo = pg.image.load(f"{self.assets}{logo}")
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(f"{self.assets}lotus_round.png"))
        window_width, window_height = self.window.get_size()
        self.user_settings = json.load(open(f'{self.assets}options.json'))
        self.theme = self.user_settings['theme']
        self.background_mode = self.user_settings['background_mode']
        background_name = self.user_settings['background_image']
        self.background_image = None
        if background_name != None:
            self.background_image = pg.image.load(f'{self.assets}{background_name}')
        self.theme_path = f'{self.assets}/themes/{self.theme}/'
        self.theme_init(f'{self.theme_path}options.json')
        self.title_font = pg.font.Font(self.assets + title_font, TITLE_FONT_SIZE)
        self.subtitle_font = pg.font.Font(self.theme_path + text_font, 30)
        self.text_font = pg.font.Font(self.theme_path + text_font, 25)
        self.init_sessions()
        self.running = True
        self.timec = len(self.session.get_times())
        self.current_scramble = self.session.generate_scramble()
        self.screens()
        

    def process_inputs(self):
        global window_width, window_height
        for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    self.screen.clicks(pygame.mouse.get_pos())
                if event.type == VIDEORESIZE:
                    self.window = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    window_width, window_height = self.window.get_size()
                    self.refresh_screen_components()
                    self.screens()
                if event.type == KEYDOWN:
                    if 'Time' in self.screen.get_selected():
                        if event.unicode in TIME_CHARS:
                            self.screen.components['Time'].enter(event.unicode)
                        elif event.key == K_RETURN and self.screen.components['Time'].valid():
                            self.publish_time(self.screen.components['Time'].text, self.screen.components['Scramble'].text)
                            self.screen.components['Time'].clear()
                            self.screen.components['Scramble'].text = self.session.generate_scramble()
                        elif event.key == K_BACKSPACE:
                            self.screen.components['Time'].backspace()
                if event.type == MOUSEWHEEL:
                    if event.y > 0 and 'Times' in self.screen.get_selected():
                        self.screen.components['Times'].scroll_up()
                    if event.y < 0 and 'Times' in self.screen.get_selected():
                        self.screen.components['Times'].scroll_down()

    def screens(self):
        self.timer_screen = {
        'ControlPanel': Box(control_panel_center, control_panel_size, visible=True, fill_color=box_fill_color),
        'Scramble': Label(scramble_center, scramble_size,self.text_font, text_color, text=self.current_scramble, enabled=True),
        'Time': TextBox(self.subtitle_font, text_color, center=time_center, size=time_size, enterable=True, bordered=True, is_valid_entry=self.valid_time),
        'Logo': Image(logo_center, logo_size, self.logo),
        'LogoText': Label(logo_text_center, logo_text_size, self.title_font, lotus_purple, text='Lotus', scaling=True),
        }
        if self.timec > 0:
            self.timer_screen = {**self.timer_screen, 
                **{'TimeBox': Box(times_box_center, times_box_size, visible=True),
                'QuickStatsBox': Box(stats_center, stats_size, visible=True),
                'Times': ScrollBox(times_center, times_size, True, items=self.get_time_elements(), scroll_speed=25),
                'QuickStats': Panel(stats_lbls_center, stats_size, items=self.stat_labels(), columns=2, column_width=310),
                'Timetrends': LineGraph(graph_center, graph_size, self.session.get_scores(), linecolor=lotus_purple)}}
        self.screen = Screen(((window_width+188)/2, window_height/2), DEFAULT_WINDOW_SIZE, True, self.timer_screen)

    def draw(self):
        if self.background_mode == 'solid':
            self.window.fill(background_color)
        elif self.background_mode == 'image':
            if self.background_image != None:
                self.window.blit(self.background_image, (0,0))
            else:
                self.window.fill((0,0,0))

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

    def refresh_screen_components(self):
        global control_panel_center, control_panel_size, scramble_center, scramble_size,\
        time_center, time_size, logo_center, logo_size, logo_text_center, logo_text_size, \
        stats_center, stats_size, times_center, times_size, graph_size, stats_lbls_center, \
        graph_center, times_box_center, times_box_size        

        control_panel_center = (int(window_width*.05875), int(window_height/2))
        control_panel_size = (int(0.1175*window_width), window_height+14)
        scramble_center = (int((window_width + control_panel_size[0])/2), int(0.22222*window_height))
        scramble_size = (window_width/2, window_height/3)
        time_center = (scramble_center[0], int(0.28888*window_height))
        time_size = (int(.375*window_width), int(window_height/10))
        logo_center = (control_panel_center[0], int(0.07111*window_height))
        logo_size = (int(.08*window_width), int(.14222*window_height))
        logo_text_center = (logo_center[0], logo_size[1])
        logo_text_size = (logo_size[0], int(0.06*window_height))
        stats_center = (int(.74688*window_width), int(.75555*window_height))
        stats_lbls_center = (int(0.01188*window_width)+stats_center[0], stats_center[1])
        stats_size = (int(.46875*window_width), int(.44444*window_height))
        times_box_center = (int(0.30813*window_width), stats_center[1])
        times_box_size = (int(.28125*window_width), stats_size[1])
        times_center = (int(.32053*window_width), stats_center[1])
        times_size = (times_box_size[0], stats_size[1])
        graph_center = (stats_center[0], stats_center[1]+int(stats_size[1]/4))
        graph_size = (int(stats_size[0]*0.9), int(stats_size[1]/2))

        

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
                elelments.append(
                    Label((100, 40), (200, 80), self.text_font, text_color, str(idx) + '.   ' + ts, just='l'))
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
            self.timer_screen = {**self.timer_screen, **{
            ['TimeBox']: Box((188 + 305, window_height-220), (450, 400), visible=True),
            'QuickStatsBox': Box((window_width - 425, window_height - 220), (750, 400), visible=True),
            'Times': ScrollBox((188 + 325, window_height-220), (450, 400), True, items=self.get_time_elements(), scroll_speed=35),
            'QuickStats': Panel((window_width - 405, window_height - 220), (750, 400), items=self.stat_labels(), columns=2, column_width=310),
            'Timetrends': LineGraph(graph_center, graph_size, self.session.get_scores(), linecolor=lotus_purple)}}
        self.timec += 1
        if score > 0  or penalty == -1:
            timestamp = int(time.time())
            self.session.add_time([penalty, score], scramble, timestamp)
            self.screen.components['Times'].items = self.get_time_elements()
            self.screen.components['QuickStats'].items = self.stat_labels()
            self.screen.components['Timetrends'].update(self.session.get_scores())

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
        if hours != 0:
            ts = str(hours) + ':' + str(minutes) + ':'
        elif minutes != 0:
            ts = str(minutes) + ':'
        ts = (ts + "%.2f" % seconds)
        return ts

    def stat_labels(self):
        best = self.format_time(self.session.best)
        ao5 = self.format_time(self.session.ao5)
        ao12 = self.format_time(self.session.ao12)
        avg = self.format_time(self.session.avg)
        sdev = self.format_time(self.session.sdev)
        solve_rate = f'{len(self.session.solve_rate[0])}/{self.session.solve_rate[1]}'
        print(solve_rate)
        
        labels = [
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Best:   {best}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Ao5:   {ao5}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Ao12:    {ao12}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Mean:   {avg}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'S Dev:   {sdev}', just='l'),
            Label((100, 40), (200, 80), self.subtitle_font, text_color, f'Solved:   {solve_rate}', just='l')]
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