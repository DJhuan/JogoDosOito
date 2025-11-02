from JogoDosOito import JogoDosOito
from JogoDos8GUI import GUIJogoDos8

if __name__ == "__main__":
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
    # Cria a instância do jogo (lógica)
    jogo = JogoDosOito(tabuleiro_inicial, tabuleiro_final)
    
    # Cria a interface gráfica passando o jogo
    gui = GUIJogoDos8(jogo)
    
    # Executa o jogo
    gui.on_execute()