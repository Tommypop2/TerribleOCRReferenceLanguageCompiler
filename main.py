from compiler import compiler
import os
import sys


def main():
    fileName = ""
    args = sys.argv
    fileArgs = list(filter(lambda x: ".ocrref" in x, args))
    if (len(fileArgs) < 1):
        fileName = "main.ocrref"
    else:
        fileName = fileArgs[0]
    compiler.main(fileName)
    os.system("g++ main.cpp")
    print("Compilation Successful")
    # os.system("del main.cpp")
    os.system("a.exe")


if __name__ == "__main__":
    main()
