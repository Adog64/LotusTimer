from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from backends.util import ScrambleGenerator, SessionManager, LotusTimeManager
from kivy.core.window import Window
from kivy.config import Config
from gui.cwidgets.roundedrectangle import RoundedRectangle
import os
import time


_lotus = os.getenv('APPDATA') + '\\.lotus\\'
assets = _lotus + 'assets\\'
session_data = _lotus + 'session_data\\'
title_font = assets + 'logo.ttf'
ltm = LotusTimeManager()

session_manager = SessionManager(session_data)

class TimerScreen(Widget):
    assets = assets
    title_font = title_font

    session_manager = session_manager
    session = session_manager.get_session()
    ltm = ltm
    
    time = ObjectProperty(None)
    scramble = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.generate_scramble()
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
        Window.resizeable = True
        Window.icon = assets + 'window_icon.png'
        #Window.borderless = True
        Config.set('kivy', 'exit_on_escape', 0)
        return TimerScreen()

if __name__ == '__main__':
    LotusTimer().run()