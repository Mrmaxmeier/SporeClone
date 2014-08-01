import sys
from cx_Freeze import setup, Executable
print()
print("#" * 15)
print()
print('Building on', sys.platform)
print()
print("#" * 15)
print()

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=["OpenGL"],
					include_files=['data/'],
					excludes=[]#Icon Crashes on Windows Build#icon="icon.png"
					)

base = None

executables = [Executable('creaturecreator.py', base=base)]
#executables = [Executable('main.py', base=base)]
#executables = [Executable('tktest.py', base=base)]

#if sys.platform == 'darwin':
#	bundle = dict(iconfile="icon.icns")
#	dmg = dict(volume_label="Sp0re Disk Image")
#	options = dict(build_exe=buildOptions, build_mac=bundle, build_dmg=dmg)
#else:
#	options = dict(build_exe=buildOptions)
options = dict(build_exe=buildOptions)

setup(name='Sp0re',
	version='0.2',
	description='A Spore Clone',
	options=options,
	executables=executables)
