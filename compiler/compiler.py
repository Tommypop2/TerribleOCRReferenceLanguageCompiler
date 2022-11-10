from compiler.parseStatements import parseStatements
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
int main()
{
    std::srand(time(0));
    "actualCode";
}
"""


def compile(fileName):
    with open(fileName, "r") as f:
        file = f.readlines()
    file = list(map(lambda x: str(x).strip(), file))
    file = list(filter(lambda x: x != "", file))
    tokenizedFile = tokenize(file)
    with open("main.cpp", "w") as f:
        codeToWrite = template.replace(
            '"actualCode";', parseStatements(tokenizedFile))
        f.write(codeToWrite)
