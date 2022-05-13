#!/usr/bin/env python3
from os import walk, path
from cv2 import cv2 as cv


keypressDict = {
    97: "LEFT_PINKY",
    115: "LEFT_RING",
    100: "LEFT_MIDDLE",
    102: "LEFT_INDEX",
    106: "RIGHT_INDEX",
    107: "RIGHT_MIDDLE",
    108: "RIGHT_RING",
    59: "RIGHT_PINKY",
    233: "LEFT_THUMB",
    32: "RIGHT_THUMB",
    27: "ESCAPE",
    72: "INVALID",
}


def main():
    (_, _, filenames) = next(walk("../dataset/test"))
    files = sorted(
        [file for file in filenames if not "mp4" in file and not "labeled" in file]
    )

    for index, file in enumerate(files):
        fileLocation = f"../dataset/test/{file}"
        cap = cv.VideoCapture(fileLocation + ".mp4")
        labeledFile = f"{fileLocation}-labeled"

        newFileContent = []

        with open(labeledFile) as fp:
            fileContent = [line.rstrip() for line in fp]

        cap.set(cv.CAP_PROP_POS_FRAMES, 10)
        ret, frame = cap.read()
        frame = cv.rotate(frame, cv.ROTATE_180)

        cv.imshow("setup", frame)

        for keypressIndex, keypress in enumerate(fileContent):
            data = keypress.split(":")
            cap.set(cv.CAP_PROP_POS_FRAMES, int(data[0]))
            ret, frame = cap.read()

            if not ret:
                raise Exception(f"label: frame {data[0]} not found for {file}")

            frame = cv.rotate(frame, cv.ROTATE_180)
            cv.putText(
                frame,
                keypress,
                (10, 25),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
                cv.LINE_AA,
            )

            cv.putText(
                frame,
                f"kp: {keypressIndex + 1}/{len(fileContent)} | file: {index + 1}/{len(files)}",
                (10, 465),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
                cv.LINE_AA,
            )

            cv.imshow("debug", frame)

            keypressString = ""

            while True:
                key = cv.waitKey(0)

                if key % 256 == 27:
                    cv.destroyAllWindows()
                    return

                if key % 256 == 13:
                    keypressString = ""
                    break

                try:
                    keypressString = keypressDict[key]
                    break
                except:
                    keypressString = "ERR"

            if len(keypressString) > 0:
                keypressItems = keypress.split(":")
                newFileContent.append(
                    f"{keypressItems[0]}:{keypressItems[1]}:{keypressString}\n"
                )
                continue

            newFileContent.append(f"{keypress}\n")

        with open(labeledFile, "w") as fl:
            fl.writelines(newFileContent)
            fl.truncate()
            print(f"Written {labeledFile}")


if __name__ == "__main__":
    main()
