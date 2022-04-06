from cv2 import cv2 as cv
import numpy as np

from common import (
    findContours,
    approximateLargestContour,
    sortContourPoints,
    DEBUG_displayContours,
    DEBUG,
)


def getKeyboardImage() -> np.ndarray | None:
    cam = cv.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        if not ret:
            return None

        cv.imshow("keyboard", frame)

        key = cv.waitKey(1)

        if key % 256 == 155:
            cv.destroyWindow("keyboard")
            return frame


def getEdgeFrame(frame: np.ndarray) -> np.ndarray:
    grayscaleFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Denoise while maintaining edges
    bilateralFilteredFrame = cv.bilateralFilter(grayscaleFrame, 11, 17, 17)

    # Perform Sobel Filtering
    sobelX = cv.Sobel(
        src=bilateralFilteredFrame,
        ddepth=cv.CV_64F,
        dx=1,
        dy=0,
        ksize=3,
        borderType=cv.BORDER_DEFAULT,
    )

    sobelY = cv.Sobel(
        src=bilateralFilteredFrame,
        ddepth=cv.CV_64F,
        dx=0,
        dy=1,
        ksize=3,
        borderType=cv.BORDER_DEFAULT,
    )

    absSobelX = cv.convertScaleAbs(sobelX)
    absSobelY = cv.convertScaleAbs(sobelY)

    finalSobel = cv.addWeighted(absSobelX, 0.5, absSobelY, 0.5, 0)

    # Use Otsu's Threshold to get better defined edges while not using arbitrary
    # values
    _, threshedFrame = cv.threshold(
        finalSobel, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
    )

    if DEBUG:
        cv.imshow("debug", threshedFrame)
        cv.waitKey(0)

    return threshedFrame


def transformImageMap(contour: np.ndarray, imageShape: tuple) -> np.ndarray:
    imageMap = cv.imread("image-map.png")
    height, width, _ = imageMap.shape

    # Points are ordered to transform the image map to the position each edge
    # should be in
    initialPoints = np.array(
        [[width, height], [0, height], [0, 0], [width, 0]], np.float32
    )

    # Reshape to be the same as initial points
    contourPoints = np.reshape(contour, (4, 2))

    # Sort contour points to be clockwise, as the initial points expect the
    # contour points to be clockwise. If not, the mapping would fail.
    contourPoints = np.float32(sortContourPoints(contourPoints))

    transform = cv.getPerspectiveTransform(initialPoints, contourPoints)

    shapeHeight, shapeWidth, _ = imageShape

    modifiedImageMap = cv.warpPerspective(
        imageMap, transform, (shapeWidth, shapeHeight)
    )

    if DEBUG:
        cv.imshow("debug", modifiedImageMap)
        cv.waitKey(0)

    return modifiedImageMap


def getImageMap(image: np.ndarray) -> np.ndarray:
    if DEBUG:
        cv.namedWindow("debug")

    edgeFrame = getEdgeFrame(image)
    contours = findContours(edgeFrame)
    largestContour = approximateLargestContour(contours)

    DEBUG_displayContours(edgeFrame, largestContour)

    imageMap = transformImageMap(largestContour, image.shape)

    if DEBUG:
        cv.destroyAllWindows()

    return imageMap


if __name__ == "__main__":
    image = cv.imread("keyboard.jpg")
    getImageMap(image)
