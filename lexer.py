from enum import Enum
from typing import Tuple


class TokenType(Enum):
    LeftParen = "LeftParen"
    RightParen = "RightParen"
    LeftBrace = "LeftBrace"
    RightBrace = "RightBrace"
    LeftBracket = "LeftBracket"
    RightBracket = "RightBracket"
    Plus = "Plus"
    PlusEqual = "PlusEqual"
    Minus = "Minus"
    MinusEqual = "MinusEqual"
    Star = "Star"
    StarEqual = "StarEqual"
    Slash = "Slash"
    SlashEqual = "SlashEqual"
    Carrot = "Carrot"
    CarrotEqual = "CarrotEqual"
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
    While = "While"
    Return = "Return"
    Colon = "Colon"
    Semicolon = "Semicolon"
    Comma = "Comma"
    Illegal = "Illegal"
    Eof = "Eof"


class Token:
    def __init__(self, type: TokenType, lexeme: str) -> None:
        self.type = type
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f"Token(type: {self.type}, lexeme: '{self.lexeme}')"


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.curr_index = 0
        self.row = 0
        self.col = 0

    def curr(self) -> str:
        return self.source[self.curr_index]

    def advance(self):
        self.curr_index += 1
        self.col += 1

    def is_at_end(self) -> bool:
        return self.curr_index >= len(self.source)

    def next(self) -> Token:
        if self.is_at_end():
            return Token(TokenType.Eof, "Eof")

        match self.curr():
            case '(':
                self.advance()
                return Token(TokenType.LeftParen, "(")
            case ')':
                self.advance()
                return Token(TokenType.RightParen, ")")
            case '[':
                self.advance()
                return Token(TokenType.LeftBrace, "[")
            case ']':
                self.advance()
                return Token(TokenType.RightBrace, "]")
            case '{':
                self.advance()
                return Token(TokenType.LeftBracket, "{")
            case '}':
                self.advance()
                return Token(TokenType.RightBracket, "}")
            case '=':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.EqualEqual, "==")
                return Token(TokenType.Equal, "=")
            case '>':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.GreaterThanEqual, ">=")
                return Token(TokenType.GreaterThan, ">")
            case '<':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.LessThanEqual, "<=")
                return Token(TokenType.LessThan, "<")
            case '+':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.PlusEqual, "+=")
                return Token(TokenType.Plus, "+")
            case '-':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.MinusEqual, "-=")
                return Token(TokenType.Minus, "-")
            case '*':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.StarEqual, "*=")
                return Token(TokenType.Star, "*")
            case '/':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.SlashEqual, "/=")
                return Token(TokenType.Slash, "/")
            case '^':
                self.advance()
                if self.curr() == '=':
                    self.advance()
                    return Token(TokenType.CarrotEqual, "^=")
                return Token(TokenType.Carrot, "^")
            case '"':
                result = self.a_string()
                return Token(TokenType.String, result)
            case i if i.isnumeric():
                result, is_float = self.a_number()
                if is_float:
                    return Token(TokenType.Float, result)
                return Token(TokenType.Int, result)
            case ':':
                self.advance()
                return Token(TokenType.Colon, ":")
            case ';':
                self.advance()
                return Token(TokenType.Semicolon, ";")
            case '\n':
                self.advance()
                self.col = 0
                self.row += 1
                return self.next()
            case ',':
                self.advance()
                return Token(TokenType.Comma, ",")
            case ' ':
                self.advance()
                return self.next()
            case a if a.isalpha():
                identifier = self.an_identifier()
                match identifier:
                    case "and": return Token(TokenType.And, identifier)
                    case "or": return Token(TokenType.Or, identifier)
                    case "if": return Token(TokenType.If, identifier)
                    case "var": return Token(TokenType.Var, identifier)
                    case "const": return Token(TokenType.Const, identifier)
                    case "function": return Token(TokenType.Function, identifier)
                    case "class": return Token(TokenType.Class, identifier)
                    case "for": return Token(TokenType.For, identifier)
                    case "while": return Token(TokenType.While, identifier)
                    case "return": return Token(TokenType.Return, identifier)
                    case _:
                        return Token(TokenType.Identifier, identifier)
            case _:
                illegal = self.curr()
                self.advance()
                return Token(TokenType.Illegal, illegal)

    def a_string(self) -> str:
        self.advance()
        result = ""

        while not self.is_at_end():
            if self.curr() == '"':
                break

            result += self.curr()
            self.advance()

        self.advance()

        return result

    def a_number(self) -> Tuple[str, bool]:
        result, is_float = "", False

        while not self.is_at_end():
            if self.curr() == '.':
                is_float = True
                result += self.curr()
                self.advance()
                continue

            if not self.curr().isnumeric():
                break

            result += self.curr()
            self.advance()

        return result, is_float

    def an_identifier(self) -> str:
        result = ""

        while not self.is_at_end():
            if not self.curr().isalnum():
                break

            result += self.curr()
            self.advance()

        return result
