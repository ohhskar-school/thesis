from cv2 import cv2 as cv
import numpy as np

from copy import deepcopy

from algorithm import keyboard_map, common


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

    if common.DEBUG:
        cv.imshow("debug", grayscaleFrame)
        cv.waitKey(0)

    # Denoise while maintaining edges
    bilateralFilteredFrame = cv.bilateralFilter(grayscaleFrame, 11, 17, 17)

    if common.DEBUG:
        cv.imshow("debug", bilateralFilteredFrame)
        cv.waitKey(0)

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

    if common.DEBUG:
        cv.imshow("debug", finalSobel)
        cv.waitKey(0)

    # Use Otsu's Threshold to get better defined edges while not using arbitrary
    # values
    _, threshedFrame = cv.threshold(
        finalSobel, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
    )

    if common.DEBUG:
        cv.imshow("debug", threshedFrame)
        cv.waitKey(0)

    return threshedFrame


def transformImageMap(contour: np.ndarray, imageShape: tuple) -> np.ndarray:
    imageMap = cv.imread("./algorithm/images/image-map.png")
    height, width, _ = imageMap.shape

    if common.DEBUG:
        cv.imshow("debug", imageMap)
        cv.waitKey(0)

    # Points are ordered to transform the image map to the position each edge
    # should be in
    initialPoints = np.array(
        [[width, height], [0, height], [0, 0], [width, 0]], np.float32
    )

    # Reshape to be the same as initial points
    contourPoints = np.reshape(contour, (4, 2))

    if len(contourPoints) != 4:
        raise Exception(
            "keyboard_detection: contour points does not match expected amount"
        )

    # Sort contour points to be clockwise, as the initial points expect the
    # contour points to be clockwise. If not, the mapping would fail.
    contourPoints = np.float32(common.sortContourPoints(contourPoints))

    transform = cv.getPerspectiveTransform(initialPoints, contourPoints)

    shapeHeight, shapeWidth, _ = imageShape

    modifiedImageMap = cv.warpPerspective(
        imageMap, transform, (shapeWidth, shapeHeight)
    )

    if common.DEBUG:
        cv.imshow("debug", modifiedImageMap)
        cv.waitKey(0)

    return modifiedImageMap


def getImageMap(image: np.ndarray) -> np.ndarray:
    if common.DEBUG:
        cv.namedWindow("debug")

    edgeFrame = getEdgeFrame(image)
    contours = common.findContours(edgeFrame)
    largestContour = common.approximateLargestContour(contours)

    common.DEBUG_displayContours(edgeFrame, largestContour)

    imageMap = transformImageMap(largestContour, image.shape)

    if common.DEBUG:
        cv.destroyAllWindows()

    return imageMap


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

    if common.DEBUG:
        cv.imshow("debug", filteredVirtualMap)

        cv.waitKey(0)

    return filteredVirtualMap


def getKeyContourPoints(virtualMap: np.ndarray, key: list[int]) -> np.ndarray:
    filteredMap = filterVirtualMap(virtualMap, key)

    if common.DEBUG:
        cv.imshow("debug", filteredMap)

        cv.waitKey(0)

    grayMap = cv.cvtColor(filteredMap, cv.COLOR_BGR2GRAY)

    contours = common.findContours(grayMap)

    largestContour = common.approximateLargestContour(contours)

    common.DEBUG_displayContours(grayMap, np.reshape(largestContour, (4, 1, 2)))

    largestContour = np.reshape(largestContour, (4, 2))
    sortedContour = common.sortContourPoints(largestContour)
    scaledContour = common.scaleContours(sortedContour)

    common.DEBUG_displayContours(grayMap, np.reshape(scaledContour, (4, 1, 2)))

    return scaledContour


def getAllContourPoints(virtualMap: np.ndarray) -> dict[str, list]:
    return {
        key: getKeyContourPoints(virtualMap, color).tolist()
        for key, color in keyboard_map.keyDict.items()
    }


def getContourPointsFromImage(keyboardImage: np.ndarray) -> dict[str, list]:
    virtualMap = getImageMap(keyboardImage)

    if virtualMap is None:
        raise Exception("Virtual map cannot be obtained")

    return getAllContourPoints(virtualMap)


if __name__ == "__main__":
    image = cv.imread("images/keyboard.jpg")
    getImageMap(image)
