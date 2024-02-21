"""Analizador Lexico."""


import sys

class Lexer:
    """Divide el texto en tokens."""
    ER1 = -1
    ER2 = -2

    ACP = 99
    SIM = [4, 5]
    COM = 7
    STR = 8

    linea_archivo = 0
    columna_archivo = 0

    booleanos = ['verdadero', 'falso']
    reservadas = [
        'fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'decimal', 'logico',
        'alfabetico', 'sea', 'si', 'sino', 'para', 'en', 'mientras', 'ciclo', 'regresa',
        'leer', 'interrumpe', 'continua'
    ]

    # A^_ := A-z | _ ; M := [+-*%^] ; ' ' := ' ' | \t ; D := [()\[\]{},:;]
    #     *   ' '  \n   0-9  A^_   !    .    M    /    "    \    <>   =    |    &    D
    #     0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
    # TODO: Eliminar todos los estados de error?
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
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  12, ACP, ACP, ACP],  # 13 Operador de Asignación
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 14 Operador Lógico
        [ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ACP, ER2, ER2,  14, ER2, ER2],  # 15 |
        [ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ER2, ACP, ER2, ER2, ER2,  14, ER2],  # 16 &
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  12, ACP, ACP, ACP],  # 17 Operador Lógico !
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
        -2: 'operador logico incompleto', 
        # -3: 'backlash outside of string', 

        # Tipos
         1: 'Entero',
         3: 'Decimal',
         6: 'Operador Matematico',
         7: 'Comentario',
         9: 'Cadena de texto',
        11: 'Operador Relacional',
        12: 'Operador Relacional',
        13: 'Operador de Asignación',
        14: 'Operador Lógico',
        17: 'Operador Lógico',
        18: 'Delimitador',
        19: 'Simbolo Especial',
        20: 'Delimitador',

        # Simbolos
       101: 'Palabra Reservada',
       102: 'Booleano',
       103: 'Identificador'
    }

    def __call__(self, entrada):
        # entrada += '\n'  # Aseguramos capturar el ultimo token
        output = []
        token = ''
        lexema = ""
        estado_anterior = 0

        # TODO: Identificación de errores lexicos
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
                        estado_anterior = 101 if lexema in self.reservadas else 102 if lexema in self.booleanos else 103
                        
                    tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    output.append((tipo, lexema))
                    lexema = ""

                    idx -= 1
                    self.columna_archivo -= 1
                    estado = 0

            # All errors are negative 
            elif estado < 0:
                lexema += token
                output.append(('ERR_0', lexema))
                tipo = self.tipos.get(estado, 'ERR_1')
                print(f"[{self.linea_archivo}][{self.columna_archivo}] Error lexico, {tipo}: {lexema}")

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

            # Contador de lineas
            if token == '\n':
                self.linea_archivo += 1
                self.columna_archivo = 0
                    
            idx += 1
            self.columna_archivo += 1
            estado_anterior = estado

        # TODO: Procesar ultimo token?
        if estado_anterior == self.STR:
            output.append(('ERR_0', lexema))
            print(f"[{self.linea_archivo}][{self.columna_archivo}] Error lexico, cadena nunca finalizada: {lexema}")

        return output

    def _obtener_columna(self, c):
        for columna in self.columnas:
            if columna[1](c):
                return columna[0]

        return self.default


def main():
    """Change depending if program has file input."""
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            output = tokenize_file(file)
            print(f"### {file} ###")
            for token in output:
                print(f"{token[0]}: {token[1]}")
            print()

    else:
        interactive()


def tokenize_file(path):
    """Get a file path from console."""
    lexer = Lexer()

    with open(path, 'r') as file:
        data = file.read()

    data += ' '
    output = lexer(data)
    return output


def interactive():
    """Simple read of user input."""
    lexer = Lexer()

    print("Escribe una entrada. Escape en linea vacia para salir:")
    texto = ""
    entrada = input("> ")
    
    while entrada != '':
        texto += entrada + '\n'
        entrada = input("| ")

    print()
    output += ' '
    output = lexer(texto)
    for token in output:
        print(f"{token[0]}: {token[1]}")


if __name__ == '__main__':
    main()
