from ast_lib import ASTNode, NodeType

function_register_values = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']

class CodeGenerator:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.output = []
        self.label_counter = 0
        self.num_string_literals = 0
        self.string_literals = []
        self.variables = {}  # Maps variable names to their initialization status
        self.initial_values = {}  # Store initial values for variables

    def generate_code(self) -> str:
        # First pass: collect all variable declarations and their initial values
        self._collect_variables(self.ast)
        
        self.output.append("section .text")
        self.output.append("global _start")
        self.output.append("_start:")

        # Generate code for each statement in order
        node = self.ast.right
        print("\nGenerating code for statements:")
        while node:
            print(f"Processing node: {node.type} {node.value}")
            if node.type == NodeType.LET_STMT:
                print(f"  LET statement: {node.left.value} = {node.right.value if node.right else 'None'}")
                self._generate_let_statement(node)
            elif node.type == NodeType.EXIT_STMT:
                print(f"  EXIT statement with arg: {node.left.type if node.left else 'None'}")
                self._generate_exit_statement(node)
            elif node.type == NodeType.PRINT_STMT:
                self._generate_print_statement(node)
            elif node.type == NodeType.IF_STMT:
                print(f"node: {node}")
                print(f"  IF statement: {node.left.value} {node.right.value} {node.else_node.value if node.else_node else 'None'}")
                self._generate_if_statement(node)
            elif node.type == NodeType.PROCESSOR_STMT:
                print(f"  PROCESSOR statement: {node.left.value} {node.right.value}")
                self._generate_processor_statement(node)
            elif node.type == NodeType.WHILE_STMT:
                print(f"  WHILE statement: {node.left.value} {node.right.value}")
                self._generate_while_statement(node)
            elif node.type == NodeType.ELSE_STMT:
                print(f"  ELSE statement")
                self._generate_else_statement(node)
            elif node.type == NodeType.ASSIGN_STMT:
                self._generate_assign_stmt(node)
            elif node.type == NodeType.FUNCTION_CALL:
                self._generate_function_call(node)
            node = node.next_node

        self.output.append("\n; System exit")
        self.output.append("mov eax, 1    ; sys_exit")
        self.output.append("int 0x80")

        # Deduplicate section .data
        if self.string_literals or self.variables:
            self.output.append("\nsection .data")

        # Output string literals
        for label, text in self.string_literals:
            self.output.append(f"{label}: db \"{text}\", 10")

        # Output variable definitions with their initial values
        for var, val in self.variables.items():
            if var in self.initial_values:
                self.output.append(f"{var}: dd {self.initial_values[var]}")
            else:
                self.output.append(f"{var}: dd 0")

        return "\n".join(self.output)



    def _collect_variables(self, node: ASTNode):
        """First pass to collect all variable declarations and their initial values"""
        if not node:
            return
        
        if node.type == NodeType.LET_STMT:
            var_name = node.left.value
            self.variables[var_name] = "dd 0"  # Pre-declare all variables
            
            # If the right side is an integer literal, store its value
            if node.right and node.right.type == NodeType.INT_LIT:
                self.initial_values[var_name] = node.right.value
                print(f"Collected initial value for {var_name}: {node.right.value}")
        
        self._collect_variables(node.left)
        self._collect_variables(node.right)
        self._collect_variables(node.next_node)

    def _generate_variable(self, node):
        var_name = node.value
        if var_name not in self.variables:
            raise RuntimeError(f"Variable '{var_name}' used before declaration")
        self.output.append(f"mov eax, [{var_name}]")

    def _generate_let_statement(self, node: ASTNode):
        var_name = node.left.value
        
        # Generate right-hand side first (e.g., mov eax, 2)
        if node.right.type == NodeType.INT_LIT:
            print(f"  Generating integer literal: {node.right.value}")
            self.output.append(f"mov eax, {node.right.value}")
        elif node.right.type == NodeType.VAR:
            print(f"  Generating variable reference: {node.right.value}")
            self._generate_variable(node.right)
        elif node.right.type == NodeType.BINARY_OP:
            print(f"  Generating binary operation")
            self._generate_binary_op(node.right)
        else:
            print(f"  Generating other expression type: {node.right.type}")
            self._generate_node(node.right)
        
        # Store the value in eax into the variable
        print(f"  Storing value in variable: {var_name}")
        self.output.append(f"mov [{var_name}], eax")

    def _generate_assign_stmt(self, node):
        var_name = node.left.value

        # Generate right-hand side first (e.g., mov eax, x + 1)
        if node.right.type == NodeType.INT_LIT:
            self.output.append(f"mov eax, {node.right.value}")
        elif node.right.type == NodeType.VAR:
            self._generate_variable(node.right)
        elif node.right.type == NodeType.BINARY_OP:
            self._generate_binary_op(node.right)
        else:
            self._generate_node(node.right)
        
        # Store the value in eax into the variable
        self.output.append(f"mov [{var_name}], eax")

    def _generate_while_statement(self, node: ASTNode):
        start_label = f"start_while_{self.label_counter}"
        end_label = f"end_while_{self.label_counter}"
        self.label_counter += 1
        
        self.output.append(f"{start_label}:")
        
        # Generate condition
        self._generate_node(node.left)
        
        # For comparison operators, we need to handle them specially
        if hasattr(node.left, 'value') and node.left.value in ['>', '<', '>=', '<=', '==', '!=']:
            # The condition is already evaluated, just check if it's non-zero
            self.output.append("cmp eax, 0")
        else:
            # For other conditions, just check if the result is non-zero
            self.output.append("cmp eax, 0")
        
        # Jump to end if condition is false
        self.output.append(f"je {end_label}")
        
        # Generate loop body
        if node.right:
            self._generate_node(node.right)
        
        # Jump back to start
        self.output.append(f"jmp {start_label}")
        self.output.append(f"{end_label}:")

    def _generate_processor_statement(self, node: ASTNode):
        # TODO: Implement processor statement generation
        pass

    def _generate_function_call(self, node: ASTNode):
        """Generate assembly code for function calls"""
        # Save current registers
        self.output.append("push rax")
        self.output.append("push rbx")
        self.output.append("push rcx")
        self.output.append("push rdx")
        
        # Generate arguments (reverse order for x86_64 calling convention)
        if node.args:
            for i, arg in enumerate(reversed(node.args)):
                self._generate_node(arg)
                if i == 0:
                    self.output.append("mov rdi, rax")  # First arg in rdi
                elif i == 1:
                    self.output.append("mov rsi, rax")  # Second arg in rsi
                elif i == 2:
                    self.output.append("mov rdx, rax")  # Third arg in rdx
                elif i == 3:
                    self.output.append("mov rcx, rax")  # Fourth arg in rcx
                elif i == 4:
                    self.output.append("mov r8, rax")   # Fifth arg in r8
                elif i == 5:
                    self.output.append("mov r9, rax")   # Sixth arg in r9
                else:
                    # Additional args go on stack
                    self.output.append("push rax")
        
        # Call the function
        self.output.append(f"call {node.function_name}")
        
        # Restore registers
        self.output.append("pop rdx")
        self.output.append("pop rcx")
        self.output.append("pop rbx")
        self.output.append("pop rax")

    def _generate_if_statement(self, node: ASTNode):
        print("Generating if statement")
        
        # Generate condition
        self._generate_node(node.left)
        
        # For comparison operators, we need to handle them specially
        if hasattr(node.left, 'value') and node.left.value in ['>', '<', '>=', '<=', '==', '!=']:
            # The condition is already evaluated, just check if it's non-zero
            self.output.append("cmp eax, 0")
        else:
            # For other conditions, just check if the result is non-zero
            self.output.append("cmp eax, 0")
        
        else_label = f"else_{self.label_counter}"
        end_label = f"end_if_{self.label_counter}"
        self.label_counter += 1
        
        # Jump to else block if condition is false
        self.output.append(f"je {else_label}")
        
        # Generate then block
        if node.right:
            self._generate_node(node.right)
        self.output.append(f"jmp {end_label}")
        
        # Generate else block
        self.output.append(f"{else_label}:")
        if node.else_node:
            self._generate_node(node.else_node)
        
        # End of if statement
        self.output.append(f"{end_label}:")

    def _generate_exit_statement(self, node: ASTNode):
        if node.left:
            print(f"  Generating exit argument: {node.left.type}")
            if node.left.type == NodeType.VAR:
                self._generate_variable(node.left)
            else:
                self._generate_node(node.left)
        self.output.append("mov ebx, eax  ; exit status")

    def _generate_node(self, node: ASTNode):
        print(f"  Generating node: {node.type} {node.value}")
        if node.type == NodeType.INT_LIT:
            self.output.append(f"mov eax, {node.value}")
        elif node.type == NodeType.VAR:
            self._generate_variable(node)
        elif node.type == NodeType.BINARY_OP:
            self._generate_binary_op(node)
        elif node.type == NodeType.LET_STMT:
            self._generate_let_statement(node)
        elif node.type == NodeType.EXIT_STMT:
            self._generate_exit_statement(node)
        elif node.type == NodeType.PRINT_STMT:
            self._generate_print_statement(node)
        elif node.type == NodeType.ASSIGN_STMT:
            self._generate_assign_stmt(node)
        elif node.type == NodeType.IF_STMT:
            self._generate_if_statement(node)
        elif node.type == NodeType.WHILE_STMT:
            self._generate_while_statement(node)
        elif node.type == NodeType.FUNCTION_CALL:
            self._generate_function_call(node)

    def _generate_binary_op(self, node: ASTNode):
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
            self.output.append("cdq")
            self.output.append("idiv ebx")

    def _generate_integer(self, node: ASTNode):
        self.output.append(f"mov eax, {node.value}")

    def _generate_print_statement(self, node: ASTNode):
        if node.left.type == NodeType.STRING_LIT:
            label = self.add_string_literal(node.left.value)
            length = len(node.left.value)

            self.output.append(f"\n; print string: {node.left.value}")
            self.output.append("mov eax, 4")  # sys_write
            self.output.append("mov ebx, 1")  # stdout
            self.output.append(f"mov ecx, {label}")
            self.output.append(f"mov edx, {length}")
            self.output.append("int 0x80")
        else:
            # For integers, convert to string and print
            self._generate_node(node.left)
            # TODO: Add integer to string conversion and printing
            self.output.append("; TODO: Add integer printing")

    def add_string_literal(self, text):
        label = f"msg_{self.num_string_literals}"
        self.num_string_literals += 1
        self.string_literals.append((label, text))
        return label

    def write_to_file(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.generate_code())
