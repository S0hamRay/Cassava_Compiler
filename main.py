import sys
from lexer import lexer
from parser_1 import Parser
from ast_lib import print_ast
from code_generator import CodeGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Step 1: Lexical analysis
    tokens = lexer(input_file)
    
    # Step 2: Parsing
    parser = Parser(tokens)
    ast = parser.parse()

    generator = CodeGenerator(ast)
    generator.write_to_file("output.asm")
        
    # Step 3: Output the AST
    print("\nGenerated AST:")
    print_ast(ast)

if __name__ == "__main__":
    main()