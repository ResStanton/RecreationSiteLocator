# Import libraries 
import subprocess
import os
import sys
import webbrowser

# get the path to the python executable within the python environment 
def get_environment_python(venv_path):
    return os.path.join(venv_path, os.path.join("scripts", "python.exe"))

# run and open the recreation site locator application using the python virtual environment  
def run_in_environment(venv_path: str, source_path: str):
    python = get_environment_python(venv_path)
    print("Starting the application . . .")
    webbrowser.open_new("http://127.0.0.1:5000")
    subprocess.call([python, os.path.abspath(os.path.join('src', 'main.py'))], cwd=source_path)

# create the python virtual environment in a given location
def create_environment(venv_path):
    subprocess.check_call([sys.executable, '-m', "venv", venv_path]) 

# get important directories 
venv_path = os.path.join(os.getcwd(), ".venv")
source_path = os.path.join(os.getcwd(), "src")

# check if the environment needs created
if os.path.exists(venv_path):
    # The environment exists so use the existing environment
    print("Environment already configured")
    run_in_environment(venv_path, source_path)
else:
    # The environment needs created so create the environment
    print("Creating Python Environment . . .")
    create_environment(venv_path)

    # Install requirements in the environment 
    print("Installing Required Files")
    try:
        subprocess.check_call([get_environment_python(venv_path), '-m', 'pip', 'install', '-r', os.path.abspath(os.path.join('src', 'requirements.txt'))])
        print("Successfully installed packages")
    except subprocess.CalledProcessError as e:
        print(f'Error installing packages: {e}')
    
    # run the application in the newly created environment 
    print("Setup complete")
    run_in_environment(venv_path, source_path)