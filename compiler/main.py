"""Ejecutamos el programa."""


import sys
from lexer import Lexer
from parser import Parser


def main():
    if len(sys.argv) > 1:
        tokenize_all_files()

    else:
        print("SCRIPT ERROR: No input files")
        exit()


def tokenize_all_files():
    """Change depending if program has file input."""
    for file in sys.argv[1:]:
        lexer = tokenize_file(file)
        parser = Parser(lexer)
        print(f"##### {file} #####")
        parser()
        print()
        print()


def tokenize_file(path):
    """Get a file path from console."""
    with open(path, 'r') as file:
        data = file.read()

    data += ' '
    lexer = Lexer(data)
    return lexer


if __name__ == '__main__':
    main()
