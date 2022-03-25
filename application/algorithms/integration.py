#!/usr/bin/env python3

from cv2 import cv2 as cv
import numpy as np

from common import (
    findContours,
    approximateLargestContour,
    sortContourPoints,
    DEBUG_displayContours,
    DEBUG_SHOW_IMAGES,
)
from keyboard_map import keyDict
from keyboard_detection import getImageMap


def filterVirtualMap(virtualMap: np.ndarray, key: list[int]) -> np.ndarray:
    # Flip key, as they are stored in RGB, but the image is in BGR
    key = [key[-1], key[1], key[0]]

    # Create mask where all other colors are blacked out .all is used here as
    # np.where(virtualMap != key, ...) will consider other pixel values where
    # only 1 channel is the same. i.e. pixel [100, 0, 0] will not be blacked out
    # if the key is [100, 243, 0] as the blue channel of the pixel matches the
    # key
    mask = np.invert((virtualMap == key).all(axis=2))

    virtualMap[mask] = [0, 0, 0]

    # virtualMap = np.where(virtualMap != key, [0, 0, 0], virtualMap).astype(np.uint8)

    if DEBUG_SHOW_IMAGES:
        cv.imshow("debug", virtualMap)
        print(key)

        cv.waitKey(0)

    return virtualMap


# TODO: Pre calculate contour points for all keys
def getROIContourPoints(virtualMap: np.ndarray, key: list[int]) -> np.ndarray:
    filteredMap = filterVirtualMap(virtualMap, key)

    grayMap = cv.cvtColor(filteredMap, cv.COLOR_BGR2GRAY)

    contours = findContours(grayMap)
    largestContour = approximateLargestContour(contours)

    DEBUG_displayContours(grayMap, largestContour)

    return sortContourPoints(largestContour)


def main():
    if DEBUG_SHOW_IMAGES:
        cv.namedWindow("debug")

    virtualMap = getImageMap()

    if virtualMap is None:
        return

    getROIContourPoints(virtualMap, keyDict["Q"])

    if DEBUG_SHOW_IMAGES:
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
