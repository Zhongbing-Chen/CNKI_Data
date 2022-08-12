import subprocess
import time

filename = 'GetDetail.py'
while True:
    """However, you should be careful with the '.wait()'"""
    p = subprocess.Popen('python '+filename, shell=True).wait()

    """This is a program that will restart automatically GetDetail.py if it finds this program is killed due to some unknown reasons"""
    time.sleep(200)