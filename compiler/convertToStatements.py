from compiler.helpers import getIndexes


def getStatementStartingIndex(index: int, indexes: list[tuple]) -> int:
    for i in range(len(indexes)):
        element = indexes[i]
        if (element[0] == index):
            return i
    return -1


def convertIfsToStatements(contents: list):
    ifIndexes = getIndexes("IF", contents)
    endIfIndexes = getIndexes("END IF", contents)
    indexes = list(zip(ifIndexes, endIfIndexes))
    ifStatements: list[str] = []
    for i in indexes:
        ifStatement = ""
        for i in range(i[0], i[1] + 1):
            ifStatement += contents[i]
        ifStatements.append(ifStatement)
    indexesToNotInclude = []
    for i in indexes:
        for n in range(i[0], i[1] + 1):
            indexesToNotInclude.append(n)

    statements = []
    for i in range(len(contents)):
        if (i not in indexesToNotInclude):
            statements.append(contents[i])
        else:
            ifstatementindex = getStatementStartingIndex(i, indexes)
            if (ifstatementindex != -1):
                statements.append(tokenizeContents(
                    ifStatements[ifstatementindex]))
    return statements


def convertWhilesToStatements(contents: list):
    whileIndexes = getIndexes("WHILE", contents)
    endWhileIndexes = getIndexes("END WHILE", contents)
    indexes = list(zip(whileIndexes, endWhileIndexes))
    whileLoops = []
    for i in indexes:
        whileLoop = ""
        for i in range(i[0], i[1] + 1):
            whileLoop += contents[i]
        whileLoops.append(whileLoop)
    indexesToNotInclude = []
    for i in indexes:
        for n in range(i[0], i[1] + 1):
            indexesToNotInclude.append(n)
    statements = []
    for i in range(len(contents)):
        if (i not in indexesToNotInclude):
            statements.append(contents[i])
        else:
            whileLoopIndex = getStatementStartingIndex(i, indexes)
            if (whileLoopIndex != -1):
                statements.append(tokenizeContents(whileLoops[whileLoopIndex]))
    return statements


def convertForsToStatements(contents: list):
    forIndexes = getIndexes("FOR", contents)
    endForIndexes = getIndexes("NEXT", contents)
    indexes = list(zip(forIndexes, endForIndexes))
    forLoops = []
    for i in indexes:
        forLoop = ""
        for i in range(i[0], i[1] + 1):
            forLoop += contents[i]
        forLoops.append(forLoop)
    indexesToNotInclude = []
    for i in indexes:
        for n in range(i[0], i[1] + 1):
            indexesToNotInclude.append(n)
    statements = []
    for i in range(len(contents)):
        if (i not in indexesToNotInclude):
            statements.append(contents[i])
        else:
            forLoopIndex = getStatementStartingIndex(i, indexes)
            if (forLoopIndex != -1):
                statements.append(tokenizeContents(forLoops[forLoopIndex]))
    return statements


def tokenizeContents(loop: str):
    loopContents = list(map(lambda x: x.strip(), list(
        filter(lambda x: x != "", loop.split("\n")))))
    return loopContents

def convertEverythingToStatements(statements: list):
    newStatements = []
    for i in statements:
        if(isinstance(i, str)):
            newStatements.append([i])
        else:
            newStatements.append(i)
    return newStatements
def convertToStatements(contents: list[str]):
    statements = convertIfsToStatements(contents)
    statements = convertWhilesToStatements(statements)
    statements = convertForsToStatements(statements)
    statements = convertEverythingToStatements(statements)
    print(statements)
    return statements
