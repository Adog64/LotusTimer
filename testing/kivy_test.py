from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class TimerScreen(FloatLayout):
    pass

class LotusTimer(App):
    def build(self):
        self.title = 'Lotus Timer'
        self.window_icon = 'D:\Aidan\GitHub\LotusTimer\src\assets\lotus_round.png'
        screen = TimerScreen()
        return screen

if __name__ == '__main__':
    LotusTimer().run()