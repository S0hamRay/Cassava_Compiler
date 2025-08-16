from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

class NodeType(Enum):
    PROGRAM = auto()
    EXIT_STMT = auto()
    INT_LIT = auto()
    BINARY_OP = auto()
    PAREN_EXPR = auto()
    PRINT_STMT = auto()
    LET_STMT = auto()
    IDENTIFIER = auto()
    IF_STMT = auto()
    VAR = auto()
    ELSE_STMT = auto()
    STRING_LIT = auto()
    BOOL_LIT = auto()
    WHILE_STMT = auto()
    FOR_STMT = auto()
    BREAK_STMT = auto()
    CONTINUE_STMT = auto()
    RETURN_STMT = auto()
    FUNCTION_CALL = auto()
    FUNCTION_DEF = auto()
    ASSIGN_STMT = auto()
    PROCESSOR_STMT = auto()

@dataclass
class ASTNode:
    type: NodeType
    value: Optional[str] = None
    left: Optional['ASTNode'] = None
    right: Optional['ASTNode'] = None
    next_node: Optional['ASTNode'] = None
    else_node: Optional['ASTNode'] = None
    args: Optional[List['ASTNode']] = None
    body: Optional['ASTNode'] = None
    condition: Optional['ASTNode'] = None
    increment: Optional['ASTNode'] = None
    return_value: Optional['ASTNode'] = None
    function_name: Optional[str] = None
def print_ast(node: ASTNode, indent: int = 0):
    """Pretty print the AST"""
    if not node:
        return
    print("  " * indent + f"{node.type.name}: {node.value if node.value else ''}")
    print_ast(node.left, indent + 1)
    print_ast(node.right, indent + 1)