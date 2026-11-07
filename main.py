import argparse
from enum import Enum

class TokenType(Enum):
    FUNCTION = 0,
    COMMAND = 1,
    COMMENT = 2,
    INCLUDE = 3,
    NOTHING = 4

class Line:
    def __init__(self, line : str, type : TokenType):
        self.line = line
        self.type = type

def ParseCode(code : str) -> list[Line]:
    pass

def InsertPromptInjections(parsedCode : list[Line]) -> str:
    output = parsedCode.copy()

    promptInjectionLinesFile = open("config/ai_prompt_injections.txt", "r")
    promptInjectionLines = promptInjectionLinesFile.read().split("\n")
    promptInjectionLinesFile.close()

    for line in range(len(parsedCode)):
        if line+1 > len(parsedCode)-1:
            break

        if parsedCode[line].type == TokenType.INCLUDE and parsedCode[line+1].type != TokenType.INCLUDE:
            output.insert(line+1, promptInjectionLines[0])

    return output

def main():
    parser = argparse.ArgumentParser(prog="AIProofer", 
                                     description="A pre-processor command line tool that modifies C/C++ source code to make it harder for AI reverse engineering tools to decompile.",
                                    )
    parser.add_argument("-f", "--file", help="File to AI-Proof")
    parser.add_argument("-o", "--output", help="The name of the output file")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            code = f.read()
        parsed_code = ParseCode(code)
        promptInjectedCode = InsertPromptInjections(parsed_code)
            
        with open(args.output if args.output else args.file + "_converted", "w") as f:
            f.write(promptInjectedCode)
    else:
        print("ERROR: INPUT FILE MUST BE DEFINED")
        exit(1)
    
if __name__ == "__main__":
    main()
    