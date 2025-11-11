import pygame
import sys
import database # importa o database

# cores da caixa de input
COR_INPUT_BOX = (200, 200, 200)
COR_INPUT_BOX_ATIVA = (255, 255, 255)
COR_INPUT_TEXTO = (0, 0, 0)

# cores das mensagens
COR_ERRO = (255, 50, 50) # Vermelho 
COR_BEMVINDO = (50, 255, 50) # Verde 
COR_NOVO_JOGADOR = (230, 230, 230) # Cinza claro

#cores do botão 
COR_BOTAO = (214, 130, 116)
COR_BOTAO_HOVER = (194, 91, 81)
COR_TEXTO_BOTAO = (255, 255, 255) 
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

ITEM_LARGURA = 1200
ITEM_ALTURA = 800

try:
    icone  = pygame.transform.scale(pygame.image.load('assets/logo.png').convert_alpha(), (ITEM_LARGURA, ITEM_ALTURA))
except pygame.error as e:
    print("Erro ao carregar imagens")


def mostrar_tela_regras(tela, cor_fundo, font, small_font, TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS):
    """
    Mostra a tela de regras com navegação entre imagens
    """
    try:
   
        REGRA1 = pygame.transform.scale(pygame.image.load('regras/REGRA1.png').convert_alpha(), (600, 400))
        REGRA2 = pygame.transform.scale(pygame.image.load('regras/REGRA2.png').convert_alpha(), (5, 5))
        REGRA3 = pygame.transform.scale(pygame.image.load('regras/REGRA3.png').convert_alpha(), (100, 100))

    except pygame.error as e:
       print("Erro ao carregar imagens")
       print(e)
       pygame.quit()
       sys.exit()
    regras_imagens = [
        {'imagem': 'regras/REGRA1.png', 'legenda': 'Clique no espaço ou seta do teclado para esquivar das formas erradas'},
        {'imagem': 'regras/REGRA2.png', 'legenda': 'Pegue a quantidade de formas indicadas'},
        {'imagem': 'regras/REGRA3.png', 'legenda': 'Você tem 3 vidas e precisa pegar as formas no menor tempo possível'}
    ]
    
    regra_atual = 0
    
    # Botões de navegação
    btn_voltar_rect = pygame.Rect(50, TELA_ALTURA - 80, 150, 50)
    btn_proximo_rect = pygame.Rect(TELA_LARGURA - 200, TELA_ALTURA - 80, 150, 50)
    btn_fechar_rect = pygame.Rect(TELA_LARGURA - 60, 20, 40, 40)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botão voltar
                if btn_voltar_rect.collidepoint(event.pos) and regra_atual > 0:
                    regra_atual -= 1
                
                # Botão próximo
                if btn_proximo_rect.collidepoint(event.pos):
                    if regra_atual < len(regras_imagens) - 1:
                        regra_atual += 1
                    else:
                        return True  # Fechar tela de regras
                
                # Botão fechar (X)
                if btn_fechar_rect.collidepoint(event.pos):
                    return True
        
        # Desenhar fundo
        tela.fill(cor_fundo)
        
        # Título
        titulo_texto = font.render("Regras do Jogo", True, WHITE)
        titulo_rect = titulo_texto.get_rect(center=(TELA_LARGURA // 2, 60))
        tela.blit(titulo_texto, titulo_rect)
        
        # Tentar carregar e exibir imagem da regra atual
        try:
            imagem_path = regras_imagens[regra_atual]['imagem']
            img = pygame.image.load(imagem_path).convert_alpha()
            # Redimensionar mantendo proporção
            img_ratio = img.get_width() / img.get_height()
            nova_largura = min(450, TELA_LARGURA - 70)
            nova_altura = int(nova_largura / img_ratio)
            img = pygame.transform.scale(img, (nova_largura, nova_altura))
            
            img_rect = img.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 - 50))
            tela.blit(img, img_rect)
        except:
            # Fallback se a imagem não carregar
            erro_texto = small_font.render(f"Imagem: {regras_imagens[regra_atual]['imagem']}", True, WHITE)
            erro_rect = erro_texto.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2))
            tela.blit(erro_texto, erro_rect)
        
        # Legenda
        legenda_texto = small_font.render(regras_imagens[regra_atual]['legenda'], True, WHITE)
        legenda_rect = legenda_texto.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 200))
        tela.blit(legenda_texto, legenda_rect)
        
        # Indicador de página
        pagina_texto = small_font.render(f"{regra_atual + 1}/{len(regras_imagens)}", True, WHITE)
        pagina_rect = pagina_texto.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA - 50))
        tela.blit(pagina_texto, pagina_rect)
        
        # Botão Voltar 
        if regra_atual > 0:
            cor_voltar = COR_BOTAO_HOVER if btn_voltar_rect.collidepoint(mouse_pos) else COR_BOTAO
            pygame.draw.rect(tela, cor_voltar, btn_voltar_rect, border_radius=10)
            voltar_texto = small_font.render(" Voltar", True, COR_TEXTO_BOTAO)
            voltar_rect = voltar_texto.get_rect(center=btn_voltar_rect.center)
            tela.blit(voltar_texto, voltar_rect)
        
        # Botão Próximo/Avançar
        texto_proximo = "Avançar" if regra_atual < len(regras_imagens) - 1 else "Fechar"
        cor_proximo = COR_BOTAO_HOVER if btn_proximo_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_proximo, btn_proximo_rect, border_radius=10)
        proximo_texto = small_font.render(texto_proximo, True, COR_TEXTO_BOTAO)
        proximo_rect = proximo_texto.get_rect(center=btn_proximo_rect.center)
        tela.blit(proximo_texto, proximo_rect)
        
        # Botão Fechar (X)
        cor_fechar = COR_BOTAO_HOVER if btn_fechar_rect.collidepoint(mouse_pos) else VERMELHO
        pygame.draw.rect(tela, cor_fechar, btn_fechar_rect, border_radius=5)
        fechar_texto = small_font.render("X", True, COR_TEXTO_BOTAO)
        fechar_rect = fechar_texto.get_rect(center=btn_fechar_rect.center)
        tela.blit(fechar_texto, fechar_rect)
        
        pygame.display.update()
        clock.tick(FPS)

def mostrar_tela_inicial(tela, cor_fundo, font, small_font, TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS):
    """
    Mostra a tela inicial com entrada de nome e botão Iniciar.
    """
    
    nome_jogador = ""

    input_box_rect = pygame.Rect(TELA_LARGURA // 2 - 150, TELA_ALTURA // 2 + 90, 300, 40)
    input_ativo = False
    
    status_mensagem = "" 
    status_cor = WHITE 

    # define o retângulo do botão Iniciar
    btn_iniciar_rect = pygame.Rect(TELA_LARGURA // 2 - 150, TELA_ALTURA // 2 + 190, 300, 50)
    # define o retângulo do botão Regras no canto superior direito
    btn_regras_rect = pygame.Rect(TELA_LARGURA - 120, 20, 100, 40)
    
    while True:
        # pega a posição do mouse a cada frame
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # lógica da caixa de input
                if input_box_rect.collidepoint(event.pos):
                    input_ativo = True
                else:
                    input_ativo = False
                
                # lógica do botão
                if btn_iniciar_rect.collidepoint(event.pos):
                    if len(nome_jogador) > 0:
                        return nome_jogador 
                    else:
                        status_mensagem = "O nome não pode estar vazio!"
                        status_cor = COR_ERRO
                
                # lógica do botão regras
                if btn_regras_rect.collidepoint(event.pos):
                    # Chama a tela de regras
                    mostrar_tela_regras(tela, cor_fundo, font, small_font, TELA_LARGURA, TELA_ALTURA, WHITE, clock, FPS)
            
            # bloco de eventos de teclado
            if event.type == pygame.KEYDOWN:
                if input_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        nome_jogador = nome_jogador[:-1]
                    elif event.key == pygame.K_RETURN: 
                        if len(nome_jogador) <= 0:
                            status_mensagem = "O nome não pode estar vazio!"
                            status_cor = COR_ERRO
                    else:
                        if len(nome_jogador) < 10: # limite de 10 letras
                            nome_jogador += event.unicode
                    
                    # verificação em tempo real
                    if len(nome_jogador) > 0:
                        if database.check_name_exists(nome_jogador):
                            status_mensagem = f"Bem-vindo de volta, {nome_jogador}!"
                            status_cor = COR_BEMVINDO
                        else:
                            status_mensagem = f"Nome '{nome_jogador}' disponível!"
                            status_cor = COR_NOVO_JOGADOR
                    else:
                        status_mensagem = ""

        tela.fill(cor_fundo)

        # titulo do jogo
        # mudar pro icone
        
        # define a posição Y central para a linha do meio ("das")
        y_base = TELA_ALTURA // 2 - 100 
        
        titulo1_texto = font.render("Mergulho", True, WHITE)
        # Posiciona acima da base
        titulo1_rect = titulo1_texto.get_rect(center=(TELA_LARGURA // 2, y_base - 40)) 
        
        # Linha 2: das 
        titulo2_texto = small_font.render("das", True, WHITE)
        titulo2_rect = titulo2_texto.get_rect(center=(TELA_LARGURA // 2, y_base))
        
        # Linha 3: Formas! 
        titulo3_texto = font.render("Formas!", True, WHITE)
        # Posiciona abaixo da base
        titulo3_rect = titulo3_texto.get_rect(center=(TELA_LARGURA // 2, y_base + 40))
        
        # Desenha os 3 textos
        tela.blit(titulo1_texto, titulo1_rect)
        tela.blit(titulo2_texto, titulo2_rect)
        tela.blit(titulo3_texto, titulo3_rect)
        
        # instrução para digitar o nome 
        instru_nome_texto = small_font.render("Digite seu nome:", True, WHITE)
        instru_nome_rect = instru_nome_texto.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 50))
        tela.blit(instru_nome_texto, instru_nome_rect)

        # caixa de texto
        cor_caixa_atual = COR_INPUT_BOX_ATIVA if input_ativo else COR_INPUT_BOX
        pygame.draw.rect(tela, cor_caixa_atual, input_box_rect, border_radius=5)
        
        texto_surface = small_font.render(nome_jogador, True, COR_INPUT_TEXTO)
        pos_texto = (input_box_rect.x + (input_box_rect.width - texto_surface.get_width()) // 2, 
                     input_box_rect.y + (input_box_rect.height - texto_surface.get_height()) // 2)
        tela.blit(texto_surface, pos_texto)
        
        # mensagem de status 
        if status_mensagem:
            msg_texto = small_font.render(status_mensagem, True, status_cor)
            msg_rect = msg_texto.get_rect(center=(TELA_LARGURA // 2, input_box_rect.bottom + 25))
            tela.blit(msg_texto, msg_rect)

        # desenha o botão Regras no canto superior direito
        cor_btn_regras = COR_BOTAO_HOVER if btn_regras_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_regras, btn_regras_rect, border_radius=10)
        
        texto_btn_regras = small_font.render("regras", True, COR_TEXTO_BOTAO)
        texto_btn_regras_rect = texto_btn_regras.get_rect(center=btn_regras_rect.center)
        tela.blit(texto_btn_regras, texto_btn_regras_rect)

        # desenha o botão Iniciar
        cor_btn_atual = COR_BOTAO_HOVER if btn_iniciar_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_btn_atual, btn_iniciar_rect, border_radius=10)
        
        texto_btn = small_font.render("iniciar", True, COR_TEXTO_BOTAO)
        texto_btn_rect = texto_btn.get_rect(center=btn_iniciar_rect.center)
        tela.blit(texto_btn, texto_btn_rect)
        
        pygame.display.update()
        clock.tick(FPS)