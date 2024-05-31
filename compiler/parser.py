"""Analizador Sintactico."""


def show_level(func):
    """Print when the program enter and exit of the function."""
    def inner_function(*args, **kwargs):
        print(f"Enter {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exited {func.__name__}")
        return result

    return inner_function


def tabla_tipos(a, b, opr):
    if a == 'E':
        if opr in '+-*^' and b in 'ED' :
            return b

        if opr == '%' and b == 'E':
            return 'E'

        if opr in ['<', '>', '==', '!=', '<=', '>='] and b in 'ED':
            return 'L'

    if a == 'D':
        if opr in '+-*^' and b in 'ED' :
            return 'D'

        if opr in ['<', '>', '==', '!=', '<=', '>='] and b in 'ED':
            return 'L'

    if a == 'A':
        if opr in ['==', '!=']:
            return 'L'

    if a == 'L':
        if opr in ['&&', '||', '==', '!=']:
            return 'L'

    return 'I'


class Parser:
    """Valida el orden de los tokens (comprueba la gramatica).
    Simbolos: Diccionario de variables y valores.
    Codigo: Mapa de simbolos [clase, tipo, dim1, dim2].
    Clase: [V]ariable, [C]onstante, [I]ndefinido, [P]rocedimiento, [F]uncion, pa[R]ametro.
    Tipo: [E]ntero, [D]ecimal, p[A]labra, [L]ogico, [I]ndefinido.
    Dim1: El tamano del arreglo, los escalares tiene tamano 0.
    Dim2: Siempre es 0 para esta implementacion.
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

        self.pila_tipos = []
        self.error_count = 0

        self.contexto = ""

        self.tipo = ''
        self.lexema = ''
        self.linea = -1
        self.columna = -1

        self.reg_inc = 0
        self.line_inc = 1

        self.mapa_simbolos = {}
        self.constantes = {}
        self.codigo = []

    def __call__(self):
        try:
            self.programa()

        except StopIteration:
            # self.add_line("OPR 0, 0")
            self.mapa_simbolos['_P'] = ['I', 'I', 1, 0]
            print("Compilacion finalizada.")
            print(self.mapa_simbolos)
            print(self.codigo)

    def error_tipo(self, esperado):
        print(f"ERROR SINTACTICO: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba un {esperado} y recibio un {self.tipo}.")
        self.error_count += 1

    def error_lexema(self, esperado):
        print(f"ERROR SINTACTICO: [{self.linea}:{self.columna}] '{self.lexema}'. Se esperaba '{esperado}' y recibio '{self.lexema}'.")
        self.error_count += 1

    def error_semantico(self, msg):
        print(f"ERROR SEMANTICO: [{self.linea}:{self.columna}]", msg)
        self.error_count += 1

    def error_personalizado(self, tipo, msg):
        print(f"ERROR {tipo}: [{self.linea}:{self.columna}]", msg)
        self.error_count += 1

    def next_token(self):
        self.tipo, self.lexema, self.linea, self.columna = next(self.lexer)

        if self.tipo == 'Comentario':
            self.next_token()

        else:
            print(f"[{self.tipo}:{self.lexema}]")

    def add_line(self, line):
        line = f"{self.line_inc} {line}\n"
        self.codigo.append(line)
        self.line_inc += 1
        print(f":-{line}")

    def add_var(self, var, value):
        self.add_line(f"LIT {value}, 0")
        self.add_line(f"STO 0, {var}")

    def check_types(self, opr):
        a = self.pila_tipos.pop()
        b = self.pila_tipos.pop()
        c = tabla_tipos(a, b, opr)
        self.pila_tipos.append(c)

        if c == 'I':
            self.error_semantico(f"Operador '{opr}' aplicado con tipos invalidos: '{a}' y '{b}'")

    def make_tab(self):
        lines = []
        for x, y in self.mapa_simbolos.items():
            line = ','.join(str(x) for x in y)
            lines.append(f"{x},{line},#,\n")
        return lines

    def make_file(self, name='out'):
        if self.error_count:
            print(f"Se han encontrado {self.error_count} errores. El archivo no se compilara.")

        else:
            with open(name + '.eje', 'w') as f:
                f.writelines(self.make_tab())
                f.write('@\n')
                f.writelines(self.codigo)

    # NOTE: Axioma
    @show_level
    def programa(self):
        self.next_token()
        while self.lexema == 'sea':
            self.declaracion()
            self.next_token()

        self.add_line("JMP 0, _principal")
        
        while self.lexema == 'fn':
            self.funcion()
            self.next_token()

    @show_level
    def bloque(self, fun_id=""):
        self.next_token()
        while self.lexema in ['sea', 'si', 'para', 'mientras', 'tpm', 'leer',
                              'imprimeln', 'imprimeln!', 'regresa', 'ciclo'] \
              or self.tipo == 'Identificador':
            self.sentencia(fun_id)

    @show_level
    def sentencia(self, fun_id=""):
        if self.lexema == 'si':
            self.si_sino(fun_id)

        if self.lexema == 'sino':
            self.error_personalizado("SINTACTICO", "'sino' sin un bloque 'si' asociado.")

        if self.lexema == 'mientras':
            self.mientras(fun_id)

        if self.lexema == 'para':
            self.para(fun_id)

        if self.lexema == 'ciclo':
            self.ciclo(fun_id)

        if self.lexema == 'regresa':
            self.next_token()
            if self.lexema != ';':
                self.expresion()

                self.add_line(f"STO 0, {fun_id}")
                self.add_line("OPR 0, 1")

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

            if self.lexema not in self.mapa_simbolos:
                self.error_semantico(f"La variable '{self.lexema}' no existe.")

            self.add_line(f"OPR {self.lexema}, 19")

            self.next_token()
            if self.lexema != ')':
                self.error_lexema(')')

            self.next_token()
            if self.lexema != ';':
                self.error_lexema(';')
            self.next_token()
             
        if self.tipo == 'Identificador':
            ide = self.lexema
            self.next_token()


            if self.lexema == '=' or self.lexema == '[':
                self.asignacion(ide)

            # Llamada de funcion
            if self.lexema == '(':
                args_types = []
                ri = self.reg_inc
                self.add_line(f"LOD _RE{ri}, 0")
                self.reg_inc += 1

                self.next_token()
                if self.lexema != ')':
                    self.expresion()
                    args_types.append( self.pila_tipos[-1] )
                    ide += f"${self.pila_tipos[-1]}"

                    while self.lexema == ',':
                        self.next_token()
                        self.expresion()
                        args_types.append( self.pila_tipos[-1] )
                        ide += f"${self.pila_tipos[-1]}"

                    if self.lexema != ')':
                        self.error_lexema(')')

                    self.next_token()

                else:
                    self.next_token()

                if ide not in self.mapa_simbolos:
                    self.error_semantico(f"La funcion {ide} no existe.")

                elif self.mapa_simbolos[ide][0] != 'F':
                    self.error_semantico("El elemento llamado no es una funcion.")

                self.add_line(f'CAL {ide}, 0')
                self.mapa_simbolos[f'_RE{ri}'] = ['I', 'I', self.line_inc, '0']

                if self.lexema != ";":
                   self.error_lexema(";")

            self.next_token()

        # else:
        #     self.error_tipo('Palabra Reservada')
        #     self.next_token()

    @show_level
    def declaracion(self):
        sim = []
        ids = []
        leng = 0

        # Constante o Variable
        self.next_token()
        if self.lexema == 'mut':
            sim.append('V')
            self.next_token()

        else:
            sim.append('C')

        # Simbolo
        if self.tipo == 'Identificador':
            if self.lexema in self.mapa_simbolos:
                self.error_semantico(f"La variable '{self.lexema}' ya existe.")

            else:
                ids.append(self.lexema)

        else:
            self.error_lexema('Identificador')

        self.next_token()
        if self.lexema == '[':
            self.next_token()
            if self.lexema == '0':
                self.error_semantico("0 no es una longitud valida para un vector.")
                
            elif self.tipo == 'Entero':
                leng = int(self.lexema)

            # TODO: Capturar los casos de error - Esto funciona?
            elif self.tipo == 'Identificador':
                if self.lexema not in self.mapa_simbolos:
                    self.error_semantico(f"El simbolo '{self.lexema}' no existe.")

                else:
                    if self.mapa_simbolos[self.lexema][1] != 'E':
                        self.error_semantico("Tipo de constante incorrecto.")

                    elif int( self.constantes[self.lexema] ) < 1:
                        self.error_semantico("Valor de constante incorrecto.")

                    else:
                        leng = int( self.constantes[self.lexema] )

            else:
                self.error_tipo("Entero o Identificador")

            self.next_token()
            if self.lexema != ']':
                self.error_lexema(']')
            self.next_token()

        while self.lexema == ',':
            self.next_token()
            # Identificador
            if self.tipo == 'Identificador':
                if self.lexema in self.mapa_simbolos:
                    self.error_semantico(f"La variable '{self.lexema}' ya existe.")
    
                else:
                    ids.append(self.lexema)
    
            else:
                self.error_lexema('Identificador')

            self.next_token()

            # Leng
            leng_p = 0
            if leng > 0:
                if self.lexema != '[':
                    self.error_semantico("Intentando definir vectores con no vectores.")
                    continue

                self.next_token()
                if self.tipo == 'Entero':
                    leng_p = int(self.lexema)
    
                # TODO: Capturar los casos de error - Esto funciona?
                elif self.tipo == 'Identificador':
                    if self.lexema not in self.mapa_simbolos:
                        self.error_semantico(f"El simbolo '{self.lexema}' no existe.")
    
                    else:
                        if self.mapa_simbolos[self.lexema][1] != 'E':
                            self.error_semantico("Tipo de constante incorrecto.")
    
                        elif int( self.constantes[self.lexema] ) < 1:
                            self.error_semantico("Valor de constante incorrecto.")
    
                        else:
                            leng_p = int( self.constantes[self.lexema] )
    
                else:
                    self.error_tipo("Entero o Identificador")

                if leng_p != leng:
                    self.error_semantico("Vectores de longitudes distintas en la misma declaracion.")
    
                self.next_token()
                if self.lexema != ']':
                    self.error_lexema(']')
                self.next_token()

        if self.lexema != ':':
            self.error_lexema(':')

        self.tipo_variable()
        tipo = self.tipo_var[self.lexema]

        sim.append(tipo)
        sim.append(leng)
        sim.append(0)

        self.next_token()
        if self.lexema == '=':
            self.next_token()
            if self.lexema == '[':
                i = 0
                value = ''
                while True:
                    self.next_token()
                    if sim[1] in ['E', 'D']:
                        if self.lexema == '-':
                            value += '-'
                            self.next_token()
    
                        if self.tipo in ['Entero', 'Decimal']:
                            value += self.lexema
    
                        else:
                            self.error_tipo('Entero' if sim[1] == 'E' else 'Decimal')
    
                    elif sim[1] == 'A':
                        if self.tipo == 'Alfabetico':
                            self.error_lexema('Alfabetico')
    
                        else:
                            value = self.lexema
    
                    elif sim[1] == 'L':
                        if self.tipo == 'Logico':
                            value = 'V' if self.lexema == 'verdadero' else 'F'
    
                        else:
                            self.error_tipo('Logico')
    
                    else:
                        self.error_tipo('Literal')

                    for v in ids:
                        self.add_line(f"LIT {i}, 0")
                        self.add_line(f"LIT {value if value[0] != '-' else value[1:]}, 0")
                        if value[0] == '-':
                            self.add_line("OPR 0, 8")
                        self.add_line(f"STO 0, {v}")
                        self.mapa_simbolos[v] = sim.copy()
                        self.constantes[v] = value

                    i += 1
                    value = ''
                    self.next_token()
                    if self.lexema != ',':
                        break

                if self.lexema != ']':
                    self.error_lexema(']')

            else:
                value = ''
                # TODO: Verificacion semantica de tipos
                if self.lexema == '-':
                    self.next_token()
                    if self.tipo in ['Logico', 'Alfabetico']:
                        self.error_semantico("Operador '-' en tipo incompatible.")

                    else:
                        value = '-'

                if self.tipo == 'Logico':
                    value = 'V' if self.lexema == 'verdadero' else 'F'

                elif self.tipo in ['Alfabetico', 'Entero', 'Decimal']:
                    value += self.lexema

                else:
                    self.error_lexema('Literal o Variable')

                tipos = {'E': 'Entero', 'D': 'Decimal', 'A': 'Alfabetico', 'L': 'Logico'}
                if self.tipo[0] != sim[1]:
                    self.error_semantico(f"Asignando un '{self.tipo}' a una variable de tipo '{tipos[ sim[1] ]}'.")

                for v in ids:
                    self.add_line(f"LIT {value if value[0] != '-' else value[1:]}, 0")
                    if value[0] == '-':
                        self.add_line("OPR 0, 8")
                    self.add_line(f"STO 0, {v}")
                    self.mapa_simbolos[v] = sim.copy()
                    self.constantes[v] = value

            self.next_token()

        # Default values
        else:
            if sim[0] == 'C':
                self.error_semantico("Constante no inicializada.")

            def_val = {'E': 0, 'D': 0.0, 'A': '""', 'L': 'F'}[tipo]

            if leng:
                for v in ids:
                    self.mapa_simbolos[v] = sim.copy()
                    for i in range(leng):
                        self.add_line(f"LIT {i}, 0")
                        self.add_line(f"LIT {def_val}, 0")
                        self.add_line(f"STO 0, {v}")

            else:
                for v in ids:
                    self.mapa_simbolos[v] = sim.copy()
                    self.add_line(f"LIT {def_val}, 0")
                    self.add_line(f"STO 0, {v}")

        if self.lexema != ';':
            self.error_lexema(';')

    @show_level
    def imprime(self, new_line):
        self.next_token()
        if self.lexema != '(':
            self.error_lexema('(')

        self.next_token()
        if self.lexema == ')':
            self.add_line('LIT "", 0')
            self.add_line("OPR 0, 21" if new_line else "OPR 0, 20")

        else:
            self.expresion()

            while self.lexema == ',':
                self.add_line("OPR 0, 20")
                self.next_token()
                self.expresion()

            if self.lexema != ')':
                self.error_lexema(')')

            self.pila_tipos.pop()
            self.add_line("OPR 0, 21" if new_line else "OPR 0, 20")

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
    def funcion(self):
        li = self.line_inc
        args = []
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
            argumento.append(0)
            argumento.append(0)

            args.append((id, argumento))

            self.next_token()
            while self.lexema == ",":
                argumento = []
                argumento.append('R')

                self.next_token()
                if self.tipo != "Identificador":
                    self.error_lexema("Identificador")

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

                args.append((id, argumento))
                self.next_token()

        if self.lexema != ")":
            self.error_lexema(")")

        self.contexto = f"${func_id}"
        for lexema, tabla in args[::-1]:
            lexema += f"${func_id}"
            self.add_line(f"STO 0, {lexema}")
            self.mapa_simbolos[lexema] = tabla

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

        func.append(li)
        func.append(0)

        if func_id == 'principal':
            func_id = '_principal'
        self.mapa_simbolos[func_id] = func

        self.bloque(func_id)

        if self.lexema != "}":
            self.error_lexema("}")

        else:
            self.add_line("OPR 0, 0" if func_id == '_principal' else "OPR 0, 1")

    # TODO: Hacer que use sus propios simbolos (simbolos locales)
    @show_level
    def para(self, fun_id):
        eq = False
        neg = False
        inc = 1

        self.next_token()
        if self.tipo != 'Identificador':
            self.error_tipo('Identificador')

        id = self.lexema

        # self.mapa_simbolos[id] = ['V', 'E', '0', '0']
        if id not in self.mapa_simbolos:
            self.error_semantico(f"La variable '{id}' no existe.")

        self.next_token()
        if self.lexema != 'en':
            self.error_lexema('en')

        self.next_token()
        self.expresion()
        self.add_line(f"STO 0, {id}")

        if self.lexema != '..':
            self.error_lexema('..')

        self.next_token()
        if self.lexema == '=':
            eq = True
            self.next_token()

        li = self.line_inc
        self.add_line(f"LOD {id}, 0")
        self.expresion()

        if self.lexema == 'inc':
            self.next_token()

            if self.lexema == '-':
                neg = True
                self.next_token()

            if self.tipo == 'Entero':
                inc = self.lexema
                self.next_token()

            else:
                self.error_tipo('entero')

        ri = self.reg_inc
        self.reg_inc += 1

        if neg:
            self.add_line("OPR 0, 12" if eq else "OPR 0, 10")

        else:
            self.add_line("OPR 0, 11" if eq else "OPR 0, 9")

        self.add_line(f"JMC F, _RE{ri}")

        if self.lexema == '{':
            self.bloque(fun_id)

            if self.lexema != '}':
                self.error_lexema('}')

            self.add_line(f"LOD {id}, 0")
            self.add_line(f"LIT {inc}, 0")
            self.add_line("OPR 0, 3" if neg else "OPR 0, 2")
            self.add_line(f"STO 0, {id}")

            self.add_line(f"JMP 0, {li}")
            self.mapa_simbolos[f'_RE{ri}'] = ['I', 'I', self.line_inc, '0']
            self.next_token()

        else:
            self.error_lexema('{')

    # Do - While
    @show_level
    def ciclo(self, fun_id=""):
        li = self.line_inc
        self.next_token()
        if self.lexema == '{':
            self.bloque(fun_id)

            if self.lexema != '}':
                self.error_lexema('}')

        else:
            self.error_lexema('{')

        self.next_token()
        if self.lexema != 'mientras':
            self.error_lexema('mientras')

        self.next_token()
        self.expresion()

        if self.lexema != ';':
            self.error_lexema(';')

        self.add_line(f"JMC V, {li}")
        self.next_token()

    @show_level
    def mientras(self, fun_id=""):
        ri = self.reg_inc
        li = self.line_inc
        self.reg_inc += 1

        self.next_token()
        self.expresion()

        self.add_line(f"JMC F, _RE{ri}")

        if self.lexema == '{':
            self.bloque(fun_id)

            if self.lexema != '}':
                self.error_lexema('}')

            self.add_line(f"JMP 0, {li}")
            self.mapa_simbolos[f'_RE{ri}'] = ['I', 'I', self.line_inc, '0']
            self.next_token()

        else:
            # self.sentencia()
            self.error_lexema('{')

    @show_level
    def si_sino(self, fun_id=""):
        ri = self.reg_inc
        self.reg_inc += 1
        ri2 = self.reg_inc
        self.reg_inc += 1

        # si
        self.next_token()
        self.expresion()
        self.add_line(f"JMC F, _RE{ri2}")
        if self.lexema == '{':
            self.bloque(fun_id)

            if self.lexema != '}':
                self.error_lexema('}')

            self.next_token()

        else:
            self.error_lexema('{')

        self.add_line(f"JMP 0, _RE{ri}")
        self.mapa_simbolos[f"_RE{ri2}"] = ['I', 'I', self.line_inc, '0']

        # NOTE: Esto es un parche
        exist_sino = True
        # sino si
        if self.lexema == 'sino':
            self.next_token()
            while self.lexema == 'si':
                self.reg_inc += 1
                self.next_token()
                self.expresion()
                self.add_line(f"JMC F, _RE{self.reg_inc}")
                if self.lexema == '{':
                    self.bloque(fun_id)
    
                    if self.lexema != '}':
                        self.error_lexema('}')

                    self.next_token()
                    self.add_line(f"JMP 0, _RE{ri}")
                    self.mapa_simbolos[f"_RE{self.reg_inc}"] = ['I', 'I', self.line_inc, '0']
                    if self.lexema == 'sino':
                        self.next_token()

                    else:
                        exist_sino = False
 
                else:
                    self.error_lexema('{')

            # sino
            if self.lexema == '{':
                self.bloque(fun_id)

                if self.lexema != '}':
                    self.error_lexema('}')

                self.next_token()

            elif exist_sino:
                self.error_lexema('{')

        self.mapa_simbolos[f"_RE{ri}"] = ['I', 'I', self.line_inc, '0']

    # expr_-1
    @show_level
    def asignacion(self, id):
        id_exist = True
        if f"{id}{self.contexto}" in self.mapa_simbolos:
            id = f"{id}{self.contexto}"

        if id not in self.mapa_simbolos:
            self.error_semantico(f"El simbolo '{id}' no existe.")
            id_exist = False

        if id_exist and self.mapa_simbolos[id][0] == 'C':
            self.error_semantico(f"Intetando redefinir la constante '{id}'.")

        if self.lexema == '[':
            self.next_token()
            self.expresion()

            if self.lexema != "]":
                self.error_lexema("]")

            self.next_token()

        if self.lexema != '=':
            self.error_lexema("=")

        self.next_token()
        self.expresion()
        self.add_line(f'STO 0, {id}')

        if id_exist and self.mapa_simbolos[id][1] != self.pila_tipos.pop():
            self.error_semantico("El tipo de la variable y resultado de la expresión no coinciden.")

        if not id_exist:
            self.pila_tipos.pop()

        if self.lexema != ';':
            self.error_lexema(";")

    @show_level
    def expresion(self):
        self.disyuncion()

    @show_level
    def disyuncion(self):
        """||."""
        self.conjuncion()

        while self.lexema in ['||', 'o']:
            self.next_token()
            self.conjuncion()

            self.check_types('||')
            self.add_line(f"OPR 0, 16")

    # expr_2
    @show_level
    def conjuncion(self):
        """&&."""
        self.logico()

        while self.lexema in ['&&', 'y']:
            self.next_token()
            self.logico()

            self.check_types('&&')
            self.add_line(f"OPR 0, 15")

    # expr_3
    @show_level
    def logico(self):
        """<, >, ==, !=, <=, >=."""
        self.adicion()

        while self.lexema in ['<', '>', '==', '!=', '<=', '>=']:
            temp = self.lexema
            self.next_token()
            self.adicion()

            self.check_types(temp)
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_4
    @show_level
    def adicion(self):
        """+-."""
        self.producto()

        while self.lexema in '+-':
            temp = self.lexema
            self.next_token()
            self.producto()

            self.check_types(temp)
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_5
    @show_level
    def producto(self):
        """*/%."""
        self.exponente()

        while self.lexema in '*/%':
            temp = self.lexema
            self.next_token()
            self.exponente()

            self.check_types(temp)
            self.add_line(f"OPR 0, {self.opr_num[temp]}")

    # expr_6
    @show_level
    def exponente(self):
        """^."""
        self.termino()

        while self.lexema == '^':
            self.next_token()
            self.termino()

            self.check_types('^')
            self.add_line(f"OPR 0, 7")

    # expr_7
    # TODO: Mover prioridad de '!' justo despues de && y ||
    @show_level
    def termino(self):
        unary = 0
        if self.lexema in ['-', '!', 'no']:
            unary = 8 if self.lexema == '-' else 17
            self.next_token()

        if self.lexema == '(':
            self.next_token()
            self.expresion()

            if self.lexema != ')':
                self.error_lexema(')')

            else:
                self.next_token()

        elif self.tipo == 'Identificador':
            is_fun = False
            id = self.lexema
            self.next_token()
            if self.lexema == '[':
                self.next_token()
                self.expresion()

                if self.lexema != ']':
                    self.error_lexema(']')

                else:
                    self.next_token()

            elif self.lexema == '(':
                args_type = []
                ri = self.reg_inc
                self.add_line(f"LOD _RE{ri}, 0")
                self.reg_inc += 1

                is_fun = True
                self.next_token()
                self.expresion()
                args_type.append( self.pila_tipos[-1] )
                id += f"${self.pila_tipos[-1]}"

                while self.lexema == ',':
                    self.next_token()
                    self.expresion()
                    args_type.append( self.pila_tipos[-1] )
                    id += f"${self.pila_tipos[-1]}"

                if self.lexema != ')':
                    self.error_lexema(')')

                else:
                    self.next_token()
                    
                if id not in self.mapa_simbolos:
                    self.error_semantico(f"La funcion '{id}' no existe.")

                elif self.mapa_simbolos[id][0] != 'F':
                    self.error_semantico("El elemento llamado no es una funcion.")

                self.add_line(f"CAL {id}, 0")
                self.mapa_simbolos[f'_RE{ri}'] = ['I', 'I', self.line_inc, '0']
                self.add_line(f"LOD {id}, 0")

            if not is_fun:
                if f"{id}{self.contexto}" in self.mapa_simbolos:
                    id = f"{id}{self.contexto}"

                if id not in self.mapa_simbolos:
                    self.error_semantico(f"La variable '{id.split('$')[0]}' no existe.")
                    self.pila_tipos.append('I')

                else:
                    self.pila_tipos.append( self.mapa_simbolos[id][1] )

                self.add_line(f'LOD {id}, 0')

        elif self.tipo in ['Entero', 'Decimal', 'Alfabetico']:
            if unary and self.tipo == 'Alfabetico':
                self.error_semantico("Operador '-' en tipo incompatible.")

            self.add_line(f'LIT {self.lexema}, 0')
            self.pila_tipos.append( self.tipo[0].capitalize() )
            print("Pila Tipos:", self.pila_tipos)
            self.next_token()

        elif self.tipo == 'Logico':
            if unary:
                self.error_semantico("Operador '-' en tipo incompatible.")

            temp = 'V' if self.lexema == 'verdadero' else 'F'
            self.add_line(f'LIT {temp}, 0')
            self.pila_tipos.append( self.tipo[0].capitalize() )
            self.next_token()

        else:
            self.error_tipo('Identificador o Literal')

        if unary:
            self.add_line(f'OPR 0, {unary}')
