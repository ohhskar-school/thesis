from cv2 import cv2
import numpy as np

SHOW_DEBUG_IMAGES: bool = True
USE_DEBUG_IMAGE: bool = True


def getKeyboardImage() -> np.ndarray | None:
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        if not ret:
            return None

        cv2.imshow("keyboard", frame)
        key = cv2.waitKey(1)

        if key % 256 == 155:
            cv2.destroyWindow("keyboard")
            return frame


def applySobelFilter(frame: np.ndarray) -> np.ndarray:
    grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurredFrame = cv2.GaussianBlur(grayscaleFrame, (3, 3), 0)

    sobelX = cv2.Sobel(
        src=blurredFrame,
        ddepth=cv2.CV_64F,
        dx=1,
        dy=0,
        ksize=3,
        borderType=cv2.BORDER_DEFAULT,
    )

    sobelY = cv2.Sobel(
        src=blurredFrame,
        ddepth=cv2.CV_64F,
        dx=0,
        dy=1,
        ksize=3,
        borderType=cv2.BORDER_DEFAULT,
    )

    absSobelX = cv2.convertScaleAbs(sobelX)
    absSobelY = cv2.convertScaleAbs(sobelY)

    finalSobel = cv2.addWeighted(absSobelX, 0.5, absSobelY, 0.5, 0)

    # Apply Adaptive Thresholding
    _, threshedFrame = cv2.threshold(
        finalSobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    if SHOW_DEBUG_IMAGES:
        cv2.imshow("sobel", finalSobel)
        cv2.imshow("threshed-sobel", threshedFrame)
        cv2.waitKey(0)
        cv2.destroyWindow("sobel")

    return threshedFrame


# def applyThreshold(frame: np.ndarray) -> np.ndarray:
#     grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     bilateralFilteredFrame = cv2.bilateralFilter(grayscaleFrame, 11, 17, 17)

#     # Apply Adaptive Thresholding
#     _, threshedFrame = cv2.threshold(
#         bilateralFilteredFrame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
#     )

#     if SHOW_DEBUG_IMAGES:
#         cv2.imshow("bilateral filter", bilateralFilteredFrame)
#         cv2.imshow("threshed frame", threshedFrame)
#         cv2.waitKey(0)
#         cv2.destroyWindow("bilateral filter")
#         cv2.destroyWindow("threshed frame")

#     return threshedFrame


def findContours(frame: np.ndarray) -> tuple[np.ndarray]:
    if SHOW_DEBUG_IMAGES:
        cv2.imshow("findContoursEnter", frame)

    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if SHOW_DEBUG_IMAGES:
        contourFrame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contourFrame, contours, -1, (0, 255, 0), 3)
        cv2.imshow("contours", contourFrame)
        cv2.waitKey(0)
        cv2.destroyWindow("contours")

    return contours


def getLargestContour(contours: tuple[np.ndarray]) -> np.ndarray:
    sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)

    epsilon = 0.01 * cv2.arcLength(sortedContours[0], True)
    approximation = cv2.approxPolyDP(sortedContours[0], epsilon, True)

    return approximation


def displayContours(frame: np.ndarray, contour: np.ndarray):
    if SHOW_DEBUG_IMAGES:
        contourFrame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contourFrame, [contour], 0, (0, 255, 0), 2)
        for point in contour:
            contourFrame = cv2.circle(
                contourFrame,
                point[0],
                radius=4,
                color=(0, 0, 255),
                thickness=cv2.FILLED,
            )

        cv2.imshow("largest contour", contourFrame)
        cv2.waitKey(0)
        cv2.destroyWindow("largest contour")


def main():
    if USE_DEBUG_IMAGE:
        keyboardImage = cv2.imread("test.jpg", 1)
    else:
        keyboardImage = getKeyboardImage()

    if keyboardImage is None:
        return

    sobelFilterFrame = applySobelFilter(keyboardImage)
    contours = findContours(sobelFilterFrame)
    largestContour = getLargestContour(contours)

    displayContours(sobelFilterFrame, largestContour)


if __name__ == "__main__":
    main()
