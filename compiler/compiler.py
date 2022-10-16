from compiler.convertToStatements import convertToStatements
import compiler.parse as parse
from compiler.helpers import getIndexes
boilerPlate = """
#include <iostream>
#include <time.h>
#include <string>
#include <vector>
std::string getInput(std::string prompt)
{
    std::cout << prompt;
    std::string data = "";
    std::getline(std::cin, data);
    return data;
}
int len(std::vector<int> lst)
{
    return lst.size();
}
void extraFunctionDeclarations(){}
int main()
{
    std::srand(time(0));
"actualCode";
}
"""


def getContents(fileName):
    with open(fileName, "r") as f:
        contents = f.readlines()
    return contents


def getFunctions(contents: list[str]):
    functions = list(zip(getIndexes("FUNCTION", contents),
                         getIndexes("END FUNCTION", contents)))
    functionsList = []
    for i in functions:
        functionsList.append(contents[i[0]:i[1] + 1])
    indexesToRemove = []
    for i in functions:
        for n in range(i[0], i[1] + 1):
            indexesToRemove.append(n)
    for i in sorted(indexesToRemove, reverse=True):
        del contents[i]

    return contents, functionsList


def convertFunctions(functions: list[list[str]]):
    convertedString = ""

    for i in functions:
        convertedString += parse.parseStatement(i)
    return convertedString


def main(filePath):
    contents = getContents(filePath)
    contents, functions = getFunctions(contents)
    convertedFunctions = convertFunctions(functions)
    statements = convertToStatements(contents)
    cppCode = parse.parse(statements)
    # with open("compiler/boilerplate.cpp", "r") as f:
    #     boilerPlate = f.read()
    with open("main.cpp", "w") as f:
        stuffToWrite = boilerPlate.replace('"actualCode";', cppCode).replace(
            "void extraFunctionDeclarations(){}", convertedFunctions)
        f.write(stuffToWrite)


# if (__name__ == "__main__"):
#     main(filePath="")
