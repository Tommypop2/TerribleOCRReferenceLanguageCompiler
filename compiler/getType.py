conditions = [">", "<", "==", "!=", ">=", "<="]
keywords = ["break","return"]


def isComparison(statement):
    for i in conditions:
        if (i in statement):
            return True
    return False


def isKeyWord(statement):
    for i in keywords:
        if (i in statement):
            return True
    return False


def getType(statement):
    if ("IF " in statement):
        return "ifStatementStart"
    if ("END IF" in statement):
        return "ifStatementEnd"
    if ("NEXT " in statement):
        return "forLoopEnd"
    if ("END WHILE" in statement):
        return "whileLoopEnd"
    if ("FOR " in statement):
        return "forLoopStart"
    if ("WHILE " in statement):
        return "whileLoopStart"
    if ("FUNCTION " in statement):
        return "functionStart"
    if ("END FUNCTION" in statement):
        return "functionEnd"
    if("END CPPCode" in statement):
        return "cppStatementEnd"
    if("CPPCode" in statement):
        return "cppStatementStart"
    if (isComparison(statement)):
        return "comparison"
    if (isKeyWord(statement)):
        return "keyword"
    if ("=" in statement):
        return "assignment"
    if ("(" in statement and ")" in statement):
        return "functionCall"
    return "misc"
