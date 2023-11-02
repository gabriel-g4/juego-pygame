import pygame
import COLORES

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, fuente) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direccion = 1 # 1 derecha -1 izquierda
        self.flip = False
        self.vivo = True

        img = pygame.image.load(r"IMAGENES\PERSONAJES\FANTASMA\ghost-idle\0.png").convert_alpha()
        self.imagen = pygame.transform.scale_by(img, scale)
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.rect_valor = fuente.render(str(self.rect), True, COLORES.GRAY)
    
    def chequear_colisiones(self, flecha_rect):
        if self.rect.colliderect(flecha_rect):
            self.vivo = False
        
        
    def dibujarse(self, screen):
        screen.blit(self.imagen, self.rect)

    def dibujar_hitbox(self, screen):
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.topright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.topleft, self.rect.bottomleft)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomleft, self.rect.bottomright)
        pygame.draw.line(screen, COLORES.RED1, self.rect.bottomright, self.rect.topright)