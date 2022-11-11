from compiler.getType import getType
from compiler.parseStatements import parseStatements, parseStatement

from compiler.tokenizeProgram import tokenize
template = """
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
auto sum(int n1, int n2) { return (n1 + n2); }
"functions";
int main()
{
    std::srand(time(0));
    "actualCode";
}
"""


def generateFunctionCpp(functions: list[list[tuple[str, str]]]):
    cppCode = ""
    for i in functions:
        functionName = i[0][0].split("FUNCTION ")[1].split("(")[0].strip()
        functionArguments = i[0][0].split("(")[1].split(")")[0].split(",")
        functionArguments = list(map(lambda x: x.strip(), functionArguments))
        parsedArguments = ""
        if (functionArguments != [""]):
            for n, item in enumerate(functionArguments):
                parsedArguments += "int " + parseStatement((item, getType(item))) + (
                    "," if n < len(functionArguments) - 1 else "")
        parsedContents = parseStatements(i[1:-1])
        cppCode += f"auto {functionName}({parsedArguments}){{{parsedContents}}}"
    return cppCode


def getFunctions(arr: list):
    functionStartIndexes = []
    functionEndIndexes = []
    for i, item in enumerate(arr):
        if (item[1] == "functionStart"):
            functionStartIndexes.append(i)
        elif (item[1] == "functionEnd"):
            functionEndIndexes.append(i)
    functions = list(zip(functionStartIndexes, functionEndIndexes))
    functionsA = []
    for i in functions:
        functionsA.append(arr[i[0]:i[1] + 1])
    for i in reversed(functions):
        for n in range(i[1], i[0] - 1, -1):
            arr.pop(n)

    return arr, functionsA


def compile(fileName):
    with open(fileName, "r") as f:
        file = f.readlines()
    file = list(map(lambda x: str(x).strip(), file))
    file = list(filter(lambda x: x != "", file))
    file = list(map(lambda x: x.split("//")[0], file))
    print(file)
    tokenizedFile = tokenize(file)
    tokenizedFile, functions = getFunctions(tokenizedFile)
    with open("main.cpp", "w") as f:
        codeToWrite = template.replace(
            '"actualCode";', parseStatements(tokenizedFile)).replace('"functions";', generateFunctionCpp(functions))
        f.write(codeToWrite)
