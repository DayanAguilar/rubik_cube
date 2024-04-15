TAM=3

class Cubo:
    def __init__(self,colores = ['w', 'o', 'g', 'r', 'b', 'y'],nombre_archivo="") :
        self.estado=self.cargar_desde_archivo(nombre_archivo)
        if self.estado is None:
            self.n = TAM
            self.colores = colores
            self.cubo = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colores]
        else:
            self.n = int((len(self.estado) / 6) ** (.5))
            self.colores = []
            self.cubo = [[[]]]
            for i, s in enumerate(self.estado):
                if s not in self.colores: self.colores.append(s)
                self.cubo[-1][-1].append(s)
                if len(self.cubo[-1][-1]) == self.n and len(self.cubo[-1]) < self.n:
                    self.cubo[-1].append([])
                elif len(self.cubo[-1][-1]) == self.n and len(self.cubo[-1]) == self.n and i < len(self.estado) - 1:
                    self.cubo.append([[]])
        
    def cargar_desde_archivo(self, nombre_archivo):
        with open(nombre_archivo, "r") as file:
            estado_cubo = "".join(line.strip().replace(" ", "") for line in file)
        estado_cubo = estado_cubo.lower()  
        if len(estado_cubo) < 54: 
            raise ValueError("Faltan mas caracteres")
        if len(estado_cubo) > 54: 
            raise ValueError("Deben ser menos caracteres")
        color_count = {color: estado_cubo.count(color) for color in set(estado_cubo)}
        for color, count in color_count.items():
            if count != 9:
                raise ValueError(f"Numero invalido de colores hay {color} veces")
        return estado_cubo 
    
    def mostrar(self):
        spacing = f'{" " * (len(str(self.cubo[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cubo[0])
        l2 = '\n'.join('  '.join(str(self.cubo[i][j]) for i in range(1,5)) for j in range(len(self.cubo[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cubo[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')   
        
    def giro_horizontal(self, fila, direccion):
        if fila < len(self.cubo[0]):
            if direccion == 0: #Twist left
                self.cubo[1][fila], self.cubo[2][fila], self.cubo[3][fila], self.cubo[4][fila] = (self.cubo[2][fila],
                                                                                              self.cubo[3][fila],
                                                                                              self.cubo[4][fila],
                                                                                              self.cubo[1][fila])

            elif direccion == 1: #Twist right
                self.cubo[1][fila], self.cubo[2][fila], self.cubo[3][fila], self.cubo[4][fila] = (self.cubo[4][fila],
                                                                                              self.cubo[1][fila],
                                                                                              self.cubo[2][fila],
                                                                                              self.cubo[3][fila])
            else:
                print(f'ERROR - direccion must be 0 (left) or 1 (right)')
                return
            if direccion == 0: #Twist left
                if fila == 0:
                    self.cubo[0] = [list(x) for x in zip(*reversed(self.cubo[0]))] #Transpose top
                elif fila == len(self.cubo[0]) - 1:
                    self.cubo[5] = [list(x) for x in zip(*reversed(self.cubo[5]))] #Transpose bottom
            elif direccion == 1: #Twist right
                if fila == 0:
                    self.cubo[0] = [list(x) for x in zip(*self.cubo[0])][::-1] #Transpose top
                elif fila == len(self.cubo[0]) - 1:
                    self.cubo[5] = [list(x) for x in zip(*self.cubo[5])][::-1] #Transpose bottom
        else:
            print(f'ERROR - desired fila outside of rubiks cubo range. Please select a fila between 0-{len(self.cubo[0])-1}')
            return

    def giro_vertical(self, columna, direccion):
        if columna < len(self.cubo[0]):
            for i in range(len(self.cubo[0])):
                if direccion == 0: #Twist down
                    self.cubo[0][i][columna], self.cubo[2][i][columna], self.cubo[4][-i-1][-columna-1], self.cubo[5][i][columna] = (self.cubo[4][-i-1][-columna-1],
                                                                                                                                self.cubo[0][i][columna],
                                                                                                                                self.cubo[5][i][columna],
                                                                                                                                self.cubo[2][i][columna])
                elif direccion == 1: #Twist up
                    self.cubo[0][i][columna], self.cubo[2][i][columna], self.cubo[4][-i-1][-columna-1], self.cubo[5][i][columna] = (self.cubo[2][i][columna],
                                                                                                                                self.cubo[5][i][columna],
                                                                                                                                self.cubo[0][i][columna],
                                                                                                                                self.cubo[4][-i-1][-columna-1])
                else:
                    print(f'ERROR - direccion must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direccion == 0: #Twist down
                if columna == 0:
                    self.cubo[1] = [list(x) for x in zip(*self.cubo[1])][::-1] #Transpose left
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[3] = [list(x) for x in zip(*self.cubo[3])][::-1] #Transpose right
            elif direccion == 1: #Twist up
                if columna == 0:
                    self.cubo[1] = [list(x) for x in zip(*reversed(self.cubo[1]))] #Transpose left
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[3] = [list(x) for x in zip(*reversed(self.cubo[3]))] #Transpose right
        else:
            print(f'ERROR - desired columna outside of rubiks cubo range. Please select a columna between 0-{len(self.cubo[0])-1}')
            return

    def giro_lateral(self, columna, direccion):
        if columna < len(self.cubo[0]):
            for i in range(len(self.cubo[0])):
                if direccion == 0: #Twist down
                    self.cubo[0][columna][i], self.cubo[1][-i-1][columna], self.cubo[3][i][-columna-1], self.cubo[5][-columna-1][-1-i] = (self.cubo[3][i][-columna-1],
                                                                                                                                      self.cubo[0][columna][i],
                                                                                                                                      self.cubo[5][-columna-1][-1-i],
                                                                                                                                      self.cubo[1][-i-1][columna])
                elif direccion == 1: #Twist up
                    self.cubo[0][columna][i], self.cubo[1][-i-1][columna], self.cubo[3][i][-columna-1], self.cubo[5][-columna-1][-1-i] = (self.cubo[1][-i-1][columna],
                                                                                                                                      self.cubo[5][-columna-1][-1-i],
                                                                                                                                      self.cubo[0][columna][i],
                                                                                                                                      self.cubo[3][i][-columna-1])
                else:
                    print(f'ERROR - direccion must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direccion == 0: #Twist down
                if columna == 0:
                    self.cubo[4] = [list(x) for x in zip(*reversed(self.cubo[4]))] #Transpose back
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[2] = [list(x) for x in zip(*reversed(self.cubo[2]))] #Transpose top
            elif direccion == 1: #Twist up
                if columna == 0:
                    self.cubo[4] = [list(x) for x in zip(*self.cubo[4])][::-1] #Transpose back
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[2] = [list(x) for x in zip(*self.cubo[2])][::-1] #Transpose top
        else:
            print(f'ERROR - desired columna outside of rubiks cubo range. Please select a columna between 0-{len(self.cubo[0])-1}')
            return    