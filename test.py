from os import path, chdir
from glob import glob
from tkinter.filedialog import askdirectory as ad
from osuReplayParser import Replay


def main():  # Python scripts instead of package

    homeDir = path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        osuPath = path.join(homeDir, "AppData/Local/osu!/")
        chdir(osuPath)
    except FileNotFoundError:  # If file not found then ask user to select
        osuPath = ad(title="Select osu! Folder")
        chdir(osuPath)
    else:
        print("Successfully entered osu! replays directory")

    listOfFiles = glob(osuPath + "Replays/*.osr")  # All files with .osr
    newestFile = max(listOfFiles, key=path.getctime, default=0)

    r = Replay(newestFile)
    print(r.replay)
    print(r.songName)
    print(r.userName)
    print(r.gameMode)
    print(r.gameVersion)
    print(r.scoreData)
    r.printLifeBarData()
    print(r.poskeyData)
    print(r.replayDate)
    print(r.onlineScoreID)


if __name__ == "__main__":
    main()
