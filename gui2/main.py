from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from backends.util import ScrambleGenerator
from kivy.config import Config
import os

assets = os.getenv('APPDATA') + '//.lotus//assets//'
title_font = assets + 'logo.ttf'

class TimerScreen(Widget):
    assets = assets
    title_font = title_font

    time = ObjectProperty(None)
    scramble = ObjectProperty(None)

    def __init__(self, assets):
        super().__init__()
        self.generate_scramble()

    def generate_scramble(self):
        self.scramble.text = ScrambleGenerator().generate_scramble()

    def enter_time(self):
        self.scramble.text = ScrambleGenerator().generate_scramble()
        self.time.text = ''
        self.time.focus = True

    def get_time_input(self):
        return self.time.text

class LotusTimer(App):
    def build(self):
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')
        self.title = 'Lotus Timer'
        self.appdata = os.getenv('APPDATA') + '\\.lotus'
        self.assets = self.appdata + '\\assets'
        try:
            open(self.appdata + '\\readme.txt')
        except:
            print('essential files missing or corrupted')

        return TimerScreen(self.assets)

if __name__ == '__main__':
    LotusTimer().run()