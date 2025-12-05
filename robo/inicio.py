import pygame

def tela_inicial(TELA, LARGURA, ALTURA):

    # fundo
    fundo = pygame.image.load("img/fundo.jpg").convert()
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    pygame.mixer.init()
    pygame.mixer.music.load("sons/musica__intro.mp3")
    pygame.mixer.music.set_volume(0.45)
    pygame.mixer.music.play(-1)
    logo = pygame.image.load("img/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (600, 400))

    fonte = pygame.font.SysFont(None, 50)

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        # fundo da tela
        TELA.blit(fundo, (0, 0))

        # Logo centralizada
        TELA.blit(logo, logo.get_rect(center=(LARGURA//2, ALTURA//2.3)))

        # Texto
        texto = fonte.render("Pressione ESPAÇO para iniciar", True, (255, 255, 255))
        TELA.blit(texto, texto.get_rect(center=(LARGURA//2, ALTURA - 80)))

        pygame.display.update()
