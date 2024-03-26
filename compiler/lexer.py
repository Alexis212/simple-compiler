"""Analizador Lexico."""

class Token:
    """Estructura de tokens."""

    def __init__(self, tipo, lexema):
        self.tipo = tipo
        self.lexema = lexema

    def __repr__(self):
        return f"<{self.tipo}: {self.lexema}>"


class Lexer:
    """Divide el texto en tokens."""
    ER1 = -1

    ACP = 99
    SIM = [4, 5]
    COM = 7
    STR = 8

    linea = 1
    columna = 0

    booleanos = ['verdadero', 'falso']
    reservadas = [
        'fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'decimal', 'logico',
        'alfabetico', 'sea', 'si', 'sino', 'para', 'en', 'mientras', 'ciclo', 'regresa',
        'leer', 'interrumpe', 'continua', 'mut'
    ]

    # A^_ := A-z | _ ; M := [+-*%^] ; ' ' := ' ' | \t ; D := [()\[\]{},:;]
    #     *   ' '  \n   0-9  A^_   !    .    M    /    "    \    <>   =    |    &    D
    #     0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
    transiciones = [
        [ 19,   0,   0,   1,   4,  17,  20,   6,   6,   8,  19,  11,  13,  15,  16,  18],  # 0
        [ACP, ACP, ACP,   1, ACP, ACP,   2, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 1 Entero
        [ER1, ER1, ER1,   3, ER1, ER1, ER1, ER1, ER1, ER1, ER1, ER1, ER1, ER1, ER1, ER1],  # 2
        [ACP, ACP, ACP,   3, ACP, ACP, ER1, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 3 Decimal
        [ACP, ACP, ACP,   4,   4,   5, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 4 Simbolo
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 5 Simbolo!
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,   7, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 6 Operador Matematico
        [  7,   7, ACP,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # 7 Comentario //
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   9,  10,   8,   8,   8,   8,   8],  # 8
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 9 Cadena de Texto
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8],  # 10
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  12, ACP, ACP, ACP],  # 11 Operador Relacional <>
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 12 Operador Relacional !=
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  12, ACP, ACP, ACP],  # 13 Operador de Asignacion
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 14 Operador Logico
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  14, ACP, ACP],  # 15 Simbolo Especial |
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  14, ACP],  # 16 Simbolo Especial &
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  12, ACP, ACP, ACP],  # 17 Operador Logico !
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 18 Delimitador
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 19 Simbolo Especial
        [ACP, ACP, ACP, ER1, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP]   # 20 Delimitador .
    ]

    columnas = [
        ( 1, lambda c: c in [' ', '\t']),
        ( 2, lambda c: c == '\n'),
        ( 3, lambda c: c.isdigit()),
        ( 4, lambda c: c.isalpha() or c == '_'),
        ( 5, lambda c: c == '!'),
        ( 6, lambda c: c == '.'),
        ( 7, lambda c: c in '+-*%^'),
        ( 8, lambda c: c == '/'),
        ( 9, lambda c: c == '"'),
        (10, lambda c: c == '\\'), 
        (11, lambda c: c in '<>'),
        (12, lambda c: c == '='),
        (13, lambda c: c == '|'),
        (14, lambda c: c == '&'),
        (15, lambda c: c in '()[]{},:;')
    ]

    default = 0
    tipos = {
        # Errores
         -1: 'decimal incompleto', 
         # -2: 'cadena no finalizada', 

        # Tipos
          1: 'Entero',
          3: 'Decimal',
          6: 'Operador Matematico',
          7: 'Comentario',
          9: 'Alfabetico',
         11: 'Operador Relacional',
         12: 'Operador Relacional',
         13: 'Operador de Asignacion',
         14: 'Operador Logico',
         15: 'Simbolo Especial',
         16: 'Simbolo Especial',
         17: 'Operador Logico',
         18: 'Delimitador',
         19: 'Simbolo Especial',
         20: 'Delimitador',

        # Simbolos
        101: 'Palabra Reservada',
        102: 'Logico',
        103: 'Identificador'
    }

    def __init__(self, entrada):
        self.entrada = entrada

    def __iter__(self):
        token = ''
        lexema = ""
        estado_anterior = 0

        idx = 0
        while idx < len(self.entrada):
            token = self.entrada[idx]
            col = self._obtener_columna(token)
            estado = self.transiciones[estado_anterior][col]

            # Contador de lineas
            self.columna += 1
            if estado == self.STR or estado == self.COM or estado == 0:
                if token == '\n':
                    self.linea += 1
                    self.columna = 0

            if estado == self.ACP:
                if estado_anterior == self.COM:
                    tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    # yield tipo, lexema, self.linea, self.columna-1
                    lexema = ""
                    estado = 0

                else:
                    if estado_anterior in self.SIM:
                        estado_anterior = 101 if lexema in self.reservadas else 102 if lexema in self.booleanos else 103
                        
                    tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    yield tipo, lexema, self.linea, self.columna-1
                    lexema = ""

                    idx -= 1
                    self.columna -= 1
                    estado = 0

            # All errors are negative 
            elif estado < 0:
                lexema += token
                yield tipo, lexema, self.linea, self.columna-1
                tipo = self.tipos.get(estado, 'ERR_1')
                print(f"[{self.linea}][{self.columna-1}] Error lexico, {tipo}: {lexema}")

                lexema = ""
                estado = 0

            else:
                if estado_anterior == self.STR:
                    if token != '\\':
                        lexema += token

                elif estado_anterior == 10:
                    if token == 'n':
                        token = '\n'

                    elif token == 't':
                        token = '\t'

                    lexema += token

                else:
                    if estado != self.COM and token not in [' ', '\n', '\t']:
                        lexema += token

            idx += 1
            estado_anterior = estado

        # TODO: Procesar ultimo token?
        if estado_anterior == self.STR:
            yield tipo, lexema, self.linea, self.columna-1
            print(f"[{self.linea}][{self.columna-1}] Error lexico, cadena nunca finalizada: {lexema}")

        # yield None

    def _obtener_columna(self, c):
        for columna in self.columnas:
            if columna[1](c):
                return columna[0]

        return self.default


if __name__ == '__main__':
    text = "fn principal(arg1, arg2, arg3) { sea mul x: entero; x = (2)*(4-10); }\n"
    lexer = Lexer(text)

    for tipo, lexema, linea, columna in lexer:
        print(f"[{linea}:{columna}] Tipo: {tipo}, Lexema: {lexema}")
