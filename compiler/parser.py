"""Analizador Sintactico."""


def show_level(func):
    """Print when the program enter and exit of the function."""
    def inner_function(*args, **kwargs):
        print(f"Enter {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exited {func.__name__}")
        return result

    return inner_function


class Parser:
    def __init__(self, tokens):
        self.lexer = iter(tokens)

        self.tipo = ''
        self.lexema = ''
        self.linea = -1
        self.columna = -1

        self.simbolos = {}
        self.codigo = [[]]  # TODO

    def __call__(self):
        try:
            self.programa()

        except StopIteration:
            print("Compilacion finalizada.")

    def error_tipo(self, esperado):
        print(f"Error Sintactico: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba un {esperado} y recibio un {self.tipo}.")

    def error_lexema(self, esperado):
        print(f"Error Sintactico: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba '{esperado}' y recibio '{self.lexema}'.")

    def next_token(self):
        self.tipo, self.lexema, self.linea, self.columna = next(self.lexer)
        print(f"[{self.tipo}:{self.lexema}]")

    # NOTE: Axioma
    @show_level
    def programa(self):
        self.next_token()

        while self.lexema in ['sea', 'fn'] \
              or self.tipo in ["Identificador"]:
            if self.lexema == 'sea':
                self.definicion()

            if self.lexema == 'fn':
                self.funcion()

            if self.tipo == "Identificador":
                self.asignacion()

            self.next_token()

    @show_level
    def bloque(self):
        self.next_token()
        while self.lexema in ['sea', 'si'] \
              or self.tipo == 'Identificador':
            self.sentencia()

    @show_level
    def sentencia(self):
        if self.lexema == 'sea':
            self.definicion()
            self.next_token()

        if self.lexema == 'si':
            self.si_sino()
            
        if self.tipo == 'Identificador':
            self.asignacion()
            self.next_token()

    @show_level
    def definicion(self):
        self.next_token()
        if self.lexema == "mut":
            self.next_token()

        if self.tipo != "Identificador":
            self.error_tipo("Identificador")

        self.next_token()
        if self.lexema == "[":
            self.next_token()
            if self.tipo not in ['Entero', 'Identificador']:
                self.error_tipo("Identificador o Entero")

            self.next_token()
            if self.lexema == "]":
                self.next_token()

            else:
                self.error_lexema("]")

        if self.lexema != ":":
            self.error_lexema(":")

        self.tipo_variable()

        self.next_token()
        if self.lexema == "=":
            self.valor()
            self.next_token()

        if self.lexema != ";":
            self.error_lexema(";")

    @show_level
    def tipo_variable(self):
        self.next_token()
        if self.lexema not in ['entero', 'decimal', 'logico', 'alfabetico']:
            self.error_tipo("Tipo")

    @show_level
    def valor(self):
        self.next_token()
        if self.lexema == "{":
            self.next_token()
            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_lexema("Literal")

            self.next_token()
            while self.lexema == ",":
                self.next_token()
                if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                    self.error_lexema("Literal")
                self.next_token()

            if self.lexema != "}":
                self.error_lexema("}")

        else:
            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_tipo("literal")

    @show_level
    def funcion(self):
        self.next_token()
        if self.tipo != "Identificador" and self.lexema != "principal":
                self.error_tipo("Identificador")

        self.next_token()
        if self.lexema != "(":
            self.error_lexema("(")

        self.next_token()
        if self.tipo == "Identificador":
            self.next_token()
            if self.lexema != ':':
                self.error_lexema(':')

            self.tipo_variable()

            self.next_token()
            while self.lexema == ",":
                self.next_token()
                if self.tipo != "Identificador":
                    self.error_lexema("self.tipo")

                self.next_token()
                if self.lexema != ':':
                    self.error_lexema(':')

                self.tipo_variable()
                self.next_token()

        if self.lexema != ")":
            self.error_lexema(")")

        self.next_token()
        if self.lexema == "-":
            self.next_token()
            if self.lexema != ">":
                self.error_lexema(">")

            self.tipo_variable()
            self.next_token()

        if self.lexema != "{":
            self.error_lexema("{")

        self.bloque()

        if self.lexema != "}":
            self.error_lexema("}")

    # TODO: Estructuras de control
    # TODO: si, para, mientras
    @show_level
    def si_sino(self):
        self.next_token()
        if self.lexema != '(':
            self.error_lexema('(')

        self.expresion()

        if self.lexema != ')':
            self.error_lexema(')')

        self.next_token()
        if self.lexema == '{':
            self.bloque()

            if self.lexema != '}':
                self.error_lexema('}')

        else:
            self.sentencia()

        # temp = True
        # while temp:
        #     if self.lexema != 'sino':
        #         break

        #     self.next_token()
        #     if self.lexema != 'si':
        #         temp = False
        #         self.next_token()

        #         # if self.lexema != '(':
        #         #     self.error_lexema('(')
       
        #         # self.expresion()
       
        #         # if self.lexema != ')':
        #         #     self.error_lexema(')')

        #         self.next_token()

        #     if self.lexema == '{':
        #         self.bloque()

        #         if self.lexema != '}':
        #             self.error_lexema('}')

        #     else:
        #         self.sentencia()

    # expr_0
    @show_level
    def asignacion(self):
        self.next_token()
        if self.lexema == '[':
            self.next_token()
            if self.tipo not in ["Identificador", "Entero"]:
                self.error_tipo("Identificador o Entero")

            self.next_token()
            if self.lexema != "]":
                self.error_lexema("]")

            self.next_token()

        if self.lexema != '=':
            self.error_lexema("=")

        self.expresion()

        if self.lexema != ';':
            self.error_lexema(";")

    # expr_1
    @show_level
    def expresion(self):
        while self.lexema != ';':
            self.expr_2()

            if self.lexema not in ["&&", "||"]:
                break

    # expr_2
    @show_level
    def expr_2(self):
        while self.lexema != ';':
            self.expr_3()

            if self.tipo != "Operador Relacional":
                break

    # expr_3
    @show_level
    def expr_3(self):
        while self.lexema != ';':
            self.expr_4()

            if self.lexema not in ['+', '-']:
                break

    # expr_4
    @show_level
    def expr_4(self):
        while self.lexema != ';':
            self.expr_5()

            if self.lexema not in ['*', '/', '%']:
                break

    # expr_5
    @show_level
    def expr_5(self):
        while self.lexema != ';':
            self.term()

            if self.lexema not in ['^']:
                break

    # expr_6
    @show_level
    def term(self):
        self.next_token()
        if self.lexema in ['!', '-']:
            self.next_token()

        if self.lexema == '(':
            self.expresion()

            if self.lexema != ')':
                self.error_lexema(')')

        if self.tipo not in ["Identificador", "Entero", "Decimal", "Logico"] \
           and self.lexema != ';' and self.lexema != ')':
            self.error_tipo('literal')

        self.next_token()


if __name__ == '__main__':
    from lexer import Lexer

    text = "fn principal(arg1: entero, arg2: decimal) { sea mul x: entero; x = 10; si (arg1 > x) x = arg1 / arg2; }\n"
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser()
