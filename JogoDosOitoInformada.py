import copy
import heapq
import time
import random

TABULEIRO_PADRAO = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

class JogoDosOitoInformada:
    def __init__(self, tabuleiro_inicial=TABULEIRO_PADRAO, tabuleiro_final=TABULEIRO_PADRAO):
        self.tabuleiroInicial = tabuleiro_inicial
        self.tabuleiroFinal = tabuleiro_final
        self.passo_atual = 0
        self.solucao = []
    
    # Encontra a posição do 0 (vazio)
    def encontrar_vazio(self, tabuleiro): 
        for i, linha in enumerate(tabuleiro):
            for j, valor in enumerate(linha):
                if valor == 0:
                    return (i, j)
        return None

    # Gera uma lista de tabuleiros, um para cada movimento possível 
    def gerarMovimentos(self, tabuleiro):
        direcoes = {'c', 'b', 'd', 'e'}
        tabuleiros = []

        for direcao in direcoes:
            novo = self.moverVazio(direcao, tabuleiro)
            if novo is not None:
                tabuleiros.append(novo)
        
        return tabuleiros
    
    # Move a posição vazia para uma direção
    def moverVazio(self, direcao, tabuleiro):
        novoTabuleiro = copy.deepcopy(tabuleiro)
        linha, coluna = self.encontrar_vazio(novoTabuleiro)
        if direcao == 'c' and linha > 0:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha-1][coluna]
            novoTabuleiro[linha-1][coluna] = 0
            return novoTabuleiro
        elif direcao == 'b' and linha < 2:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha+1][coluna]
            novoTabuleiro[linha+1][coluna] = 0
            return novoTabuleiro
        elif direcao == 'd' and coluna < 2:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha][coluna+1]
            novoTabuleiro[linha][coluna+1] = 0
            return novoTabuleiro
        elif direcao == 'e' and coluna > 0:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha][coluna-1]
            novoTabuleiro[linha][coluna-1] = 0
            return novoTabuleiro

        return None
    
    # Encontra a posição do mesmo valor no tabuleiro final
    def encontrarPosicao(self, valor):
        for i in range(3):
            for j in range(3):
                if self.tabuleiroFinal[i][j] == valor:
                    return i, j
    
    # Calcula a distância de Manhattan entre o estado atual e o tabuleiro final
    def distanciaManhattan(self, tabuleiro):
        distancia = 0
        for i in range(3):
            for j in range(3):
                valor = tabuleiro[i][j]
                if valor != 0 and valor != self.tabuleiroFinal[i][j]:
                    i2, j2 = self.encontrarPosicao(valor)
                    distancia += abs(i - i2) + abs(j - j2)
        return distancia
    
    # Retorna a lista de tabuleiros referentes aos movimentos necessários para chegar ao tabuleiro final
    def gerarSolucao(self):
        inicial = self.tabuleiroInicial
        final = self.tabuleiroFinal

        fila = []
        heapq.heappush(fila, (self.distanciaManhattan(inicial), 0, inicial, []))
        visitados = set()

        while fila:
            f, profundidade, estadoAtual, caminho = heapq.heappop(fila) #Pega o elemento com o menor valor da função f

            estadoTupla = tuple(tuple(linha) for linha in estadoAtual)
            visitados.add(estadoTupla)

            if estadoAtual == final:
                self.solucao = caminho + [estadoAtual]
                self.passo_atual = 0
                return caminho + [estadoAtual]

            for tabuleiro in self.gerarMovimentos(estadoAtual):
                tabuleiroTupla = tuple(tuple(linha) for linha in tabuleiro)
                if tabuleiroTupla not in visitados:
                    heapq.heappush(fila, (profundidade + 1 + self.distanciaManhattan(tabuleiro), profundidade + 1, tabuleiro, caminho + [estadoAtual]))

        return None
    
    def passo_anterior(self):
        """Tenta voltar para o passo anterior na solução. Retorna True se conseguiu, False caso contrário."""
        if self.solucao is None:
            return False
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.tabuleiroInicial = self.solucao[self.passo_atual]
            return True
        return False

    def proximo_passo(self):
        """Tenta avançar para o próximo passo na solução. Retorna True se conseguiu, False caso contrário."""
        if self.solucao is None:
            return False
        if self.passo_atual < len(self.solucao) - 1:
            self.passo_atual += 1
            self.tabuleiroInicial = self.solucao[self.passo_atual]
            return True
        return False

    def verificar_solucao(self, tabuleiro=None):
        """Verifica se o tabuleiro está resolvido"""
        if tabuleiro is None:
            tabuleiro = self.tabuleiroInicial
        return tabuleiro == self.tabuleiroFinal

    def aleatorizar_tabuleiro(self, num_movimentos=50):
        """
        Aleatoriza o tabuleiro fazendo movimentos aleatórios válidos.
        Garante que o tabuleiro resultante seja solucionável.
        
        Args:
            num_movimentos: Número de movimentos aleatórios a fazer
        """
        tabuleiro_temp = copy.deepcopy(self.tabuleiroFinal)
        
        # Faz movimentos aleatórios
        direcoes = ['c', 'b', 'd', 'e']
        ultimo_movimento = None
        
        for _ in range(num_movimentos):
            random.shuffle(direcoes)
            
            for direcao in direcoes:
                # Evita desfazer o último movimento
                movimento_oposto = {
                    'c': 'b',
                    'b': 'c',
                    'd': 'e',
                    'e': 'd'
                }
                
                if ultimo_movimento and direcao == movimento_oposto.get(ultimo_movimento):
                    continue
                
                novo = self.moverVazio(direcao, tabuleiro_temp)
                if novo is not None:
                    tabuleiro_temp = novo
                    ultimo_movimento = direcao
                    break
        
        # Define o novo tabuleiro inicial
        self.tabuleiroInicial = tabuleiro_temp
        
        # Limpa a solução anterior
        self.solucao = []
        self.passo_atual = 0
        
        return tabuleiro_temp
    

def main():
    tabuleiro_inicial = [
        [8, 7, 4],
        [5, 1, 3],
        [0, 2, 6]
    ]
    tabuleiro_final = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    jogo = JogoDosOitoInformada(tabuleiro_inicial, tabuleiro_final)
    print("Buscando solução (isso pode demorar um pouquinho)...\n")

    t_ini = time.perf_counter()
    solucao = jogo.gerarSolucao()
    t_fim = time.perf_counter()
    if solucao:
        print(f"Solução encontrada em {len(solucao) - 1} movimentos:\n")
        for i, estado in enumerate(solucao):
            print(f"Movimento {i}:")
            for linha in estado:
                print(linha)
            print()
    else:
        print("Não há solução possível 😢")
    
    print(t_fim - t_ini)


if __name__ == "__main__":
    main()