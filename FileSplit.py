# Program to split file into seperate files

import argparse # for command-line parsing
import os # to make directories and to read their contents
import sys # for access to stderr

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

versionString = "FileSplit v0.2"

parser = argparse.ArgumentParser("Split files into subfiles.")

parser.add_argument('-c', '--count', help=f"How many files the file should be split into.", default=argparse.SUPPRESS, type=int)
parser.add_argument('-g', '--glue', help="'Glue' subfiles back into their original file.", action=argparse.BooleanOptionalAction)
parser.add_argument('-o', '--out', help="Where to store output of --glue'd files. Default=FileSplit.out.", nargs='?', default="FileSplit.out")
parser.add_argument('-i', '--input', help="Input file to split.", type=str)
parser.add_argument('-s', '--maxsize', help=f"How large each output file can get in bytes.", default=argparse.SUPPRESS, type=int)
parser.add_argument('-v', '--version', help="Print version information and exit.", action=argparse.BooleanOptionalAction)


args = parser.parse_args()

if args.version: # print version and exit with -v/--version flag
    print(versionString)
    exit()


if args.glue: # sew subfiles within current working directory back together
    fileContents = bytearray()
    for fileName in sorted(os.listdir('.'), key=lambda x: int(x.split('_')[-1:][0])):
        with open(fileName, "rb") as file:
            print(f"Reading {fileName}")
            fileContents.extend(bytearray(file.read()))
    with open(args.out, "wb") as outFile:
        outFile.write(fileContents)
else: # split files apart

    try:
        with open(args.input, 'rb') as file:
            inputArray = file.read()
    except TypeError:
        eprint("FileSplit: fatal error: no input files detected")
        exit(1)
    
    def fileSizes(inputSize, specifiedOutputSize, specifiedOutputCount): # returns (normalFileCount, normalFileSize, lastFileSize)
        eprint(f"InputSize: {inputSize}\nspecifiedOutputSize: {specifiedOutputSize}\nspecifiedOutputCount:{specifiedOutputCount}\n")
        if specifiedOutputSize and specifiedOutputCount:
            eprint("FileSplit: fatal error: cannot specify filesize and filecount at the same time")
            exit(1)
        if not(specifiedOutputSize or specifiedOutputCount):
            eprint("FileSplit: fatal error: neither filesize nor filecount specified")
            exit(1)
        if specifiedOutputCount: # count is specified
            normalFileCount = specifiedOutputCount - 1
            eprint(f"normalFileCount: {normalFileCount}")
            lastFileSize = inputSize % specifiedOutputCount
            eprint(f"lastFileSize: {lastFileSize}")
            normalFileSize = int((inputSize - lastFileSize) / normalFileCount)
            eprint(f"normalFileSize: {normalFileSize}")
            return (normalFileCount, normalFileSize, lastFileSize)
        else: # max size is specified
            lastFileSize = inputSize % specifiedOutputSize
            eprint(f"lastFileSize: {lastFileSize}")
            normalFileCount = int((inputSize - lastFileSize) / ((inputSize-lastFileSize)/specifiedOutputSize))
            eprint(f"normalFileCount: {normalFileCount}")
            return (normalFileCount, specifiedOutputSize, lastFileSize)
    
    outputFileCount = 0
    outputFileSize = 0

    try:
        outputFileCount = args.count
    except AttributeError:
        pass

    try:
        outputFileSize = args.maxsize
    except AttributeError:
        pass
    
    (normalFileCount, normalFileSize, lastFileSize) = fileSizes(len(inputArray),outputFileSize,outputFileCount)
    outputFilesContents = [inputArray[i:i+normalFileSize] for i in range(0, len(inputArray) - len(inputArray) % normalFileSize, normalFileSize)] + [inputArray[-lastFileSize:]]

    directorySeparator = '/' if os.name == 'posix' else '\\'
    outputDirName = ".".join(args.input.split(".")[:-1])+"_split" # removes file extensions
    os.mkdir(outputDirName)
    
    for index, fileContents in enumerate(outputFilesContents):
        with open(f"{outputDirName}{directorySeparator}{outputDirName}_{index}","wb") as currentOutputFile:
            currentOutputFile.write(fileContents)
    eprint("FileSplit done")
