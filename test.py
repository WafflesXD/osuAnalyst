import os
import glob

homeDir = os.path.expanduser("~")  # Makes a path to C:/Users/HomeUser
path = os.path.join(homeDir, "AppData/Local/osu!/Replays/")
os.chdir(path)
print(path)

listOfFiles = glob.glob(path + "/*.osr")  # Makes a list of all files with .osr
newestFile = max(listOfFiles, key=os.path.getctime, default=0)
print(newestFile)  # ^Finds file with newest metadata change

with open(newestFile, "rb") as replay:  # Opens replay file
    print(replay.read())  # DOESNT WORK CANT READ AS BINARY
