from cv2 import cv2 as cv
import numpy as np

DEBUG_SHOW_IMAGES: bool = True
DEBUG_USE_WEBCAM: bool = True


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

    if DEBUG_SHOW_IMAGES:
        cv.imshow("debug", threshedFrame)
        cv.waitKey(0)

    return threshedFrame


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

    if DEBUG_SHOW_IMAGES:
        cv.imshow("debug", modifiedImageMap)
        cv.waitKey(0)

    return modifiedImageMap


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


def getImageMap():
    if DEBUG_SHOW_IMAGES:
        cv.namedWindow("debug")

    if DEBUG_USE_WEBCAM:
        keyboardImage = cv.imread("fail.jpg", 1)
    else:
        keyboardImage = getKeyboardImage()

    if keyboardImage is None:
        return

    edgeFrame = getEdgeFrame(keyboardImage)
    contours = findContours(edgeFrame)
    largestContour = approximateLargestContour(contours)

    DEBUG_displayContours(edgeFrame, largestContour)

    imageMap = transformImageMap(largestContour, keyboardImage.shape)

    return imageMap


if __name__ == "__main__":
    getImageMap()
