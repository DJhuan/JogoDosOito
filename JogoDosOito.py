import copy

TABULEIRO_PADRAO = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

class JogoDosOito:
    def __init__(self, tabuleiro_inicial=TABULEIRO_PADRAO, tabuleiro_final=TABULEIRO_PADRAO):
        self.tabuleiroInicial = tabuleiro_inicial
        self.tabuleiroFinal = tabuleiro_final

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
            tabuleiros.append(self.moverVazio(direcao, tabuleiro))
        
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

            if estado_tupla not in visitados:
                visitados.add(estado_tupla)
                if estadoAtual == final:
                    return caminho + [estadoAtual]

                for tabuleiro in self.gerarMovimentos(estadoAtual):
                    fila.append((tabuleiro, caminho + [estadoAtual]))

        return None

    # Move a posição vazia para uma direção
    def moverVazio(self, direcao, tabuleiro):
        novoTabuleiro = copy.deepcopy(tabuleiro)
        linha, coluna = self.encontrar_vazio(novoTabuleiro)
        if direcao == 'c' and linha > 0:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha-1][coluna]
            novoTabuleiro[linha-1][coluna] = 0
        elif direcao == 'b' and linha < 2:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha+1][coluna]
            novoTabuleiro[linha+1][coluna] = 0
        elif direcao == 'd' and coluna < 2:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha][coluna+1]
            novoTabuleiro[linha][coluna+1] = 0
        elif direcao == 'e' and coluna > 0:
            novoTabuleiro[linha][coluna] = novoTabuleiro[linha][coluna-1]
            novoTabuleiro[linha][coluna-1] = 0

        return novoTabuleiro

    def mostrarTabuleiro(self):
        for linha in self.tabuleiro:
            print(linha)
        print()
    



def main():
    tabuleiro_inicial = [
        [4, 7, 1],
        [0, 2, 3],
        [8, 5, 6]
    ]
    tabuleiro_final = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    jogo = JogoDosOito(tabuleiro_inicial, tabuleiro_final)
    print("Buscando solução (isso pode demorar um pouquinho)...\n")

    solucao = jogo.gerarSolucao()
    if solucao:
        print(f"Solução encontrada em {len(solucao) - 1} movimentos:\n")
        for i, estado in enumerate(solucao):
            print(f"Movimento {i}:")
            for linha in estado:
                print(linha)
            print()
    else:
        print("Não há solução possível 😢")


if __name__ == "__main__":
    main()