from __future__ import annotations
from enum import Enum
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


class FunctionExpr:
    def __init__(self, identifier: Expression, params: List[Expression], body: Expression) -> None:
        self.identifier = identifier
        self.params = params
        self.body = body

    def __str__(self) -> str:
        params = [str(param) for param in self.params]
        return f"FunctionExpr(identifier: {self.identifier}, params: {params}, body: {self.body})"


class ReturnExpr:
    def __init__(self, expr: Expression) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return f"ReturnExpr(expr: {self.expr})"


class Associativity(Enum):
    Left = "Left"
    Right = "Right"


class Operator:
    def __init__(self, op: str, precedence: int, associativity: Associativity) -> None:
        self.op = op
        self.precedence = precedence
        self.associativity = associativity

    def __str__(self) -> str:
        return f"Operator(op: {self.op}, precedence: {self.precedence}, associativity: {self.associativity})"


ALLOWED_OPS = {
    "or":  Operator("or", 0, Associativity.Left),
    "and": Operator("and", 0, Associativity.Left),
    "not": Operator("not", 0, Associativity.Left),

    "==":  Operator("==", 0, Associativity.Left),
    "<":   Operator("<", 1, Associativity.Left),
    "<=":  Operator("<=", 1, Associativity.Left),
    ">":   Operator(">", 1, Associativity.Left),
    ">=":  Operator(">", 1, Associativity.Left),

    "+":   Operator("+", 6, Associativity.Left),
    "-":   Operator("-", 6, Associativity.Left),
    "*":   Operator("*", 7, Associativity.Left),
    "/":   Operator("/", 7, Associativity.Left),
    "^":   Operator("^", 8, Associativity.Right),
}

PrimaryExpr = IntExpr | StringExpr | FloatExpr | IdentifierExpr
Expression = PrimaryExpr | BinaryExpr | BlockExpr | VarExpr | ConstExpr | FunctionExpr | ReturnExpr


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

    def parse_expr(self, min_precedence=0) -> Expression:
        lhs = self.parse_primary()

        while not self.is_at_end():
            op = self.curr_token.lexeme
            op_is_allowed = op in ALLOWED_OPS

            if not op_is_allowed or ALLOWED_OPS[op].precedence < min_precedence:
                break

            curr_op = ALLOWED_OPS[op]
            next_min_precedence = curr_op.precedence

            if curr_op.associativity == Associativity.Right:
                next_min_precedence += 1

            self.advance()
            rhs = self.parse_expr(next_min_precedence)
            lhs = BinaryExpr(lhs, op, rhs)

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

        return self.parse_function_expr()

    def parse_function_expr(self) -> Expression:
        if self.match(TokenType.Function):
            if not self.match(TokenType.Identifier):
                return self.unexpected_token("identifier")
            identifier = IdentifierExpr(self.prev_token.lexeme)

            if not self.match(TokenType.LeftParen):
                return self.unexpected_token("(")

            params = []
            while not self.is_at_end():
                if self.match(TokenType.Comma):
                    continue

                if self.peek(TokenType.RightParen):
                    break
                expr = self.parse_expr()
                params.append(expr)

            if not self.match(TokenType.RightParen):
                return self.unexpected_token(")")

            block = self.parse_block()

            return FunctionExpr(identifier, params, block)

        return self.parse_return_expr()

    def parse_return_expr(self) -> Expression:
        if self.match(TokenType.Return):
            expr = self.parse_expr()

            if not self.match(TokenType.Semicolon):
                return self.unexpected_token(";")
            return ReturnExpr(expr)

        return self.unexpected_token()

    def unexpected_token(self, token_str="primary expression"):
        raise UnexpectedToken(f"""{self.lexer.row}:{
                              self.lexer.col} -> Expected '{token_str}' instead got '{self.curr_token.lexeme}'""")
