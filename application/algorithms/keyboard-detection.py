from cv2 import cv2 as cv
import numpy as np

SHOW_DEBUG_IMAGES: bool = True
USE_DEBUG_IMAGE: bool = False


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


def applySobelFilter(frame: np.ndarray) -> np.ndarray:
    grayscaleFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    bilateralFilteredFrame = cv.bilateralFilter(grayscaleFrame, 11, 17, 17)

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

    _, threshedFrame = cv.threshold(
        finalSobel, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
    )

    if SHOW_DEBUG_IMAGES:
        cv.imshow("sobel", finalSobel)
        cv.imshow("threshed-sobel", threshedFrame)
        cv.waitKey(0)
        cv.destroyWindow("sobel")
        cv.destroyWindow("threshed-sobel")

    return threshedFrame


def findContours(frame: np.ndarray) -> tuple[np.ndarray]:
    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if SHOW_DEBUG_IMAGES:
        contourFrame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        cv.drawContours(contourFrame, contours, -1, (0, 255, 0), 3)
        cv.imshow("contours", contourFrame)
        cv.waitKey(0)
        cv.destroyWindow("contours")

    return contours


def getLargestContour(contours: tuple[np.ndarray]) -> np.ndarray:
    sortedContours = sorted(contours, key=cv.contourArea, reverse=True)

    epsilon = 0.01 * cv.arcLength(sortedContours[0], True)
    approximation = cv.approxPolyDP(sortedContours[0], epsilon, True)

    return approximation


def displayContoursAndBoundingBox(frame: np.ndarray, contour: np.ndarray):
    if SHOW_DEBUG_IMAGES:
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
        cv.imshow("largest contour", contourFrame)
        cv.waitKey(0)
        cv.destroyWindow("largest contour")


def transformImageMap(contour: np.ndarray, imageShape: tuple) -> np.ndarray:
    imageMap = cv.imread("image-map.png")
    height: int
    width: int
    height, width, _ = imageMap.shape

    # Points are ordered to transform the image map to the position each edge
    # should be in
    initialPoints = np.array(
        [[width, height], [0, height], [0, 0], [width, 0]], np.float32
    )

    # Reshape to be the same as initial points
    contourPoints = np.reshape(contour, (4, 2))

    # Sort contour points to be clockwise, as the initial points expect the
    # contour points to be clockwise. If not, the transformation will fail
    contourPoints = np.float32(sortContourPoints(contourPoints))

    transform = cv.getPerspectiveTransform(initialPoints, contourPoints)

    shapeHeight, shapeWidth, _ = imageShape

    modifiedImageMap = cv.warpPerspective(
        imageMap, transform, (shapeWidth, shapeHeight)
    )

    if SHOW_DEBUG_IMAGES:
        cv.imshow("image map", modifiedImageMap)
        cv.imshow("modified image map", modifiedImageMap)
        cv.waitKey(0)
        cv.destroyWindow("image map")
        cv.destroyWindow("modified image map")

    return modifiedImageMap


def sortContourPoints(contour: np.ndarray) -> np.ndarray:
    indices = np.lexsort((contour[:, 1], contour[:, 0]))
    contour = contour[indices]

    left = contour[:2]
    leftIndices = left[:, 1].argsort()
    left = left[leftIndices]

    right = contour[2:]
    rightIndices = right[:, 1].argsort()
    right = right[rightIndices]

    return np.array([left[0], right[0], right[1], left[1]])


def main():
    if USE_DEBUG_IMAGE:
        keyboardImage = cv.imread("test.jpg", 1)
    else:
        keyboardImage = getKeyboardImage()

    if keyboardImage is None:
        return

    sobelFilterFrame = applySobelFilter(keyboardImage)
    contours = findContours(sobelFilterFrame)
    largestContour = getLargestContour(contours)

    displayContoursAndBoundingBox(sobelFilterFrame, largestContour)

    imageMap = transformImageMap(largestContour, keyboardImage.shape)


if __name__ == "__main__":
    main()
