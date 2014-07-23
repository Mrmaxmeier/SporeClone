from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=["OpenGL"],
					include_files=['data/'],
					excludes=['tkinter'],
					icon="icon.icns"
					)

base = None

executables = [
	Executable('creaturecreator.py', base=base)
]

setup(name='Sp0re',
	  version='0.1',
	  description='THE Spore CLONE!!!oneoneone',
	  options=dict(build_exe=buildOptions),
	  executables=executables)
