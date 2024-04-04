"""Analizador Sintactico."""


def show_level(func):
    """Print when the program enter and exit of the function."""
    def inner_function(*args, **kwargs):
        # print(f"Enter {func.__name__}")
        result = func(*args, **kwargs)
        # print(f"Exited {func.__name__}")
        return result

    return inner_function


class Parser:
    """Valida el orden de los tokens (comprueba la gramatica).
    Simbolos: Diccionario de variables y valores.
    Codigo: Mapa de simbolos [clase, tipo, dim1, dim2].
    Clase: [V]ariable, [C]onstante, [I]ndefinido, [P]rocedimiento, [F]uncion, pa[R]ametro.
    Tipo: [E]ntero, [D]ecimal, p[A]labra, [L]ogico, [I]ndefinido.
    Dim1: El tamaño del arreglo, los escalares tiene tamaño 1.
    Dim2: Siempre en 0 por esta vez."""
    def __init__(self, tokens):
        self.lexer = iter(tokens)
        self.tipo_var = {'entero': 'E', 'decimal': 'D', 'alfabetico': 'A', 'logico': 'L'}

        self.tipo = ''
        self.lexema = ''
        self.linea = -1
        self.columna = -1

        self.simbolos = {}
        self.codigo = []

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
        # print(f"[{self.tipo}:{self.lexema}]")

    # NOTE: Axioma
    # @show_level
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

    # @show_level
    def bloque(self):
        self.next_token()
        while self.lexema in ['sea', 'si'] \
              or self.tipo == 'Identificador':
            self.sentencia()

    # @show_level
    def sentencia(self):
        if self.lexema == 'sea':
            self.definicion()
            self.next_token()

        if self.lexema == 'si':
            self.si_sino()

        if self.lexema == 'mientras':
            self.mientras()

        if self.lexema == 'para':
            self.para()
            
        if self.tipo == 'Identificador':
            self.asignacion()
            self.next_token()

    # @show_level
    def definicion(self):
        simbolo = []
        id = "ERROR"
        value = ''

        self.next_token()
        if self.lexema == "mut":
            self.next_token()
            simbolo.append('V')

        else:
            simbolo.append('C')

        if self.tipo != "Identificador":
            self.error_tipo("Identificador")

        else:
            id = self.lexema

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
        simbolo.append( self.tipo_var.get(self.lexema, 'I') )

        self.next_token()
        if self.lexema == "=":
            value = self.valor()
            simbolo.append(1 if not isinstance(value, list) else len(value))
            self.next_token()

        else:
            value = ''
            simbolo.append(1)

        if self.lexema != ";":
            self.error_lexema(";")

        else:
            self.simbolos[id] = value
            simbolo.append(0)
            self.codigo.insert(0, simbolo)

    # @show_level
    def tipo_variable(self):
        self.next_token()
        if self.lexema not in ['entero', 'decimal', 'logico', 'alfabetico']:
            self.error_tipo("Tipo")

    # @show_level
    def valor(self):
        self.next_token()
        if self.lexema == "{":
            values = []

            self.next_token()
            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_lexema("Literal")

            else:
                values.append(self.lexema)

            self.next_token()
            while self.lexema == ",":
                self.next_token()
                if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                    self.error_lexema("Literal")

                else:
                    values.append(self.lexema)
                self.next_token()

            if self.lexema != "}":
                self.error_lexema("}")

            else:
                return values

        else:
            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_tipo("literal")

            else:
                return self.lexema

    # @show_level
    def funcion(self):
        func = []
        func.append('F')

        self.next_token()
        if self.tipo != "Identificador" and self.lexema != "principal":
                self.error_tipo("Identificador")

        self.next_token()
        if self.lexema != "(":
            self.error_lexema("(")

        self.next_token()
        if self.tipo == "Identificador":
            argumento = []
            argumento.append('R')

            self.next_token()
            if self.lexema != ':':
                self.error_lexema(':')

            self.tipo_variable()
            argumento.append( self.tipo_var[self.lexema] )
            argumento.append(1)
            argumento.append(0)

            self.codigo.insert(0, argumento)
            self.next_token()
            while self.lexema == ",":
                argumento = []
                argumento.append('R')

                self.next_token()
                if self.tipo != "Identificador":
                    self.error_lexema("self.tipo")

                self.next_token()
                if self.lexema != ':':
                    self.error_lexema(':')

                self.tipo_variable()
                argumento.append( self.tipo_var[self.lexema] )
                argumento.append(1)
                argumento.append(0)

                self.codigo.insert(0, argumento)
                self.next_token()

        if self.lexema != ")":
            self.error_lexema(")")

        self.next_token()
        if self.lexema == "-":
            self.next_token()
            if self.lexema != ">":
                self.error_lexema(">")

            self.tipo_variable()
            func.append( self.tipo_var[self.lexema] )
            self.next_token()

        else:
            func.append('I')

        if self.lexema != "{":
            self.error_lexema("{")

        self.bloque()

        if self.lexema != "}":
            self.error_lexema("}")

        else:
            func.append(0)
            func.append(0)
            self.codigo.insert(0, func)

    # TODO: Probar para
    # @show_level
    def para(self):
        self.next_token()
        if self.tipo != 'Identificador':
            self.error_tipo('Identificador')

        self.next_token()
        if self.lexema != 'en':
            self.error_lexema('en')

        self.next_token()
        if self.tipo not in ['Identificador', 'Entero']:
            self.error_tipo('Identificador o Entero')

        self.next_token()
        if self.lexema != '.':
            self.error_lexema('.')

        self.next_token()
        if self.lexema != '.':
            self.error_lexema('.')

        self.next_token()
        if self.lexema == '=':
            self.next_token()

        if self.tipo not in ['Identificador', 'Entero']:
            self.error_tipo('Identificador o Entero')

        if self.lexema not in ['inc', 'dec']:
            self.error_lexema('inc o dec')

        self.next_token()
        if self.lexema == '{':
            self.bloque()

            if self.lexema != '}':
                self.error_lexema('}')

            self.next_token()

        else:
            self.sentencia()

    # @show_level
    def mientras(self):
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

            self.next_token()

        else:
            self.sentencia()

    # @show_level
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

            self.next_token()

        else:
            self.sentencia()

        if self.lexema == 'sino':
            self.next_token()
            if self.lexema == 'si':
                self.si_sino()

            if self.lexema == '{':
                self.bloque()
    
                if self.lexema != '}':
                    self.error_lexema('}')
 
            else:
                self.sentencia()

    # expr_0
    # @show_level
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
    # @show_level
    def expresion(self):
        while self.lexema != ';':
            self.expr_2()

            if self.lexema not in ["&&", "||"]:
                break

    # expr_2
    # @show_level
    def expr_2(self):
        while self.lexema != ';':
            self.expr_3()

            if self.tipo != "Operador Relacional":
                break

    # expr_3
    # @show_level
    def expr_3(self):
        while self.lexema != ';':
            self.expr_4()

            if self.lexema not in ['+', '-']:
                break

    # expr_4
    # @show_level
    def expr_4(self):
        while self.lexema != ';':
            self.expr_5()

            if self.lexema not in ['*', '/', '%']:
                break

    # expr_5
    # @show_level
    def expr_5(self):
        while self.lexema != ';':
            self.termino()

            if self.lexema not in ['^']:
                break

    # expr_6
    # @show_level
    def termino(self):
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

    text = 'fn principal(arg1: entero, arg2: decimal) -> entero { sea x: entero = 0; sea y[3]: entero = {1, 2, 3}; sea w: decimal = 4.5; sea z: alfabetico = "a"; }\n'
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser()
    print(parser.simbolos)
    print(parser.codigo)
