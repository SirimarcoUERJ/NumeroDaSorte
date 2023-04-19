import AI_Reinforcement as ML
import Lucky_game as BS

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

while True:
    try:
        # Numero de partidas
        n_partidas = int(input("Quantas partidas vamos jogar? (int): "))
        
        # Define o número máximo possível da tabela Q
        possiveis_numeros_da_sorte = int(input("\nEscolha o limite superior para treinarmos a 'AI'\nlimite inferior = 0.\nLimite Superior = "))
        
        break
    except:
        print("\nErro! Os valores esperados são do Tipo <class 'int'>.\n")

# Cria instâncias do jogo e da IA
game = BS.Game(maior_possivel=possiveis_numeros_da_sorte)
AI = ML.Q_Ai(possiveis_numeros_da_sorte, 0.5)

# Define as variáveis iniciais do jogo
running = True
state = None
partida = 1
user_pts = 0
agente_pts = 0

while running:

    if game.times == 0:
        number = AI.choose_action()
        feedback = game.Set_choice(number)
        game.times -= 1
        state = number, feedback

    next_number = AI.choose_action(state)
    next_feedback = game.Set_choice(next_number)
    reward = AI.calculate_reward(number, next_number, feedback)

    if(state == (0,1) or state == (10,0)):
        print(state, "errado")
        AI.heatmap()

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
    print_game_state(user_number, user_feedback_str, number, game.times, partida, n_partidas, user_pts, agente_pts)
    arg = user_number, user_feedback_str, number, game.times, partida, n_partidas, user_pts, agente_pts

    # Verifica se houve um empate 
    if game.won(user_number) and game.won(number):
        game.restart_game()
        user_pts += 1
        agente_pts += 1
        partida += 1
        
        print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], user_pts, agente_pts)
        print("Você empatou com o agente!\n")

        # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
        if partida > n_partidas:
            running = False
    
    # Verifica se o usuario ganhou
    if game.won(user_number):
        user_pts += 1
        game.restart_game()
        partida += 1
        
        print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], user_pts, arg[7])
        print("Você acertou! Parabéns!\n")

        # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
        if partida > n_partidas:
            running = False

    # Verifica se o agente ganhou
    if game.won(number):
        agente_pts += 1
        partida += 1
        game.restart_game()

        print_game_state(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], agente_pts)
        print("Você perdeu para o agente! Parabéns burrão!\n")
        
        # Verifica se todas as partidas foram jogadas para interromper o loop, ou pergunta ao jogador se deseja continuar jogando.
        if partida > n_partidas:
            running = False
        
    # Salva a tabela Q com as novas interações.
    if partida == n_partidas + 1:
        print("\nTabela Salva\n")
        AI.save_table()

    number = next_number
    feedback = next_feedback
    state = number, feedback

AI.heatmap()