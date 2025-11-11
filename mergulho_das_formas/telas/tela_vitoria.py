import pygame
import sys

# Cores
COR_BOTAO = (214, 130, 116)
COR_BOTAO_HOVER = (194, 91, 81)
COR_TEXTO_BOTAO = (255, 255, 255)
COR_VITORIA = (60, 200, 60) # Verde
COR_TEMPO = (240, 240, 100) # Amarelo claro
COR_RANKING = (200, 200, 200) # Cinza claro (para o texto do ranking)

# Paleta de cores
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


COR_FUNDO_BOX_RANKING = AZUL_BALEIA 

def mostrar_tela_vitoria(tela, cor_fundo, font, small_font, TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS, seu_tempo, ranking):
    """
    Mostra a tela de Vitória com o tempo e o ranking.
    Retorna: 'jogar_novamente', 'menu_inicial', ou 'sair'.
    """
    
    btn_largura = 300
    btn_altura = 50
    center_x = TELA_LARGURA // 2
    center_y = TELA_ALTURA // 2

    btn_jogar_novamente_rect = pygame.Rect(center_x - (btn_largura // 2), TELA_ALTURA - 160, btn_largura, btn_altura)
    btn_menu_rect = pygame.Rect(center_x - (btn_largura // 2), TELA_ALTURA - 90, btn_largura, btn_altura)

    ranking_box_rect = pygame.Rect(center_x - 250, 200, 500, 280)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'sair'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if btn_jogar_novamente_rect.collidepoint(mouse_pos):
                        return 'jogar_novamente'
                    if btn_menu_rect.collidepoint(mouse_pos):
                        return 'menu_inicial'

        tela.fill(cor_fundo) 
        # texto de vitória
        vitoria_texto = font.render("VOCÊ VENCEU!", True, COR_VITORIA)
        vitoria_rect = vitoria_texto.get_rect(center=(center_x, 80))
        tela.blit(vitoria_texto, vitoria_rect)
        
        # 
        tempo_texto_str = f"seu tempo: {seu_tempo:.2f} segundos" 
        tempo_texto = small_font.render(tempo_texto_str, True, COR_TEMPO)
        tempo_rect = tempo_texto.get_rect(center=(center_x, 140))
        tela.blit(tempo_texto, tempo_rect)
        
        # tabela de ranking

        # desenha o fundo do box do ranking
        pygame.draw.rect(tela, COR_FUNDO_BOX_RANKING, ranking_box_rect, border_radius=15)
        
        # desenha o título do ranking
        ranking_titulo = small_font.render(" RANKING TOP 5 ", True, WHITE)
        ranking_titulo_rect = ranking_titulo.get_rect(center=(center_x, 220)) 
        tela.blit(ranking_titulo, ranking_titulo_rect)
        
        # posicionamento inicial para os nomes e tempos
        pos_y_ranking = 270 
        
        if not ranking:
            # Mensagem se o ranking estiver vazio
            vazio_texto = small_font.render("Ninguém jogou ainda!", True, COR_RANKING)
            vazio_rect = vazio_texto.get_rect(center=(center_x, pos_y_ranking + 20))
            tela.blit(vazio_texto, vazio_rect)
        else:
            for i, (nome, tempo) in enumerate(ranking):
                
                linha_str = f"{i+1}. {nome} - {tempo:.2f} s"
                linha_texto = small_font.render(linha_str, True, WHITE) 
                linha_rect = linha_texto.get_rect(center=(center_x, pos_y_ranking))
                tela.blit(linha_texto, linha_rect)
                
                pos_y_ranking += 40 # prox linha

       #botões
        cor_btn_1 = COR_BOTAO_HOVER if btn_jogar_novamente_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_1, btn_jogar_novamente_rect, border_radius=10)
        texto_btn1 = small_font.render("jogar novamente", True, COR_TEXTO_BOTAO)
        texto_btn1_rect = texto_btn1.get_rect(center=btn_jogar_novamente_rect.center)
        tela.blit(texto_btn1, texto_btn1_rect)

        cor_btn_2 = COR_BOTAO_HOVER if btn_menu_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_2, btn_menu_rect, border_radius=10)
        texto_btn2 = small_font.render("menu inicial", True, COR_TEXTO_BOTAO)
        texto_btn2_rect = texto_btn2.get_rect(center=btn_menu_rect.center)
        tela.blit(texto_btn2, texto_btn2_rect)

        pygame.display.update()
        clock.tick(FPS)