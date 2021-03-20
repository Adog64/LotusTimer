from cx_Freeze import setup, Executable

build_exe_options = {"packages":["pygame", "src"], "excludes":["zmq", "h5py", "tkinter"], "silent":True, "optimize":2}

setup(name="Lotus Timer",
    version='beta-1.1',
    author='Aidan Sharpe',
    options={"build_exe":build_exe_options},
    executables=[Executable("launcher.py", base="Win32GUI", target_name="LotusTimer")])