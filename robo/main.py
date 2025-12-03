import pygame
import random
from typing import List
from classes import * 

pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
fundo = pygame.image.load("img/fundo.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

FPS = 60
clock = pygame.time.Clock()

# grupos e objetos iniciais
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()


def reset_game():
    global jogador, todos_sprites, inimigos, tiros, pontos, spawn_timer, game_over
    # limpar grupos
    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()

  
    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)

 
    pontos = 0
    spawn_timer = 0
    game_over = False



jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)


pygame.mixer.init()
pygame.mixer.music.load("sons/musica de fundo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

tiro_som = pygame.mixer.Sound("sons/tiro.wav")
morte_som = pygame.mixer.Sound("sons/morte.wav")
item_som = pygame.mixer.Sound("sons/interação com item.wav")
morteini_som = pygame.mixer.Sound("sons/morteini.wav")

pontos = 0
spawn_timer = 0

rodando = True
game_over = False
telaparada = None  

while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

     
        if game_over:
            pygame.mixer.music.set_volume(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                
                reset_game()
                pygame.mixer.init()
                pygame.mixer.music.load("sons/musica de fundo.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            continue

      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)
                tiro_som.play()

    if not game_over:
        # timer de entrada dos inimigos
        spawn_timer += 1
        if spawn_timer > 80:
            x = random.randint(40, LARGURA - 40)
            y = -40
            escolha = random.randint(1, 5)
            if escolha == 1:
                robo = Robo(x, y)
            if escolha == 2:
                robo = RoboZigueZague(x, y)
            if escolha == 3:
                robo = RoboRapido(x, y)
            if escolha == 4:
                robo = RoboCiclico(x, y)
            if escolha == 5:
                robo = RoboSaltador(x, y)
            todos_sprites.add(robo)
            inimigos.add(robo)
            spawn_timer = 0

        colisoes = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        for robo in colisoes:
            pontos += 1
            
            explosao = Explosao(robo.rect.centerx, robo.rect.centery)
            todos_sprites.add(explosao)
            if colisoes:
                morteini_som.play()

        colidiram = pygame.sprite.spritecollide(jogador, inimigos, True)
        for robo in colidiram:
            explosao = Explosao(robo.rect.centerx, robo.rect.centery)
            todos_sprites.add(explosao)
            jogador.vida -= 1
            if jogador.vida>=1:
                morteini_som.play()
            if jogador.vida <= 0:
                print("GAME OVER!")
                morte_som.play()
            
                telaparada = TELA.copy()
                game_over = True

    
        todos_sprites.update()

    
        TELA.blit(fundo, (0, 0))
        todos_sprites.draw(TELA)

        # Painel de pontos e vida
        font = pygame.font.SysFont(None, 30)
        texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
        TELA.blit(texto, (10, 10))

    else:
      
        if telaparada:
            TELA.blit(telaparada, (0, 0))
        else:
        
            TELA.blit(fundo, (0, 0))

        textomaior = pygame.font.SysFont(None, 64)
        textomenor = pygame.font.SysFont(None, 28)
        texto_morte = textomaior.render("VOCÊ MORREU", True, (255, 0, 0))
        instrucoes = textomenor.render("Pressione R para reiniciar", True, (255, 255, 255))

       
        rect_morte = texto_morte.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20))
        rect_instr = instrucoes.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30))

       
        sombra = pygame.Surface((rect_morte.width + 20, rect_morte.height + 20), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        TELA.blit(sombra, (rect_morte.x - 10, rect_morte.y - 10))

        TELA.blit(texto_morte, rect_morte)
        TELA.blit(instrucoes, rect_instr)

    pygame.display.flip()

pygame.quit()
