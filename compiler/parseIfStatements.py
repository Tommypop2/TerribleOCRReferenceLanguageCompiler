def getIfIndexes(StatementsAndTypes) -> tuple:
    ifOpeners = []
    ifClosures = []
    for i, item in enumerate(StatementsAndTypes):
        if ("StatementStart" in str(item[1])):
            ifOpeners.append(i)
        elif ("StatementEnd" in str(item[1])):
            ifClosures.append(i)
        if (len(ifOpeners) == len(ifClosures) and len(ifOpeners) > 0):
            return (ifOpeners, ifClosures)
    return ()


def parseIfStatement(data):
    return max(getIfIndexes(data)[1])
