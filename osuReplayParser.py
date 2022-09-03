from os import path
from struct import unpack_from, calcsize
from itertools import islice
from lzma import decompress, FORMAT_AUTO
from datetime import datetime, timedelta


class Replay:

    gmDict = {0: "osu!",
              1: "osu!Taiko",
              2: "osu!Catch",
              3: "osu!Mania"}
    Dict100s = {"osu!": "100s in standard: ",
                "osu!Taiko": "150s in Taiko: ",
                "osu!Catch": "100s in CTB: ",
                "osu!Mania": "100s in mania: "}
    Dict50s = {"osu!": "50s in standard: ",
               "osu!Catch": "small fruit in CTB: ",
               "osu!Mania": "50s in mania: "}
    DictGekis = {"osu!": "Gekis in standard: ",
                 "osu!Mania": "Max 300s in mania: "}
    DictKatus = {"osu!": "Katus in standard: ",
                 "osu!Mania": "200s in mania: "}
    fcDict = {1: "Yes!",
              0: "No"}
    modsDict = {0: "No mods",
                1: "NoFail",
                2: "Easy",
                4: "TouchDevice",
                8: "Hidden",
                16: "HardRock",
                32: "SuddenDeath",
                64: "DoubleTime",
                128: "Relax",
                256: "HalfTime",
                512: "Nightcore",
                1024: "Flashlight",
                2048: "Autoplay",
                4096: "SpunOut",
                8192: "Relax2",
                16384: "Perfect",
                32768: "Key4",
                65536: "Key5",
                131072: "Key6",
                262144: "Key7",
                524288: "Key8",
                1048576: "FadeIn",
                2097152: "Random",
                4194304: "Cinema",
                8388608: "Target",
                16777216: "Key9",
                33554432: "KeyCoop",
                67108864: "Key1",
                134217728: "Key3",
                268435456: "Key2",
                536870912: "ScoreV2",
                1073741824: "Mirror"}
    keysDict = {0: "No Keys Pressed",
                1: "M1 Pressed",
                2: "M2 Pressed",
                4: "K1 Pressed",
                5: "K1/M1 Pressed",
                8: "K2 Pressed",
                10: "K2/M2 Pressed",
                15: "K1/M1 and K2/M2 Pressed",
                16: "Smoke Pressed"}
    hexOffset = None
    lastHealthOffset = None
    replayLength = None
    rngSeed = None

    def __init__(self, replayDir):
        self.replayDir = replayDir
        self.replay = self.openReplayFile()
        self.songName = path.basename(replayDir)
        self.userName = self.getUserName()
        self.gameMode = self.getGameMode()
        self.gameVersion = "Release: " + self.getGameVersion()
        self.scoreData = self.scoreData()
        self.lifeBarData = self.getLifeBarData()

        dataSize = len(self.replay.hex()) / 2
        posDataCheck = (self.hexOffset - self.LastHealtOffset) == dataSize
        healthDataCheck = (self.hexOffset - int(self.hexOffset)) == 0
        if not healthDataCheck or posDataCheck:  # Check for health data
            self.hexOffset = 77 + len(self.userName) + calcsize("<hhhhhhihbi")

        self.replayDate = "Played on: " + str(self.getTime())
        self.onlineScoreID = "Score ID: " + str(self.getOnlineScoreID())

        if not healthDataCheck or not posDataCheck:
            self.poskeyData = self.getPosKeyData()
        else:
            self.poskeyData = "No position or key data avaliable"

    def openReplayFile(self):
        with open(self.replayDir, "rb") as r:  # Opens replay file
            return r.read()

    def getUserName(self):
        userNameHex = (str(self.replay.hex()).split("0b")[2])[2:]
        return bytes.fromhex(userNameHex).decode()

    def extractReplayData(self):
        gameData = unpack_from("<bi", self.replay, 0)
        offset = 75 + len(self.userName)
        scoreData = unpack_from("<hhhhhhihbi", self.replay, offset)
        return gameData + scoreData

    def printLifeBarData(self):
        pLifeBarData = []
        if self.getLifeBarData():
            for i in self.getLifeBarData():
                pLifeBarData.append(["Health: {}".format(i[0]),
                                     "Time: {} sec".format(i[1] / 1000)])
        else:
            print("No Health Data Avaliable")
        [print(i) for i in pLifeBarData]
        return None

    def printPosData(self):
        printposKeyData = []
        time = 0
        if isinstance(self.poskeyData, list):
            for i in self.poskeyData:
                if i[0] > 0:
                    time += i[0]
                if i[0] == -12345:
                    self.rngSeed = i[3]
                    break
                printposKeyData.append(["Time: {} sec".format(time / 1000),
                                        "X Position: {}".format(i[1]),
                                        "Y Position: {}".format(i[2]),
                                        self.keysDict.get(i[3])])
        else:
            print("No Position or Key Data Avaliable")
        [print(i) for i in printposKeyData]
        return None

    def scoreData(self):
        scoreData = "".join(["Number of 300s: {}\nNumber of {}{}\n",
                             "Number of {}{}\nNumber of {}{}\n",
                             "Number of {}{}\nNumber of misses: {}\n",
                             "Total score: {}\nGreatest combo: {}\n",
                             "Full Combo: {}\nMods Used: {}"])
        return scoreData.format(str(self.getNum300s()),
                                self.Dict100s.get(self.gameMode),
                                str(self.getNum100s()),
                                self.Dict50s.get(self.gameMode),
                                str(self.getNum50s()),
                                self.DictGekis.get(self.gameMode),
                                str(self.getNumGekis()),
                                self.DictKatus.get(self.gameMode),
                                str(self.getNumKatus()),
                                str(self.getNumMisses()),
                                str(self.getTotalScore()),
                                str(self.getGreatestCombo()),
                                self.getFC(),
                                self.getMods())

    def getGameMode(self):
        return self.gmDict.get(self.extractReplayData()[0])

    def getGameVersion(self):
        return str(self.extractReplayData()[1])

    def getNum300s(self):
        return self.extractReplayData()[2]

    def getNum100s(self):
        return self.extractReplayData()[3]

    def getNum50s(self):
        return self.extractReplayData()[4]

    def getNumGekis(self):
        return self.extractReplayData()[5]

    def getNumKatus(self):
        return self.extractReplayData()[6]

    def getNumMisses(self):
        return self.extractReplayData()[7]

    def getTotalScore(self):
        return self.extractReplayData()[8]

    def getGreatestCombo(self):
        return self.extractReplayData()[9]

    def getFC(self):
        return self.fcDict.get(self.extractReplayData()[10])

    def getMods(self):
        return self.modsDict.get(self.extractReplayData()[11])

    def getLifeBarData(self):
        graphList = []
        self.hexOffset = len(self.replay.hex().split("7c3")[0]) / 2
        for i in self.replay.hex().split("7c"):
            if "2c" or "302e3" in i:
                try:
                    h = i.partition("2c")[0]
                    t = i.partition("2c")[2]
                    health = bytes.fromhex(h).decode("utf-8")
                    time = bytes.fromhex(t).decode("utf-8")
                    graphList.append([float(health), int(time)])
                    self.hexOffset += len(i) / 2 + 1
                except ValueError:
                    pass
            else:
                pass
        lastOffset = int(self.hexOffset) * 2
        lastHealth = (self.replay.hex()[lastOffset:lastOffset + 12])
        self.LastHealtOffset = 1 + len(lastHealth.split("2c")[0]) / 2
        self.hexOffset += self.LastHealtOffset
        return graphList

    def getTime(self):
        miscData = unpack_from("<qi", self.replay, int(self.hexOffset))
        self.replayLength = miscData[1]
        time = datetime(1, 1, 1) + timedelta(microseconds=miscData[0] / 10)
        time.strftime("%Y-%m-%d %H:%M:%S")
        return time

    def getOnlineScoreID(self):
        self.hexOffset += calcsize("<qi")
        hexOffset2 = int(self.hexOffset) + self.replayLength
        onlineScoreID = unpack_from("<q", self.replay, hexOffset2)
        if onlineScoreID[0] == 0:
            return "Score not submitted"
        else:
            return onlineScoreID[0]

    def getPosKeyData(self):
        hexOffset2 = self.hexOffset + self.replayLength
        posData = self.replay[int(self.hexOffset): int(hexOffset2)]
        posData = decompress(posData, format=FORMAT_AUTO)
        posData = posData.decode("ascii")  # Pulls mouse + key data
        posDataList = []
        posDataRange = len(posData.split(",")) - 1
        for i in islice(posData.split(","), 0, posDataRange):
            timeFromLastEvent = int(i.split("|")[0])
            xPos = float(i.split("|")[1])
            yPos = float(i.split("|")[2])
            keyCombo = int(i.split("|")[3])
            posDataList.append([timeFromLastEvent, xPos, yPos, keyCombo])
        # [print(i) for i in posDataList]  # Organized posData into list
        return posDataList
