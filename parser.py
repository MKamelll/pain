from __future__ import annotations
from typing import List
from lexer import Lexer, TokenType


class UnexpectedToken(Exception):
    pass


class IntExpr:
    def __init__(self, val: int) -> None:
        self.val = val

    def __str__(self) -> str:
        return f"IntExpr(val: {self.val})"


class StringExpr:
    def __init__(self, val: str) -> None:
        self.val = val

    def __str__(self) -> str:
        return f"StringExpr(val: '{self.val}')"


class FloatExpr:
    def __init__(self, val: float) -> None:
        self.val = val

    def __str__(self) -> str:
        return f"FloatExpr(val: {self.val})"


class IdentifierExpr:
    def __init__(self, val: str) -> None:
        self.val = val

    def __str__(self) -> str:
        return f"IdentifierExpr(val: '{self.val}')"


class BinaryExpr:
    def __init__(self, lhs: Expression, op: str, rhs: Expression) -> None:
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self) -> str:
        return f"BinaryExpr(lhs: {self.lhs}, op: {self.op}, rhs: {self.rhs})"


class BlockExpr:
    def __init__(self, exprs: List[Expression]) -> None:
        self.exprs = exprs

    def __str__(self) -> str:
        exprs = [str(expr) for expr in self.exprs]
        return f"BlockExpr(exprs: {exprs})"


class VarExpr:
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"VarExpr(lhs: {self.lhs}, rhs: {self.rhs})"


class ConstExpr:
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"ConstExpr(lhs: {self.lhs}, rhs: {self.rhs})"


PrimaryExpr = IntExpr | StringExpr | FloatExpr | IdentifierExpr
Expression = PrimaryExpr | BinaryExpr | BlockExpr | VarExpr | ConstExpr


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.curr_token = self.lexer.next()
        self.prev_token = self.curr_token
        self.parsed_trees: List[Expression] = []

    def advance(self) -> None:
        self.prev_token = self.curr_token
        self.curr_token = self.lexer.next()

    def is_at_end(self) -> bool:
        return self.curr_token.type == TokenType.Eof

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.curr_token.type == type:
                self.advance()
                return True
        return False

    def peek(self, type: TokenType) -> bool:
        return self.curr_token.type == type

    def parse(self) -> List[Expression]:
        if self.is_at_end():
            return self.parsed_trees

        expr = self.parse_expr()
        self.parsed_trees.append(expr)

        return self.parse()

    def parse_expr(self) -> Expression:
        lhs = self.parse_primary()
        return lhs

    def parse_primary(self) -> Expression:
        return self.parse_int()

    def parse_int(self) -> Expression:
        if self.match(TokenType.Int):
            return IntExpr(int(self.prev_token.lexeme))

        return self.parse_float()

    def parse_float(self) -> Expression:
        if self.match(TokenType.Float):
            return FloatExpr(float(self.prev_token.lexeme))

        return self.parse_string()

    def parse_string(self) -> Expression:
        if self.match(TokenType.String):
            return StringExpr(self.prev_token.lexeme)

        return self.parse_identifier()

    def parse_identifier(self) -> Expression:
        if self.match(TokenType.Identifier):
            return IdentifierExpr(self.prev_token.lexeme)

        return self.parse_var()

    def parse_var(self) -> Expression:
        if self.match(TokenType.Var):
            lhs = self.parse_expr()
            if not type(lhs) is IdentifierExpr:
                return self.unexpected_token("identifier")
            if not self.match(TokenType.Equal):
                return self.unexpected_token("=")
            rhs = self.parse_expr()
            if not self.match(TokenType.Semicolon):
                return self.unexpected_token(";")

            return VarExpr(lhs, rhs)

        return self.parse_const()

    def parse_const(self) -> Expression:
        if self.match(TokenType.Const):
            lhs = self.parse_expr()
            if not type(lhs) is IdentifierExpr:
                return self.unexpected_token("identifier")
            if not self.match(TokenType.Equal):
                return self.unexpected_token("=")
            rhs = self.parse_expr()
            if not self.match(TokenType.Semicolon):
                return self.unexpected_token(";")

            return ConstExpr(lhs, rhs)

        return self.parse_block()

    def parse_block(self) -> Expression:
        if self.match(TokenType.LeftBracket):
            exprs = []
            while not self.is_at_end():
                if self.peek(TokenType.RightBracket):
                    break
                exprs.append(self.parse_expr())

            if not self.match(TokenType.RightBracket):
                return self.unexpected_token("}")

            return BlockExpr(exprs)

        return self.unexpected_token()

    def unexpected_token(self, token_str="primary expression"):
        raise UnexpectedToken(f"""{self.lexer.row}:{
                              self.lexer.col} -> Expected '{token_str}' instead got '{self.curr_token.lexeme}'""")
