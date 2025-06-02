from ast_lib import ASTNode, NodeType
from lexer import Token, INT, OPERATOR, SEPARATOR

class ExpressionParser:
    def __init__(self, tokens, position):
        self.tokens = tokens 
        self.position = position 
        self.current_token = tokens[position]

    def advance(self):
        self.position+=1
        self.current_token = self.tokens[self.position]
        return self.current_token
    
    def parse_expression(self) -> tuple[ASTNode, int]:
        return self.parse_addition()
    
    def parse_addition(self):
        node, self.pos = self.parse_multiplicative()

        while self.current_token.type == OPERATOR and self.current_token.value in "+-":
            op = self.current_token.value
            self.advance()
            right, self.pos = self.parse_multiplicative()
            node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
        return node, self.position

    def parse_multiplicative(self) -> tuple[ASTNode, int]:
        node, self.pos = self.parse_primary()
        
        while self.current_token and self.current_token.type == OPERATOR and self.current_token.value in '*/':
            op = self.current_token.value
            self.advance()
            right, self.pos = self.parse_primary()
            node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
        
        return node, self.pos
    
    def parse_primary(self):
        if self.current_token.type == INT:
            node = ASTNode(NodeType.INT_LIT, self.current_token.value)
            self.advance()
            return node, self.position
        elif self.current_token.type == SEPARATOR and self.current_token.value == '(':
            self.advance()
            node, self.pos = self.parse_expression()
            if not(self.current_token and self.current_token.value == '('):
                print("Missing closing paren")
                exit(1)
            self.advance()
            return node, self.pos
        else:
            print("What on earth is that")
            exit(1)
        