#! /home/rico/Apps/anaconda3/envs/image-editing/bin/python

import sys
import os
import datetime
import exifread
from tqdm import tqdm


def main():
    if len(sys.argv) < 2:
        print("Please specify a directory with images to copy from")
        return -1
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("Not a directory")
        return -1

    if len(sys.argv) < 3:
        print("Please specify a directory to copy into")
        return -1

    copyIntoPath = sys.argv[2]
    if not os.path.isdir(path):
        print("Not a directory")
        return -1

    if len(sys.argv) < 4:
        print("Please specify the extension as a second input argument")
        return -1
    extensionToChange = sys.argv[3]

    existingDates = {}
    for name in tqdm(os.listdir(copyIntoPath)):
        listExif(name, copyIntoPath, existingDates, extensionToChange)
    for name in tqdm(os.listdir(path)):
        listExif(name, path, existingDates, extensionToChange)
    print(existingDates)


def listExif(name, path, existingDates, extensionToChange):
    _, extension = os.path.splitext(os.path.join(path, name))
    if extensionToChange == extension:
        imgPath = os.path.join(path, name)
        f = open(imgPath, 'rb')
        tags = exifread.process_file(f)
        # print(name)
        # print(tags["Image DateTime"])
        key = "Image Tag 0x014A"
        dateKey = "Image DateTime"
        if key in tags:
            strDate = str(tags[key])
            if strDate not in existingDates:
                existingDates[strDate] = name
            else:
                if name == existingDates[strDate]:
                    tqdm.write("There seems to be a duplicate between {} and {}".format(
                        existingDates[strDate], name))


def convertToDate(strDate):
    return datetime.datetime.strptime(strDate, "%Y:%m:%d %H:%M:%S")


if __name__ == "__main__":
    main()
