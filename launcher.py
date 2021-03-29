from src.main import App

a = App()
while a.running:
    a.process_inputs()
    a.draw()