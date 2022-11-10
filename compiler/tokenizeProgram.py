from compiler.getType import getType
from compiler.parseLoops import *


def tokenize(file) -> list:
    types = [getType(x) for x in file]
    StatementsAndTypes = zip(file, types)
    StatementsAndTypes = list(
        filter(lambda x: x[1] != None, StatementsAndTypes))
    return StatementsAndTypes
