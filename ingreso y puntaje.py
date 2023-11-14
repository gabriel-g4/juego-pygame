import pygame

pygame.init()

font_input = pygame.font.Font(r"IMAGENES\PROPS\monogram.ttf", 32)

ingreso = ""

ingreso_rect = pygame.Rect(220,0,300,300)

on = True

screen = pygame.display.set_mode([800, 600])

while on:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            elif len(ingreso) < 3:
                ingreso += event.unicode
    
    screen.fill((127,127,0))
    font_input_surface = font_input.render(ingreso, True, (0,0,0))
    font_rect = font_input_surface.get_rect()
    pygame.draw.rect(screen, (0,0,0),(font_rect.x-10, font_rect.y-10, font_rect.w+20, font_rect.h+20), 2)
    screen.blit(font_input_surface, (ingreso_rect.x+5, ingreso_rect.y+5))

    pygame.display.flip()

pygame.quit()