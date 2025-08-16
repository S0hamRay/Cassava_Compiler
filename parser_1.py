from typing import List
from ast_lib import ASTNode, NodeType
from lexer import Token, END_OF_TOKENS, KEYWORD, SEPARATOR, INT, OPERATOR, STRING, IDENTIFIER, UNKNOWN
from expressions import ExpressionParser

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return self.current_token

    def parse(self) -> ASTNode:
        program_node = ASTNode(NodeType.PROGRAM, "PROGRAM")
        statements = []

        print("\nParsing statements:")
        while self.current_token and self.current_token.type != END_OF_TOKENS:
            if self.current_token.type == KEYWORD and self.current_token.value == "EXIT":
                stmt = self.parse_exit_statement()
                print(f"Parsed EXIT statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "PRINT":
                stmt = self.parse_print_statement()
                print(f"Parsed PRINT statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "LET":
                stmt = self.parse_let_statement()
                print(f"Parsed LET statement: {stmt.left.value} = {stmt.right.value if stmt.right else 'None'}")
            elif self.current_token.type == KEYWORD and self.current_token.value == "IF":
                stmt = self.parse_if_statement()
                print(f"Parsed IF statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "ELSE":
                self.advance()
                continue
            elif self.current_token.type == KEYWORD and self.current_token.value == "WHILE":
                stmt = self.parse_while_stmt()
                print(f"Parsed WHILE statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "ASSIGN":
                stmt = self.parse_assign_statement()
                print(f"Parsed ASSIGN statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "PROCESSOR":
                stmt, num_args = self.parse_processor_statement()
                print(f"Parsed PROCESSOR statement")
            elif self.current_token.type == KEYWORD and self.current_token.value == "CALL":
                stmt = self.parse_function_call()
                print(f"Parsed FUNCTION CALL statement")
            else:
                print(f"Unexpected token: {self.current_token.value}")
                exit(1)

            statements.append(stmt)

        # Link statements in order
        print("\nLinking statements:")
        for i in range(len(statements) - 1):
            statements[i].next_node = statements[i + 1]
            print(f"Linked statement {i} to {i+1}")
        
        if statements:
            program_node.right = statements[0]
            print(f"Linked first statement to program node")

        return program_node
    
    def parse_while_stmt(self):
        while_node = ASTNode(NodeType.WHILE_STMT, "WHILE_STMT")
        self.advance()
        if self.current_token.value != '(':
            print("expected opening bracket after while")
            exit(1)
        self.advance()

        parser_exp = ExpressionParser(self.tokens, self.pos)
        condition_node, new_pos = parser_exp.parse_expression()
        self.pos = new_pos
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        while_node.left = condition_node 
        
        if self.current_token.value != ')':
            print("expected closing bracket after while")
            exit(1)
        self.advance()
        
        if self.current_token.value != '{':
            print(f"expected opening curly bracket after while, got '{self.current_token.value}'")
            exit(1)
        self.advance()

        # Parse while loop body
        body_statements = []
        while self.current_token and self.current_token.type != END_OF_TOKENS:
            if self.current_token.type == KEYWORD and self.current_token.value == "EXIT":
                stmt = self.parse_exit_statement()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "PRINT":
                stmt = self.parse_print_statement()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "LET":
                stmt = self.parse_let_statement()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "ASSIGN":
                stmt = self.parse_assign_statement()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "CALL":
                stmt = self.parse_function_call()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "IF":
                stmt = self.parse_if_statement()
                body_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "WHILE":
                stmt = self.parse_while_stmt()
                body_statements.append(stmt)
            elif self.current_token.type == SEPARATOR and self.current_token.value == '}':
                self.advance()  # consume closing brace
                break
            elif self.current_token.type == SEPARATOR and self.current_token.value == ';':
                self.advance()
            else:
                print(f"Unexpected token in while body: {self.current_token.value}")
                exit(1)
        
        # Link while body statements
        if body_statements:
            while_node.right = body_statements[0]
            for i in range(len(body_statements) - 1):
                body_statements[i].next_node = body_statements[i + 1]
        
        return while_node
    
    def parse_processor_stmt(self):
        processor_node = ASTNode(NodeType.PROCESSOR_STMT, "PROCESSOR_STMT")
        self.advance()
        if self.current_token.type != IDENTIFIER:
            print("expected an identifier")
            exit(1)
        processor_node.left = ASTNode(NodeType.IDENTIFIER, self.current_token.value)
        self.advance()
        if self.current_token.type != SEPARATOR or self.current_token.value != '(':
            print("expected opening bracket after function definition")
            exit(1)
        self.advance()
        prev_node = None
        num_args = 0
        while(self.current_token.type != SEPARATOR or self.current_token.value != ')'):
            if self.current_token.type != IDENTIFIER:
                print("expected an identifier")
                exit(1)
            if prev_node is not None:
                prev_node.next_node = ASTNode(NodeType.IDENTIFIER, self.current_token.value)
                prev_node = prev_node.next_node
            else:
                processor_node.left.next_node = ASTNode(NodeType.IDENTIFIER, self.current_token.value)
                prev_node = processor_node.left.next_node
            num_args += 1
            self.advance()
        if self.current_token.type != SEPARATOR or self.current_token.value != ')':
            print("expected closing bracket after function definition")
            exit(1)
        self.advance()
        processor_node.right = self.parse()
        
        return processor_node, num_args

    def parse_let_statement(self):
        let_node = ASTNode(NodeType.LET_STMT, "LET_STMT")
        self.advance()  # consume LET

        if self.current_token.type != IDENTIFIER:
            print("expected an identifier")
            exit(1)
        let_node.left = ASTNode(NodeType.IDENTIFIER, self.current_token.value)
        print(f"  LET statement identifier: {self.current_token.value}")
        self.advance()

        if self.current_token.type != OPERATOR or self.current_token.value != '=':
            print("expected '=' after identifier")
            exit(1)
        self.advance()

        # Parse the expression value
        parser_exp = ExpressionParser(self.tokens, self.pos)
        value_node, new_pos = parser_exp.parse_expression()
        self.pos = new_pos
        print(f"  LET statement expression: {value_node.type} {value_node.value}")

        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

        # Set the right child to the value node
        let_node.right = value_node

        if self.current_token.type != SEPARATOR or self.current_token.value != ';':
            print("expected ';' after let statement")
            exit(1)
        self.advance()  # consume ';'

        return let_node
    
    def parse_if_statement(self):
        if_node = ASTNode(NodeType.IF_STMT, "IF")
        self.advance()  # consume IF

        # Parse condition
        if self.current_token.value != '(':
            print("expected opening bracket after if")
            exit(1)
        self.advance()  # consume '('

        parser_exp = ExpressionParser(self.tokens, self.pos)
        condition_node, new_pos = parser_exp.parse_expression()
        self.pos = new_pos
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

        if_node.left = condition_node

        if self.current_token.value != ')':
            print("expected closing bracket after if condition")
            exit(1)
        self.advance()  # consume ')'

        # Expect opening brace
        if self.current_token.value != '{':
            print("expected opening brace after if condition")
            exit(1)
        self.advance()  # consume '{'

        # Parse then block
        then_statements = []
        while self.current_token and self.current_token.type != END_OF_TOKENS:
            if self.current_token.type == KEYWORD and self.current_token.value == "EXIT":
                stmt = self.parse_exit_statement()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "PRINT":
                stmt = self.parse_print_statement()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "LET":
                stmt = self.parse_let_statement()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "ASSIGN":
                stmt = self.parse_assign_statement()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "CALL":
                stmt = self.parse_function_call()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "IF":
                stmt = self.parse_if_statement()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "WHILE":
                stmt = self.parse_while_stmt()
                then_statements.append(stmt)
            elif self.current_token.type == KEYWORD and self.current_token.value == "ELSE":
                break
            elif self.current_token.type == SEPARATOR and self.current_token.value == '}':
                self.advance()  # consume closing brace
                break
            elif self.current_token.type == SEPARATOR and self.current_token.value == ';':
                self.advance()
            else:
                print(f"Unexpected token in then block: {self.current_token.value}")
                exit(1)

        print(f"Then block statements: {then_statements}")

        # Link then block statements
        if then_statements:
            if_node.right = then_statements[0]
            for i in range(len(then_statements) - 1):
                then_statements[i].next_node = then_statements[i + 1]

        # Check for else block
        if self.current_token and self.current_token.type == KEYWORD and self.current_token.value == "ELSE":
            self.advance()  # consume ELSE
            
            # Expect opening brace after ELSE
            if self.current_token.value != '{':
                print("expected opening brace after ELSE")
                exit(1)
            self.advance()  # consume '{'
            
            # Parse else block
            else_statements = []
            while self.current_token and self.current_token.type != END_OF_TOKENS:
                if self.current_token.type == KEYWORD and self.current_token.value == "EXIT":
                    stmt = self.parse_exit_statement()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "PRINT":
                    stmt = self.parse_print_statement()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "LET":
                    stmt = self.parse_let_statement()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "ASSIGN":
                    stmt = self.parse_assign_statement()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "CALL":
                    stmt = self.parse_function_call()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "IF":
                    stmt = self.parse_if_statement()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value == "WHILE":
                    stmt = self.parse_while_stmt()
                    else_statements.append(stmt)
                elif self.current_token.type == KEYWORD and self.current_token.value in ["IF", "ELSE"]:
                    break
                elif self.current_token.type == SEPARATOR and self.current_token.value == '}':
                    self.advance()  # consume closing brace
                    break
                elif self.current_token.type == SEPARATOR and self.current_token.value == ';':
                    self.advance()
                else:
                    print(f"Unexpected token in else block: {self.current_token.value}")
                    exit(1)

            print(f"Else block statements: {else_statements}")

            # Link else block statements
            if else_statements:
                if_node.else_node = else_statements[0]
                for i in range(len(else_statements) - 1):
                    else_statements[i].next_node = else_statements[i + 1]

        print(f"Final if node structure: {if_node}")
        return if_node

    def parse_exit_statement(self):
        exit_node = ASTNode(NodeType.EXIT_STMT, "EXIT")
        self.advance()  # consume EXIT

        if self.current_token.value != "(":
            print("expected '(' after EXIT")
            exit(1)
        self.advance()  # consume '('

        # Parse the expression argument
        parser_exp = ExpressionParser(self.tokens, self.pos)
        arg_node, new_pos = parser_exp.parse_expression()
        self.pos = new_pos
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

        # Set the left child to the argument node
        exit_node.left = arg_node

        if self.current_token.value != ")":
            print("expected ')' after EXIT argument")
            exit(1)
        self.advance()  # consume ')'

        if self.current_token.value != ";":
            print("expected ';' after EXIT statement")
            exit(1)
        self.advance()  # consume ';'

        return exit_node
    
    def parse_assign_statement(self):
        assign_node = ASTNode(NodeType.ASSIGN_STMT, "ASSIGN_STMT")
        self.advance()  # consume ASSIGN
        
        if self.current_token.type != IDENTIFIER:
            print("expected an identifier")
            exit(1)
        assign_node.left = ASTNode(NodeType.IDENTIFIER, self.current_token.value)
        self.advance()
        
        if self.current_token.type != OPERATOR or self.current_token.value != '=':
            print("expected '=' after identifier")
            exit(1)
        self.advance()
        
        parser_exp = ExpressionParser(self.tokens, self.pos)
        new_val, new_pos = parser_exp.parse_expression()
        self.pos = new_pos
        assign_node.right = new_val
        
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

        if self.current_token.type != SEPARATOR or self.current_token.value != ';':
            print("expected ';' after assign statement")
            exit(1)
        self.advance()  # consume ';'
        
        return assign_node
    
    def parse_function_call(self):
        call_node = ASTNode(NodeType.FUNCTION_CALL, "FUNCTION_CALL")
        self.advance()  # consume CALL
        
        if self.current_token.type != IDENTIFIER:
            print("expected function name after CALL")
            exit(1)
        call_node.function_name = self.current_token.value
        self.advance()
        
        if self.current_token.type != SEPARATOR or self.current_token.value != '(':
            print("expected opening bracket after function name")
            exit(1)
        self.advance()
        
        # Parse arguments
        args = []
        if self.current_token.type != SEPARATOR or self.current_token.value != ')':
            while True:
                parser_exp = ExpressionParser(self.tokens, self.pos)
                arg_node, new_pos = parser_exp.parse_expression()
                self.pos = new_pos
                self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
                args.append(arg_node)
                
                if self.current_token.type == SEPARATOR and self.current_token.value == ')':
                    break
                elif self.current_token.type == SEPARATOR and self.current_token.value == ',':
                    self.advance()  # consume comma
                else:
                    print("expected ',' or ')' in function call arguments")
                    exit(1)
        
        call_node.args = args
        
        if self.current_token.type != SEPARATOR or self.current_token.value != ')':
            print("expected closing bracket after function arguments")
            exit(1)
        self.advance()
        
        if self.current_token.type != SEPARATOR or self.current_token.value != ';':
            print("expected ';' after function call")
            exit(1)
        self.advance()
        
        return call_node
        

    def parse_print_statement(self):
        print_node = ASTNode(NodeType.PRINT_STMT, "PRINT_STMT")
        self.advance()  # consume PRINT

        if self.current_token.value != "(":
            print("expected '(' after PRINT")
            exit(1)
        self.advance()  # consume '('

        if self.current_token.type in [STRING, UNKNOWN]:  # Handle both STRING and UNKNOWN types as string literals
            string_node = ASTNode(NodeType.STRING_LIT, self.current_token.value)
            self.advance()
            print_node.left = string_node
        else:
            parser_exp = ExpressionParser(self.tokens, self.pos)
            parsed, new_pos = parser_exp.parse_expression()
            self.pos = new_pos
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            print_node.left = parsed

        if self.current_token.value != ")":
            print("expected ')' after PRINT argument")
            exit(1)
        self.advance()  # consume ')'

        if self.current_token.value != ";":
            print("expected ';' after PRINT statement")
            exit(1)
        self.advance()  # consume ';'

        return print_node
