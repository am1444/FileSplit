# Program to split file into seperate files

import argparse # for command-line parsing
import os # to make directories and to read their contents
import sys # for access to stderr

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

versionString = "FileSplit v0.2.4"

parser = argparse.ArgumentParser("Split files into subfiles.")

parser.add_argument('-c', '--count', help=f"How many files the file should be split into.", default=argparse.SUPPRESS, type=int)
parser.add_argument('-g', '--glue', help="'Glue' subfiles back into their original file.", action=argparse.BooleanOptionalAction)
parser.add_argument('-o', '--out', help="Where to store output of --glue'd files. Default=FileSplit.out.", nargs='?', default="FileSplit.out")
parser.add_argument('-i', '--input', help="Input file/dir to split/glue. Defaults to PWD.", type=str, default=".")
parser.add_argument('-s', '--maxsize', help=f"How large each output file can get in bytes.", default=argparse.SUPPRESS, type=int)
parser.add_argument('-v', '--version', help="Print version information and exit.", action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if args.version: # print version and exit with -v/--version flag
    print(versionString)
    exit()

if os.path.exists(os.path.abspath(args.input)):
    if not(args.glue): # if we're splitting the input apart
        try:
            with open(os.path.abspath(args.input), 'rb') as file:
                inputArray = file.read()
        except TypeError:
            eprint("FileSplit: fatal error: no input files detected")
            exit(1)
        except IsADirectoryError:
            eprint("FileSplit: fatal error: attempted to split a directory")
            exit(1)
    else: # if were glueing subfiles back together
        if not(os.path.isdir(os.path.abspath(args.input))): # make sure it's a directory
            eprint("FileSplit: fatal error: attempted to glue with input of a file instead of a directory containing subfiles.")
            exit(1)

directorySeparator = '/' if os.name == 'posix' else '\\'

if args.glue: # string subfiles within input directory back together
    inputDirectory = os.path.abspath(args.input)
    fileContents = bytearray()
    for fileName in [i for i in sorted(os.listdir(inputDirectory), key=lambda x: int(x.split('_')[-1:][0])) if i[0]!='.']:
        with open(f"{inputDirectory}{directorySeparator}{fileName}", "rb") as file:
            print(f"Reading {fileName}")
            fileContents.extend(bytearray(file.read()))
    with open(args.out, "wb") as outFile:
        outFile.write(fileContents)

else: # split files apart
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
            if specifiedOutputSize < inputSize:
                lastFileSize = inputSize % specifiedOutputSize
                eprint(f"lastFileSize: {lastFileSize}")
                normalFileCount = int((inputSize - lastFileSize) / ((inputSize-lastFileSize)/specifiedOutputSize))
                eprint(f"normalFileCount: {normalFileCount}")
                return (normalFileCount, specifiedOutputSize, lastFileSize)
            else:
                eprint("File is smaller than specified output size, not modifying")
                return (0,0,0)
    
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
    if normalFileSize > 0:
        outputFilesContents = [inputArray[i:i+normalFileSize] for i in range(0, len(inputArray) - len(inputArray) % normalFileSize, normalFileSize)] + [inputArray[-lastFileSize:]]
    else:
        outputFilesContents = [inputArray]
    
    if args.out:
        outputDirName = os.path.basename(os.path.abspath(args.out))
    else:
        outputDirName = os.path.basename(os.path.abspath(".".join(args.input.split(".")[:-1])+"_split")) # removes file extensions
    
    print("creating DIR:", outputDirName)
    os.makedirs(outputDirName, exist_ok=True)
    
    for index, fileContents in enumerate(outputFilesContents):
        currentOutputFilePath = os.path.abspath(f"{outputDirName}{directorySeparator}{outputDirName}_{index+1}")
        with open(currentOutputFilePath,"wb") as currentOutputFile:
            currentOutputFile.write(fileContents)
    eprint("FileSplit done")
