
from io import UnsupportedOperation
import gamelib
import png
from control import Accion

TAM = 20 # CANT DE FILAS Y COLUMNAR
MARGEN = 10     # espacio para separar
CELDA = int(MARGEN * 1.5)   # tam de cada celda de la grilla
# ubico y agrego tam de la grilla
ARR_GRILLA = MARGEN
IZQ_GRILLA =MARGEN
GRILLA = CELDA * TAM 
# acomodo paleta con tam determinados por grilla
PALETA= 16
IZQ_PALETA = MARGEN
ARR_PALETA = GRILLA + ARR_GRILLA *2
ALTO_PALETA = CELDA
ANCHO_PALETA = GRILLA 
TAM_BORDE_PALETA =3
BASE_PALETA = [ '#FFFFFF', '#000000', '#FF0000', '#00FF00',    # colores iniciales
             '#0000FF', '#00FFFF', '#FFFF00', '#FF00FF' ]
# ubico los botones segun mi grilla
IZQ_BOTON = MARGEN
ARR_BOTON = ARR_PALETA + ALTO_PALETA + MARGEN
ALTO_BOTON = MARGEN*2
ANCHO_BOTON = (GRILLA - MARGEN * 3) // 7
DIAGONALES = 4
CANT_BOTONES = 7
BASE_BOTONES = [ 'Guargar\nPPM', 'Cargar\nPPM', 'Guardar\nPNG', 'Agregar\nColor', 'Pintar\nbalde', 'Deshacer', 'Rehacer' ]
# tamaño de la intefaz
ANCHO_VENTANA = GRILLA + IZQ_GRILLA * 2
ALTO_VENTANA = GRILLA + ALTO_PALETA + ALTO_BOTON + ARR_GRILLA * 4
# colores para diferenciar cada uno
FONDO_PANTALLA = '#C0C0C0'
FONDO_GRILLA = '#F0F0F0'
FONDO_BOTON = '#D8D8D8'
BORDE = '#800000'

def grilla_crear():
    '''Inicializa grilla'''
    grilla = [None] * TAM
    arriba = ARR_GRILLA
    for fila in range(TAM):
        grilla[fila] =[None] * TAM
        horizontal = IZQ_GRILLA
        for columna in range(TAM):
            grilla[fila][columna] = [(horizontal, arriba, horizontal+CELDA, arriba+CELDA), None]
            horizontal += CELDA
        arriba += CELDA
    return grilla

def paleta_crear():
    '''Inicializa las paletas'''
    paleta = [None] * PALETA
    separador = TAM - PALETA
    x_izq = IZQ_PALETA
    y_sup = ARR_PALETA
    y_inf = y_sup + ALTO_PALETA
    for cuadri in range(len(BASE_PALETA)):
        paleta[cuadri] = [(x_izq, y_sup, x_izq+CELDA, y_inf), BASE_PALETA[cuadri] ]
        x_izq += CELDA + separador
    for cuadri in range(len(BASE_PALETA), PALETA):
        paleta[cuadri] = [(x_izq, y_sup, x_izq+CELDA, y_inf), None]
        x_izq += CELDA +separador
    return paleta

def botones_crear():
    """Inicializa los botones"""
    botones = [None] * CANT_BOTONES 
    x_izq = IZQ_BOTON
    y_sup = ARR_BOTON
    y_inf = y_sup + ALTO_BOTON
    for indice in range(CANT_BOTONES):
        botones[indice] = [(x_izq, y_sup, x_izq +ANCHO_BOTON, y_inf), FONDO_BOTON ]
        x_izq += ANCHO_BOTON + MARGEN//2
    return botones

def dibujar(celda, fondo, borde, ancho):
    ''' Desde la celda se ingresa a una lista de dos elementos del cual se accede en [0] para x_izq, en [1] esta la y_sup, [2] para x_der y [3] para y_inf. Además, con estos 2dos valores se acomoda el string.
    particularmente, en celda[1] es un string al cual le defino un color y le agrego el predeterminado de fondo si es que no llega a existir.'''
    rectangulo = celda[0]
    gamelib.draw_rectangle(rectangulo[0], rectangulo[1], rectangulo[2], rectangulo[3],
        width = ancho, outline = borde , fill = celda[1] if celda[1] else fondo) 
    
def dibujar_grilla(grilla):
    '''Preparo interfaz'''
    for fila in range(TAM):
        for columna in range(TAM):
            dibujar(grilla[fila][columna], FONDO_GRILLA, FONDO_PANTALLA, 1)

def dibujar_paleta(paleta, indice_actual):
    '''Acomodo paleta'''
    for indice in range(len(paleta)):
        dibujar(paleta[indice], FONDO_GRILLA, BORDE if indice_actual == indice else None, TAM_BORDE_PALETA if indice_actual == indice else 0)

def dibujar_botones(botones, balde):
    '''Obtengo su posicion x, y como superior izquierda e inferior derecha donde el segundo elemento agregado indica el string para posicionar el texto de los botones'''
    posicion_x_y = botones[0][0]
    arriba = (posicion_x_y[1] + posicion_x_y[3]) //2  
    for indice in range(len(botones)):
        borde = 'red' if indice == DIAGONALES and balde else FONDO_PANTALLA
        dibujar(botones[indice], FONDO_PANTALLA, borde, 2)
        horizontal = (botones[indice][0][0] + botones[indice][0][2]) // 2
        gamelib.draw_text(BASE_BOTONES[indice], horizontal, arriba, fill = 'black', size = 7)

def posicionar_tablero(horizontal, arriba, posicion):
    x_izq = posicion[0]
    x_der = posicion[2]
    y_sup = posicion[1]
    y_inf = posicion[3]
    return horizontal >= x_izq and horizontal <= x_der and arriba >= y_sup and arriba <= y_inf

def click_en_grilla(horizontal, arriba, grilla):
    fila = (arriba - ARR_GRILLA) // CELDA
    columna = (horizontal - IZQ_GRILLA) // CELDA
    en_grilla = fila in range(TAM) and columna in range(TAM)
    return grilla[fila][columna] if en_grilla else None

def click_en_funciones(horizontal, arriba, paleta_boton):
    indice = 0
    while indice < len(paleta_boton) and not posicionar_tablero(horizontal, arriba, paleta_boton[indice][0]):
        indice +=1
    return indice if indice < len(paleta_boton) else None

def paint_mostrar(grilla, paleta, indice_actual, botones,balde): # defino interfaz
    gamelib.draw_begin()
    gamelib.draw_rectangle(0, 0, ANCHO_VENTANA+1, ALTO_VENTANA+1, fill = FONDO_PANTALLA, width = 0)
    dibujar_grilla(grilla)
    dibujar_paleta(paleta, indice_actual)
    dibujar_botones(botones, balde)
    gamelib.draw_end()

def color_a_num(color):
    
    if(color):
        if color[0] != '#' or len(color) != 7:
            raise Exception('ErrorAlProcesarColor')
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
    else:
        r, g, b = color_a_num(FONDO_GRILLA)
    return r, g, b
    

def num_a_color(r, g, b, m):
    val = range(m+1)
    if r in val or g in val or b in val:
        return f'#{r:02x}{g:02x}{b:02x}'
    raise Exception('ErrorEnColor')

    

def guardar_PPM(grilla):
    nombre = gamelib.input('Nombre del archivo PPM')
    if nombre == None or nombre.strip() == '':
        return
    w = len(grilla[0])
    h = len(grilla)
    with open(nombre,'w') as archivo:
        archivo.write('P3\n')
        archivo.write(f'{w} {h}\n')
        archivo.write(f'{255}\n')
        for fila in range(h):
            for columna in range(w):
                r, g, b = color_a_num(grilla[fila][columna][1])
                archivo.write(f'{r:3} {g:3} {b:3} ')
            archivo.write('\n')
    gamelib.say(f'Archivo "{nombre}" guardado con éxito')

def cargar_PPM(grilla):
    nombre = gamelib.input('Nombre del archivo PPM')
    if nombre == None or nombre.strip() == '':
        return
    try:
        with open(nombre,'r') as archivo:
            linea = archivo.read().split()
        try:
            if linea[0].upper() == 'P3': 
                w = int(linea[1]) 
                h = int(linea[2])
                m = int(linea[3])
                k = 4
            for fila in range(h):
                for columna in range(w):
                    r = int(linea[k])
                    k+=1
                    g = int(linea[k])
                    k+=1
                    b = int(linea[k])
                    k+=1
                    grilla[fila][columna][1] = num_a_color(r, g, b, m)
            gamelib.say(f'Archivo "{nombre}" cargado con éxito')
        except UnsupportedOperation:
            gamelib.say(f'Archivo "{nombre}" tiene un formato erróneo')
    except IOError:
        gamelib.say(f'Archivo "{nombre}" no se encuentra')

def paleta_a_lista(paleta):
    lista = []
    indice = 0
    while indice < len(paleta) and paleta[indice][1]:
        lista.append(color_a_num(paleta[indice][1]))
        indice += 1
    return lista

def guardar_PNG(paleta, grilla):
    nombre = gamelib.input('Nombre del archivo PNG')
    if nombre == None or nombre.strip() == '':
        return
    w = len(grilla[0])
    h = len(grilla)
    lista_colores = paleta_a_lista(paleta)
    lista_colores.append(color_a_num(FONDO_GRILLA))
    imagen = [None] * h
    for fila in range(h):
        imagen[fila] = [None] * w
        for col in range(w):
            color = grilla[fila][col][1]
            if not color:
                color = FONDO_GRILLA
            rgb = color_a_num(color)
            lista_colores.append(rgb)
            imagen[fila][col] = lista_colores.index(rgb)
    png.escribir(nombre, lista_colores, imagen)
    gamelib.say(f'Archivo "{nombre}" guardado con éxito')

def agregar_color(paleta):
    indice = 0
    while indice < PALETA and paleta[indice][1]:
        indice += 1
    if indice < PALETA:
        color = gamelib.input('Ingrese un color (#rrggbb)')
        if color == None or color.strip() == '':
            return
        try:
            color_a_num(color)  #lanza una excepción si el formato no es correcto
            paleta[indice][1] = color
            gamelib.say(f'Color "{color}" agregado con éxito')
        except Exception:
            gamelib.say(f'"{color}" no es un formato correcto')
    else:
        gamelib.say('La paleta de colores está completa')

def pintar_balde(grilla, fila, col, color, color_actual):
     if grilla[fila][col][1] == color:
        grilla[fila][col][1] = color_actual
        if fila > 0:
            pintar_balde(grilla, fila-1, col, color, color_actual)
        if fila+1 < len(grilla):
            pintar_balde(grilla, fila+1, col, color, color_actual)
        if col > 0:
             pintar_balde(grilla, fila, col-1, color, color_actual)
        if col+1 < len(grilla[0]):
             pintar_balde(grilla, fila, col+1, color, color_actual)

    
def main():
    gamelib.title("AlgoPaint")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    grilla = grilla_crear()
    paleta = paleta_crear()
    botones = botones_crear()
    indice_actual = 1
    color_actual = paleta[indice_actual][1]
    balde = False
    accion = Accion()
    accion.agregar(grilla, paleta, indice_actual, balde)
    while gamelib.is_alive():
        paint_mostrar(grilla, paleta, indice_actual, botones, balde)
        ev = gamelib.wait()
        if not ev:
            # El usuario cerró la ventana.
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            celda = click_en_grilla(ev.x, ev.y, grilla)
            indice_paleta = click_en_funciones(ev.x, ev.y, paleta)
            boton = click_en_funciones(ev.x, ev.y, botones)
            if celda:
                if balde:
                    fila = (ev.y-ARR_GRILLA) // CELDA
                    col = (ev.x-IZQ_GRILLA) // CELDA
                    color = grilla[fila][col][1]
                    if color != color_actual:
                        pintar_balde(grilla, fila, col, color, color_actual)
                else:
                    if not celda[1] or celda[1] != color_actual:
                        celda[1] = color_actual
                    else:
                        celda[1] = None
                accion.agregar(grilla, paleta, indice_actual, balde)  
            elif indice_paleta != None:
                if paleta[indice_paleta][1]:
                    indice_actual = indice_paleta
                    color_actual = paleta[indice_actual][1] 
                    accion.agregar(grilla, paleta, indice_actual, balde)               
            elif boton != None:
                # ubico mi funcion boton para que realice las modificaciones del balde y luego el poder hacer y rehacer
                if boton == 0:
                    guardar_PPM(grilla)
                elif boton == 1:
                    cargar_PPM(grilla)
                    accion.agregar(grilla, paleta, indice_actual, balde)
                elif boton == 2:
                    guardar_PNG(paleta, grilla)
                elif boton == 3:
                    agregar_color(paleta)
                    accion.agregar(grilla, paleta, indice_actual, balde)
                elif boton == 4:
                    balde = not balde
                    accion.agregar(grilla, paleta, indice_actual, balde)
                elif boton == 5:
                    item = accion.deshacer(grilla, paleta)
                    if item:
                        indice_actual = item[2]
                        balde = item[3]
                elif boton == 6:
                    item = accion.rehacer(grilla, paleta)
                    if item:
                        indice_actual = item[2]
                        balde = item[3]

        elif ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

gamelib.init(main)