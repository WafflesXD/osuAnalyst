import os
import glob
from tkinter.filedialog import askdirectory as ad
import struct


def main():  # Python scripts instead of package
    homeDir = os.path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        path = os.path.join(homeDir, "AppData/Local/osu!/")
        os.chdir(path)
    except FileNotFoundError:  # If file not found then ask user to select
        path = ad(title='Select osu! Folder')
        os.chdir(path)
    else:
        print("Successfully entered osu! replays directory")

    listOfFiles = glob.glob(path + "Replays/*.osr")  # All files with .osr
    newestFile = max(listOfFiles, key=os.path.getctime, default=0)
    # ^Finds file with newest metadata change
    songName = os.path.basename(newestFile)
    userName = songName.partition(' ')[0]
    # Gets username from first part, using partition, of replay file name

    with open(newestFile, "rb") as replay:  # Opens replay file
        r = replay.read()
        unpacked = struct.unpack_from('<bi', r, 0)  # Gamemode & version
        unpacked1 = struct.unpack_from('<hhhhhhihbi', r, 75 + len(userName))
        print(str(r).split("|")[71])  # Use for loop to create table for graph
        """
        Byte offset # for version number @ 1 (i)
        Byte offset # for 300's @ 85 then + 2 for next data point (h)
            reference for ^^ @
            https://osu.ppy.sh/wiki/en/Client/File_formats/Osr_%28file_format%29
        Byte offset # for Total score @ 97 (i)
        Byte offset # for Max Combo @ 101 (h)
        Byte offset # for mods used @ 104 (i)
            reference table for ^^ @ https://github.com/ppy/osu-api/wiki#mods
        """
        print(unpacked)
        print(unpacked1)  # Read from binary, the game version for replay


if __name__ == "__main__":
    main()
