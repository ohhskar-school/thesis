#!/usr/bin/env python3

import sys
import random
from cv2 import cv2 as cv

asciiDict = {
    8: "Backspace",
    9: "Tab",
    13: "Enter",
    27: "LeftControl",
    32: "Spacebar",
    33: "1",
    34: "'",
    35: "3",
    36: "4",
    37: "5",
    38: "7",
    39: "'",
    40: "9",
    41: "0",
    42: "8",
    43: "=",
    44: ",",
    45: "-",
    46: ".",
    47: "/",
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
    58: ";",
    59: ";",
    60: ",",
    61: "=",
    62: ".",
    63: "//",
    64: "2",
    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
    71: "G",
    72: "H",
    73: "I",
    74: "J",
    75: "K",
    76: "L",
    77: "M",
    78: "N",
    79: "O",
    80: "P",
    81: "Q",
    82: "R",
    83: "S",
    84: "T",
    85: "U",
    86: "V",
    87: "W",
    88: "X",
    89: "Y",
    90: "Z",
    91: "[",
    92: "\\",
    93: "]",
    94: "6",
    95: "-",
    96: "`",
    97: "A",
    98: "B",
    99: "C",
    100: "D",
    101: "E",
    102: "F",
    103: "G",
    104: "H",
    105: "I",
    106: "J",
    107: "K",
    108: "L",
    109: "M",
    110: "N",
    111: "O",
    112: "P",
    113: "Q",
    114: "R",
    115: "S",
    116: "T",
    117: "U",
    118: "V",
    119: "W",
    120: "X",
    121: "Y",
    122: "Z",
    123: "[",
    124: "\\",
    125: "]",
    126: "`",
    225: "LeftShift",
    226: "RightShift",
    233: "LeftAlt",
    234: "RightAlt",
    235: "LeftSuper",
    255: "Delete",
}


def collect(filename: str):
    cam = cv.VideoCapture(0)

    frameWidth = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cam.get(cv.CAP_PROP_FPS))

    videoFile = cv.VideoWriter(
        filename + ".mp4",
        cv.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frameWidth, frameHeight),
    )
    textFile = open(filename, "w")

    frameNum = 0

    while True:
        ret, frame = cam.read()

        if not ret:
            return None

        videoFile.write(frame)

        cv.imshow("frame", frame)

        key = cv.waitKey(1)

        if key != -1 and key % 256 != 155:
            print(chr(key % 256))

            textFile.write(
                "{frameNum}: {key}\n".format(
                    frameNum=frameNum, key=asciiDict[key % 256]
                )
            )

        frameNum += 1

        if key % 256 == 155:
            cv.destroyWindow("frame")
            break

    cam.release()
    videoFile.release()
    textFile.close()


def getFrames():
    cap = cv.VideoCapture(sys.argv[1] + ".mp4")
    cap.set(cv.CAP_PROP_POS_FRAMES, 5)
    ret, frame = cap.read()

    if not ret:
        return None

    cv.imshow("frame", frame)

    cv.waitKey(0)


def splitData():
    slow = range(1, 11)
    medium = range(1, 11)
    fast = range(1, 11)

    trainingSlow = random.sample(slow, k=6)
    trainingMedium = random.sample(medium, k=6)
    trainingFast = random.sample(fast, k=6)

    print(trainingSlow)
    print(trainingMedium)
    print(trainingFast)


if __name__ == "__main__":
    getFrames()
    # splitData()
    # time.sleep(1)
    # collect("test-data/" + sys.argv[1])
