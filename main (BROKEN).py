import argparse
import random
from enum import Enum
from pycparser import c_ast, parse_file
from importlib.resources import files

class TokenType(Enum):
    COMMAND = 1
    INCLUDE = 3
    NOTHING = 4

class VariableTypes(Enum):
    SHORT = 0
    INT = 1
    CHAR = 2
    FLOAT = 3
    DOUBLE = 4

class Line:
    def __init__(self, line : str, type : TokenType):
        self.line = line
        self.type = type

class Variable:
    def __init__(self, name: str, varType : VariableTypes, lineDef: int):
        self.name = name
        self.type = varType
        self.lineDef = lineDef

class FuncFinder(c_ast.NodeVisitor):
    def __init__(self, targetFunctionName: str):
        self.targetFunctionName = targetFunctionName
        self.targetFunctionNode : c_ast.Node = None
        self.functionCalls : list[c_ast.Node] = []

    def visit_FuncDef(self, node):
        if node.decl.name == self.targetFunctionName:
            self.targetFunctionNode = node

    def visit_FuncCall(self, node: c_ast.FuncCall) -> None:
        if isinstance(node.name, c_ast.ID) and node.name.name == self.targetFunctionName:
            self.functionCalls.append(node)

        if node.args is not None:
            self.visit(node.args)

def ParseCode(code : str) -> list[Line]:
    lines = code.splitlines()
    output = []

    for line in lines:
        if line.isspace():
            output.append(Line(line, TokenType.NOTHING))
        elif line.startswith("#include"):
            output.append(Line(line, TokenType.INCLUDE))
        else:
            output.append(Line(line, TokenType.COMMAND)) #Catch all as we only need to look specifically for include statements

    return output

def generateUniqueStringName() -> str:
    length = random.randint(10, 20)
    name = ""
    for i in range(length):
        name += random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
        name += random.choice("1234567890")

    return name

def InsertPromptInjections(file : str, parsedCode : list[Line], targetFunction : str) -> str:

    fake_libc_path = files('pycparser').joinpath('utils/fake_libc_include')
    ast = parse_file(file, use_cpp=True,
        cpp_path='gcc',
        cpp_args=['-E', r'-I{}'.format(fake_libc_path)])

    functionFinder = FuncFinder(targetFunction)
    functionFinder.visit(ast)

    defLineNumber = int(str(functionFinder.targetFunctionNode.coord).split(":")[1])+1

    print(parsedCode[defLineNumber])

    callLineNumbers = []
    for i in functionFinder.functionCalls:
        callLineNumbers.append(int(str(i.coord).split(":")[1])+1)

    newFunctionName = generateUniqueStringName()

    parsedCode[defLineNumber].line.replace(targetFunction + "(", newFunctionName + "(")


    for callLine in range(len(callLineNumbers)):
        parsedCode[callLineNumbers[callLine]].replace(targetFunction + "(", newFunctionName + "(")

    for line in parsedCode:
        print(line.line)

    
    #output_lines = [item.line for item in parsedCode]
#
    #try:
    #    with open("config/promptInjections/basic.c", "r") as f:
    #        promptInjectionLines = f.read()
    #except FileNotFoundError:
    #    print("PROMPT INJECTION CONFIG FILE NOT FOUND, ABORTING!!!")
    #    exit(1)
#
    #injection_text = promptInjectionLines.replace("[[NAME]]", generateUniqueStringName())
#
    #targetFunctionName, targetFunctionLine = targetFunction.split(":")
#
    #if targetFunctionName in parsedCode[int(targetFunctionLine)-1].line:
    #    functionDefinition = parsedCode[int(targetFunctionLine)-1].line
#
#
    #    if functionDefinition.endswith("{"):
    #        output_lines.insert(int(targetFunctionLine), injection_text)
    #    else:
    #        output_lines.insert(int(targetFunctionLine)+1, injection_text)
    
    #i = 0
    #while i < len(parsedCode):
    #    if parsedCode[i].type == TokenType.INCLUDE:
    #        if i + 1 < len(parsedCode) and parsedCode[i+1].type != TokenType.INCLUDE:
    #            injection_str = f'const char fdgkljgjgfj[{len(injection_text)}] = "{injection_text}";'
    #            output_lines.insert(i + 1, injection_str)
    #            i += 1
    #    i += 1

    #return "\n".join(output_lines)

def main():
    parser = argparse.ArgumentParser(prog="AIProofer", 
                                     description="A pre-processor command line tool that modifies C/C++ source code to make it harder for AI reverse engineering tools to decompile.",
                                    )
    parser.add_argument("-f", "--file", help="File to AI-Proof")
    parser.add_argument("-o", "--output", help="The name of the output file")
    parser.add_argument("-func", "--function", help="The name of the function to target for prompt injection (format is [name]:definitionLine)")
    args = parser.parse_args()

    if args.file and args.function:
        with open(args.file, "r") as f:
            code = f.read()
        parsed_code = ParseCode(code)
        promptInjectedCode = InsertPromptInjections(args.file, parsed_code, args.function)

        if args.output:
            with open(args.output, "w") as f:
                f.write(promptInjectedCode)
        else:
            newFileNameParts : list[str] = args.file.split(".")
            newFileNameParts[-2] += "_converted" # not 0 because we need to account for potential multiple "."s, this just ensures that were at the file part of the file before the extension

            fileName = ""
            for i in range(len(newFileNameParts)):
                fileName += newFileNameParts[i] + ("." if i < len(newFileNameParts)-1 else "")

            with open(fileName, "w") as f:
                f.write(promptInjectedCode)

    else:
        print("ERROR: INPUT FILE AND FUNCTION MUST BE DEFINED")
        exit(1)
    
if __name__ == "__main__":
    main()
    