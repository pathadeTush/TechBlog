import os
import subprocess


path = 'pip3 install -r '

path = path + os.path.abspath('requirements.txt')

subprocess.call(path, shell=True)
