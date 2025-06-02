from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class NodeType(Enum):
    PROGRAM = auto()
    EXIT_STMT = auto()
    INT_LIT = auto()
    BINARY_OP = auto()
    PAREN_EXPR = auto()
    PRINT_STMT = auto()
    LET_STMT = auto()
    IDENTIFIER = auto()

@dataclass
class ASTNode:
    type: NodeType
    value: Optional[str] = None
    left: Optional['ASTNode'] = None
    right: Optional['ASTNode'] = None

def print_ast(node: ASTNode, indent: int = 0):
    """Pretty print the AST"""
    if not node:
        return
    print("  " * indent + f"{node.type.name}: {node.value if node.value else ''}")
    print_ast(node.left, indent + 1)
    print_ast(node.right, indent + 1)