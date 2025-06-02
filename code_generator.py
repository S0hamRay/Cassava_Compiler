from ast_lib import ASTNode, NodeType

class CodeGenerator:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.output = []
        self.label_counter = 0
        self.num_string_literals = 0
        self.string_literals = []
        self.variables = {}

    def generate_label(self, prefix: str) -> str:
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

    def generate_code(self) -> str:
        self.output.append("section .text")
        self.output.append("global _start")
        self.output.append("_start:")
        
        self._generate_node(self.ast.right)  # Process the EXIT statement
        
        self.output.append("\n; System exit")
        self.output.append("mov eax, 1    ; sys_exit")
        self.output.append("int 0x80")
        if self.string_literals:
            self.output.append("\nsection .data")
            for label, text in self.string_literals:
                self.output.append(f"{label}: db \"{text}\", 10")  # 10 = newline
        if self.variables:
            self.output.append("\nsection .data")
            for var, val in self.variables.items():
                self.output.append(f"{var}: {val}")

        return "\n".join(self.output)
    
    def add_string_literal(self, text):
        label = f"msg_{self.num_string_literals}" # generates the index for the string
        self.num_string_literals += 1
        self.string_literals.append((label, text))
        return label

    def _generate_node(self, node: ASTNode):
        if node.type == NodeType.EXIT_STMT:
            self._generate_exit_statement(node)
        elif node.type == NodeType.BINARY_OP:
            self._generate_binary_op(node)
        elif node.type == NodeType.INT_LIT:
            self._generate_integer(node)
        elif node.type == NodeType.PRINT_STMT:
            self._generate_print_statement(node)
        elif node.type == NodeType.LET_STMT:
            self._generate_let_statement(node)

    def _generate_let_statement(self, node : ASTNode):
        var_name = node.left if isinstance(node.left, str) else node.left.value
        self._generate_node(node.right)
        self.output.append(f"mov [{var_name}], eax")
        self.variables[var_name] = "dd 0"

    def _generate_print_statement(self, node: ASTNode):
        if node.left.type == NodeType.INT_LIT and isinstance(node.left.value, str):
            label = self.add_string_literal(node.left.value)
            length = len(node.left.value)

            self.output.append(f"\n; print string: {node.left.value}")
            self.output.append("mov eax, 4")  # sys_write
            self.output.append("mov ebx, 1")  # stdout
            self.output.append(f"mov ecx, {label}")
            self.output.append(f"mov edx, {length}")
            self.output.append("int 0x80")
        else:
            # expression print, might do this
            pass


    def _generate_exit_statement(self, node: ASTNode):
        # Generate code for the exit expression first
        if node.left:
            self._generate_node(node.left)
        
        # The result should be in eax from expression evaluation
        self.output.append("mov ebx, eax  ; exit status")

    def _generate_binary_op(self, node: ASTNode):
        # Evaluate right operand first (reverse order for stack-like behavior)
        self._generate_node(node.right)
        self.output.append("push eax")
        self._generate_node(node.left)
        self.output.append("pop ebx")
        
        if node.value == '+':
            self.output.append("add eax, ebx")
        elif node.value == '-':
            self.output.append("sub eax, ebx")
        elif node.value == '*':
            self.output.append("imul eax, ebx")
        elif node.value == '/':
            self.output.append("cdq")          # Sign extend eax into edx:eax
            self.output.append("idiv ebx")    # Result in eax, remainder in edx

    def _generate_integer(self, node: ASTNode):
        self.output.append(f"mov eax, {node.value}")

    def write_to_file(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.generate_code())