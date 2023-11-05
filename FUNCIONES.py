import pygame
import os

def cargar_imagenes(personaje: str, lista_nombre_animaciones: list, scale: int)-> list:

    lista_animaciones = []

    for animacion in lista_nombre_animaciones:
        lista_temporal = []
        numero_frames = len(os.listdir(f"IMAGENES\PERSONAJES\{personaje}\{animacion}"))
        for i in range(numero_frames):
            img = pygame.image.load(f"IMAGENES\PERSONAJES\{personaje}\{animacion}\{i}.png").convert_alpha()
            img = pygame.transform.scale_by(img, scale)
            lista_temporal.append(img)
        lista_animaciones.append(lista_temporal)

    return lista_animaciones     
    