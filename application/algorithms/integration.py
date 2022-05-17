#!/usr/bin/env python3

from cv2 import cv2 as cv
import numpy as np

# import time

from common import DEBUG

from keyboard_detection import getContourPointsFromImage
from finger_detection import classifyPressedFinger


def main(keyboardImage: np.ndarray, handImage: np.ndarray):

    # start = time.time()
    if DEBUG:
        cv.namedWindow("debug")

    # Step 1
    allContourPoints = getContourPointsFromImage(keyboardImage)

    contourPoints = allContourPoints["Spacebar"]

    # elapsed = time.time() - start

    # Step 2
    if DEBUG:
        cv.imshow("debug", handImage)
        cv.waitKey(0)

    result = classifyPressedFinger(handImage, contourPoints)

    if result is not None:
        print(result)

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
