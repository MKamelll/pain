import lexer
import sys

VERSION = "0.1.0"


def repl() -> None:
    print(f"Welcome to pain version '{VERSION}'")

    while True:
        line = input("> ").strip("\n")
        if line == ".exit":
            break
        lex = lexer.Lexer(line)
        token = lex.next()

        while token.type != lexer.TokenType.Eof:
            print(token)
            token = lex.next()


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 1:
        return repl()


if __name__ == "__main__":
    main()
