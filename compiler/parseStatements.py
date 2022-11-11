import json
from compiler import parseLoops
from compiler.getType import getType
from compiler import parseIfStatements
typeAliases = {str.__name__: "std::string", int.__name__: "std::int",
               "list: string": "std::vector<std::string>", "list: int": "std::vector<int>"}
initialisedVariables = []
conditions = [">", "<", "==", "!=", ">=", "<="]


def generateCppAssignment(statement: str):
    val = list(map(lambda x: str(x).strip(), statement.split("=")))
    variableName = val[0]
    variableValue = val[1]
    parsedName = parseStatement((variableName, getType(variableName)))
    parsedValue = parseStatement((variableValue, getType(variableValue)))
    variableType = "auto"
    if (parsedName in initialisedVariables):
        return f"{parsedName} = {parsedValue};"
    if (parsedValue[0] == "[" and parsedValue[len(parsedValue) - 1] == "]"):
        typeOfArray = type(json.loads(parsedValue)[0])
        if (typeOfArray == str):
            typeOfArray = "list: string"
        if (typeOfArray == int):
            typeOfArray = "list: int"
        parsedValue = parsedValue.replace("[", "{", 1)
        parsedValue = (parsedValue[::1].replace("]", "}"))[::1]
        variableType = typeAliases[typeOfArray]
    if ("[" in parsedName and "]" in parsedName):
        variableType = ""
    initialisedVariables.append(parsedName)
    return f"{variableType} {parsedName} = {parsedValue};"


def generateCppForLoop(loopStart: tuple[str, str], contents: list[tuple[str, str]]):
    loopCondition = loopStart[0]
    val = loopCondition.split("TO")
    limit = val[1].strip()
    parsedLimit = parseStatement((limit, getType(limit)))
    assignment = val[0].split("FOR")[1].strip()
    parsedAssignment = parseStatement((assignment, getType(assignment)))
    print(parsedAssignment)
    variableName = parsedAssignment.split("auto")[1].split("=")[0].strip()
    semiColon = "" if ";" in parsedLimit else ";"
    return f"for({parsedAssignment} {variableName}<{parsedLimit}{semiColon} {variableName}++){{{contents}}}"


def generateCppWhileLoop(loopStart: str, contents):
    condition = loopStart[0].split("WHILE")[1].strip()
    parsedCondition = parseStatement((condition, "condition"))
    return f"while({parsedCondition}) {{{contents}}}"


def generateCppComparison(condition: str):
    operator: str = ""
    for i, item in enumerate(conditions):
        if (item in condition):
            operator = item
    val = condition.split(operator)
    val = list(map(lambda x: x.strip(), val))
    x = parseStatement((val[0], getType(val[0])))
    y = parseStatement((val[1], getType(val[1])))
    return f"{x} {operator} {y}"


def generateCppIfStatement(statementStart: str, contents):
    condition = statementStart[0].split("IF")[1].strip()
    parsedCondition = parseStatement((condition, "comparison"))
    # print(f"{statementStart}, {contents}")
    return f"if({parsedCondition}) {{{contents}}}"


def generateCppLoop(loopStart, contents):
    if ("for" in loopStart[1]):
        return generateCppForLoop(loopStart, contents)
    if ("while" in loopStart[1]):
        return generateCppWhileLoop(loopStart, contents)
    if ("if" in loopStart[1]):
        return generateCppIfStatement(loopStart, contents)
    return ""


def generateCppFunctionCall(statement: str):
    print(statement)
    if (statement.split("(")[0].strip() == "print"):
        argument = statement.replace("print(", "")[0:-1]
        parsedArgument = parseStatement((argument, getType(argument)))
        return f"std::cout << {parsedArgument} << '\\n';"
    return statement  # Bad solution for now


def generateCppKeyWord(statement: str):
    if ("break" in statement):
        return "break;"
    if ("return" in statement):
        if ("(" in statement and ")" in statement):
            value = statement.split("(")[1].split(")")[0]
            return f"return({value});"
        return "return;"
    return ""


def parseStatement(statement: tuple[str, str]):
    statType = statement[1]
    if (statType == "assignment"):
        return generateCppAssignment(statement[0])
    if (statType == "functionCall"):
        return generateCppFunctionCall(statement[0])
    if (statType == "comparison"):
        return generateCppComparison(statement[0])
    if (statType == "keyword"):
        return generateCppKeyWord(statement[0])
    return str(statement[0])


def parseStatements(tokenizedFile: list[tuple[str, str]]):
    cppCode = ""
    mostRecentEndIndex = None
    for i, item in enumerate(tokenizedFile):
        if (mostRecentEndIndex != None and i <= mostRecentEndIndex):
            continue
        elif ("LoopStart" in item[1]):
            loopEndIndex = i + parseLoops.parseLoop(tokenizedFile[i:])
            mostRecentEndIndex = loopEndIndex
            cppCode += generateCppLoop(
                tokenizedFile[i], parseStatements(tokenizedFile[i+1:loopEndIndex]))
        elif ("ifStatementStart" in item[1]):
            statementEndIndex = i + \
                parseIfStatements.parseIfStatement(tokenizedFile[i:])
            mostRecentEndIndex = statementEndIndex
            cppCode += generateCppLoop(tokenizedFile[i], parseStatements(
                tokenizedFile[i+1:statementEndIndex]))
        else:
            cppCode += parseStatement(item)
    return cppCode
