import pygame
import random
from classes import * 

pygame.init()

# --- Configurações da tela  ---
try:
    LARGURA  
except NameError:
    LARGURA = 1020
try:
    ALTURA
except NameError:
    ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))
fundo = pygame.image.load("img/fundo.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

FPS = 60
clock = pygame.time.Clock()

# --- Grupos e objetos iniciais ---
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
powerups = pygame.sprite.Group()  





def reset_game():
    global jogador, todos_sprites, inimigos, tiros, powerups, pontos, spawn_timer, game_over
    # limpar grupos
    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    powerups.empty()

    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)

    pontos = 0
    spawn_timer = 0
    game_over = False

# Cria jogador inicial 
jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

# Inicializa sons/música 
pygame.mixer.init()
pygame.mixer.music.load("sons/musica de fundo.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

tiro_som = pygame.mixer.Sound("sons/tiro.wav")
morte_som = pygame.mixer.Sound("sons/morte.wav")
item_som = pygame.mixer.Sound("sons/interação com item.wav")
morteini_som = pygame.mixer.Sound("sons/morteini.wav")
cura = pygame.mixer.Sound("sons/powerheal.mp3")
tirot = pygame.mixer.Sound("sons/powershoot.mp3")
velocidade = pygame.mixer.Sound("sons/powerspeed.mp3")


pontos = 0
spawn_timer = 0

rodando = True
game_over = False
telaparada = None


DURACAO_POWERUP_MS = 10000  

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
              
                current_time = pygame.time.get_ticks()
                tiro_triplo_tempo = getattr(jogador, "tempo_tiro_triplo", 0)
                if current_time < tiro_triplo_tempo:
                  
                    cx = jogador.rect.centerx
                    cy = jogador.rect.y
                    tiro1 = Tiro(cx - 20, cy)
                    tiro1.vel_x = -2
                    tiro2 = Tiro(cx, cy)
                    tiro2.vel_x = 0
                    tiro3 = Tiro(cx + 20, cy)
                    tiro3.vel_x = 2
                    for t in (tiro1, tiro2, tiro3):
                        todos_sprites.add(t)
                        tiros.add(t)
                else:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                tiro_som.play()


    if not game_over:

        spawn_timer += 1
        if spawn_timer > 80:
            x = random.randint(40, LARGURA - 40)
            y = -40
            escolha = random.randint(1, 6)
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
            if escolha == 6:
              
                try:
                    robo = RoboCacador(x, y, jogador)
                except Exception:
                  
                    robo = Robo(x, y)
            todos_sprites.add(robo)
            inimigos.add(robo)
            spawn_timer = 0

    
        colisoes = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        for robo in colisoes:
            pontos += 1
          
            try:
                explosao = Explosao(robo.rect.centerx, robo.rect.centery)
                todos_sprites.add(explosao)
            except Exception:
                pass
     
            if colisoes:
                try:
                    morteini_som.play()
                except Exception:
                    pass

         
            if random.random() < 0.35:
                px, py = robo.rect.center
                p_tipo = random.choice([PowerUpTiroTriplo, PowerUpVelocidade, PowerUpVidaExtra])
                powerup = p_tipo(px, py)
                todos_sprites.add(powerup)
                powerups.add(powerup)

     
        colidiram = pygame.sprite.spritecollide(jogador, inimigos, True)
        for robo in colidiram:
            try:
                explosao = Explosao(robo.rect.centerx, robo.rect.centery)
                todos_sprites.add(explosao)
            except Exception:
                pass
     
            jogador.vida -= 1
            if jogador.vida >= 1:
                morteini_som.play()
            if jogador.vida <= 0:
                print("GAME OVER!")
                morte_som.play()
                telaparada = TELA.copy()
                game_over = True

      
        powerup_col = pygame.sprite.spritecollide(jogador, powerups, True)
        for p in powerup_col:
            current_time = pygame.time.get_ticks()
           
            if isinstance(p, PowerUpVelocidade):
                velocidade.play()
                if not hasattr(jogador, "vel_base"):
                    jogador.vel_base = getattr(jogador, "velocidade", 5)
               
                try:
                    jogador.velocidade = 8
                except Exception:
                    pass
             
                jogador.tempo_vel = current_time + DURACAO_POWERUP_MS

        
            elif isinstance(p, PowerUpTiroTriplo):
                jogador.tempo_tiro_triplo = current_time + DURACAO_POWERUP_MS
                tirot.play()
        
            elif isinstance(p, PowerUpVidaExtra):
                jogador.vida += 1
                cura.play()
                

          
           
              
            

     
        current_time = pygame.time.get_ticks()
       
        if hasattr(jogador, "tempo_vel") and jogador.tempo_vel:
            if current_time > jogador.tempo_vel:
                
                if hasattr(jogador, "vel_base"):
                    try:
                        jogador.velocidade = jogador.vel_base
                    except Exception:
                        pass
                jogador.tempo_vel = 0

        
        todos_sprites.update()

   
        TELA.blit(fundo, (0, 0))
        todos_sprites.draw(TELA)

        # Painel de pontos e vida 
        font = pygame.font.SysFont(None, 30)
        texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
        TELA.blit(texto, (10, 10))

    else:
        # tela de morte 
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
