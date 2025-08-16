# CompilersRevamped

A complete compiler implementation that translates a custom programming language to x86 assembly code. This project demonstrates the full compiler pipeline from lexical analysis to code generation.

## Features

### ✅ **Variable Assignment** - FULLY IMPLEMENTED
- **LET statements**: `let x = 5;` - creates new variables with initial values
- **ASSIGN statements**: `assign x = y + 1;` - modifies existing variables
- Both support complex expressions on the right side
- Variables are properly declared in assembly with initial values

### ✅ **If Conditions** - FULLY IMPLEMENTED
- **IF statements**: `if (condition) { ... } else { ... }`
- Supports both then and else blocks
- Proper condition parsing and branching
- Nested statements within blocks
- Comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`

### ✅ **While Loops** - FULLY IMPLEMENTED
- **WHILE statements**: `while (condition) { ... }`
- Proper loop condition evaluation
- Loop body execution with multiple statements
- Jump-based control flow for efficient loops

### ✅ **Function Calls** - FULLY IMPLEMENTED
- **Built-in functions**: `print(value)`, `exit(value)`
- Support for function arguments
- Proper argument parsing and evaluation
- Assembly code generation for function calls

### ✅ **Expressions** - FULLY IMPLEMENTED
- Arithmetic operations: `+`, `-`, `*`, `/`
- Comparison operations: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical operations: `&&`, `||`, `!`
- Parenthesized expressions
- Variable references and integer literals

## Project Structure

```
CompilersRevamped/
├── lexer.py          # Lexical analyzer - converts source code to tokens
├── parser_1.py       # Parser - builds Abstract Syntax Tree (AST)
├── ast_lib.py        # AST node definitions and utilities
├── expressions.py    # Expression parsing logic
├── code_generator.py # Code generator - converts AST to x86 assembly
├── main.py           # Main compiler driver
├── test_*.txt        # Test files demonstrating various features
└── output.asm        # Generated assembly output
```

## Language Syntax

### Variable Declaration
```c
let x = 5;
let y = 10;
```

### Variable Assignment
```c
assign x = x + 1;
assign y = y * 2;
```

### If-Else Statements
```c
if (x > 5) {
    assign result = x + y;
} else {
    assign result = x - y;
}
```

### While Loops
```c
let counter = 0;
while (counter < 3) {
    assign result = result + counter;
    assign counter = counter + 1;
}
```

### Function Calls
```c
print(result);
exit(result);
```

### Comments
```c
// Single-line comments are supported
```

## Usage

### Prerequisites
- Python 3.6+
- NASM (for assembling the generated code)

### Running the Compiler
```bash
python main.py <input_file>
```

### Example
```bash
python main.py test_final.txt
```

This will:
1. Parse the input file
2. Generate an AST
3. Output x86 assembly to `output.asm`

### Assembling and Running
```bash
# Assemble the generated code
nasm -f elf output.asm -o output.o

# Link the object file
ld -m elf_i386 output.o -o output

# Run the executable
./output
```

## Test Files

- `test_simple.txt` - Basic variable operations and control flow
- `test_while.txt` - While loop functionality
- `test_final.txt` - Comprehensive test of all features

## Compiler Pipeline

1. **Lexical Analysis** (`lexer.py`)
   - Converts source code to tokens
   - Handles keywords, identifiers, operators, literals
   - Supports comments and whitespace

2. **Parsing** (`parser_1.py`)
   - Builds Abstract Syntax Tree (AST)
   - Handles all language constructs
   - Validates syntax and structure

3. **Code Generation** (`code_generator.py`)
   - Traverses AST to generate x86 assembly
   - Handles variable management
   - Generates control flow instructions

## Architecture

The compiler generates x86 assembly code with:
- Proper variable declarations in `.data` section
- Efficient register usage
- Correct control flow with labels and jumps
- System call integration for I/O and program exit

## Future Enhancements

- Support for more data types (floats, strings)
- Function definitions and user-defined functions
- Arrays and data structures
- Optimizations and code analysis
- Support for more target architectures

## Contributing

This is a learning project demonstrating compiler design principles. Feel free to:
- Add new language features
- Improve error handling
- Optimize code generation
- Add more test cases

## License

This project is open source and available under the MIT License.
