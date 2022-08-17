import subprocess
import time

filename = 'GridTableGetter.py'
while True:
    """However, you should be careful with the '.wait()'"""
    p = subprocess.Popen('python '+filename, shell=True).wait()

    """This is a program that will restart automatically GridTableGetter.py if it finds this program is killed due to some unknown reasons"""
    if p!=0:
        time.sleep(60)
        continue
    else:
        break