from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class GameScreen(Widget):
    pass

class LotusTimer(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    LotusTimer().run()