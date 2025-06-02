from typing import List
from ast_lib import ASTNode, NodeType
from lexer import Token, END_OF_TOKENS, KEYWORD, SEPARATOR, INT, OPERATOR, STRING, IDENTIFIER
from expressions import ExpressionParser

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return self.current_token

    def parse(self) -> ASTNode:
        """Entry point to build the AST"""
        program_node = ASTNode(NodeType.PROGRAM, "PROGRAM")
        
        while self.current_token and self.current_token.type != END_OF_TOKENS:
            if (self.current_token.type == KEYWORD and self.current_token.value == "EXIT"):
                program_node.right = self.parse_exit_statement()
            elif(self.current_token.type == KEYWORD and self.current_token.value == 'PRINT'):
                program_node.right = self.parse_print_statement()
            elif(self.current_token.type == KEYWORD and self.current_token.value == 'LET'):
                program_node.right = self.parse_let_statement()
            else:
                print(f"Unexpected token: {self.current_token.value}")
                exit(1)

        return program_node
    
    def parse_let_statement(self):
        let_node = ASTNode(NodeType.LET_STMT, "LET_STMT")
        self.advance()

        if self.current_token.type != IDENTIFIER:
            print("expected an identifier")
            exit(1)
        let_node.left = ASTNode(NodeType.IDENTIFIER, self.current_token.value)

        self.advance()

        if self.current_token.type != OPERATOR or self.current_token.value != '=':
            print("expected =")
            exit(1)

        self.advance()

        parser_exp = ExpressionParser(self.tokens, self.pos)
        parsed, self.pos = parser_exp.parse_expression()
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None 
        let_node.right = parsed
        
        if self.current_token.type != SEPARATOR or self.current_token.value != ';':
            print("expected semicolon after let")
            exit(1)
        self.advance()

        return let_node


    def parse_print_statement(self):
        print_node = ASTNode(NodeType.PRINT_STMT, "PRINT_STMT")
        self.advance()

        if not (self.current_token and self.current_token.value == '('):
            print("expected opening bracket for print statement")
            exit(1)
        else:
            self.advance()

        is_string = False
        if(self.current_token.type == STRING):
            is_string = True

        if not is_string:
            # we're now inside the print statement, you wanna parse the expression if it's a number or something
            parser_exp = ExpressionParser(self.tokens, self.pos)
            parsed, self.pos = parser_exp.parse_expression()
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None 
            print_node.left = parsed
        else:
            string_node = ASTNode(NodeType.INT_LIT, self.current_token.value)
            self.advance()  # Consume the string
            print_node.left = string_node


        if not (self.current_token and self.current_token.value == ')'):
            print("expected closing bracket after print")
            exit(1)

        self.advance()

        if not (self.current_token and self.current_token.value == ';'):
            print("expected semicolon after print")
            exit(1)
        self.advance()

        return print_node
    
    def parse_exit_statement(self):
        exit_node = ASTNode(NodeType.EXIT_STMT, "EXIT")
        self.advance()  # Consume 'EXIT'
        
        if not (self.current_token.value == "("):
            raise SyntaxError("Expected '('")
        self.advance()  # Consume '('
        
        # Parse expression instead of just integer
        expr_parser = ExpressionParser(self.tokens, self.pos)
        arg_node, self.pos = expr_parser.parse_expression()
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        
        exit_node.left = arg_node
        
        if not (self.current_token.value == ")"):
            raise SyntaxError("Expected ')'")
        self.advance()  # Consume ')'
        
        if not (self.current_token.value == ";"):
            raise SyntaxError("Expected ';'")
        self.advance()  # Consume ';'
        
        return exit_node