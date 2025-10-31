from JogoDosOito import JogoDosOito
from JogoDos8GUI import GUIJogoDos8

if __name__ == "__main__":
    # Cria a instância do jogo (lógica)
    jogo = JogoDosOito()
    
    # Cria a interface gráfica passando o jogo
    gui = GUIJogoDos8(jogo)
    
    # Executa o jogo
    gui.on_execute()