import pygame
import random
from classes import *
from inicio import tela_inicial


pygame.init()

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

continuar = tela_inicial(TELA, LARGURA, ALTURA)
if not continuar:
    pygame.quit()
    exit()
tempo_inicio = pygame.time.get_ticks()
tempo_sem_dano = tempo_inicio
pausado = False

SPAWN_INICIAL = 120
SPAWN_MINIMO = 40

boss_ocorreu = 0
FPS = 60
clock = pygame.time.Clock()

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
powerups = pygame.sprite.Group()
tiros_boss = pygame.sprite.Group()
boss_grupo = pygame.sprite.Group()

def efeito_apocalipse(tela):
    flash = pygame.Surface((LARGURA, ALTURA))
    flash.fill((255, 255, 255))

    for alpha in range(0, 180, 15):
        flash.set_alpha(alpha)
        tela.blit(flash, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def carregar_recorde(caminho="robo/recorde.txt"):
    try:
        with open(caminho, "r") as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0

def salvar_recorde(valor, caminho="robo/recorde.txt"):
    try:
        with open(caminho, "w") as f:
            f.write(str(int(valor)))
    except Exception:
        pass

recorde = carregar_recorde()

def tela_pause(tela, largura, altura, recorde, pontos):
    font1 = pygame.font.SysFont(None, 64)
    font2 = pygame.font.SysFont(None, 36)

    texto = font1.render("JOGO PAUSADO", True, (255, 255, 255))
    texto_pontos = font2.render(f"Pontos atuais: {pontos}", True, (255, 255, 255))
    texto_recorde = font2.render(f"Recorde: {recorde}", True, (255, 255, 255))
    texto_info = font2.render("Pressione ESC para continuar", True, (255, 255, 255))

    rect_titulo = texto.get_rect(center=(largura // 2, altura // 2 - 60))
    rect_pontos = texto_pontos.get_rect(center=(largura // 2, altura // 2 - 10))
    rect_recorde = texto_recorde.get_rect(center=(largura // 2, altura // 2 + 30))
    rect_info = texto_info.get_rect(center=(largura // 2, altura // 2 + 80))

    fundo = pygame.image.load("img/fundo.jpg")
    fundo = pygame.transform.scale(fundo, (largura, altura))
    tela.blit(fundo, (0, 0))

    tela.blit(texto, rect_titulo)
    tela.blit(texto_pontos, rect_pontos)
    tela.blit(texto_recorde, rect_recorde)
    tela.blit(texto_info, rect_info)

def reset_jogo():
    global jogador, pontos, spawn_timer, game_over, boss_ocorreu
    global tempo_inicio, easter_ativo, game_victory, continuar_jogo
    global todos_sprites, inimigos, tiros, powerups, boss_grupo, tiros_boss

    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    powerups.empty()
    boss_grupo.empty()
    tiros_boss.empty()

    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)

    pontos = 0
    spawn_timer = 0
    boss_ocorreu = 0
    game_over = False
    game_victory = False
    continuar_jogo = False
    easter_ativo = False
    tempo_inicio = pygame.time.get_ticks()

def tela_derrota():
    fonte_grande = pygame.font.SysFont(None, 64)
    fonte_media = pygame.font.SysFont(None, 36)
    fonte_pequena = pygame.font.SysFont(None, 28)
    texto_morte = fonte_grande.render("VOCÊ MORREU", True, (255, 0, 0))
    pontos_du_player = fonte_media.render(f"Sua pontuação: {pontos}", True, (255, 255, 255))
    recorde_newbie = fonte_media.render(f"Maior pontuação: {recorde}", True, (255, 255, 255))
    instrucoes = fonte_pequena.render("Pressione R para reiniciar", True, (255, 255, 255))

    rect_morte = texto_morte.get_rect(center=(LARGURA // 2, ALTURA // 2 - 80))
    rect_pontos = pontos_du_player.get_rect(center=(LARGURA // 2, ALTURA // 2 - 10))
    rect_recorde = recorde_newbie.get_rect(center=(LARGURA // 2, ALTURA // 2 + 40))
    rect_instr = instrucoes.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))

    sombra = pygame.Surface((rect_morte.width + 20, rect_morte.height + 20), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 150))
    TELA.blit(sombra, (rect_morte.x - 10, rect_morte.y - 10))

    TELA.blit(texto_morte, rect_morte)
    TELA.blit(pontos_du_player, rect_pontos)
    TELA.blit(recorde_newbie, rect_recorde)
    TELA.blit(instrucoes, rect_instr)

def tela_vitoria():
    fonte_grande = pygame.font.SysFont(None, 64)
    fonte_media = pygame.font.SysFont(None, 36)
    fonte_pequena = pygame.font.SysFont(None, 28)
    texto_morte = fonte_grande.render("VOCÊ VENCEU!", True, (255, 255, 0))
    pontos_du_player = fonte_media.render(f"Sua pontuação: {pontos}", True, (255, 255, 255))
    recorde_newbie = fonte_media.render(f"Maior pontuação: {recorde}", True, (255, 255, 255))
    instrucao1 = fonte_pequena.render("Pressione R para reiniciar", True, (255, 255, 255))
    instrucao2 = fonte_pequena.render("Pressione V para continuar", True, (255, 255, 255))

    rect_morte = texto_morte.get_rect(center=(LARGURA // 2, ALTURA // 2 - 80))
    rect_pontos = pontos_du_player.get_rect(center=(LARGURA // 2, ALTURA // 2 - 10))
    rect_recorde = recorde_newbie.get_rect(center=(LARGURA // 2, ALTURA // 2 + 40))
    rect_instr = instrucao1.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))
    rect_instr2 = instrucao2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 140))

    sombra = pygame.Surface((rect_morte.width + 20, rect_morte.height + 20), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 150))
    TELA.blit(sombra, (rect_morte.x - 10, rect_morte.y - 10))

    TELA.blit(texto_morte, rect_morte)
    TELA.blit(pontos_du_player, rect_pontos)
    TELA.blit(recorde_newbie, rect_recorde)
    TELA.blit(instrucao1, rect_instr)
    TELA.blit(instrucao2, rect_instr2)
 

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

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
velocidade_som = pygame.mixer.Sound("sons/powerspeed.mp3")

pontos = 0
spawn_timer = 0
tempo_easter_egg = 30000
tempo_sem_dano = pygame.time.get_ticks()
easter_ativo = False

rodando = True
game_over = False
game_victory = False
continuar_jogo = False
telaparada = None

DURACAO_POWERUP_MS = 10000

logo = pygame.image.load("img/logo.png").convert_alpha()
logo = pygame.transform.scale(logo, (600, 400))

while rodando:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if game_over:
            pygame.mixer.music.set_volume(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_jogo()
                pygame.mixer.init()
                pygame.mixer.music.load("sons/musica de fundo.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            
        if game_victory:
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_r:
                    reset_jogo()
                    game_victory = False
                    continuar_jogo = False

                    pygame.mixer.music.load("sons/musica de fundo.mp3")
                    pygame.mixer.music.set_volume(0.35)
                    pygame.mixer.music.play(-1)

                elif event.key == pygame.K_v:
                    game_victory = False
                    continuar_jogo = True

                    pygame.mixer.music.load("sons/musica de fundo.mp3")
                    pygame.mixer.music.set_volume(0.35)
                    pygame.mixer.music.play(-1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE  and not pausado and not game_over:
                pausado = True
            elif event.key == pygame.K_ESCAPE and pausado:
                pausado = False
            if event.key == pygame.K_SPACE:
                tempo_do_jogo = pygame.time.get_ticks()
                tiro_triplo_tempo = getattr(jogador, "tempo_tiro_triplo", 0)
                if tempo_do_jogo < tiro_triplo_tempo:
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

    if pausado:
        tela_pause(TELA, LARGURA, ALTURA, recorde, pontos)
        pygame.display.flip()
        continue

    if game_victory:
        if telaparada:
            TELA.blit(telaparada, (0, 0))
        else:
            TELA.blit(fundo, (0, 0))

        tela_vitoria()
        pygame.display.flip()
        continue

    if not game_over and not game_victory:
        agora = pygame.time.get_ticks()

        if not easter_ativo and agora - tempo_sem_dano >= tempo_easter_egg:
            robo_dourado = RoboDourado(random.randint(100, LARGURA-100), -80)
            todos_sprites.add(robo_dourado)
            inimigos.add(robo_dourado)
            easter_ativo = True

        tempo_atual = pygame.time.get_ticks()
        tempo_sobrevivido = (tempo_atual - tempo_inicio) // 1000

        intervalo_spawn = SPAWN_INICIAL - (tempo_sobrevivido * 2)
        if intervalo_spawn < SPAWN_MINIMO:
            intervalo_spawn = SPAWN_MINIMO

        spawn_timer += 1

        if spawn_timer >= intervalo_spawn and len(boss_grupo) == 0:
            spawn_timer = 0

            x = random.randint(40, LARGURA - 40)
            y = -40

            escolha = random.randint(1, 6)
            if escolha == 1:
                robo = Robo(x, y)
            elif escolha == 2:
                robo = RoboZigueZague(x, y)
            elif escolha == 3:
                robo = RoboRapido(x, y)
            elif escolha == 4:
                robo = RoboCiclico(x, y)
            elif escolha == 5:
                robo = RoboSaltador(x, y)
            elif escolha == 6:
                try:
                    robo = RoboCacador(x, y, jogador)
                except Exception:
                    robo = Robo(x, y)

            todos_sprites.add(robo)
            inimigos.add(robo)

        if pontos >= 75 and len(boss_grupo) == 0 and boss_ocorreu == 0:
            for inimigo in inimigos:
                inimigo.kill()

            boss = Boss(LARGURA // 2, 120, jogador, tiros_boss)
            todos_sprites.add(boss)
            boss_grupo.add(boss)
            boss_ocorreu = 1

        if boss_ocorreu == 1 and len(boss_grupo) == 0:
            game_victory = True
            continuar_jogo = False
            boss_ocorreu = 2
            telaparada = TELA.copy()

            pygame.mixer.music.load("sons/vitoria.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(0)
        elif game_victory and continuar_jogo:
            game_victory = False
                
        colisoes = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        for robo in colisoes:
            pontos += 1
            if isinstance(robo, RoboDourado):
                power = PowerUpApocalipse(robo.rect.centerx, robo.rect.centery)
                todos_sprites.add(power)
                powerups.add(power)
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
            if random.random() < 0.05:
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
            tempo_sem_dano = pygame.time.get_ticks()
            if jogador.vida >= 1:
                morteini_som.play()
            if jogador.vida <= 0:
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(recorde)
                morte_som.play()
                telaparada = TELA.copy()
                game_over = True

        colisão_com_powup = pygame.sprite.spritecollide(jogador, powerups, True)
        for p in colisão_com_powup:
            tempo_do_jogo = pygame.time.get_ticks()
            if isinstance(p, PowerUpVelocidade):
                velocidade_som.play()
                if not hasattr(jogador, "vel_base"):
                    jogador.vel_base = getattr(jogador, "velocidade", 5)
                try:
                    jogador.velocidade = 8
                except Exception:
                    pass
                jogador.tempo_vel = tempo_do_jogo + DURACAO_POWERUP_MS
            elif isinstance(p, PowerUpTiroTriplo):
                jogador.tempo_tiro_triplo = tempo_do_jogo + DURACAO_POWERUP_MS
                tirot.play()
            elif isinstance(p, PowerUpVidaExtra):
                jogador.vida += 1
                cura.play()
            elif isinstance(p, PowerUpApocalipse):
                efeito_apocalipse(TELA)

                for sprite in inimigos:
                    sprite.kill()

                for boss in boss_grupo:
                    boss.kill()

                for tiro in tiros_boss:
                    tiro.kill()

        colisao_boss = pygame.sprite.groupcollide(boss_grupo, tiros, False, True)
        for boss in colisao_boss:
            boss.vida -= 5
            if boss.vida <= 0:
                boss.kill()
                pontos += 20
                pygame.mixer.music.load("sons/musica de fundo.mp3")
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)

        acertou = pygame.sprite.spritecollide(jogador,tiros_boss,True,collided=lambda a, b: a.rect.colliderect(b.hitbox))
        for _ in acertou:
            jogador.vida -= 1
            tempo_sem_dano = pygame.time.get_ticks()
            if jogador.vida <= 0:
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(recorde)
                morte_som.play()
                telaparada = TELA.copy()
                game_over = True

        tempo_do_jogo = pygame.time.get_ticks()
        if hasattr(jogador, "tempo_vel") and jogador.tempo_vel:
            if tempo_do_jogo > jogador.tempo_vel:
                if hasattr(jogador, "vel_base"):
                    try:
                        jogador.velocidade = jogador.vel_base
                    except Exception:
                        pass
                jogador.tempo_vel = 0

        todos_sprites.update()
        tiros_boss.update()

        TELA.blit(fundo, (0, 0))
        todos_sprites.draw(TELA)
        tiros_boss.draw(TELA)

        for boss in boss_grupo:
            boss.desenhar_barra_vida(TELA)

        fonte_painel = pygame.font.SysFont(None, 30)
        texto = fonte_painel.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
        TELA.blit(texto, (10, 10))

    else:
        if game_over:
            if telaparada:
                TELA.blit(telaparada, (0, 0))
            else:
                TELA.blit(fundo, (0, 0))
            tela_derrota()
        elif game_victory:
            if telaparada:
                TELA.blit(telaparada, (0, 0))
            else:
                TELA.blit(fundo, (0, 0))
            tela_vitoria()

    pygame.display.flip()

pygame.quit()
