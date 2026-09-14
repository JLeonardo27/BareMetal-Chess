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
        self.derechos_enroque = {'K': True, 'Q': True, 'k': True, 'q': True}

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

    def mover_pieza(self, origen, destino, promocion=None):
        fila_origen, col_origen = self.notacion_a_indices(origen)
        fila_destino, col_destino = self.notacion_a_indices(destino)

        pieza = self.matriz[fila_origen][col_origen]
        pieza_capturada = self.matriz[fila_destino][col_destino]
        
        es_peon = pieza.lower() == 'p'
        llego_al_final = fila_destino == 0 or fila_destino == 7
        
        if es_peon and llego_al_final:
            if not promocion:
                promocion = input("¿Promover a (Q, R, B, N)?: ").strip().upper()
            pieza = promocion if pieza.isupper() else promocion.lower()

        if pieza == 'K':
            self.derechos_enroque['K'] = False
            self.derechos_enroque['Q'] = False
        elif pieza == 'k':
            self.derechos_enroque['k'] = False
            self.derechos_enroque['q'] = False
            
        if pieza == 'R':
            if col_origen == 0: self.derechos_enroque['Q'] = False
            if col_origen == 7: self.derechos_enroque['K'] = False
        elif pieza == 'r':
            if col_origen == 0: self.derechos_enroque['q'] = False
            if col_origen == 7: self.derechos_enroque['k'] = False
            
        if pieza_capturada == 'R':
            if fila_destino == 7 and col_destino == 0: self.derechos_enroque['Q'] = False
            if fila_destino == 7 and col_destino == 7: self.derechos_enroque['K'] = False
        elif pieza_capturada == 'r':
            if fila_destino == 0 and col_destino == 0: self.derechos_enroque['q'] = False
            if fila_destino == 0 and col_destino == 7: self.derechos_enroque['k'] = False

        if pieza.lower() == 'k' and abs(col_origen - col_destino) == 2:
            if col_destino == 6:
                torre = self.matriz[fila_origen][7]
                self.matriz[fila_origen][5] = torre
                self.matriz[fila_origen][7] = '.'   
            elif col_destino == 2: 
                torre = self.matriz[fila_origen][0]
                self.matriz[fila_origen][3] = torre 
                self.matriz[fila_origen][0] = '.'  

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
        pieza = self.matriz[fila][columna]
        es_blanca = pieza.isupper()

        deltas_caballo = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
            ]
        for df, dc in deltas_caballo:
            f_nueva, c_nueva = fila + df, columna + dc

            if 0 <= f_nueva <=7 and 0 <= c_nueva <= 7:
                destino = self.matriz[f_nueva][c_nueva]
                if destino == '.':
                    movimientos_legales.append((f_nueva, c_nueva))
                else:
                    es_enemiga_blanca = destino.isupper()
                    if es_blanca != es_enemiga_blanca:
                        movimientos_legales.append((f_nueva, c_nueva))

        return movimientos_legales

    def obtener_movimientos_rey(self, fila, columna):
        movimientos_legales = []
        pieza = self.matriz[fila][columna]
        es_blanca = pieza.isupper()

        deltas_rey = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for df, dc in deltas_rey:
             f_nueva, c_nueva = fila + df, columna + dc

             if 0 <= f_nueva <= 7 and 0 <= c_nueva <= 7:
                 destino = self.matriz[f_nueva][c_nueva]

                 if destino == '.':
                     movimientos_legales.append((f_nueva, c_nueva))
                 else:
                     es_enemiga_blanca = destino.isupper()
                     if es_blanca != es_enemiga_blanca:
                         movimientos_legales.append((f_nueva, c_nueva))
        #Enroques
        if es_blanca:
            # Enroque corto (K)
            if self.derechos_enroque['K'] and self.matriz[7][5] == '.' and self.matriz[7][6] == '.':
                movimientos_legales.append((7, 6))
                
            # Enroque largo (Q)
            if self.derechos_enroque['Q'] and self.matriz[7][1] == '.' and self.matriz[7][2] == '.' and self.matriz[7][3] == '.':
                movimientos_legales.append((7, 2))
                
        else:
            # Enroque corto (k)
            if self.derechos_enroque['k'] and self.matriz[0][5] == '.' and self.matriz[0][6] == '.':
                movimientos_legales.append((0, 6))
                
            # Enroque largo (q)
            if self.derechos_enroque['q'] and self.matriz[0][1] == '.' and self.matriz[0][2] == '.' and self.matriz[0][3] == '.':
                movimientos_legales.append((0, 2))
                
        return movimientos_legales
    
    def _obtener_movimientos_deslizantes(self, fila, columna, direcciones):
        movimientos_legales = []
        pieza = self.matriz[fila][columna]
        es_blanca = pieza.isupper()

        for df, dc in direcciones:
            f_actual = fila + df
            c_actual = columna + dc

            while 0 <= f_actual <= 7 and 0 <= c_actual <= 7:
                destino = self.matriz[f_actual][c_actual]
                if destino == '.':
                    movimientos_legales.append((f_actual, c_actual))

                else:
                    es_enemiga_blanca = destino.isupper()
                    if es_blanca != es_enemiga_blanca:
                        movimientos_legales.append((f_actual, c_actual))
                    break
                
                f_actual += df
                c_actual += dc
        return movimientos_legales

    def obtener_movimientos_torre(self, fila, columna):
        direcciones = [(-1, 0), (1,0), (0, -1), (0, 1)]
        return self._obtener_movimientos_deslizantes(fila, columna, direcciones)

    def obtener_movimientos_alfil(self, fila, columna):
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._obtener_movimientos_deslizantes(fila, columna, direcciones)

    def obtener_movimientos_reina(self, fila, columna):
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        return self._obtener_movimientos_deslizantes(fila, columna, direcciones)

    def esta_en_jaque(self, es_blanca):
        rey = 'K' if es_blanca else 'k'
        f_rey, c_rey = -1, -1
        for f in range(8):
            for c in range(8):
                if self.matriz[f][c] == rey:
                    f_rey, c_rey = f, c
                    break
        for f in range(8):
            for c in range(8):
                pieza = self.matriz[f][c]
                if pieza != '.':
                    es_enemiga_blanca = pieza.isupper()

                    if es_blanca != es_enemiga_blanca:
                        movs_enemigos = self.obtener_pseudo_movimientos(f,c)
                        if (f_rey, c_rey) in movs_enemigos:
                            return True
        return False

    def filtrar_movimientos_legales(self, f_origen, c_origen, pseudo_movimientos):
        movimientos_seguros = []
        pieza_movida = self.matriz[f_origen][c_origen]
        es_blanca = pieza_movida.isupper()
        for f_dest, c_dest in pseudo_movimientos:

            pieza_capturada = self.matriz[f_dest][c_dest]

            self.matriz[f_dest][c_dest] = pieza_movida
            self.matriz[f_origen][c_origen] = '.'

            if not self.esta_en_jaque(es_blanca):
                movimientos_seguros.append((f_dest, c_dest))
                
            self.matriz[f_origen][c_origen] = pieza_movida
            self.matriz[f_dest][c_dest] = pieza_capturada
            
        return movimientos_seguros

    def obtener_pseudo_movimientos(self, fila, columna, ultimo_movimiento=None):
        pieza = self.matriz[fila][columna]
        if pieza == '.':
            return []
        
        tipo_pieza = pieza.lower()

        if tipo_pieza == 'p':
            return self.obtener_movimientos_peon(fila, columna, ultimo_movimiento)
        elif tipo_pieza == 'n':
            return self.obtener_movimientos_caballo(fila, columna)
        elif tipo_pieza == 'b':
            return self.obtener_movimientos_alfil(fila, columna)
        elif tipo_pieza == 'r':
            return self.obtener_movimientos_torre(fila, columna)
        elif tipo_pieza == 'q':
            return self.obtener_movimientos_reina(fila, columna)
        elif tipo_pieza == 'k':
            return self.obtener_movimientos_rey(fila, columna)
            
        return []

    def matriz_a_fen(self, turno ='w', enroques='KQkq', al_paso='-', medios_movs=0, movs_completos=1):
        filas_fen = []

        for fila in self.matriz:
            vacios = 0
            fila_str = ""

            for casilla in fila:
                if casilla == '.':
                    vacios += 1
                else:
                    if vacios > 0:
                        fila_str += str(vacios)
                        vacios = 0
                    fila_str += casilla
            if vacios > 0:
                fila_str += str(vacios)
            
            filas_fen.append(fila_str)

        posicion_piezas = "/".join(filas_fen)
        
        fen_final = f"{posicion_piezas} {turno} {enroques} {al_paso} {medios_movs} {movs_completos}"

        return fen_final

    
if __name__ == "__main__":
    juego = TableroAjedrez()
    juego.mover_pieza('e2','e4')
    juego.mover_pieza('f2','f4')
    juego.mover_pieza('g1','f3')
    juego.imprimir_consola()
    print(juego.matriz_a_fen())
