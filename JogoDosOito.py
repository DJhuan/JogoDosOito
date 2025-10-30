TABULEIRO_PADRAO = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

class JogoDosOito:
    def __init__(self, tabuleiro_inicial=TABULEIRO_PADRAO, tabuleiro_final=TABULEIRO_PADRAO):
        self.tabuleiro = tabuleiro_inicial
        self.posicao_vazia = (2, 2)
        
        self.tabuleiro_final = tabuleiro_final

    def gerarSolucao(self):
        # Retorna uma lista de tabuleiros;
        pass

    def moverVazio(self, direcao):
        pass