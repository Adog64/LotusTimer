from src.main import App

if __name__ == '__main__':
    a = App()
    while a.running:
        a.process_inputs()
        a.draw()