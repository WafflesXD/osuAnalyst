import os

home_directory = os.path.expanduser('~')
path = os.path.join(home_directory, 'AppData', 'Local', 'osu!', 'Replays')
os.chdir(path)
print("path")