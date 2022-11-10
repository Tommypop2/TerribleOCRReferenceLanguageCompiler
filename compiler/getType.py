def getType(statement):
    if("NEXT " in statement):
        return "forLoopEnd"
    if("END WHILE" in statement):
        return "whileLoopEnd"
    if("FOR " in statement):
        return "forLoopStart"
    if("WHILE " in statement):
        return "whileLoopStart"
    if("FUNCTION " in statement):
        return "functionStart"
    if("END FUNCTION" in statement):
        return "functionEnd"
    if("=" in statement):
        return "assignment"
    return "misc"