from Rana import Rana
from CONSTANTES import *
from Decoracion import Decoracion
from Salida import Salida

class Mundo:
    def __init__(self) -> None:
        self.lista_obstaculos = []
    
    def procesar_datos(self, datos_nivel, lista_tiles, fuente, jugador, grupo_enemigos, grupo_decoracion, grupo_salida):
        
        for y, fila in enumerate(datos_nivel):
            for x, tile in enumerate(fila):
                if tile > -1:
                    img = lista_tiles[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    
                    datos_tile = [img, img_rect]
                    if tile >= 0 and tile <= 33:
                        self.lista_obstaculos.append(datos_tile)
                    elif tile > 33 and tile < 37:
                        decoracion = Decoracion(img , (x * TILE_SIZE), (y * TILE_SIZE))
                        grupo_decoracion.add(decoracion)
                    elif tile == 37:
                        rana = Rana(x * TILE_SIZE, y * TILE_SIZE, 2, 2, fuente, jugador)
                        grupo_enemigos.add(rana)
                    elif tile == 38:
                        salida = Salida(img , (x * TILE_SIZE), (y * TILE_SIZE))
                        grupo_salida.add(salida)

    def dibujar(self, screen):
        for tile in self.lista_obstaculos:
            #pygame.draw.rect(screen, (0,255,0), tile[1])
            screen.blit(tile[0], tile[1])

