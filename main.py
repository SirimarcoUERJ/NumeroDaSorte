import AI_Reinforcement as ML
import Luck_game as BS
import time

# Função que imprime o estado atual do jogo
def print_game_state(user_number, user_feedback_str, agent_number, tentativas, rodada, total_rodadas, user_pts, agent_pts):

    print("\033c", end="")
    print("                          Jogo da sorte")
    print("-----------------------------------------------------------------")
    print("                     {} de {} => {}° Tentativa".format(rodada, total_rodadas, tentativas))
    print("-----------------------------------------------------------------")
    print("                              Placar")
    print(("Jogador(a) = {}                                        Agente = {}").format(user_pts, agent_pts))
    print("-----------------------------------------------------------------")
    print("\nSua escolha: {}                               Agente escolheu: {}".format(user_number, agent_number))
    print("\nSua escolha é {} que o número da sorte.".format(user_feedback_str))
    print("\n")

    return None

# Define o número máximo possível e o nome do arquivo que irá armazenar a tabela Q
possiveis_numeros_da_sorte = 100
filename = "Luck_game.pkl"

# Cria instâncias do jogo e da IA
game = BS.Game(maior_possivel=possiveis_numeros_da_sorte)
AI = ML.Q_Ai(possiveis_numeros_da_sorte, filename)

# Define as variáveis iniciais do jogo
running = True
state = None
partida = 1
user_pts = 0
agente_pts = 0

# Primeiro estado para a IA ter um ponto de partida.
number = AI.choose_action(state)
feedback = game.Set_choice(number)
game.times -= 1
state = number, feedback

n_partidas = int(input("Quantas partidas vamos jogar? (int): "))

play_with_user = input("Deseja jogar junto com o computador? (S/N): ")

while running:

    # Escolhe a próxima jogada da IA
    last_number = AI.choose_action(state)
    last_feedback = game.Set_choice(last_number)
    reward = AI.calculate_reward(number, last_number, last_feedback)
    
    # se o usuario for jogar recebe a jogada dele
    if play_with_user.lower() == "s":
        user_number = game.Get_choice()
        user_feedback = game.Set_choice(user_number)
        game.times -= 1
        
        # Define a string que indica se o número do usuário é maior, menor ou igual ao número da sorte
        if user_feedback == 0:
            user_feedback_str = "menor"
        elif user_feedback == 1:
            user_feedback_str = "maior"
        else:
            user_feedback_str = "igual"

        # Imprime as informações do jogo 
        print_game_state(user_number, user_feedback_str, last_number, game.times, partida, n_partidas, user_pts, agente_pts)
        arg = user_number, user_feedback_str, last_number, game.times, partida, n_partidas, user_pts, agente_pts

        # Verifica se houve um empate 
        if game.won(user_number) and game.won(last_number):
            game.restart_game()
            partida += 1
            user_pts += 1
            agente_pts += 1
            
            print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], user_pts, agente_pts)
            print("Você empatou com o agente!\n")

            # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
            if partida >= n_partidas:
                running = False
            else:
                if play_with_user == "s":
                    play_with_user = input("Deseja jogar junto com o computador? (S/N)\n")

        # Verifica se o usuario ganhou
        if game.won(user_number):
            user_pts += 1
            game.restart_game()
            
            print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], user_pts, arg[7])
            print("Você acertou! Parabéns!\n")

            # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
            if partida >= n_partidas:
                running = False
            else:
                play_with_user = input("Deseja jogar junto com o computador? (S/N)\n")

            partida += 1
            
    # Verifica se o agente ganhou
    if game.won(last_number):
        agente_pts += 1
        AI.save_table(filename)

        # Verifica se o usuario está jogando
        if play_with_user == "s":

            print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], agente_pts)
            print("Você perdeu para o agente! Parabéns burrão!\n")
            
            # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
            if partida >= n_partidas:
                running = False
            else:
                if play_with_user == "s":
                    play_with_user = input("Deseja jogar junto com o computador? (S/N)\n")
        
        # Verifica se o agente está jogando sozinho e da as informações.
        else:
            print("Partida n°{} teve {} tentativa para acertar o numero da sorte {}.".format(partida, game.times, game.number))
 
            if partida >= n_partidas:
                running = False
        
        # Reinicia o estado do jogo e define o próximo movimento como a última jogada, para ser utilizado na próxima rodada.
        game.restart_game()
        partida += 1
        number = AI.choose_action(state)
        feedback = game.Set_choice(number)
        game.times -= 1
        state = number, feedback

    
    AI.update_Q_table(state, reward)
    number = last_number
    feedback = last_feedback
    state = number, feedback