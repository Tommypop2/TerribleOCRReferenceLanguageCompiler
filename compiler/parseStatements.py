import json
from compiler import parseLoops
from compiler.getType import getType
typeAliases = {str.__name__: "std::string", int.__name__: "std::int",
               list[str].__name__: "std::vector<std::string>", list[int].__name__: "std::vector<int>"}
initialisedVariables = []
def generateCppAssignment(statement: str):
    val = list(map(lambda x: str(x).strip(), statement.split("=")))
    variableName = val[0]
    variableValue = val[1]
    parsedName = parseStatement((variableName, getType(variableName)))
    parsedValue = parseStatement((variableValue, getType(variableValue)))
    variableType = "auto"
    if(parsedName in initialisedVariables):
        return f"{parsedName} = {parsedValue};"
    if (parsedValue[0] == "[" and parsedValue[len(parsedValue) - 1] == "]"):
        typeOfArray = type([int(x) for x in json.loads(parsedValue)])
        parsedValue = parsedValue.replace("[", "{", 1)
        parsedValue = (parsedValue[::1].replace("]", "}"))[::1]
        variableType = typeAliases[typeOfArray.__name__]
    initialisedVariables.append(parsedName)
    return f"{variableType} {parsedName} = {parsedValue};"

def generateCppLoop(loopStart: tuple[str,str], contents: list[tuple[str,str]], loopEnd):
    if("for" in loopStart[1]):
        loopCondition = loopStart[0]
        val = loopCondition.split("TO")
        limit = val[1].strip()
        parsedLimit = parseStatement((limit, getType(limit)))
        assignment = val[0].split("FOR")[1].strip()
        parsedAssignment = parseStatement((assignment, getType(assignment)))
        variableName = parsedAssignment.split("auto")[1].split("=")[0].strip()
        return f"for({parsedAssignment} {variableName}<{limit}; {variableName}++){{{contents}}}"

        
        

    return ""
def parseStatement(statement: tuple[str, str]):
    statType = statement[1]
    if (statType == "assignment"):
        return generateCppAssignment(statement[0])
    return str(statement[0])



def parseStatements(tokenizedFile: list[tuple[str, str]]):
    cppCode = ""
    print(tokenizedFile)
    mostRecentEndIndex = None
    for i, item in enumerate(tokenizedFile):
        if(mostRecentEndIndex != None and i <= mostRecentEndIndex):
            continue
        elif ("LoopStart" in item[1]):
            loopEndIndex = i + parseLoops.parseLoop(tokenizedFile[i:])
            mostRecentEndIndex = loopEndIndex
            cppCode += generateCppLoop(tokenizedFile[i], parseStatements(tokenizedFile[i+1:loopEndIndex]), tokenizedFile[loopEndIndex])
        else:
            cppCode += parseStatement(item)
    return cppCode
