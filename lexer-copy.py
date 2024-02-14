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

    # M := [+-*%] ; ' ' := ' ' ^ \t
    #     *   ' '  \n   0-9  A-z   _    !    .    M    /    "    \
    #     0    1    2    3    4    5    6    7    8    9    10   11
    # TODO: Cambiar 0:0 por aceptacion?
    transiciones = [
        [ERR,   0,   0,   1,   4,   4, ERR, ERR,   6,   6,   8, ERR],  # 0
        [ERR, ACP, ACP,   1, ACP, ERR, ERR,   2, ACP, ACP, ACP, ERR],  # 1 Entero
        [ERR, ERR, ERR,   3, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 2
        [ERR, ACP, ACP,   3, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ERR],  # 3 Decimal
        [ERR, ACP, ACP,   4,   4,   4,   5, ERR, ACP, ACP, ACP, ERR],  # 4 Simbolo
        [ERR, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP, ACP, ACP, ERR],  # 5 Simbolo!
        [ERR, ACP, ACP, ACP, ACP, ACP, ACP, ERR, ACP,   7, ACP, ERR],  # 6 Operador Matematico
        [  7,   7, ACP,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # 7 Comentario
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   9,  10],  # 8
        [ERR, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ERR],  # 9 Cadena de Texto
        [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8]   # 10
    ]

    columnas = [
        ( 1, lambda c: c in [' ', '\t']),
        ( 2, lambda c: c == '\n'),
        ( 3, lambda c: c.isdigit()),
        ( 4, lambda c: c.isalpha()),
        ( 5, lambda c: c == '_'),
        ( 6, lambda c: c == '!'),
        ( 7, lambda c: c == '.'),
        ( 8, lambda c: c in ['+', '-', '*', '%']),
        ( 9, lambda c: c == '/'),
        (10, lambda c: c == '"'),
        (11, lambda c: c == '\\') 
    ]

    default = 0
    tipos = {
        -1: 'Palabra Reservada',
        -2: 'Booleano',
        -3: 'Identificador',

        # 0: 'Simbolo Especial',
        1: 'Entero',
        3: 'Decimal',
        4: 'Simbolo',
        5: 'Simbolo',
        6: 'Operador Matematico',
        7: 'Comentario',
        9: 'Cadena de texto'
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


def main_file():
    """Get a file path from console."""
    path = sys.argv[1]

    with open(path, 'r') as file:
        data = file.read()

    output = lexer(texto)
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
