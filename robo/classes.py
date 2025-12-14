import pygame
import random
from typing import List
import os
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
# os sons do boss
pygame.mixer.init()
tiro_boss_som = pygame.mixer.Sound("sons/tiro_boss.mp3")
tiro_boss_som.set_volume(0.5)


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

        jogador1 = pygame.transform.scale(jogador1, (100,100))  
        jogador2 = pygame.transform.scale(jogador2, (100,100))

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
        self.rect.x = max(0, min(self.rect.x, LARGURA - 95))
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

        
        self.image = self.frames[int(self.frame)]
        self.rect = self.image.get_rect(center=self.center)

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load("img/tiro.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
      
        self.vel_x = 0

    def update(self):
      
        try:
            self.rect.x += getattr(self, "vel_x", 0)
        except Exception:
            pass
       
        self.rect.y -= self.velocidade
        if self.rect.y < 0 or self.rect.right < 0 or self.rect.left > LARGURA:
            self.kill()



# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=5)
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
        self.velocidade = 1.2
        self.vel_x = 5

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * self.vel_x

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1


class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_rosa.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 14

class RoboCiclico(Robo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("img/robo_verde.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))

    
        self.base_x = x
        self.base_y = y

        self.raio = 150
        self.vel_giro = 0.5
       
        self.tabela_x = [0, 1, 2, 3, 2, 1, 0, -1, -2, -3, -2, -1]
        self.tabela_y = [-3, -2, -1, 0, 1, 2, 3, 2, 1, 0, -1, -2]

        self.indice = 0
        self.descida = 1.4

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
        self.vel_x = 4

    def atualizar_posicao(self):

        self.vel_y += self.gravidade
        if self.vel_y > 7:
            self.vel_y = 7

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

class RoboCacador(Robo):
    def __init__(self, x, y, jogador):
        super().__init__(x, y)

        self.jogador = jogador
        self.image = pygame.image.load("img/robo_cinza.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 5

    def atualizar_posicao(self):
        
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery

        distancia = max(1, (dx**2 + dy**2) ** 0.5)

        self.rect.x += (dx / distancia) * self.velocidade
        self.rect.y += (dy / distancia) * self.velocidade

        if self.rect.y > ALTURA + 40:
            self.kill()

    def update(self):
        self.atualizar_posicao()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 2

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()

class PowerUpVelocidade(PowerUp):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/velocidade.png")
        self.image = pygame.transform.scale(self.image, (80,60))
        super().__init__(x, y)
        

class PowerUpTiroTriplo(PowerUp):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/triplo.png")
        self.image = pygame.transform.scale(self.image, (80,60))
        super().__init__(x, y)

class PowerUpVidaExtra(PowerUp):
    def __init__(self, x, y):
        self.image = pygame.image.load("img/vida.png")
        self.image = pygame.transform.scale(self.image, (80,60))
        super().__init__(x, y)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, jogador, grupo_tiros):
        super().__init__()

        self.image = pygame.image.load("img/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect(center=(x, y))

        self.jogador = jogador
        self.grupo_tiros = grupo_tiros

        self.vida_max = 100
        self.vida = 100

        self.vel_x = 3
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_tiro = 1200 

    def atirar(self):
        tiro = TiroBoss(self.rect.centerx, self.rect.centery, self.jogador)
        self.grupo_tiros.add(tiro)
        tiro_boss_som.play()

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self.vel_x *= -1

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > self.intervalo_tiro:
            self.atirar()
            self.tempo_ultimo_tiro = agora

    def desenhar_barra_vida(self, tela):
        largura = 150
        altura = 15
        x = self.rect.centerx - largura // 2
        y = self.rect.top - 20

        proporcao = self.vida / self.vida_max
        pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))
        pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * proporcao, altura))

class TiroBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo):
        super().__init__()
        self.image = pygame.image.load("img/tiro.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=(x, y))

        dx = alvo.rect.centerx - x
        dy = alvo.rect.centery - y
        distancia = max(1, (dx**2 + dy**2) ** 0.5)

        self.vel_x = (dx / distancia) * 6
        self.vel_y = (dy / distancia) * 6

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if (self.rect.top > ALTURA or self.rect.bottom < 0 or
            self.rect.left > LARGURA or self.rect.right < 0):
            self.kill()
