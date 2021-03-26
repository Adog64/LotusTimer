from cx_Freeze import setup, Executable

build_exe_options = {"packages":["src"], "excludes":["zmq", "h5py", "tkinter"], "optimize":0, "build_exe":"C:/Users/Sharpe/Desktop/build"}

setup(name="Lotus Timer",
    version='2021.03.25.1',
    author='Aidan Sharpe',
    options={"build_exe":build_exe_options},
    executables=[Executable("launcher.py", base="Win32GUI", target_name="LotusTimer")])