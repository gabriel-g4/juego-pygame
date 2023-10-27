import pygame

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, scale) -> None:
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("IMAGENES\PERSONAJES\FANTASMA\ghost-idle\0.png")
        self.imagen = pygame.transform.scale_by(img, scale)
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        
    def dibujarse(self):
        screen.blit