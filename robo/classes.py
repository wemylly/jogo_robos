import pygame
import random
from typing import List

LARGURA = 1020
ALTURA = 600

# Explosão
explosao_img = pygame.image.load("img/explosao.png")
explosao_frames = [
    pygame.transform.scale(explosao_img, (32, 32)),
    pygame.transform.scale(explosao_img, (64, 64)),
    pygame.transform.scale(explosao_img, (120, 120)),
    pygame.transform.scale(explosao_img, (64, 64)),
    pygame.transform.scale(explosao_img, (32, 32)),
]


# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.sprites: List[pygame.Surface] = []

        jogador1 = pygame.image.load("img/player.png").convert_alpha()
        jogador2 = pygame.image.load("img/player2.png").convert_alpha()

        jogador1 = pygame.transform.scale(jogador1, (80,80))  
        jogador2 = pygame.transform.scale(jogador2, (80,80))

        self.sprites.append(jogador1)
        self.sprites.append(jogador2)

        self.frame = 0

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = 5

    def update(self):
        self.frame += 0.1
        if self.frame >= len(self.sprites):
            self.frame = 0

        self.image = self.sprites[int(self.frame)]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 20))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 95))

class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = explosao_frames
        self.frame = 0
        self.image = self.frames[self.frame]

        # salva o centro fixo
        self.center = (x, y)
        self.rect = self.image.get_rect(center=self.center)

        self.velocidade_anim = 0.3

    def update(self):
        self.frame += self.velocidade_anim

        if int(self.frame) >= len(self.frames):
            self.kill()
            return

        # troca de imagem mantendo o centro
        self.image = self.frames[int(self.frame)]
        self.rect = self.image.get_rect(center=self.center)

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load("img/tiro.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.image = pygame.image.load("img/robo_azul.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_roxo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))

        self.direcao = 1
        self.velocidade = 3

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1


class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_rosa.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 6

class RoboCiclico(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_verde.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))

    
        self.base_x = x
        self.base_y = y

        self.raio = 100
        self.vel_giro = 0.6
       
        self.tabela_x = [0, 1, 2, 3, 2, 1, 0, -1, -2, -3, -2, -1]
        self.tabela_y = [-3, -2, -1, 0, 1, 2, 3, 2, 1, 0, -1, -2]

        self.indice = 0
        self.descida = 1

    def atualizar_posicao(self):
        
        self.base_y += self.descida

        self.indice = (self.indice + self.vel_giro) % len(self.tabela_x)
        i = int(self.indice)

        cx = self.tabela_x[i] * self.raio / 3
        cy = self.tabela_y[i] * self.raio / 3

        self.rect.x = self.base_x + cx
        self.rect.y = self.base_y + cy

 
        if self.rect.y > ALTURA:
            self.kill()

class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_vermelho.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))

        self.vel_y = 0
        self.gravidade = 0.5

        self.forca_pulo = -16
        self.chao = ALTURA - 40
        self.tempo_proximo_pulo = random.randint(60, 160)

     
        self.direcao = random.choice([-1, 1])
        self.vel_x = 5 

    def atualizar_posicao(self):

    
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

    
        if self.rect.bottom >= self.chao:
            self.rect.bottom = self.chao
            self.vel_y = 0

            self.tempo_proximo_pulo = 0
            if self.tempo_proximo_pulo <= 0:
                self.vel_y = self.forca_pulo
                self.tempo_proximo_pulo = random.randint(80, 200)
        
        else:
            self.tempo_proximo_pulo = 0

        self.rect.x += self.direcao * self.vel_x
      
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direcao = 1  

        if self.rect.right >= LARGURA:
            self.rect.right = LARGURA
            self.direcao = -1  
   
        if self.rect.top > ALTURA + 200:
            self.kill()
