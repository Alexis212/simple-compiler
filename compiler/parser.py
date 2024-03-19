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
        self.iter_tokens = iter(tokens)

    def __call__(self):
        try:
            self.programa()

        except StopIteration:
            print("Compilacion finalizada.")

    def error_tipo(self, linea, columna, tipo, lexema, esperado):
        print(f"Error Sintactico: [{linea}:{columna}] '{lexema}'. Se esperaba un {esperado} y recibio un {tipo}.")

    def error_lexema(self, linea, columna, tipo, lexema, esperado):
        print(f"Error Sintactico: [{linea}:{columna}] '{lexema}'. Se esperaba '{esperado}' y recibio '{lexema}'.")

    # NOTE: Axioma
    @show_level
    def programa(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)

        while lexema in ['sea', 'fn']:
            if lexema == 'sea':
                self.variable()

            if lexema == 'fn':
                self.funcion()

            tipo, lexema, linea, columna = next(self.iter_tokens)

    @show_level
    def variable(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema == "mul":
            tipo, lexema, linea, columna = next(self.iter_tokens)

        if tipo != "Identificador":
            self.error_tipo(linea, columna, tipo, lexema, "Identificador")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema == "[":
            tipo, lexema, linea, columna = next(self.iter_tokens)
            if tipo not in ['Entero', 'Identificador']:
                self.error_tipo(linea, columna, tipo, lexema, "Identificador o Entero")

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema == "]":
                tipo, lexema, linea, columna = next(self.iter_tokens)

            else:
                self.error_lexema(linea, columna, tipo, lexema, "]")

        if lexema != ":":
            self.error_lexema(linea, columna, tipo, lexema, ":")

        self.tipo_variable()

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema == "=":
            self.valor()
            tipo, lexema, linea, columna = next(self.iter_tokens)

        if lexema != ";":
            self.error_lexema(linea, columna, tipo, lexema, ";")

    @show_level
    def tipo_variable(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema not in ['entero', 'decimal', 'logico', 'alfabetico']:
            self.error_tipo(linea, columna, tipo, lexema, "tipo")

    @show_level
    def valor(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema == "{":
            tipo, lexema, linea, columna = next(self.iter_tokens)

            if tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_lexema(linea, columna, tipo, lexema, "tipo")

            tipo, lexema, linea, columna = next(self.iter_tokens)
            while lexema == ",":
                tipo, lexema, linea, columna = next(self.iter_tokens)
                if tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                    self.error_lexema(linea, columna, tipo, lexema, "tipo")
                tipo, lexema, linea, columna = next(self.iter_tokens)

            if lexema != "}":
                self.error_lexema(linea, columna, tipo, lexema, "}")

        else:
            if tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_tipo(linea, columna, tipo, lexema, "literal")

    @show_level
    def funcion(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if tipo != "Identificador":
            self.error_tipo(linea, columna, tipo, lexema, "Identificador")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != "(":
            self.error_lexema(linea, columna, tipo, lexema, "(")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if tipo == "Identificador":
            tipo, lexema, linea, columna = next(self.iter_tokens)
            while lexema == ",":
                tipo, lexema, linea, columna = next(self.iter_tokens)
                if tipo != "Identificador":
                    self.error_lexema(linea, columna, tipo, lexema, "tipo")
                tipo, lexema, linea, columna = next(self.iter_tokens)

        if lexema != ")":
            self.error_lexema(linea, columna, tipo, lexema, ")")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != "-":
            self.error_lexema(linea, columna, tipo, lexema, "-")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != ">":
            self.error_lexema(linea, columna, tipo, lexema, ">")

        self.tipo_variable()

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != "{":
            self.error_lexema(linea, columna, tipo, lexema, "{")

        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema == 'sea' or tipo == 'Identificador':
            if lexema == 'sea':
                self.variable()

            if tipo == 'Identificador':
                self.asignacion()

            tipo, lexema, linea, columna = next(self.iter_tokens)

        if lexema != "}":
            self.error_lexema(linea, columna, tipo, lexema, "}")

    @show_level
    def asignacion(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != '=':
            self.error_lexema(linea, columna, tipo, lexema, "=")

        self.expresion()

        # FIXME: Error for missing ';' not detected
        if lexema != ';':
            self.error_lexema(linea, columna, tipo, lexema, ";")

    # expr_0
    @show_level
    def expresion(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_1()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema != '=':
                self.expr_1()
                break

    @show_level
    def expr_1(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_2()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema not in ["&&", "||"]:
                self.expr_2()
                break

    @show_level
    def expr_2(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_3()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if tipo != "Comparison Operator":
                self.expr_3()
                break

    @show_level
    def expr_3(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_4()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema not in ['+', '-']:
                self.expr_4()
                break

    @show_level
    def expr_4(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_5()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema not in ['*', '/', '%']:
                self.expr_5()
                break

    @show_level
    def expr_5(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        while lexema != ';':
            self.expr_6()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if lexema not in ['^']:
                self.expr_6()
                break

    @show_level
    def expr_6(self):
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if token.lexema == '(':
            self.expr_0()

            tipo, lexema, linea, columna = next(self.iter_tokens)
            if token.lexema != ')':
                self.error_lexema(linea, columna, tipo, lexema, ')')

        if tipo not in ["Identificador", "Entero", "Decimal", "Logico"] and lexema != ';':
            self.error_tipo(linea, columna, tipo, lexema, 'literal')
