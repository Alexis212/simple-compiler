"""Analizador Lexico."""


class Lexer:
    """Divide el texto en tokens."""
    ERR = -1
    ACP = 99
    SIM = [4, 15]
    COM = 6

    booleanos = ['verdadero', 'falso']
    reservadas = [
        'fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'decimal', 'logico',
        'alfabetico', 'sea', 'si', 'sino', 'para', 'en', 'mientras', 'ciclo', 'regresa',
        'leer', 'interrumpe', 'continua'
    ]

    # M := [+-*%] ; ' ' := ' ' ^ \t
    #    ' '  \n   0-9  a-Z   _    .    M    /    &    |    !    <>   =    ()
    #     0    1    2    3    4    5    6    7    8    9    10   11   12   13
    transiciones = [
        [  0,   0,   1,   4,   4, ERR,   5,   5,   7,   9,  12,  11,  13,  16],  #  0
        [ACP, ACP,   1, ACP, ACP, 2,   ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  #  1 Entero
        [ERR, ERR,   3, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  #  2 .
        [ACP, ACP,   3, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  #  3 Decimal
        [ACP, ACP,   4,   4,   4, ERR, ACP, ACP, ACP, ACP,  15, ACP, ACP, ACP],  #  4 Simbolo
        [ACP, ACP, ACP, ACP, ACP, ERR, ACP,   6, ACP, ACP, ACP, ACP, ACP, ACP],  #  5 Matematico
        [  6, ACP,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6, ACP],  #  6 Comentario
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,   8, ERR, ERR, ERR, ERR, ERR],  #  7 &
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  #  8 Lógico &
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  10, ERR, ERR, ERR, ERR],  #  9 |
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 10 Lógico |
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  14, ACP],  # 11 Comparación <>
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  14, ACP],  # 12 Lógico !
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  14, ACP],  # 13 Asignación =
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 14 Comparación !=
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP]   # 15 Simbolo!
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP]   # 16 Par ()
    ]

    columnas = [
        ( 0, lambda c: c in [' ', '\t']),
        ( 1, lambda c: c == '\n'),
        ( 2, lambda c: c.isdigit()),
        ( 3, lambda c: c.isalpha()),
        ( 4, lambda c: c == '_'),
        ( 5, lambda c: c == '.'),
        ( 6, lambda c: c in ['+', '-', '*', '%']),
        ( 7, lambda c: c == '/'),
        ( 8, lambda c: c == '&'),
        ( 9, lambda c: c == '|'),
        (10, lambda c: c == '!'),
        (11, lambda c: c in ['<', '>']),
        (12, lambda c: c == '='),
        (13, lambda c: c in ['(', ')', '[', ']', '{', '}'])
    ]

    tipos = {
        -1: 'Palabra Reservada',
        -2: 'Booleano',
        -3: 'Identificador',

        1:  'Entero',
        3:  'Decimal',
        5:  'Operador Matematico',
        6:  'Comentario',
        8:  'Operador Lógico',
        10: 'Operador Lógico',
        11: 'Operador de Comparación',
        12: 'Operador Lógico',
        13: 'Operador de Asignación',
        14: 'Operador de Comparación'
        16: 'Par de delimitacion'
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
                    tipo = self.tipos.get(estado_anterior, 'ERR_1')
                    output.append((tipo, "###"))
                    lexema = ""
                    estado = 0
                   
                else:
                    if estado_anterior in self.SIM:
                        estado = -1 if lexema in self.reservadas else -2 if lexema in self.booleanos else -3
                        
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
                if not token in [' ', '\n', '\t'] and estado != 6:
                    lexema += token
                    
            idx += 1
            estado_anterior = estado

        # TODO: Procesar ultimo token?
        return output

    def _obtener_columna(self, c):
        for columna in self.columnas:
            if columna[1](c):
                return columna[0]

        print("Token no valido: ", c)
        return self.ERR


def main():
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
    main()
