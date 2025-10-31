import pygame
from pygame.locals import *
import sys

class GUIJogoDos8:
    def __init__(self, jogo):
        self.jogo = jogo
        self.largura = 600
        self.altura = 700
        self.tamanho_celula = 150
        self.margem = 75
        self.margem_topo = 50
        
        # Cores
        self.COR_FUNDO = (240, 240, 240)
        self.COR_CELULA = (255, 255, 255)
        self.COR_VAZIO = (200, 200, 200)
        self.COR_BORDA = (100, 100, 100)
        self.COR_TEXTO = (50, 50, 50)
        self.COR_BOTAO = (70, 130, 180)
        self.COR_BOTAO_HOVER = (100, 160, 210)
        self.COR_BOTAO_TEXTO = (255, 255, 255)
        
        # Estado da interface
        self.tela = None
        self.relogio = None
        self.rodando = False
        self.auto_play = False
        self.contador_auto = 0
        self.velocidade_auto = 30  # frames entre movimentos automáticos
        
        # Botões
        self.botoes = []
        
    def inicializar(self):
        """Inicializa o Pygame e cria a janela"""
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jogo dos 8")
        self.relogio = pygame.time.Clock()
        
        # Criar botões
        self._criar_botoes()
        
        self.rodando = True
        
    def _criar_botoes(self):
        """Cria os três botões abaixo do tabuleiro"""
        y_botao = self.margem_topo + 3 * self.tamanho_celula + 60
        largura_botao = 150
        altura_botao = 50
        espacamento = 20
        
        # Calcular posição x inicial para centralizar os 3 botões
        x_inicial = (self.largura - (3 * largura_botao + 2 * espacamento)) // 2
        
        # Botão "Anterior"
        self.botoes.append({
            'rect': pygame.Rect(x_inicial, y_botao, largura_botao, altura_botao),
            'texto': 'Anterior',
            'acao': 'anterior'
        })
        
        # Botão "Auto/Pausar"
        self.botoes.append({
            'rect': pygame.Rect(x_inicial + largura_botao + espacamento, y_botao, 
                              largura_botao, altura_botao),
            'texto': 'Auto',
            'acao': 'auto'
        })
        
        # Botão "Próximo"
        self.botoes.append({
            'rect': pygame.Rect(x_inicial + 2 * (largura_botao + espacamento), y_botao, 
                              largura_botao, altura_botao),
            'texto': 'Próximo',
            'acao': 'proximo'
        })
        
    def desenhar_tabuleiro(self):
        """Desenha o tabuleiro 3x3 com as peças"""
        tabuleiro = self.jogo.obter_tabuleiro_atual()
        
        for i in range(3):
            for j in range(3):
                x = self.margem + j * self.tamanho_celula
                y = self.margem_topo + i * self.tamanho_celula
                
                valor = tabuleiro[i][j]
                
                # Desenha a célula
                if valor == 0:
                    cor = self.COR_VAZIO
                else:
                    cor = self.COR_CELULA
                
                pygame.draw.rect(self.tela, cor, 
                               (x, y, self.tamanho_celula - 2, self.tamanho_celula - 2))
                pygame.draw.rect(self.tela, self.COR_BORDA, 
                               (x, y, self.tamanho_celula - 2, self.tamanho_celula - 2), 3)
                
                # Desenha o número
                if valor != 0:
                    fonte = pygame.font.Font(None, 80)
                    texto = fonte.render(str(valor), True, self.COR_TEXTO)
                    texto_rect = texto.get_rect(center=(x + self.tamanho_celula // 2, 
                                                        y + self.tamanho_celula // 2))
                    self.tela.blit(texto, texto_rect)
    
    def desenhar_botoes(self):
        """Desenha os botões na tela"""
        mouse_pos = pygame.mouse.get_pos()
        
        for botao in self.botoes:
            # Verifica se o mouse está sobre o botão
            hover = botao['rect'].collidepoint(mouse_pos)
            cor = self.COR_BOTAO_HOVER if hover else self.COR_BOTAO
            
            # Atualiza texto do botão Auto/Pausar
            if botao['acao'] == 'auto':
                botao['texto'] = 'Pausar' if self.auto_play else 'Auto'
            
            # Desenha o botão
            pygame.draw.rect(self.tela, cor, botao['rect'])
            pygame.draw.rect(self.tela, self.COR_BORDA, botao['rect'], 2)
            
            # Desenha o texto do botão
            fonte = pygame.font.Font(None, 32)
            texto = fonte.render(botao['texto'], True, self.COR_BOTAO_TEXTO)
            texto_rect = texto.get_rect(center=botao['rect'].center)
            self.tela.blit(texto, texto_rect)
    
    def desenhar_info(self):
        """Desenha informações sobre o estado do jogo"""
        fonte = pygame.font.Font(None, 28)
        
        if self.jogo.solucao:
            info_texto = f"Passo: {self.jogo.passo_atual + 1} / {len(self.jogo.solucao)}"
        else:
            info_texto = "Clique em 'Auto' para gerar e visualizar a solução"
        
        texto = fonte.render(info_texto, True, self.COR_TEXTO)
        texto_rect = texto.get_rect(center=(self.largura // 2, 25))
        self.tela.blit(texto, texto_rect)
        
        # Mensagem de vitória
        if self.jogo.verificar_solucao():
            fonte_grande = pygame.font.Font(None, 48)
            texto_vitoria = fonte_grande.render("Resolvido!", True, (0, 150, 0))
            texto_rect = texto_vitoria.get_rect(center=(self.largura // 2, 
                                                        self.margem_topo + 3 * self.tamanho_celula + 20))
            self.tela.blit(texto_vitoria, texto_rect)
    
    def processar_eventos(self):
        """Processa os eventos do Pygame"""
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self.rodando = False
                
            elif evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Verifica clique nos botões
                    for botao in self.botoes:
                        if botao['rect'].collidepoint(mouse_pos):
                            self._executar_acao_botao(botao['acao'])
    
    def _executar_acao_botao(self, acao):
        """Executa a ação correspondente ao botão clicado"""
        if acao == 'anterior':
            self.auto_play = False
            self.jogo.passo_anterior()
            
        elif acao == 'proximo':
            self.auto_play = False
            if not self.jogo.solucao:
                # Gera a solução se ainda não foi gerada
                pass
            else:
                self.jogo.proximo_passo()
                
        elif acao == 'auto':
            if not self.jogo.solucao:
                # Gera a solução se ainda não foi gerada
                pass

            # Alterna o modo automático
            self.auto_play = not self.auto_play
            self.contador_auto = 0
    
    def atualizar(self):
        """Atualiza o estado do jogo"""
        if self.auto_play and self.jogo.solucao:
            self.contador_auto += 1
            if self.contador_auto >= self.velocidade_auto:
                self.contador_auto = 0
                if not self.jogo.proximo_passo():
                    # Chegou ao fim, para o auto play
                    self.auto_play = False
    
    def desenhar(self):
        """Desenha todos os elementos na tela"""
        self.tela.fill(self.COR_FUNDO)
        self.desenhar_info()
        self.desenhar_tabuleiro()
        self.desenhar_botoes()
        pygame.display.flip()
    
    def on_execute(self):
        """Loop principal do jogo"""
        self.inicializar()
        
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()