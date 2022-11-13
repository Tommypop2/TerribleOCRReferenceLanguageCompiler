import json


typeAliases = {str.__name__: "std::string", int.__name__: "std::int",
               "list: string": "std::vector<std::string>", "list: int": "std::vector<int>"}

def getCppType(parsedValue: str):
    variableType = "auto"
    if (parsedValue[0] == "[" and parsedValue[len(parsedValue) - 1] == "]"):
        typeOfArray = type(json.loads(parsedValue)[0])
        if (typeOfArray == str):
            typeOfArray = "list: string"
        if (typeOfArray == int):
            typeOfArray = "list: int"
        parsedValue = parsedValue.replace("[", "{", 1)
        parsedValue = (parsedValue[::1].replace("]", "}"))[::1]
        variableType = typeAliases[typeOfArray]
    return variableType