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
    uuid = f"training-{time.time()}"
    folder = f"./results/{uuid}"
    mkdir(folder)

    files = sorted(
        [file for file in filenames if not "mp4" in file and not "labeled" in file]
    )

    # Create log for entire run
    logFileContent = []
    resultFileContent = [
        [
            "file_name",
            "frame",
            "key",
            "finger",
            "is_correct",
            "fingertips_detected",
            "keyboard_detection_time",
            "finger_classification_time",
        ]
    ]

    for file in files:
        # Output Files
        logFileContent.append(f"INFO: Start {file}")

        fileLocation = f"./dataset/training/{file}"
        labeledFile = f"{fileLocation}-labeled"

        cap = cv.VideoCapture(fileLocation + ".mp4")

        keyboardDetectionTimeStart = time.time()

        allContourPoints = {}

        for i in [10, 15, 20]:
            cap.set(cv.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                logFileContent.append(f"ERROR: Failed to get frame {i} for {file}")
                break

            try:
                keyboardDetectionTimeStart = time.time()
                allContourPoints = getContourPointsFromImage(frame)
            except Exception as e:
                logFileContent.append(
                    f"ERROR: Failed to get contour points for {file} with frame {i}"
                )
                logFileContent.append(f"ERROR: {e}")
                cv.imwrite(f"{folder}/{file}:{i}.png", frame)
            else:
                break

        if len(allContourPoints) == 0:
            logFileContent.append(f"ERROR: Failed to get contour points for {file}")
            continue

        keyboardDetectionTimeEnd = time.time() - keyboardDetectionTimeStart

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

            contourPoints = allContourPoints[data[1]]

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

            isCorrect = data[2] in result

            resultFileContent.append(
                [
                    file,
                    data[0],
                    data[1],
                    data[2],
                    str(isCorrect),
                    ",".join(result),
                    str(keyboardDetectionTimeEnd),
                    str(fingerClassificationTimeEnd),
                ]
            )

            if not isCorrect:
                cv.imwrite(f"{folder}/{file}:{keypress}.png", frame)

    with open(
        f"{folder}/{uuid}-results.csv", "w", encoding="UTF8", newline=""
    ) as results:
        writer = csv.writer(results, quoting=csv.QUOTE_ALL)
        writer.writerows(resultFileContent)

    with open(f"{folder}/{uuid}-log", "w") as logs:
        logs.writelines([f"{log}\n" for log in logFileContent])
        logs.truncate()


if __name__ == "__main__":
    main()
