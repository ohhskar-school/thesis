#!/usr/bin/env python3
import numpy as np
from cv2 import cv2 as cv


DEBUG = True


def findContours(frame: np.ndarray) -> tuple[np.ndarray]:
    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if DEBUG:
        contourFrame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        cv.drawContours(contourFrame, contours, -1, (0, 255, 0), 2)
        cv.imshow("debug", contourFrame)
        cv.waitKey(0)

    return contours


def approximateLargestContour(contours: tuple[np.ndarray]) -> np.ndarray:
    # Sort contours by area
    largestContour = sorted(contours, key=cv.contourArea, reverse=True)[0]

    # Use Douglas-Peucker algorithm to approximate a shape
    # Set accuracy using the epsilon. 1% accuracy as the simplest shape, a
    # rectangle, is expected
    epsilon = 0.01 * cv.arcLength(largestContour, True)
    approximation = cv.approxPolyDP(largestContour, epsilon, True)

    return approximation


def sortContourPoints(contour: np.ndarray) -> np.ndarray:
    # Sort by x axis
    indices = contour[:, 0].argsort()
    contour = contour[indices]

    # Get the two left points and sort by y axis
    left = contour[:2]
    leftIndices = left[:, 1].argsort()
    left = left[leftIndices]

    # Get the two right points and sort by y axis
    right = contour[2:]
    rightIndices = right[:, 1].argsort()
    right = right[rightIndices]

    # arrange clockwise
    return np.array([left[0], right[0], right[1], left[1]])


def scaleContours(contours: np.ndarray) -> np.ndarray:
    scaleFactor = 10

    upperLeft = [contours[0][0] - scaleFactor, contours[0][1] - scaleFactor]
    upperRight = [contours[1][0] + scaleFactor, contours[1][1] - scaleFactor]
    lowerRight = [contours[2][0] + scaleFactor, contours[2][1] + scaleFactor]
    lowerLeft = [contours[3][0] - scaleFactor, contours[3][1] + scaleFactor]

    return np.array([upperLeft, upperRight, lowerRight, lowerLeft])


# def scaleContours(contours: np.ndarray) -> np.ndarray:
#     M = cv.moments(contours)
#     cx = int(M["m10"] / M["m00"])
#     cy = int(M["m01"] / M["m00"])

#     cnt_norm = contours - [cx, cy]
#     cnt_scaled = cnt_norm * 1.5
#     cnt_scaled = cnt_scaled + [cx, cy]
#     cnt_scaled = cnt_scaled.astype(np.int32)

#     print(cnt_scaled.shape)

#     return cnt_scaled


def DEBUG_displayContours(frame: np.ndarray, contour: np.ndarray):
    if DEBUG:
        contourFrame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        cv.drawContours(contourFrame, [contour], 0, (0, 255, 0), 1)
        for point in contour:
            contourFrame = cv.circle(
                contourFrame,
                point[0],
                radius=4,
                color=(0, 0, 255),
                thickness=cv.FILLED,
            )
        cv.imshow("debug", contourFrame)
        cv.waitKey(0)


def convertResultToStr(result: tuple[str, str]) -> str:
    return result[0] + "_" + result[1].split("_")[0]
