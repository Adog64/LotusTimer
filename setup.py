import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages":["pygame", "src"], "excludes":["zmq", "h5py", "tkinter"], "silent":True}

setup(name="Lotus Timer",
    version='0.1',
    author='Aidan Sharpe',
    options={"build_exe":build_exe_options},
    executables=[Executable("launcher.py", base="Win32GUI", target_name="LotusTimer")])