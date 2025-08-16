import sys
from typing import List, Optional, Tuple

BEGINNING = 0
INT = 1
KEYWORD = 2
SEPARATOR = 3
END_OF_TOKENS = 4
OPERATOR = 5
STRING = 6
IDENTIFIER = 7
UNKNOWN = 8
BOOL_LIT = 9
ASSIGN = 10

class Token:
    def __init__(self, type_: int, value: Optional[str] = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        type_names = {
            BEGINNING: "BEGINNING",
            INT: "INT",
            KEYWORD: "KEYWORD",
            SEPARATOR: "SEPARATOR",
            END_OF_TOKENS: "END_OF_TOKENS",
            OPERATOR: "OPERATOR",
            IDENTIFIER: "IDENTIFIER",
            BOOL_LIT: "BOOL_LIT",
            ASSIGN: "ASSIGN",
            UNKNOWN: "UNKNOWN"
        }
        return f"Token(type={type_names.get(self.type, 'UNKNOWN')}, value='{self.value}')"

def print_token(token: Token):
    type_names = {
        BEGINNING: "BEGINNING",
        INT: "INT",
        KEYWORD: "KEYWORD",
        SEPARATOR: "SEPARATOR",
        END_OF_TOKENS: "END_OF_TOKENS",
        OPERATOR: "OPERATOR",
        IDENTIFIER: "IDENTIFIER",
        BOOL_LIT: "BOOL_LIT",
        ASSIGN: "ASSIGN",
        UNKNOWN: "UNKNOWN"
    }
    print(f"TOKEN VALUE: '{token.value if token.value else ''}' TOKEN TYPE: {type_names.get(token.type, 'UNKNOWN')}")

def generate_number(current: str, current_index: int) -> Tuple[Token, int]:
    buffer = []
    while current_index < len(current) and current[current_index].isdigit():
        buffer.append(current[current_index])
        current_index += 1
    
    return Token(INT, ''.join(buffer)), current_index

def generate_keyword(current: str, current_index: int) -> Tuple[Token, int]:
    buffer = []
    while current_index < len(current) and current[current_index].isalpha():
        buffer.append(current[current_index])
        current_index += 1
    
    keyword = ''.join(buffer)
    if keyword == "exit":
        return Token(KEYWORD, "EXIT"), current_index
    elif keyword == 'print':
        return Token(KEYWORD, "PRINT"), current_index
    elif keyword == 'let':
        return Token(KEYWORD, "LET"), current_index
    elif keyword == 'if':
        return Token(KEYWORD, "IF"), current_index
    elif keyword == 'else':
        return Token(KEYWORD, "ELSE"), current_index
    elif keyword == 'while':
        return Token(KEYWORD, "WHILE"), current_index
    elif keyword == 'true':
        return Token(BOOL_LIT, "TRUE"), current_index
    elif keyword == 'false':
        return Token(BOOL_LIT, "FALSE"), current_index
    elif keyword == 'assign':
        return Token(KEYWORD, "ASSIGN"), current_index
    elif keyword == 'processor':
        return Token(KEYWORD, "PROCESSOR"), current_index
    elif keyword == 'call':
        return Token(KEYWORD, "CALL"), current_index
    else:
        return Token(IDENTIFIER, keyword), current_index

def generate_separator(current: str, current_index: int) -> Tuple[Token, int]:
    token = Token(SEPARATOR, current[current_index])
    return token, current_index + 1

def generate_operator(current: str, current_index: int) -> Tuple[Token, int]:
    token = Token(OPERATOR, current[current_index])
    return token, current_index + 1

def generate_string(current: str, current_index: int) -> Tuple[Token, int]:
    current_index += 1  # Skip the opening quote
    buffer = []
    while current_index < len(current) and current[current_index] != '"':
        buffer.append(current[current_index])
        current_index += 1

    if current_index >= len(current) or current[current_index] != '"':
        sys.stderr.write("Unterminated string literal\n")
        sys.exit(1)

    current_index += 1  # Skip the closing quote
    return Token(STRING, ''.join(buffer)), current_index


def lexer(file_path: str) -> List[Token]:
    with open(file_path, 'r') as file:
        current = file.read()
    
    tokens = []
    current_index = 0
    
    while current_index < len(current):
        if current[current_index].isspace():
            current_index += 1
            continue
            
        token = None
        
        if current[current_index].isdigit():
            token, current_index = generate_number(current, current_index)
        elif current[current_index].isalpha():
            token, current_index = generate_keyword(current, current_index)
        elif current[current_index] == '"':
            token, current_index = generate_string(current, current_index)
        elif current[current_index] in ["(", ")", "{", "}", ";", ","]:
            token, current_index = generate_separator(current, current_index)
        elif current[current_index] == "/" and current_index + 1 < len(current) and current[current_index + 1] == "/":
            # Handle single-line comments
            while current_index < len(current) and current[current_index] != "\n":
                current_index += 1
            continue
        elif current[current_index] in "+-*/=<>":
            token, current_index = generate_operator(current, current_index)
        else:
            sys.stderr.write(f"Unknown character: {current[current_index]}\n")
            sys.exit(1)
            
        tokens.append(token)
    
    tokens.append(Token(END_OF_TOKENS))
    print(tokens)
    return tokens