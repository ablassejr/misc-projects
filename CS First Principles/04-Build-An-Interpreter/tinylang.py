"""
TinyLang: Build an Interpreter from First Principles

This module implements a complete interpreter for a simple programming language.
Work through GUIDE.md to understand each component deeply.
"""

from typing import List, Any, Optional, Dict
from dataclasses import dataclass
from enum import Enum, auto


# =============================================================================
# Part 1: Lexical Analysis (Tokenization)
# =============================================================================

class TokenType(Enum):
    """Types of tokens in TinyLang."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()

    # Comparison
    EQUALS = auto()          # =
    EQUALS_EQUALS = auto()   # ==
    NOT_EQUALS = auto()      # !=
    LESS_THAN = auto()       # <
    GREATER_THAN = auto()    # >
    LESS_EQUAL = auto()      # <=
    GREATER_EQUAL = auto()   # >=

    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # Punctuation
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    COMMA = auto()      # ,
    SEMICOLON = auto()  # ;
    COLON = auto()      # :

    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a token from the lexer."""
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """
    Tokenizer for TinyLang.

    Converts source code (string) into a list of tokens.
    """

    KEYWORDS = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'func': TokenType.FUNC,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        """Get current character without advancing."""
        # TODO: Implement
        pass

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at future character."""
        # TODO: Implement
        pass

    def advance(self) -> Optional[str]:
        """Move to next character and return it."""
        # TODO: Implement
        # Remember to track line and column numbers!
        pass

    def skip_whitespace(self):
        """Skip spaces and tabs (but not newlines)."""
        # TODO: Implement
        pass

    def skip_comment(self):
        """Skip single-line comments (e.g., // or #)."""
        # TODO: Implement
        pass

    def read_number(self) -> Token:
        """
        Read a number token (integer or float).

        Challenge: Handle both integers and decimals
        """
        # TODO: Implement
        pass

    def read_string(self) -> Token:
        """
        Read a string literal.

        Challenge: Handle escape sequences like \n, \t, \"
        """
        # TODO: Implement
        pass

    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword.

        Challenge: Check if it's a keyword or identifier
        """
        # TODO: Implement
        pass

    def tokenize(self) -> List[Token]:
        """
        Main tokenization method.

        Challenge: Handle all token types, track position for errors
        """
        # TODO: Implement
        # Hint: Big switch/if-elif on current character
        pass


# =============================================================================
# Part 2: Abstract Syntax Tree (AST) Nodes
# =============================================================================

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    line: int = 0
    column: int = 0


# Literals
@dataclass
class NumberNode(ASTNode):
    value: float


@dataclass
class StringNode(ASTNode):
    value: str


@dataclass
class BooleanNode(ASTNode):
    value: bool


@dataclass
class NullNode(ASTNode):
    pass


# Variables
@dataclass
class VariableNode(ASTNode):
    name: str


@dataclass
class AssignmentNode(ASTNode):
    name: str
    value: ASTNode


# Operations
@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode


# Control Flow
@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: ASTNode


@dataclass
class ForNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: ASTNode


# Functions
@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: ASTNode


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None


# Compound
@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode]


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]


# =============================================================================
# Part 3: Parser
# =============================================================================

class Parser:
    """
    Parser for TinyLang.

    Converts tokens into an Abstract Syntax Tree (AST).
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        """Get current token."""
        # TODO: Implement
        pass

    def peek_token(self, offset: int = 1) -> Token:
        """Look ahead at future token."""
        # TODO: Implement
        pass

    def advance(self) -> Token:
        """Move to next token and return current."""
        # TODO: Implement
        pass

    def expect(self, token_type: TokenType) -> Token:
        """
        Consume token of expected type or raise error.

        Challenge: Provide helpful error messages
        """
        # TODO: Implement
        pass

    def parse(self) -> ProgramNode:
        """
        Parse entire program.

        Challenge: Handle multiple statements
        """
        # TODO: Implement
        pass

    def parse_statement(self) -> ASTNode:
        """
        Parse a single statement.

        Challenge: Dispatch to correct parser based on token type
        """
        # TODO: Implement
        pass

    def parse_if_statement(self) -> IfNode:
        """Parse if-else statement."""
        # TODO: Implement
        pass

    def parse_while_statement(self) -> WhileNode:
        """Parse while loop."""
        # TODO: Implement
        pass

    def parse_function_def(self) -> FunctionDefNode:
        """Parse function definition."""
        # TODO: Implement
        pass

    def parse_return_statement(self) -> ReturnNode:
        """Parse return statement."""
        # TODO: Implement
        pass

    def parse_expression(self) -> ASTNode:
        """
        Parse an expression (lowest precedence level).

        Challenge: Handle operator precedence correctly
        """
        # TODO: Implement
        # This should handle logical OR (lowest precedence)
        pass

    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND expressions."""
        # TODO: Implement
        pass

    def parse_comparison(self) -> ASTNode:
        """Parse comparison expressions (==, !=, <, >, <=, >=)."""
        # TODO: Implement
        pass

    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction."""
        # TODO: Implement
        pass

    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication and division."""
        # TODO: Implement
        pass

    def parse_unary(self) -> ASTNode:
        """Parse unary operators (-, not)."""
        # TODO: Implement
        pass

    def parse_power(self) -> ASTNode:
        """Parse exponentiation (right-associative)."""
        # TODO: Implement
        pass

    def parse_primary(self) -> ASTNode:
        """
        Parse primary expressions (numbers, strings, variables, etc.).

        Challenge: Handle parentheses, function calls, array access
        """
        # TODO: Implement
        pass


# =============================================================================
# Part 4: Environment (Symbol Table)
# =============================================================================

class Environment:
    """
    Environment for variable storage with lexical scoping.

    Supports nested scopes through parent reference.
    """

    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        """Define a new variable in current scope."""
        # TODO: Implement
        pass

    def get(self, name: str) -> Any:
        """
        Get variable value, checking parent scopes if needed.

        Challenge: Implement scope chain lookup
        """
        # TODO: Implement
        pass

    def set(self, name: str, value: Any):
        """
        Set variable value in the scope where it's defined.

        Challenge: Find the right scope
        """
        # TODO: Implement
        pass


# =============================================================================
# Part 5: Evaluator (Interpreter)
# =============================================================================

@dataclass
class Function:
    """Represents a user-defined function."""
    params: List[str]
    body: ASTNode
    closure: Environment  # For lexical scoping!


class ReturnValue(Exception):
    """Exception used to implement return statements."""
    def __init__(self, value):
        self.value = value


class Evaluator:
    """
    Evaluator for TinyLang.

    Walks the AST and executes it.
    """

    def __init__(self):
        self.global_env = Environment()
        self._setup_builtins()

    def _setup_builtins(self):
        """Setup built-in functions."""
        # TODO: Add built-ins like print, len, range, etc.
        self.global_env.define('print', self._builtin_print)
        pass

    def _builtin_print(self, *args):
        """Built-in print function."""
        print(*args)
        return None

    def evaluate(self, node: ASTNode, env: Environment) -> Any:
        """
        Main evaluation method.

        Challenge: Implement visitor pattern for each node type
        """
        # TODO: Implement dispatch to specific evaluate methods

        if isinstance(node, NumberNode):
            return self.evaluate_number(node, env)
        # TODO: Add other node types
        pass

    def evaluate_number(self, node: NumberNode, env: Environment) -> float:
        """Evaluate number literal."""
        return node.value

    def evaluate_string(self, node: StringNode, env: Environment) -> str:
        """Evaluate string literal."""
        # TODO: Implement
        pass

    def evaluate_variable(self, node: VariableNode, env: Environment) -> Any:
        """Evaluate variable reference."""
        # TODO: Implement using environment
        pass

    def evaluate_assignment(self, node: AssignmentNode, env: Environment) -> Any:
        """Evaluate variable assignment."""
        # TODO: Implement
        pass

    def evaluate_binary_op(self, node: BinaryOpNode, env: Environment) -> Any:
        """
        Evaluate binary operation.

        Challenge: Handle +, -, *, /, %, **, ==, !=, <, >, <=, >=, and, or
        """
        # TODO: Implement
        pass

    def evaluate_unary_op(self, node: UnaryOpNode, env: Environment) -> Any:
        """Evaluate unary operation (-, not)."""
        # TODO: Implement
        pass

    def evaluate_if(self, node: IfNode, env: Environment) -> Any:
        """Evaluate if-else statement."""
        # TODO: Implement
        pass

    def evaluate_while(self, node: WhileNode, env: Environment) -> Any:
        """Evaluate while loop."""
        # TODO: Implement
        pass

    def evaluate_function_def(self, node: FunctionDefNode, env: Environment) -> Any:
        """
        Evaluate function definition.

        Challenge: Create Function object with closure!
        """
        # TODO: Implement
        # Remember to capture current environment for closures
        pass

    def evaluate_function_call(self, node: FunctionCallNode, env: Environment) -> Any:
        """
        Evaluate function call.

        Challenge: Create new environment, bind parameters, handle return
        """
        # TODO: Implement
        # 1. Get function object
        # 2. Evaluate arguments
        # 3. Create new environment with function's closure as parent
        # 4. Bind parameters to arguments
        # 5. Execute function body
        # 6. Handle ReturnValue exception
        pass

    def evaluate_return(self, node: ReturnNode, env: Environment) -> Any:
        """Evaluate return statement."""
        # TODO: Implement using ReturnValue exception
        pass

    def evaluate_block(self, node: BlockNode, env: Environment) -> Any:
        """Evaluate block of statements."""
        # TODO: Implement
        pass

    def evaluate_program(self, node: ProgramNode, env: Environment) -> Any:
        """Evaluate entire program."""
        # TODO: Implement
        pass


# =============================================================================
# Part 6: REPL and File Execution
# =============================================================================

class TinyLang:
    """Main interpreter interface."""

    def __init__(self):
        self.evaluator = Evaluator()

    def run(self, source: str) -> Any:
        """
        Execute source code.

        Challenge: Handle errors gracefully with good messages
        """
        try:
            # Tokenize
            lexer = Lexer(source)
            tokens = lexer.tokenize()

            # Parse
            parser = Parser(tokens)
            ast = parser.parse()

            # Evaluate
            result = self.evaluator.evaluate(ast, self.evaluator.global_env)
            return result

        except Exception as e:
            print(f"Error: {e}")
            return None

    def repl(self):
        """
        Read-Eval-Print Loop for interactive use.

        Challenge: Handle multi-line input, show results nicely
        """
        print("TinyLang REPL v1.0")
        print("Type 'exit()' to quit")
        print()

        while True:
            try:
                source = input(">>> ")
                if source.strip() == "exit()":
                    break

                result = self.run(source)
                if result is not None:
                    print(result)

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
            except EOFError:
                break

    def run_file(self, filename: str):
        """Execute a file."""
        with open(filename, 'r') as f:
            source = f.read()
        return self.run(source)


# =============================================================================
# Testing
# =============================================================================

def test_lexer():
    """Test the lexer."""
    code = """
    x = 42
    y = x + 3 * 4
    if y > 50 {
        print("large")
    }
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    print("Tokens:")
    for token in tokens:
        print(f"  {token}")


def test_parser():
    """Test the parser."""
    code = "2 + 3 * 4"

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    print("AST:")
    print(ast)


def test_evaluator():
    """Test the evaluator."""
    test_cases = [
        ("2 + 3", 5),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 / 2", 5),
        ("2 ** 3", 8),
        ("5 > 3", True),
        ("5 == 5", True),
        ("true and false", False),
        ("true or false", True),
        ("not true", False),
    ]

    interpreter = TinyLang()

    print("Testing expressions:")
    for code, expected in test_cases:
        result = interpreter.run(code)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {code} => {result} (expected {expected})")


def test_variables():
    """Test variables."""
    interpreter = TinyLang()

    code = """
    x = 10
    y = 20
    z = x + y
    z
    """

    result = interpreter.run(code)
    print(f"Variables test: {result} (expected 30)")


def test_functions():
    """Test functions."""
    interpreter = TinyLang()

    code = """
    func add(a, b) {
        return a + b
    }

    add(5, 3)
    """

    result = interpreter.run(code)
    print(f"Function test: {result} (expected 8)")


def test_recursion():
    """Test recursive functions."""
    interpreter = TinyLang()

    code = """
    func factorial(n) {
        if n <= 1 {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }

    factorial(5)
    """

    result = interpreter.run(code)
    print(f"Recursion test: {result} (expected 120)")


if __name__ == "__main__":
    print("TinyLang Interpreter: First Principles Implementation")
    print("=" * 80)
    print("\nWork through GUIDE.md to implement each component.")
    print("Run this file to test your implementations.\n")

    # TODO: Uncomment as you implement
    # test_lexer()
    # test_parser()
    # test_evaluator()
    # test_variables()
    # test_functions()
    # test_recursion()

    # Start REPL
    # TinyLang().repl()
