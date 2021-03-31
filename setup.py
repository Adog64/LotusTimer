from cx_Freeze import setup, Executable

build_exe_options = {"packages":["src", "numpy.lib.format", "numpy", "matplotlib"], "includes":['numpy', 'matplotlib', 'spotipy', 'pygame', 'pyTwistyScrambler', 'execjs', 'six'], "excludes":["zmq", "h5py", "tkinter", "matplotlib.tests", "numpy.random._examples"], "build_exe":"C:/Users/Sharpe/Desktop/build"}

setup(name="Lotus Timer",
    version='0.1.1',
    author='Aidan Sharpe',
    options={"build_exe":build_exe_options},
    executables=[Executable("launcher.py", target_name="LotusTimer", base="Win32GUI")])