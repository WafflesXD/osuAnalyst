import os
import glob
from tkinter.filedialog import askdirectory as ad
import struct


def main():  # Python scripts instead of package
    homeDir = os.path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        path = os.path.join(homeDir, "AppData/Local/osu!/")
        os.chdir(path)
    except FileNotFoundError:
        path = ad(title='Select osu! Folder')
        os.chdir(path)
    else:
        print("Successfully entered osu! replays directory")
    # Couldnt have os.chdir outside the try except
    print(path)

    listOfFiles = glob.glob(path + "Replays/*.osr")  # All files with .osr
    newestFile = max(listOfFiles, key=os.path.getctime, default=0)
    print(newestFile)  # ^Finds file with newest metadata change

    with open(newestFile, "rb") as replay:  # Opens replay file
        byte_data = replay.read()  # Conceptual reading of .osr
        unpacked = struct.unpack_from('h', byte_data, 101)
        """
        Byte offset # for Version @ 1 (i)
        Byte offset # for 300's @ 85 then + 2 for next data point (h)
        Byte offset # for Total score @ 97 (i)
        Byte offset # for Max Combo @ 101 (h)
        Byte offset # for mods used @ 104 (i)
            refrence table for ^^ @ https://github.com/ppy/osu-api/wiki#mods
        Ill keep going after!
        """
        print(unpacked)  # Read from binary, the game version for replay


if __name__ == "__main__":
    main()
