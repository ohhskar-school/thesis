#!/usr/bin/env python3
from os import walk


def main():
    (_, _, filenames) = next(walk("../dataset/test"))
    files = [file for file in filenames if not "mp4" in file]

    for file in files:
        with open(f"../dataset/test/{file}", "r+") as f:
            content = f.read().replace(" ", "")
            f.seek(0)
            f.write(content)
            f.truncate()


if __name__ == "__main__":
    main()
