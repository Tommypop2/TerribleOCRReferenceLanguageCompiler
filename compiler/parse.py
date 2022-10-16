import json
initialisedVariables = []
typeAliases = {str.__name__: "std::string", int.__name__: "std::int",
               list[str].__name__: "std::vector<std::string>", list[int].__name__: "std::vector<int>"}


def generateCPPAssignment(statement: list):
    val = list(map(lambda x: x.strip(), statement[0].split("=")))
    variableName = val[0]
    variableValue = val[1]
    parsedName = parseStatement([variableName])
    parsedValue = parseStatement([variableValue])
    variableType = "auto"

    if (parsedName in initialisedVariables):
        return f"{parsedName} = {parsedValue};"
    if (parsedValue[0] == "[" and parsedValue[len(parsedValue) - 1] == "]"):
        typeOfArray = type([int(x) for x in json.loads(parsedValue)])
        parsedValue = parsedValue.replace("[", "{", 1)
        parsedValue = (parsedValue[::1].replace("]", "}"))[::1]
        variableType = typeAliases[typeOfArray.__name__]
    initialisedVariables.append(parsedName)
    return f"{variableType} {parsedName} = {parsedValue};"


def generateCPPFunctionCall(statement: list):
    functionName = statement[0].split("(")[0].strip()
    functionArgument = ""
    temp = statement[0].replace(functionName, "")
    for i in range(len(temp)):
        if (i != 0 and i != len(temp) - 1):
            functionArgument += temp[i]
    functionArgument = parseStatement([functionArgument]).strip()
    if (functionName == "print"):
        return f"std::cout << {functionArgument} << '\\n';"
    elif (functionName == "input"):
        return f"getInput({functionArgument})"
    elif (functionName == "random"):
        start = float(str(functionArgument).split(",")[0])
        end = float(str(functionArgument).split(",")[1])
        offset = start
        numRange = round(end - start)
        return f"""
        ({offset} + (rand() % {numRange}))
        """
    elif (functionName == "return"):
        return f"return{functionArgument};"
    return ""


def generateCPPIfStatement(statement: list[str]):
    condition = statement[0].split("IF")[1].split("THEN")[0].strip()
    parsedCondition = parseStatement([condition])
    contents = statement[1:len(statement) - 1]
    parsedContentsString = ""
    if ("END" in contents[len(contents) - 1] or "NEXT" in contents[len(contents) - 1]):
        # Find start of loop
        indexOfLoop = 0
        for i in range(len(contents)):
            element = contents[i]
            if ("FOR" in element or "WHILE" in element or "IF" in element):
                indexOfLoop = i
        # Parse anything before loop
        for i, elem in enumerate(contents[0:indexOfLoop]):
            parsedContentsString += elem
        # Parse loop itself
        parsedContentsString = parseStatement(contents[indexOfLoop:])
    else:
        parsedContents = list(map(lambda x: parseStatement([x]), contents))
        for i in parsedContents:
            parsedContentsString += i
        parsedContentsString = parseStatement(contents)
    return f'if ({parsedCondition})' + "{" + f"{parsedContentsString}" + "}"


def generateCPPWhileLoop(statement: list[str]) -> str:
    condition = statement[0].split("WHILE")[1].strip()
    parsedCondition = parseStatement([condition])
    contents = statement[1:len(statement) - 1]
    parsedContents = list(map(lambda x: parseStatement([x]), contents))
    parsedContentsString = ""
    if ("END" in contents[len(contents) - 1] or "NEXT" in contents[len(contents) - 1]):
        # Find start of loop
        indexOfLoop = 0
        for i in range(len(contents)):
            element = contents[i]
            if ("FOR" in element or "WHILE" in element or "IF" in element):
                indexOfLoop = i
        # Parse anything before loop
        for i, elem in enumerate(contents[0:indexOfLoop]):
            parsedContentsString += elem
        # Parse loop itself
        parsedContentsString = parseStatement(contents[indexOfLoop:])
    else:
        parsedContents = list(map(lambda x: parseStatement([x]), contents))
        for i in parsedContents:
            parsedContentsString += i
    return f"while({parsedCondition})" + "{" + parsedContentsString + "}"


def generateCPPComparison(statement: list):
    operators = [">", "<", "==", "!="]
    operator = ""
    for i in operators:
        if (len(statement[0].split(i)) > 1):
            operator = i
    lst = list(map(lambda x: x.strip(), statement[0].split(operator)))

    x = parseStatement([lst[0]])
    y = parseStatement([lst[1]])

    return f"{x} {operator} {y}"


def generateCPPForLoop(statement: list[str]):
    variableAssignment = statement[0].split("FOR")[1].split("TO")[0].strip()
    parsedVariableAssignment = parseStatement([variableAssignment])
    assignedVariableName = variableAssignment.split("=")[0].strip()
    limit = statement[0].split("TO")[1].strip()
    parsedLimit = parseStatement([limit])
    variableToIncrement = statement[len(
        statement) - 1].split("NEXT")[1].strip()
    parsedVariableToIncrement = parseStatement([variableToIncrement])
    contents = statement[1:len(statement) - 1]
    parsedContents = list(map(lambda x: parseStatement([x]), contents))
    parsedContentsString = ""
    if ("END" in contents[len(contents) - 1] or "NEXT" in contents[len(contents) - 1]):
        # Find start of loop
        indexOfLoop = 0
        for i in range(len(contents)):
            element = contents[i]
            if ("FOR" in element or "WHILE" in element or "IF" in element):
                indexOfLoop = i
        # Parse anything before loop
        for i, elem in enumerate(contents[0:indexOfLoop]):
            parsedContentsString += elem
        # Parse loop itself
        parsedContentsString = parseStatement(contents[indexOfLoop:])
    else:
        parsedContents = list(map(lambda x: parseStatement([x]), contents))
        for i in parsedContents:
            parsedContentsString += i
    return f"for({parsedVariableAssignment} {assignedVariableName} < {parsedLimit}; {parsedVariableToIncrement}++)" + "{" + parsedContentsString + "}"


def generateCPPFunction(statement: list[str]):
    functionName = statement[0].split("FUNCTION")[1].split("(")[0].strip()
    functionParameters = list(
        map(lambda x: x.strip(), statement[0].split("(")[1].split(")")[0].split(",")))
    functionParametersString = ""
    for i in range(len(functionParameters)):
        if (i < (len(functionParameters) - 1)):
            functionParametersString += f"int {functionParameters[i]},"
        else:
            functionParametersString += f"int {functionParameters[i]}"
    functionContents = statement[1: len(statement) - 1]
    parsedContents = list(
        map(lambda x: parseStatement([x]).strip(), functionContents))
    parsedContentsString = ""
    for i in parsedContents:
        parsedContentsString += i
    return f"auto {functionName}({functionParametersString})" + "{" + f"{parsedContentsString}" + "}"


def parseStatement(statement: list) -> str:
    # if (len(statement) > 1 and statement[0] == '"' and statement[len(statement) - 1] == '"'):
    #     return statement
    if (len(statement) < 1):
        return ""
    if ("FUNCTION" in statement[0] and "END FUNCTION" in statement[len(statement) - 1]):
        return generateCPPFunction(statement)
    if ("IF" in statement[0] and "THEN" in statement[0]):
        return generateCPPIfStatement(statement)
    if ("WHILE" in statement[0] and "END WHILE" in statement[len(statement) - 1]):
        return generateCPPWhileLoop(statement)
    if ("FOR" in statement[0] and "NEXT" in statement[len(statement) - 1]):
        return generateCPPForLoop(statement)
    if (statement[0].__contains__("=") and "==" not in statement[0]):
        return generateCPPAssignment(statement)
    if (">" in statement[0] or "<" in statement[0] or "==" in statement[0] or "!=" in statement[0]):
        return generateCPPComparison(statement)
    if (statement[0].__contains__("print") or "random" in statement[0] or "input" in statement[0] or "return" in statement[0]):
        return generateCPPFunctionCall(statement)
    if (statement[0] == "break"):
        return "break;"
    return str(statement[0])


def parse(contents: list):
    cppCode = ""
    for i in range(len(contents)):
        statement = contents[i]
        cppCode += "\t" + parseStatement(statement) + "\n"

    return cppCode
