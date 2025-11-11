import pygame
import sys

COR_BOTAO = (100, 100, 100) 
COR_BOTAO_HOVER = (150, 150, 150)
COR_TEXTO_BOTAO = (255, 255, 255) 
COR_GAME_OVER = (220, 50, 50) 

def mostrar_tela_game_over(tela, cor_fundo, font, small_font, TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS):
    
    btn_largura = 300
    btn_altura = 50
    center_x = TELA_LARGURA // 2
    center_y = TELA_ALTURA // 2

    btn_jogar_novamente_rect = pygame.Rect(center_x - (btn_largura // 2), center_y + 20, btn_largura, btn_altura)
    btn_menu_rect = pygame.Rect(center_x - (btn_largura // 2), center_y + 90, btn_largura, btn_altura)

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

        # desenha o fundo
        tela.fill(cor_fundo)

        game_over_texto = font.render("GAME OVER", True, COR_GAME_OVER)
        game_over_rect = game_over_texto.get_rect(center=(center_x, center_y - 70))
        tela.blit(game_over_texto, game_over_rect)

        # botões
        cor_btn_1 = COR_BOTAO_HOVER if btn_jogar_novamente_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_1, btn_jogar_novamente_rect, border_radius=10)
        texto_btn1 = small_font.render("jogar Novamente", True, COR_TEXTO_BOTAO)
        texto_btn1_rect = texto_btn1.get_rect(center=btn_jogar_novamente_rect.center)
        tela.blit(texto_btn1, texto_btn1_rect)

        cor_btn_2 = COR_BOTAO_HOVER if btn_menu_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_2, btn_menu_rect, border_radius=10)
        texto_btn2 = small_font.render("menu inicial", True, COR_TEXTO_BOTAO)
        texto_btn2_rect = texto_btn2.get_rect(center=btn_menu_rect.center)
        tela.blit(texto_btn2, texto_btn2_rect)

        pygame.display.update()
        clock.tick(FPS)