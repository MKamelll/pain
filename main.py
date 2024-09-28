from lexer import Lexer
from parser import Parser, UnexpectedToken
import sys

VERSION = "0.1.0"


def repl() -> None:
    print(f"Welcome to pain version '{VERSION}'")

    while True:
        line = input("> ").strip("\n")
        if line == ".exit":
            break
        lexer = Lexer(line)
        parser = Parser(lexer)

        try:
            result = parser.parse()
            for tree in result:
                print(tree)
        except UnexpectedToken as error:
            print(error)
            continue


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 1:
        return repl()


if __name__ == "__main__":
    main()
