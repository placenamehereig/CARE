import argparse
from enum import Enum

class TokenType(Enum):
    FUNCTION = 0
    COMMAND = 1
    COMMENT = 2
    INCLUDE = 3
    NOTHING = 4

class Line:
    def __init__(self, line : str, type : TokenType):
        self.line = line
        self.type = type

def ParseCode(code : str) -> list[Line]:
    pass

def InsertPromptInjections(parsedCode: list[Line]) -> str:
    output_lines = [item.line for item in parsedCode]

    try:
        with open("config/ai_prompt_injections.txt", "r") as f:
            promptInjectionLines = f.read().split("\n")
    except FileNotFoundError:
        promptInjectionLines = [""]

    injection_text = promptInjectionLines[0] if promptInjectionLines else ""

    i = 0
    while i < len(parsedCode):
        if parsedCode[i].type == TokenType.INCLUDE:
            if i + 1 >= len(parsedCode) or parsedCode[i+1].type != TokenType.INCLUDE:
                injection_str = f'const char fdgkljgjgfj[{len(injection_text)}] = "{injection_text}";'
                output_lines.insert(i + 1, injection_str)
                i += 1
        i += 1

    return "\n".join(output_lines)

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
    