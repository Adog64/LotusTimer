from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class TimerScreen(FloatLayout):
    time = ObjectProperty(None)

class LotusTimer(App):
    def build(self):
        screen = TimerScreen()
        print(screen.time.text)
        return screen

if __name__ == '__main__':
    LotusTimer().run()