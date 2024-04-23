#############################################
# Codigo: Compilador 2024A Lenguaje Oxido
# Autor : Manuel Corona Perez
# Fecha : 7/Marzo/2024
##########################################
ERR = -1
ACP = 999
entrada = '' 
lex = ''
tok = ''
idx = 0
dim1 = 0
dim2 = 0
bERR = False
archE = ''
conLin = 1
conCol = 0
conCod = 1
bImp = False

ctelog = ['verdadero', 'falso']
palRes = ['fn', 'principal', 'imprimeln!', 'entero', 'const',
          'decimal', 'logico', 'alfabetico', 'sea', 'si', 'sino', 
          'para', 'en', 'mientras', 'ciclo', 'regresa', 'leer', 'interrumpe', 
          'continua', 'mut', 'entero', 'decima', 'logico', 'palabra']

opa = ['+', '-', '*', '%', '^']

tabSim = {}
progm = []

def initPrgm():
    global progm
    for i in range(0, 10000):
        progm.append([])

def insCodigo(conC, cPl0):
    global progm
    progm[conC] = cPl0 

def impCod(linC, cod):
    print(linC, cod[0]+' '+cod[1]+  ', '+ cod[2])

def impTab(key, data):
    print(key + ', ' + data[0] + ', '+ data[1] + ', ' + str(data[2]) + ', ' + str(data[3]) + ', #,')

def insTabSim(key, colec):
    global tabSim
    tabSim[key] = colec

def obtTabSim(key):
    global tabSim
    return tabSim[key]

def colCar( c ):
    if c.isalpha():     return 0
    if c == '_':        return 1
    if c == '.':        return 2
    if c.isdigit():     return 3
    if c in opa:        return 4
    if c == '&':        return 5
    if c == '!':        return 6
    if c == '=':        return 7
    if c == '"':        return 8
    if c == '/':        return 9
    if c in ['<', '>']: return 10
    if c == '|':        return 11
    if c in dlm:        return 12
    if c in [' ', '\t', '\n']: return 0
    print(c ,'NO es valido en el alfabeto del Lenguaje')
    return ERR

def erra(rn, cl, erx, desE):
    global bERR
    bERR = True
    print('['+str(rn)+']['+str(cl)+'] '+ erx + " " + desE)

matran = [
    [1,   1,   18,  2,   7,   8,   19,  14,  12,  5,   15,  10,  18 ], #0
    [1,   1,   ACP, 1,   ACP, ACP, 1,   ACP, ACP, ACP, ACP, ACP, ACP], #1
    [ACP, ACP, 3,   2,   ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #2
    [ERR, ERR, ERR, 4,   ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #3
    [ACP, ACP, ACP, 4,   ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #4
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, 6,   ACP, ACP, ACP], #5  
    [6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6  , 6  ], #6
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #7
    [ERR, ERR, ERR, ERR, ERR, 9,   ERR, ERR, ERR, ERR, ERR, ERR, ERR], #8
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP, ACP, ACP, ACP, ACP], #9
    [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, 9  , ERR], #10
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #11
    [12,  12,  12,  12,  12,  12,  12,  12,  13,  12,  12,  12,  12 ], #12
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #13
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #14
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #15
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #16
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #17
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #18
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, 17,  ACP, ACP, ACP, ACP, ACP]  #19
]
dlm = ['[', ']', '{', '}', '(', ')', ',', ';', ':']
    

def lexico():
    global entrada, ERR, ACP, matran, idx, conLin, conCol
    estado = 0
    estAnt = 0
    lex = ''
    tok = ''
    while idx < len(entrada) and estado != ERR and estado != ACP:
        while(idx < len(entrada) and entrada[idx] in [' ', '\n', '\t', ''] 
              and estado == 0): 
            if entrada[idx] == '\n': 
                conLin += 1
                conCol = 0
            elif entrada[idx] == ' ': conCol += 1
            elif entrada[idx] == '\t': conCol += 4
            idx += 1

        if idx >= len(entrada): break

        x = entrada[idx]
        idx += 1
        if x != '\t' and x != '\n' and x != '': conCol += 1 
        if x == '\t': conCol += 4
        if x == '\n': 
            conLin += 1
            conCol = 0

        if estado == 6 and x == '\n': 
            break
        if estado == 8 and x == '\n':
            estAnt = 8
            estado = ERR
            break
        if estado == 1 and x in [' ', '\t', '\n']: 
            estAnt = estado
            estado = ACP
            break

        col = colCar(x)
        if col>=0 and col <= 12 and estado != ERR:
            estAnt = estado
            estado = matran[estado][col]
            if estado != ACP and estado != ERR: 
                lex += x
        if estado == ACP or estado == ERR:
            if x == '\n' and conCol < 2: 
                conLin -= 1
                conCol = 1 
            idx -= 1
            conCol -= 1
            break

    #print(estAnt, estado, lex)
    if estado != ACP and estado != ERR: estAnt = estado
    if estAnt == 3:
        erra(conLin, conCol, 'Error Lexico', 'Cte Decimal en ERROR '+lex)
    elif estAnt == 12:
        erra(conLin, conCol, 'Error Lexico', 'Cte Alfabetica SIN cerrar '+lex)

    elif estAnt == 1: 
        tok = 'Ide'
        if lex in palRes: tok = 'Res'
        elif lex in ctelog: tok = 'CtL'
    elif estAnt == 2:
        tok = 'Ent'
    elif estAnt == 4:
        tok = 'Dec'
    elif estAnt in [9, 19]:
        tok = 'OpL'
    elif estado == 6: 
        tok = 'Com'
        lex = '//'
    elif estAnt == 7: 
        tok = 'OpA'
    elif estAnt == 13:
        tok = 'CtA'
    elif estAnt == 14:
        tok = 'OpS'
    elif estAnt == 15:
        tok = 'OpR'
    elif estAnt == 18:
        tok = 'Del'
    else: tok = 'NtK'

    return tok, lex #Termina lexico

def tokeniza():
    global idx, entrada
    if idx >= len(entrada):
        return '', ''

    token = 'NtK'
    lexema = ''
    while (token in ['Com', 'NtK'] and idx < len(entrada)):
       token, lexema = lexico()
    
    return token, lexema

def termino():
    global tok, lex, conCod
    if lex == '(':
        tok, lex = tokeniza()
        expr()
        tok, lex = tokeniza()
        if lex != ')':
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ) y llego '+ lex)
    if tok in ['Ent', 'Dec', 'CtA', 'CtL']:
        if tok in ['Ent', 'Dec', 'CtA']:
           insCodigo(conCod, ['LIT', lex, '0'])
        elif lex == 'verdadero':
           insCodigo(conCod, ['LIT', 'V', '0'])
        elif lex == 'falso':
           insCodigo(conCod, ['LIT', 'F', '0'])
        conCod = conCod + 1
    if tok == 'Ide':
        nIde = lex
        insCodigo(conCod, ['LOD', nIde, '0'])
        conCod = conCod + 1

    tok, lex = tokeniza()

def expr():
    termino()

def imprimenl():
    global lex, tok, conCod, conLin, conCol, bImp
    tok, lex = tokeniza()
    if lex != '(':
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ( y llego '+ lex)
    tok, lex = tokeniza()
    if lex == ')':
                insCodigo(conCod, ['LIT', '""', '0'])
                conCod = conCod + 1
    elif lex != ')':
        sep = ','
        while sep == ',':
            sep = ''
            expr() 
            sep = lex
            if lex != ')': tok, lex = tokeniza()
            if sep == ',':
                insCodigo(conCod, ['OPR', '0', '20'])
                conCod = conCod + 1           

        

    if lex != ')': tok, lex = tokeniza()
    if lex != ')':
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ) y llego '+ lex)
    else:
        if bImp == False:
            insCodigo(conCod, ['OPR', '0', '21'])
        if bImp == True:
            insCodigo(conCod, ['OPR', '0', '20'])
        conCod = conCod + 1           

def leer():  #Comando leer Oxido
    global lex, tok, conCod, conLin, conCol, bImp
    tok, lex = tokeniza()
    nIde = ''
    if lex != '(':
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ( y llego '+ lex)
    tok, lex = tokeniza()
    if tok != 'Ide':
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba Identificador y llego '+ lex)
    else:
        nIde = lex
        tok, lex = tokeniza()
        if lex == '[':
            udim()
    if lex == ')':
                insCodigo(conCod, ['OPR', nIde, '19'])
                conCod = conCod + 1
    else:
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ")" y llego '+ lex)


def comando(): 
    global tok, lex, entrada, idx, conCod, bImp
    if lex == 'imprimeln!': imprimenl()
    if lex == 'imprimeln': 
        bImp = True
        imprimenl();
        bImp = False
    if lex == 'lmp': 
        insCodigo(conCod, ['OPR', '0', '18'])
        conCod = conCod + 1
        tok, lex = tokeniza()
    if lex == 'leer': leer()

def estatutos():
    global tok, lex, entrada, idx 
    sep = ';'
    while sep == ';':
        if lex == ';':
            tok, lex = tokeniza()
        if lex == '}': break
        comando()
        if lex == ')':
            tok, lex = tokeniza()
        sep = '*'
        if lex == ';': sep = lex
        if lex != ';':
            erra(conLin, conCol, 'Error de Sintaxis', 'se esperaba ; y llego '+ lex)

def variables():
    global tok, lex, dim1, dim2, conLin, conCol, conCod
    dim1 = 0
    dim2 = 0
    nVars = []
    tipo = ''
    clVar = ''
    value = ''
    while lex == 'sea':
        tok, lex = tokeniza()
        if lex == 'mut': 
            clVar = 'V'
            tok, lex = tokeniza()
        else: 
            clVar = 'C'
        while tok == 'Ide':
            nIde = lex
            tok, lex = tokeniza()
            if lex == '[': dimens()
            nVars.append(nIde)
            if lex == ',':
               tok, lex = tokeniza()
        if lex != ':':
            erra(conLin, conCol, 'Error de Sintaxis', 'se esperaba : y llego '+ lex)
        else:
            tok, lex = tokeniza()
            if   lex == 'entero' : 
                tipo = 'E'
                value = '0'
            elif lex == 'decimal': 
                tipo = 'D'
                value = '0.0'
            elif lex == 'logico' : 
                tipo = 'L'
                value = 'F'
            elif lex == 'alfabetico': 
                tipo = 'A'
                value = '""'
            tok, lex = tokeniza()
            if lex == '=':
               tok, lex = tokeniza()
               if tok in ['Ent', 'Dec', 'CtA', 'CtL']:
                  value = lex

            for x in nVars:
                insTabSim(x, [clVar, tipo, str(dim1), '0'])
                insCodigo(conCod, ['LIT', value, '0'])
                conCod = conCod + 1
                insCodigo(conCod, ['STO', '0', x])
                conCod = conCod + 1
            nVars = []
        if lex != ';':
            tok, lex = tokeniza()
        if lex != ';':
            erra(conLin, conCol, 'Error de Sintaxis', 'se esperaba : y llego '+ lex)
        else:
            tok, lex = tokeniza()
            if lex == 'fn':
                insCodigo(conCod, ['JMP', '0', '_principal'])
                conCod = conCod + 1


def params(): 
    global tok, lex, idx, entrada
    sec = ','
    while sec == ',':
        if tok != 'Ide': 
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba Ide y llego '+ lex)
        tok, lex = tokeniza()
        if lex != ':':
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba : y llego '+ lex)
        tipo()
        tok, lex = tokeniza()
        sec = lex
        if sec == ',':
            tok, lex = tokeniza()

def tipo():
    global tok, lex
    tok, lex = tokeniza()
    if not(lex in ['entero', 'decimal', 'logico', 'palabra']):
        erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba entero, decimal, logico o palabra y llego '+ lex)
        

def funciones():
    global conCod, conLin, conCol, lex, tok, idx, entrada
    if idx >= len(entrada): return
    nomf =''
    while idx < len(entrada) and lex == 'fn':
        tok, lex = tokeniza()
        if tok == 'Ide': nomf = lex
        if tok == 'Res' and lex == 'principal':
                nomf = lex
                insTabSim('_principal', ['F', 'I', str(conCod),'0'])
                insTabSim('_P',['I', 'I', 1, 0])
        elif tok != 'Ide':
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba Ide o principal y llego '+ lex)
        tok, lex = tokeniza();
        if lex != '(': 
           erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ( y llego '+ lex)
        tok, lex = tokeniza();
        if lex != ')': params()
        if lex != ')':
           erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba ) y llego '+ lex)
        tok, lex = tokeniza();
        if lex == '-':
            tok, lex = tokeniza()
            if lex != '>':
                erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba > y llego '+ lex)
            tipo()
            tok, lex = tokeniza()

        if lex != '{':
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba { y llego '+ lex)
        tok, lex = tokeniza()
        if lex != '}': estatutos()
        if lex == '}':
            if nomf == 'principal':
                insCodigo(conCod, ['OPR', '0', '0'])
                conCod = conCod + 1           
        elif lex != '}':
            erra(conLin, conCol, 'Error de Sintaxis', 'Se esperaba } y llego '+ lex)
        
        tok, lex = tokeniza()
            

def prgm():
    global bERR, archE, tok, lex
    tok, lex = tokeniza()
    variables()
    funciones()
    if not(bERR):
        print(archE, 'COMPILO con EXITO!!!')



if __name__ == '__main__':
    archE = ''
    print(archE[len(archE)-3:])
    while (archE[len(archE)-3:] != 'icc'):
        archE = input('Archivo a compilar (*.icc) [.]=Salir: ')
        if archE == '.': exit(0)
        aEnt = None
        try:
            aEnt = open(archE, 'r+')
            break
        except FileNotFoundError:
            print(archE, 'No exite volver a intentar')
    
    if aEnt != None:
        while (linea := aEnt.readline()):
            entrada += linea
        aEnt.close()

    print('\n\n' + entrada + '\n\n')  
    idx = len(entrada) 
    while idx < len(entrada):
        token, lexema = tokeniza()
        print(token, lexema)
    idx = 0   
    if len(entrada) > 0:
       initPrgm()
       prgm()
       if bERR == False:
           archS = archE[0:len(archE)-3] + 'eje'
           try:
              #print(archS)
              with open(archS, 'w') as aSal:
                for x, y in tabSim.items():
                    aSal.write(x + ',')
                    aSal.write(y[0]+',')
                    aSal.write(y[1]+',')
                    aSal.write(str(y[2])+',')
                    aSal.write(str(y[3])+',')
                    aSal.write('#,\n')
                aSal.write('@\n')
                for i in range(1, conCod):
                    aSal.write(str(i) + ' ')
                    aSal.write(progm[i][0] + ' ')
                    aSal.write(progm[i][1] + ', ')
                    aSal.write(progm[i][2]  + '\n')
              aSal.close()
           except FileNotFoundError:
              print(archE, 'No exite volver a intentar')



