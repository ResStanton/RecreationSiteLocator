# update the requirements for the project
import sys
import os
import subprocess

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', os.path.abspath('requirements.txt')])
    print("Successfully installed packages")
except subprocess.CalledProcessError as e:
    print(f'Error installing packages: {e}')
