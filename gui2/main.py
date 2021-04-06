from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color
from kivy.graphics import Rectangle
from backends.util import ScrambleGenerator

class TimerScreen(Widget):
    time = ObjectProperty(None)
    scramble = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.generate_scramble()

    def generate_scramble(self):
        self.scramble.text = ScrambleGenerator().generate_scramble()

    def enter_time(self):
        self.scramble.text = ScrambleGenerator().generate_scramble()
        self.time.text = ''

    def get_time_input(self):
        return self.time.text


class LotusTimer(App):
    def build(self):
        self.title = 'Lotus Timer'
        return TimerScreen()

if __name__ == '__main__':
    LotusTimer().run()