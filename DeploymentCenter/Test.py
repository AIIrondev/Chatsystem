import os
import sys
import subprocess

os.system("ls")
os.system("cd DeploymentCenter/api")
subprocess.Popen(['cd DeploymentCenter/api & gunicorn', '-w', '2', '-b', '127.0.0.1:4999', 'api:app'])