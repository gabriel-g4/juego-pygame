from .Rana import Rana
from constantes.CONSTANTES import *
from clases.Decoracion import Decoracion
from clases.Salida import Salida

class Mundo:
    def __init__(self) -> None:
        self.lista_obstaculos = []
    
    def procesar_datos(self, mapa_nivel, lista_tiles, fuente, jugador, grupo_enemigos, grupo_decoracion, grupo_salida):

        for y, fila in enumerate(mapa_nivel):
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
                        decoracion = Decoracion(img , (x * TILE_SIZE), (y * TILE_SIZE))
                        grupo_decoracion.add(decoracion)
                        jugador.rect.x = (x * TILE_SIZE)
                        jugador.rect.y = (y * TILE_SIZE)
                    elif tile == 39:
                        salida = Salida(img , (x * TILE_SIZE), (y * TILE_SIZE))
                        grupo_salida.add(salida)

    def dibujar(self, screen, screen_scroll):
        for tile in self.lista_obstaculos:
            tile[1].x += screen_scroll
            #pygame.draw.rect(screen, (0,255,0), tile[1])
            screen.blit(tile[0], tile[1])

