import pygame


def cargar_sprites(path_parcial: str, rango: int, scale = 1) -> list:

    lista = []

    for i in range(rango):
        path = (path_parcial) + str(i) + ".png"
        imagen = pygame.image.load(path)
        imagen = pygame.transform.scale_by(imagen, scale)
        lista.append(imagen)
    
    return lista