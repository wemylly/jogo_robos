
import pygame
from pygame.locals import *
from sys import exit

def mostrar_inicio():
    pygame.init()
    largura = 1500
    altura = 700
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo')

    estado = 'menu'

    imagem_inicio = pygame.image.load('imagens/inicio.png').convert()
    imagem_inicio = pygame.transform.scale(imagem_inicio, (largura, altura))

    #logo
    logo = pygame.image.load('imagens/imagemquevaibalançar.png').convert_alpha()
    logo = pygame.transform.scale(logo, (200 * 3, 100 * 5))
    logo_x = 475
    logo_y = 50

    logo_vel = 60.0
    logo_y_min = 50 - 10
    logo_y_max = 50 + 10

    botao = pygame.image.load('imagens/botao.png').convert_alpha()
    botao = pygame.transform.scale(botao, (501 * 0.5, 124 * 0.5))
    botao_x = 650
    botao_y = 300

    botao_rect = botao.get_rect(topleft=(botao_x, botao_y))
    clock = pygame.time.Clock()
    FPS = 60

    while True:
        dt = clock.tick(FPS) / 1000.0
        logo_y += logo_vel * dt

        if logo_y < logo_y_min: 
            logo_y= logo_y_min
            logo_vel = -logo_vel
        elif logo_y> logo_y_max:
            logo_y= logo_y_max
            logo_vel = -logo_vel

        if estado == 'menu':
                tela.blit(imagem_inicio, (0,0))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
               mouse_x, mouse_y = pygame.mouse.get_pos()
               if botao_rect.collidepoint(mouse_x, mouse_y):
                 print ("botão acionado")
                 if estado == 'menu':
                    return
                
        tela.blit(botao,(botao_x, botao_y))
        tela.blit(logo,(logo_x, logo_y))
        pygame.display.update()
        clock.tick(60)
