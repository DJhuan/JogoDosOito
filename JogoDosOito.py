TABULEIRO_PADRAO = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

class JogoDosOito:
    def __init__(self, tabuleiro_inicial=None, tabuleiro_final=None):
        self.posicao_vazia = (0, 0)
        if tabuleiro_inicial is None:
            tabuleiro_inicial = [[7, 2, 4],
                                  [5, 0, 6],
                                  [8, 3, 1]]
            self.posicao_vazia = (1, 1)
            
        if tabuleiro_final is None:
            tabuleiro_final = TABULEIRO_PADRAO
        
        self.tabuleiro_inicial = [row[:] for row in tabuleiro_inicial]
        self.tabuleiro = [row[:] for row in tabuleiro_inicial]
        self.tabuleiro_final = [row[:] for row in tabuleiro_final]
        
        # Solução
        self.solucao = []
        self.passo_atual = 0
        
    def moverVazio(self, direcao):
        """Move o espaço vazio em uma direção ('cima', 'baixo', 'esquerda', 'direita')"""
        linha, coluna = self.posicao_vazia
        nova_linha, nova_coluna = linha, coluna
        
        if direcao == 'cima':
            nova_linha -= 1
        elif direcao == 'baixo':
            nova_linha += 1
        elif direcao == 'esquerda':
            nova_coluna -= 1
        elif direcao == 'direita':
            nova_coluna += 1
        
        # Verifica se o movimento é válido
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            # Troca o vazio com a peça
            self.tabuleiro[linha][coluna] = self.tabuleiro[nova_linha][nova_coluna]
            self.tabuleiro[nova_linha][nova_coluna] = 0
            self.posicao_vazia = (nova_linha, nova_coluna)
            return True
        return False
    
    def obter_tabuleiro_atual(self):
        """Retorna o tabuleiro no passo atual da solução"""
        if self.solucao and 0 <= self.passo_atual < len(self.solucao):
            return self.solucao[self.passo_atual]
        return self.tabuleiro
    
    def proximo_passo(self):
        """Avança um passo na solução"""
        if self.solucao and self.passo_atual < len(self.solucao) - 1:
            self.passo_atual += 1
            self.tabuleiro = [row[:] for row in self.solucao[self.passo_atual]]
            self.posicao_vazia = self._encontrar_vazio(self.tabuleiro)
            return True
        return False
    
    def passo_anterior(self):
        """Retrocede um passo na solução"""
        if self.solucao and self.passo_atual > 0:
            self.passo_atual -= 1
            self.tabuleiro = [row[:] for row in self.solucao[self.passo_atual]]
            self.posicao_vazia = self._encontrar_vazio(self.tabuleiro)
            return True
        return False
    
    def resetar(self):
        """Reseta o jogo para o estado inicial"""
        self.tabuleiro = [row[:] for row in self.tabuleiro_inicial]
        self.posicao_vazia = self._encontrar_vazio(self.tabuleiro)
        self.passo_atual = 0
        
    def verificar_solucao(self):
        """Verifica se o tabuleiro atual está no estado objetivo"""
        return self.tabuleiro == self.tabuleiro_final