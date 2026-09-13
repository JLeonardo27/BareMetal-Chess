#Mayusculas para las piezas blancas
#Minusculas para las piezas negras
class TableroAjedrez:
    
    def __init__(self):
        self.matriz = [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ]

    def imprimir_consola(self):

        print("\n    a b c d e f g h")
        print("  +-----------------+")

        for i, fila in enumerate(self.matriz):
            rango = 8 - i
            fila_str = " ".join(fila)
            print(f"{rango} | {fila_str} | {rango}")

        print("  +-----------------+")
        print("    a b c d e f g h\n")

    def notacion_a_indices(self, casilla):

        casilla = casilla.lower()
        columna_letra = casilla[0]
        fila_numero = int(casilla[1])

        columna = ord(columna_letra) - ord('a')
        fila = 8 - fila_numero

        return fila, columna

    def indices_a_notacion(self, fila, columna):

        columna_letra = chr(ord('a') + columna)
        fila_numero = 8 - fila
        
        return f"{columna_letra}{fila_numero}"

    def mover_pieza(self, origen, destino):
        fila_origen, col_origen = self.notacion_a_indices(origen)
        fila_destino, col_destino = self.notacion_a_indices(destino)

        pieza = self.matriz[fila_origen][col_origen]
        self.matriz[fila_destino][col_destino] = pieza    
        self.matriz[fila_origen][col_origen] = '.'

    def obtener_movimientos_peon(self, fila, columna, ultimo_movimiento=None):
        movimientos_legales = []
        pieza = self.matriz[fila][columna]
        es_blanca = (pieza == 'P')
    
        direccion = -1 if es_blanca else 1
        fila_inicio = 6 if es_blanca else 1
    
        #AVANCE SIMPLE 
        f_frente = fila + direccion
        if 0 <= f_frente <= 7 and self.matriz[f_frente][columna] == '.':
            movimientos_legales.append((f_frente, columna))
        
        #AVANCE DOBLE 
            if fila == fila_inicio:
                f_doble = fila + (2 * direccion)
                if self.matriz[f_doble][columna] == '.':
                    movimientos_legales.append((f_doble, columna))
                
        # CAPTURAS 
        for delta_columna in [-1, 1]:
            c_diag = columna + delta_columna
            if 0 <= c_diag <= 7:
                pieza_destino = self.matriz[f_frente][c_diag]
                if pieza_destino != '.':
                    es_enemiga = pieza_destino.islower() if es_blanca else pieza_destino.isupper()
                    if es_enemiga:
                        movimientos_legales.append((f_frente, c_diag))
                    
        #EN PASSANT
        if ultimo_movimiento:
            (u_fo, u_co), (u_fd, u_cd), u_pieza = ultimo_movimiento
        
            es_peon_enemigo = (u_pieza == 'p' if es_blanca else u_pieza == 'P')
            movio_dos_casillas = abs(u_fo - u_fd) == 2
            quedo_al_lado = (u_fd == fila and u_cd == c_diag)         
            if es_peon_enemigo and movio_dos_casillas and quedo_al_lado:
                    movimientos_legales.append((f_frente, u_cd))

        return movimientos_legales
        
    def obtener_movimientos_caballo(self, fila, columna):
        movimientos_legales = []
        deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    
        es_pieza_negra = self.matriz[fila][columna].islower() 

        for df, dc in deltas:
            f_nueva, c_nueva = fila + df, columna + dc
        
            if 0 <= f_nueva <= 7 and 0 <= c_nueva <= 7:
                pieza_destino = self.matriz[f_nueva][c_nueva]
            
                if pieza_destino == '.':
                    movimientos_legales.append((f_nueva, c_nueva))
                else:
                    es_enemigo_negro = pieza_destino.islower()
                
                    if es_pieza_negra != es_enemigo_negro:
                        movimientos_legales.append((f_nueva, c_nueva))
                    
        return movimientos_legales
        
if __name__ == "__main__":
    juego = TableroAjedrez()
    juego.imprimir_consola()

    juego.mover_pieza('d2','d4')
    juego.mover_pieza('e2','e4')
    juego.imprimir_consola() 

    juego.mover_pieza('f7','f5')
    juego.imprimir_consola() 

    movimientos_legales = []
    movimientos_legales = juego.obtener_movimientos_peon(4,4)
    for i in movimientos_legales:
        print(i)
