import pygame
from tablero import TableroAjedrez
from lichess_api import MotorLichess 

TAMANO_CASILLA = 80
ANCHO = ALTO = TAMANO_CASILLA * 8
MAX_FPS = 15

def cargar_imagenes():
    imagenes = {}
    mapa_archivos = {
        'P': 'wP', 'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK',
        'p': 'bP', 'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK'
    }
    
    for pieza, archivo in mapa_archivos.items():
        try:
            img = pygame.image.load(f"assets/{archivo}.png")
            imagenes[pieza] = pygame.transform.scale(img, (TAMANO_CASILLA, TAMANO_CASILLA))
        except FileNotFoundError:
            print(f"Error: Te falta el archivo assets/{archivo}.png")
            sup_vacia = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA))
            sup_vacia.fill((255, 0, 0))
            imagenes[pieza] = sup_vacia
            
    return imagenes
def dibujar_tablero(pantalla):
    colores = [pygame.Color(238, 238, 210), pygame.Color(118, 150, 86)] 
    for f in range(8):
        for c in range(8):
            color = colores[(f + c) % 2]
            cuadro = pygame.Rect(c * TAMANO_CASILLA, f * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA)
            pygame.draw.rect(pantalla, color, cuadro)

def dibujar_piezas(pantalla, matriz, imagenes):
    for f in range(8):
        for c in range(8):
            pieza = matriz[f][c]
            if pieza != '.':
                cuadro = pygame.Rect(c * TAMANO_CASILLA, f * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA)
                pantalla.blit(imagenes[pieza], cuadro)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Motor de Ajedrez")
    reloj = pygame.time.Clock()
    
    imagenes = cargar_imagenes()
    juego = TableroAjedrez()
    
    casilla_seleccionada = () 
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                
            # Interacción con el Mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                columna = posicion[0] // TAMANO_CASILLA
                fila = posicion[1] // TAMANO_CASILLA
                
                if casilla_seleccionada == (fila, columna):
                    casilla_seleccionada = () # Deseleccionar si haces doble clic
                else:
                    if not casilla_seleccionada:
                        # Primer clic: Seleccionar pieza
                        if juego.matriz[fila][columna] != '.':
                            casilla_seleccionada = (fila, columna)
                    else:
                        # Segundo clic: Intentar mover
                        f_ori, c_ori = casilla_seleccionada
                        
                        origen = juego.indices_a_notacion(f_ori, c_ori)
                        destino = juego.indices_a_notacion(fila, columna)
                        
                        pseudo_movs = juego.obtener_pseudo_movimientos(f_ori, c_ori)
                        movs_legales = juego.filtrar_movimientos_legales(f_ori, c_ori, pseudo_movs)
                        
                        if (fila, columna) in movs_legales:
                            juego.mover_pieza(origen, destino)
                            # (Aquí insertarías la llamada a la API de Lichess)
                            
                        casilla_seleccionada = () # Reiniciamos el selector

        # Actualización visual
        dibujar_tablero(pantalla)
        dibujar_piezas(pantalla, juego.matriz, imagenes)
        pygame.display.flip()
        reloj.tick(MAX_FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
