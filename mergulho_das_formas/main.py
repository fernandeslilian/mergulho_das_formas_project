import pygame
import random
import sys

from telas.tela_inicial import mostrar_tela_inicial
from telas.tela_game_over import mostrar_tela_game_over
from telas.tela_vitoria import mostrar_tela_vitoria
import database # importa o arquivo do banco de dados

pygame.init()
database.init_db() # inicializa o banco de dados

TELA_LARGURA = 1200
TELA_ALTURA = 800
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("Mergulho das Formas!")

AGUA_MAR = (10, 17, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COR_PONTUACAO = (160, 200, 196)

#paleta de cores do fundo
AZUL_PROFUNDO = (0, 63, 107)
AZUL_OCEANO = (26, 117, 188)
AZUL_CLARO = (126, 201, 245)
CORAL_ROSA = (247, 141, 167)
VERDE_ALGA = (76, 174, 76)
VERDE_AGUA = (163, 217, 201)
VERMELHO = (198, 40, 40)
CINZA = (122, 122, 122)
AZUL_BALEIA = (44, 62, 80)
BEGE_AREIA = (245, 230, 200)

clock = pygame.time.Clock()
FPS = 60

# carregando fontes com tratamento de erro
try:
    font = pygame.font.Font("fonts/soulwave.ttf", 50)
    small_font = pygame.font.Font("fonts/squadgoals.ttf", 25)
except FileNotFoundError:
    print("Erro: Arquivo de fonte não encontrado. Usando fontes padrão.")
    font = pygame.font.SysFont("Arial", 50) 
    small_font = pygame.font.SysFont("Arial", 25)
except pygame.error as e:
    print(f"Erro ao carregar fonte: {e}. Usando fontes padrão.")
    font = pygame.font.SysFont("Arial", 50) 
    small_font = pygame.font.SysFont("Arial", 25)

PEIXE_LARGURA = 100
PEIXE_ALTURA = 100
ITEM_LARGURA = 80
ITEM_ALTURA = 80
# carregando imagens com tratamento de erro
try:
    fundo_img_original = pygame.image.load('assets/fundo.png').convert()
    fundo_img = pygame.transform.scale(fundo_img_original, (TELA_LARGURA, TELA_ALTURA))
    
    fish_img_original = pygame.image.load('assets/peixe.png').convert_alpha()
    fish_img = pygame.transform.scale(fish_img_original, (PEIXE_LARGURA, PEIXE_ALTURA))

    vidaTotal = pygame.transform.scale(pygame.image.load('vidas/vidaTotal.png').convert_alpha(), (100, 100))
    vida2 = pygame.transform.scale(pygame.image.load('vidas/vida2.png').convert_alpha(), (90, 90))
    vida1 = pygame.transform.scale(pygame.image.load('vidas/vida1.png').convert_alpha(), (90, 90))

    circulo = pygame.transform.scale(pygame.image.load('formas/circulo.jpg').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    triangulo = pygame.transform.scale(pygame.image.load('formas/triangulo.jpg').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    trapezio = pygame.transform.scale(pygame.image.load('formas/trapezio.png').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    losango = pygame.transform.scale(pygame.image.load('formas/losango.png').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    hexagono = pygame.transform.scale(pygame.image.load('formas/hexagono.jpg').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    quadrado = pygame.transform.scale(pygame.image.load('formas/quadrado.png').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
    
    item_imagens = [circulo, triangulo, trapezio, losango, hexagono, quadrado]

except pygame.error as e:
    print("Erro ao carregar imagens")
    print(e)
    pygame.quit()
    sys.exit()


gravidade = 0.5
nado_peixe = -8
nado_peixe_right = 8
fish_rect = fish_img.get_rect(center = (TELA_LARGURA // 4, TELA_ALTURA // 2))

SPAWNITEM = pygame.USEREVENT
pygame.time.set_timer(SPAWNITEM, 1000) 

# ===================================================================
# FUNÇÕES DO JOGO
# ===================================================================

def novo_item(): 
    """ 
        Pega uma imagem aleatória para os itens que caem. 
    """
    return random.choice(item_imagens)

def desenha_areia():
    pygame.draw.rect(tela, (243, 156, 18), (0, TELA_ALTURA - 50, TELA_LARGURA, 50))
    pygame.draw.rect(tela, (230, 126, 34), (0, TELA_ALTURA - 45, TELA_LARGURA, 5))

def cria_item():
    random_item_y = random.randint(50, TELA_ALTURA - 100)
    item_image = random.choice(item_imagens) 
    item_rect = item_image.get_rect(midleft = (TELA_LARGURA + 50, random_item_y))
    return {'rect': item_rect, 'image': item_image}

def move_figura(figura):
    for item in figura:
        item['rect'].centerx -= 4
    return [item for item in figura if item['rect'].right > -10]

def figura_itens(figura):
    for item in figura:
        tela.blit(item['image'], item['rect'])

def get_vida_image(vidas):
    if vidas == 3: return vidaTotal
    elif vidas == 2: return vida2
    elif vidas == 1: return vida1
    else: return None    


def verifica_itens(figura, vidas, alvos):
    for item in figura[:]:
        if fish_rect.colliderect(item['rect']):
            
            e_alvo = False
            # verifica se o item pego é um dos alvos
            for alvo in alvos:
                # se for o alvo e a contagem for maior que zero
                if item['image'] == alvo['image'] and alvo['count'] > 0:
                    alvo['count'] -= 1 # diminui a contagem
                    e_alvo = True
                    break # para o loop, já encontrou o alvo
            
            # se colidiu e não era um alvo que precisava, perde vida
            if not e_alvo: 
                vidas-= 1
                
            figura.remove(item) # remove o item da tela
            
    return figura, vidas, alvos # retorna a lista de alvos atualizada


def display_hud(vidas, alvos, tempo_decorrido_seg): 
    
    # desenha o retangulo do HUD
    pygame.draw.rect(tela, (100, 200, 196), (1050, 10, 140, 180), border_radius=15)

    # vidas
    vida_img = get_vida_image(vidas)
    if vida_img:
        tela.blit(vida_img, (10, -20))
    
    # mostra o timer
    tempo_texto = small_font.render(f"Tempo: {int(tempo_decorrido_seg)}s", True, WHITE)
    tempo_rect = tempo_texto.get_rect(center=(TELA_LARGURA // 2, 30))
    tela.blit(tempo_texto, tempo_rect)

    # alvos
    img1 = alvos[0]['image']
    count1 = alvos[0]['count']
    
    img2 = alvos[1]['image']
    count2 = alvos[1]['count']

    pos_img1 = (1060, 20) 
    tela.blit(img1, pos_img1)
    
    texto_1 = small_font.render(f"{count1}", True, WHITE)

    pos_texto1 = (pos_img1[0] + ITEM_LARGURA + 5, pos_img1[1] + (ITEM_ALTURA//2) - 15)
    tela.blit(texto_1, pos_texto1)

    pos_img2 = (1060, pos_img1[1] + ITEM_ALTURA + 10) # Posição (embaixo da img1)
    tela.blit(img2, pos_img2)
    
    texto_2 = small_font.render(f"{count2}", True, WHITE)
    pos_texto2 = (pos_img2[0] + ITEM_LARGURA + 5, pos_img2[1] + (ITEM_ALTURA//2) - 15)
    tela.blit(texto_2, pos_texto2)



def resetar_jogo():
    """
    Reinicia as variáveis principais do jogo para um novo jogo.
    Retorna os valores resetados.
    """
    vidas = 3
    item_lista = []
    fish_rect.center = (TELA_LARGURA // 4, TELA_ALTURA // 2)
    mov_peixe = 0
    
    # escolhe 2 imagens diferentes da lista
    alvo_a, alvo_b = random.sample(item_imagens, 2)
    
    # lista de alvos a serem pegos na partida
    alvos = [
        {'image': alvo_a, 'count': 3}, # 3 unidades do primeiro
        {'image': alvo_b, 'count': 2}  # 2 unidades do segundo
    ]
    
    return vidas, item_lista, mov_peixe, alvos # retorna a lista de alvos

# ===================================================================
#   LOOP PRINCIPAL (GERENCIADOR DE ESTADO)
# ===================================================================

estado_jogo = 'menu' # 'menu', 'jogando', 'game_over', 'sair'

vidas, item_lista, mov_peixe, alvos = resetar_jogo()

# variáveis para o nome do jogador e tempo
nome_jogador = ""
tempo_inicio_partida = 0
tempo_final_segundos = 0

while estado_jogo != 'sair':
    
    if estado_jogo == 'menu':
        AGUA_MAR = AZUL_OCEANO
        nome_jogador_ou_false = mostrar_tela_inicial(
            tela, AGUA_MAR, font, small_font,
            TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS
        )
        
        # pega o nome
        if isinstance(nome_jogador_ou_false, str) and len(nome_jogador_ou_false) > 0:
            nome_jogador = nome_jogador_ou_false
            estado_jogo = 'jogando'
            vidas, item_lista, mov_peixe, alvos = resetar_jogo()
            tempo_inicio_partida = pygame.time.get_ticks() # iniciando o timer
        else:
            estado_jogo = 'sair'

    elif estado_jogo == 'jogando':
        # calculando o tempo decorrido
        tempo_atual_ms = pygame.time.get_ticks() - tempo_inicio_partida
        tempo_decorrido_seg = tempo_atual_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado_jogo = 'sair'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    mov_peixe = 0 
                    mov_peixe += nado_peixe
                if event.key == pygame.K_RIGHT:
                    mov_peixe = 0
                    mov_peixe +- nado_peixe_right
                if event.key == pygame.K_r: 
                    vidas, item_lista, mov_peixe, alvos = resetar_jogo()
                    tempo_inicio_partida = pygame.time.get_ticks() # reinicia timer no reset manual

            if event.type == SPAWNITEM:
                item_lista.append(cria_item())
        
        if estado_jogo == 'sair':
            break

        tela.blit(fundo_img, (0, 0))
        
        mov_peixe += gravidade
        fish_rect.y += int(mov_peixe)

        if fish_rect.top < 0: fish_rect.top = 0
        if fish_rect.bottom > TELA_ALTURA - 50: fish_rect.bottom = TELA_ALTURA - 50
        
        item_lista = move_figura(item_lista)
        
        item_lista, vidas, alvos = verifica_itens(item_lista, vidas, alvos)
        
        # verifica se as duas contagens de alvos são zero ou menos
        if alvos[0]['count'] <= 0 and alvos[1]['count'] <= 0:
            estado_jogo = 'vitoria'
            # salva o tempo final e adiciona no banco de dados
            tempo_final_segundos = tempo_decorrido_seg
            database.add_score(nome_jogador, tempo_final_segundos)
        
        elif vidas <= 0: 
            estado_jogo = 'game_over'
        
        figura_itens(item_lista)
        tela.blit(fish_img, fish_rect)
        desenha_areia()
        
        # passa os alvos E o tempo pro hud
        display_hud(vidas, alvos, tempo_decorrido_seg)

        pygame.display.update()
        clock.tick(FPS)

    elif estado_jogo == 'game_over':

        acao = mostrar_tela_game_over(
            tela, AGUA_MAR, font, small_font,
            TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS
        )
        
        if acao == 'jogar_novamente':
            estado_jogo = 'jogando'
            vidas, item_lista, mov_peixe, alvos = resetar_jogo()
            tempo_inicio_partida = pygame.time.get_ticks() # iniciando o timer
        elif acao == 'menu_inicial':
            estado_jogo = 'menu'
        elif acao == 'sair':
            estado_jogo = 'sair'
    
    elif estado_jogo == 'vitoria':
        ranking_atual = database.get_ranking()
        
        acao = mostrar_tela_vitoria(
            tela, AGUA_MAR, font, small_font,
            TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS,
            tempo_final_segundos, ranking_atual
        )
        
        if acao == 'jogar_novamente':
            estado_jogo = 'jogando'
            vidas, item_lista, mov_peixe, alvos = resetar_jogo()
            tempo_inicio_partida = pygame.time.get_ticks() # iniciando o timer 
        elif acao == 'menu_inicial':
            estado_jogo = 'menu'
        elif acao == 'sair':
            estado_jogo = 'sair'

pygame.quit()
sys.exit()