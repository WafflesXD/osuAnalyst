from os import path, chdir
from glob import glob
from tkinter.filedialog import askdirectory as ad
from struct import unpack_from
from lzma import decompress, FORMAT_AUTO


def main():  # Python scripts instead of package
    homeDir = path.expanduser("~")  # Makes a path to C:/Users/HomeUser
    try:
        osuPath = path.join(homeDir, "AppData/Local/osu!/")
        chdir(osuPath)
    except FileNotFoundError:  # If file not found then ask user to select
        osuPath = ad(title='Select osu! Folder')
        chdir(osuPath)
    else:
        print("Successfully entered osu! replays directory")

    listOfFiles = glob(osuPath + "Replays/*.osr")  # All files with .osr
    newestFile = max(listOfFiles, key=path.getctime, default=0)
    # ^Finds file with newest metadata change
    songName = path.basename(newestFile)
    userName = songName.partition(' ')[0]
    # Gets username from first part, using partition, of replay file name

    with open(newestFile, "rb") as replay:  # Opens replay file
        r = replay.read()
        graphList = [[0, 1.0]]
        hexOffset = len(r.hex().split("7c")[0]) / 2  # offset before health
        for i in r.hex().split("7c"):
            if "2c" or "302e" in i:  # Check if either "1," or "0.,"
                try:
                    h = bytes.fromhex(i.partition("2c")[0]).decode("utf-8")
                    t = bytes.fromhex(i.partition("2c")[2]).decode("utf-8")
                    graphList.append([float(h), int(t)])
                    hexOffset += len(i) / 2 + 1  # offset for each health data
                except ValueError:
                    pass
        hexOffset += 3  # Adds to graphList and finds hexOffset after health
        [print(i) for i in graphList]
        print(hexOffset)
        gameData = unpack_from("<bi", r, 0)  # Gamemode & version
        scoreData = unpack_from("<hhhhhhihbi", r, 75 + len(userName))
        miscData = unpack_from("<qi", r, int(hexOffset))
        onlineScoreID = unpack_from("<q", r, int(hexOffset) + 12 + miscData[1])
        bruh = r[int(hexOffset) + 12: int(hexOffset) + 12 + miscData[1]]
        bruh = decompress(bruh, format=FORMAT_AUTO)
        bruh = bruh.decode("ascii")  # Will format later pulls mouse + key data
        print(bruh)
        print(gameData)  # Gamemode and version
        print(scoreData)
        print(miscData)  # Timestamp
        print(onlineScoreID)  # Online score ID


if __name__ == "__main__":
    main()
