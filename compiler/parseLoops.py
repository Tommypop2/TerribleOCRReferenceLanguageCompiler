def getLoopIndexes(StatementsAndTypes) -> tuple:
    loopOpeners = []
    loopClosures = []
    for i, item in enumerate(StatementsAndTypes):
        if ("LoopStart" in str(item[1])):
            loopOpeners.append(i)
        elif ("LoopEnd" in str(item[1])):
            loopClosures.append(i)
        if (len(loopOpeners) == len(loopClosures) and len(loopOpeners) > 0):
            return (loopOpeners, loopClosures)
    return ()
def getAllLoopIndexes(StatementsAndTypes: list) -> list[tuple[int]]:
    startingIndex = 0
    loops = []
    while True:
        parsedLoopIndexes = getLoopIndexes(StatementsAndTypes[startingIndex:])
        if(len(parsedLoopIndexes) == 0):
            break
        res = parsedLoopIndexes[1]
        startingIndex = max(res)
        loops.append(parsedLoopIndexes)
    return loops
def parseLoop(loop):
    return max(getLoopIndexes(loop)[1])
    
# def parseAllLoops(StatementsAndTypes: list[tuple[str]]):
#     loopIndexes = getAllLoopIndexes(StatementsAndTypes)
#     for i in loopIndexes:
#         startOfLoop = min(i)[0]
#         endOfLoop = max(i)[0]
#         loop = StatementsAndTypes[startOfLoop:endOfLoop]
#         yield loop