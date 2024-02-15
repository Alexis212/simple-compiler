"""Analizador Lexico."""


import sys

class Lexer:
    """Divide el texto en tokens."""
    ERR = -1
    ACP = 99
    SIM = [4, 5]
    COM = 7
    STR = 8

    booleanos = ['verdadero', 'falso']
    reservadas = [
        'fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'decimal', 'logico',
        'alfabetico', 'sea', 'si', 'sino', 'para', 'en', 'mientras', 'ciclo', 'regresa',
        'leer', 'interrumpe', 'continua'
    ]

    # M := [+-*%] ; ' ' := ' ' ^ \t ; D := [()\[\]{},:;]
    #     *   ' '  \n   0-9  A-z   _    !    .    M    /    "    \    <>   =    |    &    D
    #     0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16
    # TODO: Agregar simbolos especiales por aceptacion?
    # TODO: Eliminar todos los estados de error?
    transiciones = [
        [ 19,   0,   0,   1,   4,   4,  17,  18,   6,   6,   8, ERR,  11,  13,  15,  16,  18],  # 0
        [ACP, ACP, ACP,   1, ACP, ERR, ERR,   2, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 1 Entero
        [ERR, ERR, ERR,   3, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 2
        [ACP, ACP, ACP,   3, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 3 Decimal
        [ACP, ACP, ACP,   4,   4,   4,   5, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 4 Simbolo
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 5 Simbolo!
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,   7, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 6 Operador Matematico
        [  7,   7, ACP,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # 7 Comentario //
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   9,  10,   8,   8,   8,   8,   8],  # 8
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 9 Cadena de Texto
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8],  # 10
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP,  12, ACP, ACP, ACP],  # 11 Operador Relacional <>
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 12 Operador Relacional !=
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP,  12, ACP, ACP, ACP],  # 13 Operador de Asignación
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 14 Operador Lógico
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  14, ERR, ACP],  # 15 |
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  14, ACP],  # 16 &
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP,  12, ACP, ACP, ACP],  # 17 Operador Lógico !
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP],  # 18 Delimitador
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ACP, ACP]   # 19 Simbolo Especial
    ]

    columnas = [
        ( 1, lambda c: c in [' ', '\t']),
        ( 2, lambda c: c == '\n'),
        ( 3, lambda c: c.isdigit()),
        ( 4, lambda c: c.isalpha()),
        ( 5, lambda c: c == '_'),
        ( 6, lambda c: c == '!'),
        ( 7, lambda c: c == '.'),
        ( 8, lambda c: c in '+-*%'),
        ( 9, lambda c: c == '/'),
        (10, lambda c: c == '"'),
        (11, lambda c: c == '\\'), 
        (12, lambda c: c in '<>'),
        (13, lambda c: c == '='),
        (14, lambda c: c == '|'),
        (15, lambda c: c == '&'),
        (16, lambda c: c in '()[]{},:;')
    ]

    default = 0
    tipos = {
        -1: 'Palabra Reservada',
        -2: 'Booleano',
        -3: 'Identificador',

       # 0: 'Simbolo Especial',
         1: 'Entero',
         3: 'Decimal',
       # 4: 'Simbolo',
       # 5: 'Simbolo',
         6: 'Operador Matematico',
         7: 'Comentario',
         9: 'Cadena de texto',
        11: 'Operador Relacional',
        12: 'Operador Relacional',
        13: 'Operador de Asignación',
        14: 'Operador Lógico',
        17: 'Operador Lógico',
        18: 'Delimitador',
        19: 'Simbolo Especial'
    }

    def __call__(self, entrada):
        # entrada += '\n'  # Aseguramos capturar el ultimo token
        output = []
        token = ''
        lexema = ""
        estado_anterior = 0

        idx = 0
        while idx < len(entrada):
            token = entrada[idx]
            col = self._obtener_columna(token)
            estado = self.transiciones[estado_anterior][col]

            if estado == self.ACP:
                if estado_anterior == self.COM:
                    # tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    # output.append((tipo, "###"))
                    lexema = ""
                    estado = 0
                   
                else:
                    if estado_anterior in self.SIM:
                        estado_anterior = -1 if lexema in self.reservadas else -2 if lexema in self.booleanos else -3
                        
                    tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    output.append((tipo, lexema))
                    lexema = ""

                    idx -= 1
                    estado = 0

            elif estado == self.ERR:
                lexema += token
                output.append(('ERR_0', lexema))
                lexema = ""
                estado = 0

            else:
                # FIXME: Cambia esto por algo que use la tabla?
                if (not token in [' ', '\n', '\t'] and estado != self.COM) or estado == self.STR:
                    lexema += token
                    
            idx += 1
            estado_anterior = estado

        # TODO: Procesar ultimo token?
        return output

    def _obtener_columna(self, c):
        for columna in self.columnas:
            if columna[1](c):
                return columna[0]

        return self.default


def main_file_simple():
    """Get a file path from console."""
    lexer = Lexer()
    path = sys.argv[1]

    with open(path, 'r') as file:
        data = file.read()

    output = lexer(data)
    for token in output:
        print(f"{token[0]}: {token[1]}")


def main_simple():
    """Simple read of user input."""
    lexer = Lexer()

    print("Escribe una entrada. Doble escape para salir.:")
    texto = ""
    entrada = input("> ")
    
    while entrada != '':
        texto += entrada + '\n'
        entrada = input("| ")

    print()
    output = lexer(texto)
    for token in output:
        print(f"{token[0]}: {token[1]}")


if __name__ == '__main__':
    main_simple()
