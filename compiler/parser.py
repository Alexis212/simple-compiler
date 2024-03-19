"""Analizador Sintactico."""


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
    def programa(self):
        print("Entro a programa")
        tipo, lexema, linea, columna = next(self.iter_tokens)

        while lexema in ['sea', 'fn']:
            if lexema == 'sea':
                self.variable()

            if lexema == 'fn':
                self.funcion()

            tipo, lexema, linea, columna = next(self.iter_tokens)

        print("Salio de programa")

    def variable(self):
        print("Entro a variable")
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
        print("Salio de variable")

    def tipo_variable(self):
        print("Entro a tipo")
        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema not in ['entero', 'decimal', 'logico', 'alfabetico']:
            self.error_tipo(linea, columna, tipo, lexema, "tipo")
        print("Salio de tipo")

    def valor(self):
        print("Entro a literal")
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
        print("Salio de literal")

    def funcion(self):
        print("Entro a funcion")
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

        # TODO: Sentences inside functions

        tipo, lexema, linea, columna = next(self.iter_tokens)
        if lexema != "}":
            self.error_lexema(linea, columna, tipo, lexema, "}")
        print("Salio de funcion")

    def expresion():
        pass
