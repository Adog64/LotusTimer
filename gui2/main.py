import os
import time

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.effects.scroll import ScrollEffect
from kivy.uix.gridlayout import GridLayout, GridLayoutException
from kivy.uix.scrollview import ScrollView

from backends.util import LotusTimeManager, ScrambleGenerator, SessionManager
from gui.cwidgets.roundedrectangle import RoundedRectangle

_lotus = os.getenv('APPDATA') + '\\.lotus\\'
assets = _lotus + 'assets\\'
session_data = _lotus + 'session_data\\'
title_font = assets + 'logo.ttf'
ltm = LotusTimeManager()

session_manager = SessionManager(session_data)

class TimesList(ScrollView):

    session_manager = session_manager
    session = session_manager.get_session()
    row_height = 20
    def __init__(self, **kwargs):
        super().__init__()

    def reconcile(self):
        print(self.session.get_times())
        grid = GridLayout(cols=3, row_default_height = '20dp', row_force_default=True, size_hint=(.95, 1))
        for t in self.session.get_times()[::-1]:
            grid.add_widget(Label(text=f'{t[2]}.', size_hint_x=0.1, halign='left'))
            grid.add_widget(Label(text=f'{ltm.format_time(t[1] + t[0] if t[0] >= 0 else -1)}', size_hint_x=0.6, halign='left'))
            btn = Button(text='×', bold=True, size_hint=(None, None), size=(19,19), background_normal='', background_color=(122/255, 28/255, 1, 1))
            btn.idx = t[2] - 1
            btn.bind(on_press=self.remove_time)
            grid.add_widget(btn)
        if self.children:
            self.remove_widget(self.children[0])
        self.add_widget(grid)

    def remove_time(self, instance):
        self.session.remove_time(instance.idx)
        self.reconcile()


class TimerScreen(Widget):
    assets = assets
    title_font = title_font

    session_manager = session_manager
    session = session_manager.get_session()
    ltm = ltm
    
    time = ObjectProperty(None)
    scramble = ObjectProperty(None)
    times = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.generate_scramble()
        self.times.reconcile()
        self.time.bind(text=self.valid_time_input)

    def generate_scramble(self):
        self.scramble.text = ScrambleGenerator().generate_scramble()

    def enter_time(self):
        if ltm.is_valid_time(self.time.text):
            score = ltm.time_ms(self.time.text)
            penalty = 2000 if self.time.text[-2:] == '+2' else -1 if self.time.text[-3:] == 'dnf' else 0
            if score > 0  or penalty == -1:
                timestamp = int(time.time())
                self.session.add_time([penalty, score], self.scramble.text, timestamp)
            self.scramble.text = ScrambleGenerator().generate_scramble()
            self.times.reconcile()
            self.time.text = ''
        self.time.focus = True

    def get_time_input(self):
        return self.time.text

    def valid_time_input(self, instance, text):
        self.time.foreground_color = (.75, .75, .75, 1) if ltm.is_valid_time(self.time.text) else (1, .55, .55, 1)

class LotusTimer(App):
    def build(self):
        self.title = 'Lotus Timer'
        Window.size = (1280, 720)
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.resizeable = True
        #Window.borderless = True
        self.icon = assets + 'window_icon_3l.png'
        Config.set('kivy', 'exit_on_escape', 0)
        return TimerScreen()

if __name__ == '__main__':
    LotusTimer().run()
