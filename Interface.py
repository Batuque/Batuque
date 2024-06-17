import time
from itertools import cycle
from pygame.locals import *
import pygame
import sys
from Batuque import run_batuque
import cv2
import screens.telaLogin as telaLogin, screens.telaRegistro as telaRegistro, screens.menu_volume as menu_volume

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da janela
largura = pygame.display.Info().current_w
altura = pygame.display.Info().current_h
tela = pygame.display.set_mode((largura, altura), pygame.SCALED)

# Carregar imagens
background_image = pygame.image.load("src/Images/tela inicial/imagem_de_fundo.png")
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")
button_play_image = pygame.image.load("src/Images/tela inicial/tocar_button.svg")
button_settings_image = pygame.image.load("src/Images/tela inicial/configuracoes_button.svg")
button_exit_image = pygame.image.load("src/Images/tela inicial/sair_button.svg")
button_login_image = pygame.image.load("src/Images/tela inicial/login_button.svg")
button_registrar_image = pygame.image.load("src/Images/tela inicial/register_button.svg")

# Carregar música
pygame.mixer.music.load("src/Images/tela inicial/drum_no_copyright.mp3")
pygame.mixer.music.set_volume(0.2)

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Definir fonte para a mensagem de boas-vindas
fonte = pygame.font.Font(None, 145)
mensagem_boas_vindas = fonte.render("Sinta o som do batuque!", True, BRANCO)

#TODO arrumar a tela de carregamento
def tocar():
    pygame.init()

    # Parar a música antes de iniciar
    pygame.mixer.music.stop()

    # Mostrar a tela de loading
    tempo_carregamento = 2
    tempo_inicial = time.time()
    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        loading_progress = tempo_decorrido / tempo_carregamento
        loading_screen(loading_progress)
        if tempo_decorrido >= tempo_carregamento:
            break
    # Esperar um curto período de tempo para simular o carregamento
    pygame.time.wait(2000)

    # Iniciar a tela do pygame para o batuque
    screen = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    frames = cycle(run_batuque())

    # Variável para controlar se o menu está aberto
    menu_aberto = False

    # Variável de controle para determinar quando voltar ao menu principal
    voltar_ao_menu_principal = False

    # Loop principal para a função tocar()
    while not voltar_ao_menu_principal:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu_aberto = not menu_aberto
                    if menu_aberto:
                        configuracoes(screen)
                    else:
                        voltar_ao_menu_principal = True  # Define a variável de controle para voltar ao menu principal
            elif event.type == MOUSEBUTTONDOWN and menu_aberto:  # Verifica o clique somente se o menu estiver aberto
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 400 and 400 <= mouse_pos[1] <= 450:
                    menu_aberto = False
                    voltar_ao_menu_principal = True  # Define a variável de controle para voltar ao menu principal

        if not menu_aberto:
            try:
                frame = next(frames)
            except StopIteration:
                break

            # Limpar o fundo da tela
            screen.fill((0, 0, 0))

            # Rotaciona o frame para a direita
            frame_rotacionado = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame_corrigido = cv2.flip(frame_rotacionado, 0)
            frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(frame_corrigido, cv2.COLOR_BGR2RGB))

            # Obtém as dimensões da tela e da superfície da imagem
            imagem_largura, imagem_altura = frame_surface.get_size()

            # Calcula a posição para centralizar a imagem
            pos_x = (largura - imagem_largura) // 2
            pos_y = (altura - imagem_altura) // 2

            screen.blit(frame_surface, (pos_x, pos_y))
            pygame.display.flip()
            clock.tick(30)

        # Verificar se a tecla Esc foi pressionada para fechar o menu
        if menu_aberto and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_aberto = False

    # Liberar a câmera antes de retornar ao menu principal
    del frames  # Liberar a referência ao objeto iterável
    cv2.VideoCapture(0).release()  # Liberar a câmera

    # Retornar ao menu principal (main()) após sair do loop
    main()

def sair():
    pygame.quit()
    sys.exit()

def menu_resolucoes():
    # Definir fonte para o título
    fonte_titulo = pygame.font.Font(None, 48)

    # Definir fonte para as opções
    fonte_opcoes = pygame.font.Font(None, 36)

    # Título da tela de resoluções
    titulo = fonte_titulo.render("Escolha a Resolução", True, BRANCO)

    # Opções disponíveis de resolução
    opcoes_resolucao = [
        {"texto": "800x600", "resolucao": (800, 600)},
        {"texto": "1024x768", "resolucao": (1024, 768)},
        {"texto": "1280x720", "resolucao": (1280, 720)},
        {"texto": "1440x900", "resolucao": (1440, 900)},
        {"texto": "1920x1080", "resolucao": (1920, 1080)},
        {"texto": "Voltar", "acao": "voltar"}
    ]

    # Espaço entre as opções
    espaco = 20

    # Loop principal da tela de resoluções
    selecionando_resolucao = True
    while selecionando_resolucao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar se o clique foi em uma opção de resolução
                for opcao in opcoes_resolucao:
                    if opcao.get("resolucao"):
                        y_pos = (opcoes_resolucao.index(opcao) + 1) * (60 + espaco) + 100
                        if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > y_pos and mouse_pos[1] < y_pos + 50:
                            pygame.display.set_mode(opcao["resolucao"])
                            selecionando_resolucao = False
                            break
                # Verificar se o clique foi no botão de voltar
                if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > 650 and mouse_pos[1] < 700:
                    selecionando_resolucao = False

        tela.fill(PRETO)
        tela.blit(titulo, (100, 50))

        # Exibir opções de resolução
        for opcao in opcoes_resolucao:
            if opcao.get("resolucao"):
                y_pos = (opcoes_resolucao.index(opcao) + 1) * (60 + espaco) + 100
                pygame.draw.rect(tela, BRANCO, pygame.Rect(100, y_pos, 300, 50))
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, PRETO)
                tela.blit(texto_renderizado, (150, y_pos + 10))

        # Exibir botão de voltar
        pygame.draw.rect(tela, BRANCO, pygame.Rect(100, 650, 300, 50))
        texto_voltar = fonte_opcoes.render("Voltar", True, PRETO)
        tela.blit(texto_voltar, (200, 660))

        pygame.display.flip()



def configuracoes(screen):
    # Definir fonte para o título
    fonte_titulo = pygame.font.Font(None, 48)

    # Definir fonte para as opções
    fonte_opcoes = pygame.font.Font(None, 36)

    # Título da tela de configurações
    titulo = fonte_titulo.render("Configurações", True, BRANCO)

    # Espaço entre as opções
    espaco = 20

    configurando = True
    while configurando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    configurando = False
                    return False  # Indicar que o menu foi fechado
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar se o clique foi no botão de resolução
                if 100 <= mouse_pos[0] <= 400 and 200 <= mouse_pos[1] <= 250:
                    menu_resolucoes()
                # Verificar se o clique foi no botão de volume
                elif 100 <= mouse_pos[0] <= 400 and 300 <= mouse_pos[1] <= 350:
                    volume = menu_volume.config_volume(screen)
                    pygame.mixer.music.set_volume(volume)
                # Verificar se o clique foi no botão de voltar
                elif 100 <= mouse_pos[0] <= 400 and 400 <= mouse_pos[1] <= 450:
                    return False

        screen.fill(PRETO)
        screen.blit(titulo, (100, 50))

        # Exibir botão de resolução
        pygame.draw.rect(screen, BRANCO, pygame.Rect(100, 200, 300, 50))
        texto_resolucao = fonte_opcoes.render("Mudar Resolução", True, PRETO)
        screen.blit(texto_resolucao, (150, 210))

        # Exibir botão de volume
        pygame.draw.rect(screen, BRANCO, pygame.Rect(100, 300, 300, 50))
        texto_volume = fonte_opcoes.render("Ajustar Volume", True, PRETO)
        screen.blit(texto_volume, (180, 310))

        # Exibir botão de voltar
        pygame.draw.rect(screen, BRANCO, pygame.Rect(100, 400, 300, 50))
        texto_voltar = fonte_opcoes.render("Menu Principal", True, PRETO)  # Alterado o texto
        screen.blit(texto_voltar, (200, 410))

        pygame.display.flip()

    # Se o loop sair sem ter retornado False, significa que o menu não foi fechado
    return True


# Função para mostrar a tela de loading
def loading_screen(loading_progress):
    tela.fill(PRETO)
    tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))

    # Desenhar a barra de progresso
    pygame.draw.rect(tela, BRANCO, (100, altura - 50, loading_progress * (largura - 200), 20))

    pygame.display.flip()

def main():
    # Definir o tempo de carregamento (em segundos)
    tempo_carregamento = 2
    tempo_inicial = time.time()

    # Mostrar a tela de loading
    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        loading_progress = tempo_decorrido / tempo_carregamento
        loading_screen(loading_progress)

        if tempo_decorrido >= tempo_carregamento:
            break
    # Esperar um curto período de tempo para simular o carregamento
    pygame.time.wait(2000)

    tela.blit(background_image, (0, 0))
    tela.blit(button_play_image, (largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
    tela.blit(button_settings_image, (largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
    tela.blit(button_exit_image, (largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
    tela.blit(mensagem_boas_vindas, (largura // 2 - mensagem_boas_vindas.get_width() // 2, altura // 8))

    tela.blit(button_login_image, (largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 375))

    tela.blit(button_registrar_image, (largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))  

    pygame.display.flip()

    # Iniciar música
    pygame.mixer.music.play(-1)  # Loop infinito

    # Loop principal do programa
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar se o clique foi nos botões
                button_play_rect = button_play_image.get_rect(center=(largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
                button_settings_rect = button_settings_image.get_rect(center=(largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
                button_exit_rect = button_exit_image.get_rect(center=(largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))

                #botão de login
                button_login_rect = button_login_image.get_rect(center=(largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 375))

                # botão registro
                button_registrar_rect = button_registrar_image.get_rect(center=(largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))

                if button_play_rect.collidepoint(event.pos):
                    tocar()
                elif button_settings_rect.collidepoint(event.pos):
                    if not configuracoes(tela):  # Verificar o retorno da função
                        tela.blit(background_image, (0, 0))
                        tela.blit(button_play_image, (largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
                        tela.blit(button_settings_image, (largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
                        tela.blit(button_exit_image, (largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
                        tela.blit(mensagem_boas_vindas, (largura // 2 - mensagem_boas_vindas.get_width() // 2, altura // 8))

                        tela.blit(button_login_image, (largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 375))

                        tela.blit(button_registrar_image, (largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))  
                        pygame.display.flip()  # Atualiza a tela

                # Tela de Login
                elif button_login_rect.collidepoint(event.pos):
                    telaLogin.login(tela, altura, largura)

                # Tela de Cadastro
                elif button_registrar_rect.collidepoint(event.pos):
                    telaRegistro.registrar(tela, altura, largura)

                elif button_exit_rect.collidepoint(event.pos):
                            sair()

        pygame.display.flip()

# Executar o programa
if __name__ == "__main__":
    main()

# Encerrar o Pygame
pygame.quit()
