import AI_Reinforcement as ML
import Lucky_game as BS

# Define o número máximo possível e o nome do arquivo que irá armazenar a tabela Q
possiveis_numeros_da_sorte = 10
filename = "Luck_game.pkl"

# Cria instâncias do jogo e da IA
game = BS.Game(maior_possivel=possiveis_numeros_da_sorte)
AI = ML.Q_Ai(possiveis_numeros_da_sorte, filename, 0.01)

# Define as variáveis iniciais do jogo
running = True
partida = 1
partidas_boas = 0

while running:
    if game.times == 0:
        while True:
            number = AI.choose_action()
            if number != game.number:
                break
        feedback = game.Set_choice(number)
        game.times -= 1
        state = number, feedback

    next_number = AI.choose_action(state)
    next_feedback = game.Set_choice(next_number)
    state = number, feedback
    reward = AI.calculate_reward(number, next_number, feedback)

    if partidas_boas > 1000:
        AI.save_table(filename)
        break

    if game.won(next_number):
        AI.update_Q_table((number, feedback), next_number, AI.calculate_reward(number, next_number, next_feedback))
        # print("Partida n°{} teve {} tentativa para acertar o numero da sorte {}.".format(partida, game.times, game.number))
        partida += 1

        if game.times < 10:
            partidas_boas += 1

        game.restart_game()
    else:
        AI.update_Q_table((number, feedback), next_number, reward)

    number = next_number
    feedback = next_feedback

AI.heatmap()