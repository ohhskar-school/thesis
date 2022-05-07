#!/usr/bin/env python3

from cv2 import cv2 as cv
import numpy as np
from copy import deepcopy

# import time

from common import (
    findContours,
    approximateLargestContour,
    sortContourPoints,
    convertResultToStr,
    DEBUG_displayContours,
    DEBUG,
)

from keyboard_map import keyDict
from keyboard_detection import getImageMap
from finger_detection import classifyPressedFinger


def filterVirtualMap(virtualMap: np.ndarray, key: list[int]) -> np.ndarray:
    # Flip key, as they are stored in RGB, but the image is in BGR
    key = [key[-1], key[1], key[0]]

    filteredVirtualMap = deepcopy(virtualMap)

    # Create mask where all other colors are blacked out .all is used here as
    # np.where(virtualMap != key, ...) will consider other pixel values where
    # only 1 channel is the same. i.e. pixel [100, 0, 0] will not be blacked out
    # if the key is [100, 243, 0] as the blue channel of the pixel matches the
    # key
    mask = np.invert((filteredVirtualMap == key).all(axis=2))

    filteredVirtualMap[mask] = [0, 0, 0]

    # virtualMap = np.where(virtualMap != key, [0, 0, 0], virtualMap).astype(np.uint8)

    if DEBUG:
        cv.imshow("debug", filteredVirtualMap)

        cv.waitKey(0)

    return filteredVirtualMap


def getKeyContourPoints(virtualMap: np.ndarray, key: list[int]) -> np.ndarray:
    filteredMap = filterVirtualMap(virtualMap, key)

    if DEBUG:
        cv.imshow("debug", filteredMap)

        cv.waitKey(0)

    grayMap = cv.cvtColor(filteredMap, cv.COLOR_BGR2GRAY)

    contours = findContours(grayMap)
    largestContour = approximateLargestContour(contours)

    DEBUG_displayContours(grayMap, largestContour)

    largestContour = np.reshape(largestContour, (4, 2))

    return sortContourPoints(largestContour)


def getAllContourPoints(virtualMap: np.ndarray) -> dict[str, np.ndarray]:
    return {
        key: getKeyContourPoints(virtualMap, color) for key, color in keyDict.items()
    }


def main(keyboardImage: np.ndarray, handImage: np.ndarray):

    # start = time.time()

    if DEBUG:
        cv.namedWindow("debug")

    # Step 1
    virtualMap = getImageMap(keyboardImage)

    if virtualMap is None:
        return

    allContourPoints = getAllContourPoints(virtualMap)

    contourPoints = allContourPoints["Spacebar"]

    # elapsed = time.time() - start

    # Step 2
    if DEBUG:
        cv.imshow("debug", handImage)
        cv.waitKey(0)

    result = classifyPressedFinger(handImage, contourPoints)

    if result is not None:
        print(convertResultToStr(result))

    # total = time.time() - start
    # classifying = total - elapsed

    # print("Init Time: " + str(elapsed))
    # print("Classifying Time: " + str(classifying))
    # print("Total Time: " + str(total))

    if DEBUG:
        print(result)
        cv.destroyAllWindows()

    return result


if __name__ == "__main__":
    keyboardImage = cv.imread("images/keyboard.jpg")
    handImage = cv.imread("images/hand.jpg")
    main(keyboardImage, handImage)
