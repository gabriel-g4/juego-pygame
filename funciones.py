import pygame
import os

def cargar_imagenes(path_parcial: str, lista_nombre_animaciones: list, scale: int)-> list:

    lista_animaciones = []

    for animacion in lista_nombre_animaciones:
        lista_temporal = []
        numero_frames = len(os.listdir(f"{path_parcial}\{animacion}"))
        for i in range(numero_frames):
            img = pygame.image.load(f"{path_parcial}\{animacion}\{i}.png").convert_alpha()
            img = pygame.transform.scale_by(img, scale)
            lista_temporal.append(img)
        lista_animaciones.append(lista_temporal)

    return lista_animaciones     
    