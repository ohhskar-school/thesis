#!/usr/bin/env python3
import numpy as np
from cv2 import cv2 as cv


DEBUG_SHOW_IMAGES = True
DEBUG_USE_WEBCAM = False


def findContours(frame: np.ndarray) -> tuple[np.ndarray]:
    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if DEBUG_SHOW_IMAGES:
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


def DEBUG_displayContours(frame: np.ndarray, contour: np.ndarray):
    if DEBUG_SHOW_IMAGES:
        contourFrame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        cv.drawContours(contourFrame, [contour], 0, (0, 255, 0), 2)
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
