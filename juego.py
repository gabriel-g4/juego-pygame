import pygame
import colores
from funciones import *
from constantes import *
#from Fantasma import *

on = True

pygame.init()

#VENTANA
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Juego")

#FUENTE
fuente = pygame.font.SysFont("Arial", 20)
texto_coordenadas = fuente.render("", True, colores.WHITE)

#CLASES

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed

        img = pygame.image.load(r"IMAGENES\PERSONAJES\FANTASMA\ghost-idle\0.png")
        self.imagen = pygame.transform.scale_by(img, scale)
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        
    def dibujarse(self):
        screen.blit(self.imagen, self.rect)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed

        img = pygame.image.load(r"IMAGENES\PERSONAJES\DUENDA\walk\duenda1.png")
        self.imagen = pygame.transform.scale_by(img, scale)
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        
    def dibujarse(self):
        screen.blit(self.imagen, self.rect)

#IMAGENES

lista_fondos = []
for i in range (1,6):
    path = r"IMAGENES\FONDO\plx-"+ str(i) + ".png"
    fondo = pygame.image.load(path)
    fondo = pygame.transform.scale_by(fondo , 2.3)
    lista_fondos.append(fondo)

lista_duenda_caminar = []
for i in range (1,5):
    path = r"IMAGENES\PERSONAJES\DUENDA\walk\duenda" + str(i) + ".png"
    duenda = pygame.image.load(path)
    if i == 1 or i == 3:
        duenda = pygame.transform.scale_by(duenda , 0.6)
    elif i == 4 or i == 2:
        duenda = pygame.transform.scale_by(duenda , 0.75)
    lista_duenda_caminar.append(duenda)

#fantasma = {}
lista_fantasma_appear = cargar_sprites("IMAGENES\PERSONAJES\FANTASMA\ghost_appears\\", 6)
lista_fantasma_idle = cargar_sprites("IMAGENES\PERSONAJES\FANTASMA\ghost-idle\\", 7)
lista_fantasma_shriek = cargar_sprites("IMAGENES\PERSONAJES\FANTASMA\ghost-shriek\\", 4)
lista_fantasma_vanish = cargar_sprites("IMAGENES\PERSONAJES\FANTASMA\ghost-vanish\\", 7)


estructuras = pygame.image.load(r"IMAGENES\estructuras2.png")
estructuras = pygame.transform.scale_by(estructuras, 1)

#Eventos usuario

timer = pygame.USEREVENT
pygame.time.set_timer(timer, 130)

pos_fotograma_duenda = 0
pos_fotograma_fantasma1 = 0
pos_fotograma_fantasma2 = 0
pos_fotograma_fantasma3 = 0
pos_fotograma_fantasma4 = 0
x_duenda = 0
y_duenda = 380
direccion = DIRECCION_R

fantasma = Fantasma(200, 200, 2, 5)
jugador = Jugador(200, 380, 0.68, 5)


while on:

    lista_eventos = pygame.event.get()
    #######################EVENTOS###########################
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            on = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            coordenadas_click = list(evento.pos)
            texto_coordenadas = fuente.render(str(coordenadas_click), True, colores.WHITE)
            print(coordenadas_click)
        elif evento.type == pygame.USEREVENT:
            pass

    
    lista_presiones = pygame.key.get_pressed()
    if True in lista_presiones:
        if lista_presiones[pygame.K_RIGHT]:
            x_duenda += 10
            pos_fotograma_duenda += 1
            if pos_fotograma_duenda >= len(lista_duenda_caminar):
                pos_fotograma_duenda = 0
            direccion = DIRECCION_R
        elif lista_presiones[pygame.K_LEFT]:
            x_duenda -= 10
            pos_fotograma_duenda += 1
            if pos_fotograma_duenda >= len(lista_duenda_caminar):
                pos_fotograma_duenda = 0
            direccion = DIRECCION_L

            
        


    ##############PANTALLA############################
    for fondo in lista_fondos:
        screen.blit(fondo, (0, 0))

    screen.blit(estructuras, (0,0))
    screen.blit(texto_coordenadas, POS_COORD)

    if direccion != DIRECCION_L:
        screen.blit(lista_duenda_caminar[pos_fotograma_duenda], (x_duenda, y_duenda))
    else:
        auxiliar = pygame.transform.flip(lista_duenda_caminar[pos_fotograma_duenda], True, False)
        screen.blit(auxiliar, (x_duenda, y_duenda))

    jugador.dibujarse()
    fantasma.dibujarse()
    

    pygame.display.flip()

pygame.quit()