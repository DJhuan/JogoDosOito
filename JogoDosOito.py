import copy
import time

TABULEIRO_PADRAO = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

class JogoDosOito:
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
            
    # Retorna a lista de tabuleiros referentes aos movimentos necessários para chegar ao tabuleiro final
    def gerarSolucao(self):
        inicial = self.tabuleiroInicial
        final = self.tabuleiroFinal

        fila = [(inicial, [])]
        visitados = set()

        while fila:
            estadoAtual, caminho = fila.pop(0)

            estado_tupla = tuple(tuple(linha) for linha in estadoAtual)

            visitados.add(estado_tupla)
            if estadoAtual == final:
                self.solucao = caminho + [estadoAtual]
                self.passo_atual = 0
                return caminho + [estadoAtual]

            for tabuleiro in self.gerarMovimentos(estadoAtual):
                tabuleiroTupla = tuple(tuple(linha) for linha in tabuleiro)
                if tabuleiroTupla not in visitados:
                    fila.append((tabuleiro, caminho + [estadoAtual]))

        return None

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

    def passo_anterior(self):
        "Tenta voltar para o passo anterior na solução. Retorna True se conseguiu, False caso contrário."
        if self.solucao is None:
            return False
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.tabuleiroInicial = self.solucao[self.passo_atual]
            return True

    def proximo_passo(self):
        "Tenta avançar para o próximo passo na solução. Retorna True se conseguiu, False caso contrário."
        if self.solucao is None:
            return False
        if self.passo_atual < len(self.solucao) - 1:
            self.passo_atual += 1
            self.tabuleiroInicial = self.solucao[self.passo_atual]
            return True

    def verificar_solucao(self, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabuleiroInicial
        return tabuleiro == self.tabuleiroFinal


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

    jogo = JogoDosOito(tabuleiro_inicial, tabuleiro_final)
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
