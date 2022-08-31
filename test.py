from os import path, chdir
from glob import glob
from tkinter.filedialog import askdirectory as ad
from struct import unpack_from, calcsize
from itertools import islice
from lzma import decompress, FORMAT_AUTO


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
    # ^Finds file with newest metadata change
    songName = path.basename(newestFile)
    userName = songName.partition(" ")[0]
    # Gets username from first part, using partition, of replay file name

    with open(newestFile, "rb") as replay:  # Opens replay file
        r = replay.read()

        graphList = [[1.0, 0]]
        hexOffset = len(r.hex().split("7c3")[0]) / 2  # offset before health
        # Handles other "|" before health data
        for i in r.hex().split("7c"):
            if "2c" or "302e3" in i:  # Check if "1," or "0.,integer"
                try:
                    h = bytes.fromhex(i.partition("2c")[0]).decode("utf-8")
                    t = bytes.fromhex(i.partition("2c")[2]).decode("utf-8")
                    graphList.append([float(h), int(t)])
                    hexOffset += len(i) / 2 + 1  # offset for each health data
                except ValueError:
                    pass
        hexOffset += 3  # Adds to graphList and finds hexOffset after health
        # [print(i) for i in graphList]
        print(hexOffset)

        gameData = unpack_from("<bi", r, 0)  # Gamemode & version
        print(gameData)  # Gamemode and version

        scoreData = unpack_from("<hhhhhhihbi", r, 75 + len(userName))
        print(scoreData)  # 300 100 50 Gekis Katus Misses Score Combo FC Mods

        healthDataCheck = (hexOffset - int(hexOffset)) == 0
        # Handles no life bar data
        healthDataCheck1 = (hexOffset - 3) == len(r.hex()) / 2
        # Handles no life bar or posData
        if not healthDataCheck or healthDataCheck1:  # Check for health data
            hexOffset = 77 + len(userName) + calcsize("<hhhhhhihbi")

        miscData = unpack_from("<qi", r, int(hexOffset))
        print(miscData)  # Timestamp

        hexOffset += calcsize("<qi")
        onlineScoreID = unpack_from("<q", r, int(hexOffset) + miscData[1])
        print(onlineScoreID)  # Online score ID
        # Returns 0 if not completed or not played online

        if not healthDataCheck or not healthDataCheck1:
            posData = r[int(hexOffset): int(hexOffset) + miscData[1]]
            posData = decompress(posData, format=FORMAT_AUTO)
            posData = posData.decode("ascii")  # Pulls mouse + key data
            posDataList = [[None, None, None, None]]
            posDataRange = len(posData.split(",")) - 1
            for i in islice(posData.split(","), 0, posDataRange):
                timeFromLastEvent = int(i.split("|")[0])
                xPos = float(i.split("|")[1])
                yPos = float(i.split("|")[2])
                keyCombo = int(i.split("|")[3])
                posDataList.append([timeFromLastEvent, xPos, yPos, keyCombo])
            # [print(i) for i in posDataList]  # Organized posData into list
            # print(mouseData)


if __name__ == "__main__":
    main()
