from cx_Freeze import setup, Executable

build_exe_options = {"packages":["src"], "includes":['numpy', 'matplotlib', 'spotipy', 'pygame', 'pyTwistyScrambler'], "optimize":2, "build_exe":"C:/Users/Sharpe/Desktop/build"}

setup(name="Lotus Timer",
    version='2021.3.26.1',
    author='Aidan Sharpe',
    options={"build_exe":build_exe_options},
    executables=[Executable("launcher.py", target_name="LotusTimer")])