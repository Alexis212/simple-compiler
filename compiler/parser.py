"""Analizador Sintactico."""


def show_level(func):
    """Print when the program enter and exit of the function."""
    def inner_function(*args, **kwargs):
        print(f"Enter {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exited {func.__name__}")
        return result

    return inner_function


# TODO: if, mientras, para code
class Parser:
    """Valida el orden de los tokens (comprueba la gramatica).
    Simbolos: Diccionario de variables y valores.
    Codigo: Mapa de simbolos [clase, tipo, dim1, dim2].
    Clase: [V]ariable, [C]onstante, [I]ndefinido, [P]rocedimiento, [F]uncion, pa[R]ametro.
    Tipo: [E]ntero, [D]ecimal, p[A]labra, [L]ogico, [I]ndefinido.
    Dim1: El tamaño del arreglo, los escalares tiene tamaño 1.
    Dim2: Siempre en 0 por esta vez.
    OPR: Primitivas
    exit 0, 0
    regresa 0, 1
    +  0, 2
    -  0, 3
    *  0, 4
    /  0, 5
    %  0, 6
    ^  0, 7
    -u 0, 8
    <  0, 9
    >  0, 10
    <= 0, 11
    >= 0, 12
    != 0, 13
    == 0, 14
    && 0, 15
    || 0, 16
    !  0, 17
    tpm 0, 18
    leer 0, 19
    imprimeln 20
    imprimeln! 21"""
    def __init__(self, tokens):
        self.lexer = iter(tokens)
        self.tipo_var = {'entero': 'E', 'decimal': 'D', 'alfabetico': 'A', 'logico': 'L'}
        self.opr_num = {'+': 2, '-': 3, '*': 4, '/': 5, '%': 6, '^': 7, '<': 9, '>': 10,
                        '<=': 11, '>=': 12, '!=': 13, '==': 14, '&&': 15, '||': 16}

        self.tipo = ''
        self.lexema = ''
        self.linea = -1
        self.columna = -1

        self.reg_inc = 0
        self.line_inc = 0

        self.mapa_simbolos = {}
        self.codigo = []

    def __call__(self):
        try:
            self.programa()

        except StopIteration:
            self.add_line("OPR 0, 0")
            self.mapa_simbolos['_P'] = ['I', 'I', '1', '0']
            print("Compilacion finalizada.")
            print(self.mapa_simbolos)
            print(self.codigo)

    def error_tipo(self, esperado):
        print(f"Error Sintactico: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba un {esperado} y recibio un {self.tipo}.")

    def error_lexema(self, esperado):
        print(f"Error Sintactico: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba '{esperado}' y recibio '{self.lexema}'.")

    def next_token(self):
        self.tipo, self.lexema, self.linea, self.columna = next(self.lexer)

        if self.tipo == 'Comentario':
            self.next_token()

        else:
            print(f"[{self.tipo}:{self.lexema}]")

    def add_line(self, line):
        self.line_inc += 1
        line = f"{self.line_inc} {line}\n"
        self.codigo.append(line)
        print(f":-{line}")

    def add_var(self, var, value):
        self.add_line(f"LIT {value}, 0")
        self.add_line(f"STO {var}, 0")

    def make_tab(self):
        lines = []
        for x, y in self.mapa_simbolos.items():
            line = ', '.join(str(x) for x in y)
            lines.append(f"{x}, {line},#\n")
        return lines

    def make_file(self, name='out'):
        with open(name + '.eje', 'w') as f:
            f.writelines(self.make_tab())
            f.write('@\n')
            f.writelines(self.codigo)

    # NOTE: Axioma
    @show_level
    def programa(self):
        self.next_token()

        while self.lexema in ['sea', 'fn'] \
              or self.tipo in ["Identificador"]:
            if self.lexema == 'sea':
                self.declaracion()

            if self.lexema == 'fn':
                self.funcion()

            if self.tipo == "Identificador":
                temp = self.lexema
                self.next_token()
                self.asignacion(temp)

            self.next_token()

    @show_level
    def bloque(self):
        self.next_token()
        while self.lexema in ['sea', 'si', 'para', 'mientras', 'tpm', 'leer',
                              'imprimeln', 'imprimeln!', 'regresa', 'ciclo'] \
              or self.tipo == 'Identificador':
            self.sentencia()

    @show_level
    def sentencia(self):
        if self.lexema == 'sea':
            self.declaracion()
            self.next_token()

        if self.lexema == 'si':
            self.si_sino()

        if self.lexema == 'mientras':
            self.mientras()

        if self.lexema == 'para':
            self.para()

        if self.lexema == 'ciclo':
            self.ciclo()

        if self.lexema == 'regresa':
            self.expresion()
            if self.lexema != ';':
                self.error_lexema(';')

            self.next_token()

        if self.lexema == 'tpm':
            self.next_token()
            if self.lexema != ';':
                self.error_lexema(';')

            else:
                self.add_line("OPR 0, 18")
                self.next_token()

        if self.lexema in ['imprimeln', 'imprimeln!']:
            new_line = self.lexema == 'imprimeln!'
            self.imprime(new_line)

        if self.lexema == 'leer':
            self.next_token()
            if self.lexema != '(':
                self.error_lexema('(')

            self.next_token()
            if self.tipo != 'Identificador':
                self.error_tipo('Identificador')

            self.add_line(f"OPR {self.lexema}, 19")

            self.next_token()
            if self.lexema != ')':
                self.error_lexema(')')

            self.next_token()
            if self.lexema != ';':
                self.error_lexema(';')
            self.next_token()
             
        if self.tipo == 'Identificador':
            temp = self.lexema
            self.next_token()

            if self.lexema == '=' or self.lexema == '[':
                self.asignacion(temp)

            if self.lexema == '(':
                self.next_token()
                if self.tipo in ["Entero", "Decimal", "Logico", "Alfabetico", "Identificador"]:
                    self.next_token()

                    while self.lexema == ",":
                        self.next_token()

                        if self.tipo not in ["Entero", "Decimal", "Logico", "Alfabetico", "Identificador"]:
                            self.error_tipo("literal o identificador")

                        self.next_token()

                if self.lexema != ")":
                   self.error_lexema(")")

                self.next_token()
                if self.lexema != ";":
                   self.error_lexema(";")

            self.next_token()

        # else:
        #     self.error_tipo('Palabra Reservada')
        #     self.next_token()

    @show_level
    def declaracion(self):
        simbolo = []
        var = []
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
            var.append(self.lexema)

        self.next_token()
        if self.lexema == "[":
            self.expresion()

            if self.lexema != "]":
                self.error_lexema("]")

        while self.lexema == ',':
            self.next_token()
            if self.tipo != "Identificador":
                self.error_tipo("Identificador")
    
            else:
                var.append(self.lexema)
    
            self.next_token()
            if self.lexema == "[":
                self.expresion()

                if self.lexema != "]":
                    self.error_lexema("]")

        # TODO: Esto podr�a dar error
        if self.lexema == ']':
            self.next_token()
    
        if self.lexema != ":":
            self.error_lexema(":")

        self.tipo_variable()
        tipo = self.tipo_var.get(self.lexema, 'I')
        simbolo.append(tipo)

        self.next_token()
        if self.lexema == "=":
            value = self.valor()
            simbolo.append(0 if not isinstance(value, list) else len(value))
            self.next_token()

        else:
            value = {'E': 0, 'D': 0.0, 'A': '""', 'L': 'F', 'I': None}[tipo]
            # FIXME: Detectar el largo de cada vector individualmente
            simbolo.append(0)

        if self.lexema != ";":
            self.error_lexema(";")

        else:
            simbolo.append(0)
            for i, val in enumerate(value):
                self.add_line(f"LIT {i}, 0")
                self.add_line(f"LIT {val}, 0")
                self.add_line(f"STO {var[0]}, 0")
                self.mapa_simbolos[var[0]] = simbolo

    @show_level
    def imprime(self, new_line):
        self.next_token()
        if self.lexema != '(':
            self.error_lexema('(')

        self.expresion()

        while self.lexema == ',':
            self.expresion()

        if self.lexema != ')':
            self.error_lexema(')')

        self.next_token()
        if self.lexema != ';':
            self.error_lexema(';')
        self.next_token()

    @show_level
    def tipo_variable(self):
        self.next_token()
        if self.lexema not in ['entero', 'decimal', 'logico', 'alfabetico']:
            self.error_tipo("Tipo")

    @show_level
    def valor(self):
        self.next_token()
        if self.lexema == "[":
            values = []

            self.next_token()
            if self.lexema == '-':
                self.next_token()

            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_tipo("Literal")

            else:
                values.append(self.lexema)

            self.next_token()
            while self.lexema == ",":
                self.next_token()
                if self.lexema == '-':
                    self.next_token()

                if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                    self.error_tipo("Literal")

                else:
                    values.append(self.lexema)
                self.next_token()

            if self.lexema != "]":
                self.error_lexema("]")

            else:
                return values

        else:
            if self.lexema == '-':
                self.next_token()

            if self.tipo not in ['Entero', 'Decimal', 'Alfabetico', 'Logico']:
                self.error_tipo("literal")

            else:
                return self.lexema

    @show_level
    def funcion(self):
        func = []
        func.append('F')

        self.next_token()
        if self.tipo != "Identificador" and self.lexema != "principal":
                self.error_tipo("Identificador")

        func_id = self.lexema
        self.next_token()
        if self.lexema != "(":
            self.error_lexema("(")

        self.next_token()
        if self.tipo == "Identificador":
            id = self.lexema
            argumento = []
            argumento.append('R')

            self.next_token()
            if self.lexema != ':':
                self.error_lexema(':')

            self.tipo_variable()
            arg_type = self.tipo_var[self.lexema]
            func_id += f"${arg_type}"
            argumento.append(arg_type)
            argumento.append(1)
            argumento.append(0)

            self.mapa_simbolos[id] = argumento
            self.next_token()
            while self.lexema == ",":
                argumento = []
                argumento.append('R')

                self.next_token()
                if self.tipo != "Identificador":
                    self.error_lexema("self.tipo")

                id = self.lexema
                self.next_token()
                if self.lexema != ':':
                    self.error_lexema(':')

                self.tipo_variable()
                arg_type = self.tipo_var[self.lexema]
                func_id += f"${arg_type}"
                argumento.append(arg_type)
                argumento.append(0)
                argumento.append(0)

                self.mapa_simbolos[id] = argumento
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
            func.append(self.line_inc)
            func.append(0)
            func_id = '_' + func_id
            self.mapa_simbolos[func_id] = func

    # TODO: A�adir expresiones en para
    @show_level
    def para(self):
        self.next_token()
        if self.tipo != 'Identificador':
            self.error_tipo('Identificador')

        self.next_token()
        if self.lexema != 'en':
            self.error_lexema('en')

        self.expresion()

        if self.lexema != '..':
            self.error_lexema('..')

        # self.next_token()
        # if self.lexema == '=':
        #     self.next_token()

        self.expresion()

        if self.lexema == 'inc':
            self.next_token()

            if self.lexema == '-':
                self.next_token()

            if self.tipo == 'Entero':
                self.next_token()

        if self.lexema == '{':
            self.bloque()

            if self.lexema != '}':
                self.error_lexema('}')

            self.next_token()

        else:
            self.sentencia()

    # Do - While
    @show_level
    def ciclo(self):
        self.next_token()
        if self.lexema == '{':
            self.bloque()

            if self.lexema != '}':
                self.error_lexema('}')

        else:
            self.error_lexema('{')

        self.next_token()
        if self.lexema != 'mientras':
            self.error_lexema('mientras')

        self.expresion()

        if self.lexema != ';':
            self.error_lexema(';')

        self.next_token()

    @show_level
    def mientras(self):
        self.next_token()
        self.expresion()

        if self.lexema == '{':
            self.bloque()

            if self.lexema != '}':
                self.error_lexema('}')

            self.next_token()

        else:
            self.sentencia()

    @show_level
    def si_sino(self):
        self.expresion()

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

                self.next_token()
 
            else:
                self.sentencia()

    # expr_-1
    @show_level
    def asignacion(self, id):
        if self.lexema == '[':
            self.expresion()

            if self.lexema != "]":
                self.error_lexema("]")

            self.next_token()

        if self.lexema != '=':
            self.error_lexema("=")

        self.expresion()
        self.add_line(f'STO {id}, 0')

        if self.lexema != ';':
            self.error_lexema(";")

    # TODO: Marcar error de falta de ) o ]
    @show_level
    def expresion(self):
        self.disyuncion()

    @show_level
    def disyuncion(self):
        """||."""
        self.conjuncion()

        while self.lexema in ['||', 'o']:
            self.conjuncion()
            self.add_line(f"OPR 0, 16")

    # expr_2
    @show_level
    def conjuncion(self):
        """&&."""
        self.logico()

        while self.lexema in ['&&', 'y']:
            self.logico()
            self.add_line(f"OPR 0, 15")

    # expr_3
    @show_level
    def logico(self):
        """<, >, ==, !=, <=, >=."""
        self.adicion()

        while self.lexema in ['<', '>', '==', '!=', '<=', '>=']:
            temp = self.lexema
            self.adicion()
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_4
    @show_level
    def adicion(self):
        """+-."""
        self.producto()

        while self.lexema in '+-':
            temp = self.lexema
            self.producto()
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_5
    @show_level
    def producto(self):
        """*/%."""
        self.exponente()

        while self.lexema in '*/%':
            temp = self.lexema
            self.exponente()
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_6
    @show_level
    def exponente(self):
        """^."""
        self.termino()

        while self.lexema == '^':
            self.termino()
            self.add_line(f"OPR 0, 7")

    # FIXME: Generaci�n de c�digo
    # expr_7
    @show_level
    def termino(self):
        self.next_token()

        # TODO: Esperar a que no cause problemas y tegas que cambiarlo
        if self.lexema == '=':
            self.next_token()

        unary = 0
        if self.lexema in '-!':
            unary = 8 if self.lexema == '-' else 17
            self.next_token()

        if self.lexema == '(':
            self.expresion()

            if self.lexema != ')':
                self.error_lexema(')')

            else:
                self.next_token()

        elif self.tipo == 'Identificador':
            self.next_token()
            if self.lexema == '[':
                self.expresion()

                if self.lexema != ']':
                    self.error_lexema(']')
                    # Insetar ID ; Cargar variable

                else:
                    self.next_token()

            if self.lexema == '(':
                self.expresion()

                while self.lexema == ',':
                    self.expresion()

                if self.lexema != ')':
                    self.error_lexema(')')

                else:
                    self.next_token()

            else:
                self.add_line(f'LOD {self.lexema}, 0')

        elif self.tipo in ['Entero', 'Decimal', 'Alfabetico']:
            self.add_line(f'LIT {self.lexema}, 0')
            self.next_token()

        elif self.tipo == 'Logico':
            # FIXME: Poner los booleanos bien [T, F]
            self.add_line(f'LIT {self.lexema[0].capitalize()}, 0')
            self.next_token()

        if unary:
            self.add_line(f'OPR 0, {unary}')
        

if __name__ == '__main__':
    from lexer import Lexer

    text = 'fn principal() { sea mut x: entero; x = 2 + 2; }\n'
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser()
