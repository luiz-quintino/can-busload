import sys
from platform import system
from cx_Freeze import setup, Executable

''' 

python setup build

'''

ver = '2.1.2'

build_exe_options = {
	'excludes': [],
	'include_files': ['img', 'README.TXT', 'dbc', 'Revision notes.txt'],
	'packages': [],
	'path': []
	}

if system() == 'Windows':
	#from windows_include_files import include_files
	
	if sys.platform == 'win32':
		base_os = 'Win32GUI'
		#build_exe_options['include_files'] = include_files
	
	if sys.platform == 'win64':
		base_os = 'Win64GUI'
		#build_exe_options['include_files'] = include_files
		
exe = Executable(
    script='main.py',
    base=base_os,
	targetName='Busload Calc.exe',
	icon='img/busloadcalc.ico',
	shortcutDir = 'short Folder'
)

setup(
	name='Busload calc',
	version=ver,
	description='Busload calculation from a .dbc file',
	author='Luiz Quintino',
	author_email='luiz.quintino@gmail.com',
	executables = [exe],
	options= {'build_exe': build_exe_options},
	)
