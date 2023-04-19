import matplotlib.pyplot as plt
import numpy as np
import AI_Reinforcement as ML
import Lucky_game as BS
import time

def progress_bar(total, atual, previous_percent, txt):
    percent = round((atual/total)*100,2)
    # print(previous_percent, percent)
    if (percent - previous_percent) > 0.01 and percent <= 100:
        bar = "["
        for i in range(int(percent//5)):
            bar += "#"
        
        for i in range(20-len(bar)):
            bar += "_"
        
        bar += "]"

        print("\033c", end="")
        print("{}\n{} {}%".format(txt, bar, percent))
    else:
        percent = previous_percent

    return percent

while True:
    try:
        # Rodadas de Treinamentos
        rodadas_treino = int(input("Quantas rodadas de treino vamos fazer?(int) "))
        
        # Define o número máximo possível da tabela Q
        possiveis_numeros_da_sorte = int(input("\nEscolha o limite superior para treinarmos a 'AI'\nlimite inferior = 0.\nLimite Superior = "))
        
        break
    except:
        print("\nErro! Os valores esperados são do Tipo <class 'int'>.\n")

total = possiveis_numeros_da_sorte * 1000
atual = 0 

# Cria instâncias do jogo e da IA
game = BS.Game(maior_possivel=possiveis_numeros_da_sorte)
AI = ML.Q_Ai(possiveis_numeros_da_sorte, 0.5)

for i in range(rodadas_treino):
    percent = 0
    txt = "{}° Rodada de Treino".format(i+1)

    # Define as variáveis iniciais do jogo
    running = True
    partida = 1
    partidas_boas = 0
    try_map = np.array([])

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

        if partidas_boas > possiveis_numeros_da_sorte*1000:
            AI.save_table()
            break

        if game.won(next_number):
            try_map = np.append(try_map, game.times)
            AI.update_Q_table((number, feedback), next_number, AI.calculate_reward(number, next_number, next_feedback))
            partida += 1

            if game.times < possiveis_numeros_da_sorte*0.75:
                partidas_boas += 1

            game.restart_game()
        else:
            AI.update_Q_table((number, feedback), next_number, reward)

        number = next_number
        feedback = next_feedback
        
        percent = progress_bar(possiveis_numeros_da_sorte * 1000, partidas_boas, percent, txt)

# Plot um grafico com a politica do agente.
AI.heatmap()