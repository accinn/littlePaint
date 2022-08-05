from pila import Pila

class Accion:
    def __init__(self):
        self.atras = Pila()
        self.adelante = Pila()

    def deshacer(self, grilla, paleta):
        try:
            item = self.atras.desapilar()
            self.adelante.apilar(item)
            item = self.atras.tope()
            if item:
                self.recuperar_grilla(grilla, item[0])
                self.recuperar_paleta(paleta, item[1])
                item = (grilla, paleta, item[2], item[3])
        except:
            item = None
        return item

    def rehacer(self, grilla, paleta):
        try:
            item = self.adelante.desapilar()
            self.atras.apilar(item)
            self.recuperar_grilla(grilla, item[0])
            self.recuperar_paleta(paleta, item[1])
            item = (grilla, paleta, item[2], item[3])
        except:
            item = None
        return item

    def agregar(self, grilla, paleta, indice_actual, balde):
        matriz = self.guardar_grilla(grilla)
        lista = self.guardar_paleta(paleta)
        self.atras.apilar((matriz, lista, indice_actual, balde))
        if not self.adelante.esta_vacia():
            self.adelante = Pila()
        
    def guardar_paleta(self, paleta):
        lista = [None] * len(paleta)
        for indice in range(len(lista)):
            lista[indice] = paleta[indice][1] #siendo el p[i][1] es el color
        return lista

    def guardar_grilla(self, grilla):
        matriz = [None] * len(grilla)
        for fil in range(len(matriz)):
            matriz[fil] = [None] * len(grilla[fil])
            for col in range(len(matriz[fil])):
                matriz[fil][col] = grilla[fil][col][1]
        return matriz
        
    def recuperar_grilla(self, grilla, matriz):
        for fil in range(len(matriz)):
            for col in range(len(matriz[fil])):
                grilla[fil][col][1] = matriz[fil][col]
                           
    def recuperar_paleta(self, paleta, lista):
        for indice in range(len(lista)):
            paleta[indice][1] = lista[indice]
    
