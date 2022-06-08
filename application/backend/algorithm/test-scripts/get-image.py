#!/usr/bin/env python3

from cv2 import cv2 as cv


def main():
    file = "fast-05"
    keyboardFrame = 10
    fingerFrame = 233
    fileLocation = f"../dataset/training/{file}"

    cap = cv.VideoCapture(f"{fileLocation}.mp4")

    cap.set(cv.CAP_PROP_POS_FRAMES, keyboardFrame)
    ret, frame = cap.read()

    if not ret:
        return

    cv.imwrite(f"../images/{file}-{keyboardFrame}.png", frame)

    cap.set(cv.CAP_PROP_POS_FRAMES, fingerFrame)
    ret, frame = cap.read()

    if not ret:
        return

    cv.imwrite(f"../images/{file}-{fingerFrame}.png", frame)


if __name__ == "__main__":
    main()
