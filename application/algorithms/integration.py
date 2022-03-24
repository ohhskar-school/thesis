#!/usr/bin/env python3
#
from cv2 import cv2 as cv
import numpy as np

keyDict = {
    "LeftControl": "#550000",
    "LeftSuper": "#2D0000",
    "LeftAlt": "#3A2300",
    "Spacebar": "#3E3700",
    "RightAlt": "#003238",
    "RightMeta": "#001C2C",
    "RightSuper": "#000349",
    "RightControl": "#18004D",
    "~": "#FF0000",
    "1": "#FF9900",
    "2": "#FFE600",
    "3": "#BDFF00",
    "4": "#8FFF00",
    "5": "#33FF00",
    "6": "#00FF66",
    "7": "#00FFC2",
    "8": "#00E0FF",
    "9": "#00A3FF",
    "0": "#0066FF",
    "-": "#000AFF",
    "+": "#5200FF",
    "Backspace": "#BD00FF",
    "Tab": "#E00000",
    "Q": "#D68000",
    "W": "#E1CB00",
    "E": "#A0D900",
    "R": "#7EE000",
    "T": "#2BD900",
    "Y": "#00D856",
    "U": "#00C395",
    "I": "#00B7D0",
    "O": "#0088D4",
    "P": "#004FC5",
    "[": "#0008D3",
    "]": "#3F00C5",
    "|": "#8600B5",
    "CapsLock": "#C30000",
    "A": "#A76400",
    "S": "#B2A100",
    "D": "#7CA800",
    "F": "#65B400",
    "G": "#1F9D00",
    "H": "#008B38",
    "J": "#018B6A",
    "K": "#008294",
    "L": "#005E93",
    ":": "#003482",
    '"': "#0007AA",
    "Enter": "#23006D",
    "LeftShift": "#960000",
    "Z": "#683E00",
    "X": "#827500",
    "C": "#4D6800",
    "V": "#3F7100",
    "B": "#125800",
    "N": "#00421A",
    "M": "#005440",
    ",": "#004B55",
    ".": "#00466D",
    "/": "#002050",
    "RightShift": "#000580",
}


def hexToRGB():
    print("keyDict = {")
    for key, value in keyDict.items():
        print(
            '"',
            key,
            '":',
        )
    print("}")


def filterVirtualMap(virtualMap: np.ndarray, key: str) -> np.ndarray:
    return virtualMap
