#!/usr/bin/env python3

from os import walk, mkdir
from cv2 import cv2 as cv
import time
import csv

from finger_detection import classifyPressedFinger
from keyboard_detection import getContourPointsFromImage


def main():
    (_, _, filenames) = next(walk("./dataset/training"))

    # Create output folder
    folder = f"./results/training-{time.time()}/"
    mkdir(folder)

    files = sorted(
        [file for file in filenames if not "mp4" in file and not "labeled" in file]
    )

    # Create log for entire run
    logFileContent = []

    for file in files:
        # Output Files
        logFileContent.append(f"INFO: Start {file}")
        resultFileContent = [
            [
                "is_correct",
                "fingertips_detected",
                "keyboard_detection_time",
                "finger_classification_time",
                "total_time",
            ]
        ]

        fileLocation = f"./dataset/training/{file}"
        labeledFile = f"{fileLocation}-labeled"

        cap = cv.VideoCapture(fileLocation + ".mp4")
        cap.set(cv.CAP_PROP_POS_FRAMES, 10)
        ret, frame = cap.read()

        keyboardDetectionTimeStart = time.time()

        allContourPoints = {}
        try:
            allContourPoints = getContourPointsFromImage(frame)
        except Exception as e:
            logFileContent.append(f"ERROR: Failed to get contour points for {file}")
            logFileContent.append(f"ERROR: {e}")
            continue

        keyboardDetectionTimeEnd = time.time() - keyboardDetectionTimeStart

        if not ret:
            logFileContent.append(f"ERROR: Failed to get frame 10 for {file}")
            continue

        with open(labeledFile) as fp:
            fileContent = [line.rstrip() for line in fp]

        for keypress in fileContent:
            data = keypress.split(":")
            cap.set(cv.CAP_PROP_POS_FRAMES, int(data[0]))
            ret, frame = cap.read()

            if not ret:
                logFileContent.append(
                    f"ERROR: Failed to get frame for {keypress} of {file}"
                )
                continue

            contourPoints = allContourPoints[fileContent[1]]

            fingerClassificationTimeStart = time.time()
            result = []
            try:
                result = classifyPressedFinger(frame, contourPoints)
            except Exception as e:
                logFileContent.append(
                    f"ERROR: Failed to classify finger for {keypress} of {file}"
                )
                logFileContent.append(f"ERROR: {e}")
                resultFileContent.append(
                    [
                        keypress,
                        str(False),
                        "Failed",
                        str(keyboardDetectionTimeEnd),
                        "0",
                        "0",
                    ]
                )
                continue

            fingerClassificationTimeEnd = time.time() - fingerClassificationTimeStart

            isCorrect = fileContent[2] in result

            resultFileContent.append(
                [
                    keypress,
                    str(isCorrect),
                    ",".join(result),
                    str(keyboardDetectionTimeEnd),
                    str(fingerClassificationTimeEnd),
                    str(keyboardDetectionTimeEnd + fingerClassificationTimeEnd),
                ]
            )

            if not isCorrect:
                cv.imwrite(f"{folder}{file}{keypress}", frame)

            with open(
                f"{folder}{file}.csv", "w", encoding="UTF8", newline=""
            ) as results:
                writer = csv.writer(results)
                writer.writerows(resultFileContent)

    with open(f"{folder}log", "w") as logs:
        logs.writelines([f"{log}\n" for log in logFileContent])
        logs.truncate()


if __name__ == "__main__":
    main()
