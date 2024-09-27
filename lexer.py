from enum import Enum


class TokenType(Enum):
    LeftParen = "LeftParen"
    RightParen = "RightParen"
    LeftBrace = "LeftBrace"
    RightBrace = "RightBrace"
    LeftBracket = "LeftBracket"
    RightBracket = "RightBracket"
    Plus = "Plus"
    PlusEqual = "PlusEqual"
    Equal = "Equal"
    EqualEqual = "EqualEqual"
    GreaterThan = "GreaterThan"
    GreaterThanEqual = "GreaterThanEqual"
    LessThan = "LessThan"
    LessThanEqual = "LessThanEqual"
    And = "And"
    Or = "Or"
    Not = "Not"
    String = "String"
    Int = "Int"
    Float = "Float"
    Identifier = "Identifier"
    Var = "Var"
    Const = "Const"
    Function = "Function"
    Class = "Class"
    If = "If"
    For = "For"
    Return = "Return"
    Colon = "Colon"
    Semicolon = "Semicolon"
    Illegal = "Illegal"
    Eof = "Eof"


class Token:
    def __init__(self, type: TokenType, lexeme: str) -> None:
        self.type = type
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f"Token(type: {self.type}, lexeme: '{self.lexeme}')"
