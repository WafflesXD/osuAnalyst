from os import path, chdir
from glob import glob
from tkinter.filedialog import askdirectory, askopenfilename
from osuReplayParser import Replay


def ReplaySelector(flag):
    homeDir = path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        osuPath = path.join(homeDir, "AppData/Local/osu!/")
        chdir(osuPath)
    except FileNotFoundError:  # If file not found then ask user to select
        osuPath = askdirectory(title="Select osu! Folder")
        chdir(osuPath)
    else:
        print("Successfully entered osu! replays directory")

    if flag:
        return askopenfilename(title="Select osu! Replay")
    else:
        listOfFiles = glob(osuPath + "Replays/*.osr")  # All files with .osr
        return max(listOfFiles, key=path.getctime, default=0)


def main():  # Python scripts instead of package

    r = Replay(ReplaySelector(True))
    # print(r.replay)
    print(r.songName)
    print(r.userName)
    print(r.gameMode)
    print(r.gameVersion)
    print(r.scoreData)
    r.printLifeBarData()
    r.printPosData()
    print(r.replayDate)
    print(r.onlineScoreID)


if __name__ == "__main__":
    main()
