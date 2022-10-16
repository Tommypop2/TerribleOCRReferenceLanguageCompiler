def getIndexes(string: str, contents: list):
    indexes = []
    for i in range(len(contents)):
        if (string in contents[i]):
            if (string.__contains__("END") == False):
                if ("END" not in contents[i]):
                    indexes.append(i)
            else:
                indexes.append(i)
    return indexes
