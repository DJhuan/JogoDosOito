import sys
from JogoDosOito import JogoDosOito
from JogoDosOitoInformada import JogoDosOitoInformada
from JogoDos8GUI import GUIJogoDos8

if __name__ == "__main__":
    tabuleiro_inicial = [
        [3, 4, 0],
        [7, 1, 5],
        [6, 8, 2]
    ]
    tabuleiro_final = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
    
    # Verifica se o parâmetro -i foi passado
    modo_informado = '-i' in sys.argv
    
    # Cria a instância do jogo (lógica)
    if modo_informado:
        print("Usando busca informada (A* & Manhattan)")
        jogo = JogoDosOitoInformada(tabuleiro_inicial, tabuleiro_final)
    else:
        print("Usando busca não informada (BFS)")
        jogo = JogoDosOito(tabuleiro_inicial, tabuleiro_final)
    
    # Cria a interface gráfica passando o jogo
    gui = GUIJogoDos8(jogo)
    
    # Executa o jogo
    gui.on_execute()