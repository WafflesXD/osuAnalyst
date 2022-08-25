import os
import glob

home_directory = os.path.expanduser('~') # Makes a path to C:/Users/HomeUser
path = os.path.join(home_directory, 'AppData', 'Local', 'osu!', 'Replays') # Appends path to osu Replays folder
os.chdir(path) 
print(path)
list_of_files = glob.glob(path+"/*.osr") # Makes a list of all files within path
latest_file = max(list_of_files, key=os.path.getctime, default=0) # Looks through list_of_files and finds file with smallest
print(latest_file)