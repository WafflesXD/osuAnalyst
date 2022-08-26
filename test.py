import os
import glob
from tkinter.filedialog import askdirectory


def main():  # Python scripts instead of package
    homeDir = os.path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        path = os.path.join(homeDir, "AppData/Local/osu!/Replays/")
        os.chdir(path)
    except FileNotFoundError:
        path = askdirectory(title='Select osu! Replay Folder')
        os.chdir(path)
    else:
        print("Successfully entered osu! replays directory")
    # Couldnt have os.chdir outside the try except
    print(path)

    listOfFiles = glob.glob(path + "/*.osr")  # All files with .osr
    newestFile = max(listOfFiles, key=os.path.getctime, default=0)
    print(newestFile)  # ^Finds file with newest metadata change

    with open(newestFile, "rb") as replay:  # Opens replay file
        print(replay.read())  # DOESNT WORK CANT READ AS BINARY


if __name__ == "__main__":
    main()
