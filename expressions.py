from ast_lib import ASTNode, NodeType
from lexer import Token, INT, IDENTIFIER, OPERATOR

class ExpressionParser:
    def __init__(self, tokens, pos=0):
        self.tokens = tokens
        self.pos = pos

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1
        return self.current_token()

    def parse_expression(self):
        node = self.parse_term()

        while self.pos < len(self.tokens):
            token = self.current_token()
            if token.type == OPERATOR and token.value in ('+', '-'):
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '==':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '!=':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '>':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '<':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '>=':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '<=':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '&&':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '||':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            elif token.type == OPERATOR and token.value == '!':
                op = token.value
                self.advance()
                right = self.parse_term()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            else:
                break

        return node, self.pos

    def parse_term(self):
        node = self.parse_factor()

        while self.pos < len(self.tokens):
            token = self.current_token()
            if token.type == OPERATOR and token.value in ('*', '/'):
                op = token.value
                self.advance()
                right = self.parse_factor()
                node = ASTNode(NodeType.BINARY_OP, op, left=node, right=right)
            else:
                break

        return node

    def parse_factor(self):
        token = self.current_token()
        if token is None:
            raise SyntaxError("Unexpected end of input during expression parsing")

        if token.type == INT:
            node = ASTNode(NodeType.INT_LIT, int(token.value))
            self.advance()
            return node
        elif token.type == IDENTIFIER:
            node = ASTNode(NodeType.VAR, token.value)
            self.advance()
            return node
        elif token.value == '(':
            self.advance()  # consume '('
            node, _ = self.parse_expression()
            if self.current_token() is None or self.current_token().value != ')':
                raise SyntaxError("Expected ')'")
            self.advance()  # consume ')'
            return node
        else:
            raise SyntaxError(f"Unexpected token in expression: {token.value}")
