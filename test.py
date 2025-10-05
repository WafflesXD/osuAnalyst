from os import path, chdir
from glob import glob
from tkinter.filedialog import askdirectory, askopenfilename
from osuReplayParser import Replay


def replaySelector(flag = False):
    """Selects replay from osu! replay directory

    Parameters
    ----------
    flag : bool
        True allows users to select their own replay\n
        False selects the most recent replay file

    Returns
    ------
    replay_file : str
        String of replay directory
    """
    homeDir = path.expanduser("~")
    try:
        osuPath = path.join(homeDir, "AppData/Local/osu!/")
        chdir(osuPath)
    except FileNotFoundError:
        osuPath = askdirectory(title="Select osu! Folder")
        chdir(osuPath)

    if flag:
        replayFile = askopenfilename(title="Select osu! Replay")
        while replayFile == '':
            print("Please select valid osu! Replay file", end='\r')
            replayFile = askopenfilename(title="Select osu! Replay")
        print("Successfully entered opened osu! replay file")
        return replayFile
    print("Successfully entered osu! replays directory")
    list_of_files = glob(osuPath + "Replays/*.osr")
    return max(list_of_files, key=path.getctime, default=0)


if __name__ == "__main__":
    r = replaySelector(False)
