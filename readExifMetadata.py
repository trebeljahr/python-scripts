#! /home/rico/Apps/anaconda3/envs/image-editing/bin/python

import sys
import os
import datetime
import exifread


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

    existingDates = {}
    for name in os.listdir(copyIntoPath):
        listExif(name, copyIntoPath, existingDates)
    for name in os.listdir(path):
        listExif(name, path, existingDates)
    print(existingDates)


def listExif(name, path, existingDates):
    _, extension = os.path.splitext(os.path.join(path, name))
    if len(sys.argv) < 4:
        print("Please specify the extension as a second input argument")
    extensionToChange = sys.argv[3]
    if extensionToChange == extension:
        imgPath = os.path.join(path, name)
        f = open(imgPath, 'rb')
        tags = exifread.process_file(f)
        # print(name)
        # print(tags["Image DateTime"])
        strDate = str(tags["Image DateTime"])
        if strDate not in existingDates:
            existingDates[strDate] = name
        else:
            print("There seems to be a duplicate between {} and {}".format(
                existingDates[strDate], name))
        # with Raw(filename=imgPath) as raw:
        #     print(raw.metadata)


def convertToDate(strDate):
    return datetime.datetime.strptime(strDate, "%Y:%m:%d %H:%M:%S")


if __name__ == "__main__":
    main()
