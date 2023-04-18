import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle as pkl
import time

class Q_Ai:
    
    def __init__(self, line_number, filename, exploitation=0.95, learn_rate=0.01, discount=0.9):
        """Inicializa a classe Q_Ai."""
        self.line_number = line_number + 1 # numero + 1 para adicionar a possibilidade do 0
        self.column_number = 2 * self.line_number  # o numero de linhas vezes dois pois cada um tem a possibilidade de maior ou menor
        self.exploitation = exploitation
        self.learn_rate = learn_rate
        self.discount = discount
        self.create_or_load_table(filename)
        self.guide = self.create_vector_array(self.line_number)
        
    def save_table(self, filename):
        """Salva a tabela Q em um arquivo com o nome 'filename'"""
        with open(filename, "wb") as f:
            pkl.dump(self.Q_table, f)
    
    def create_or_load_table(self, filename):
        """Tenta abrir o arquivo com o nome 'filename' contendo a tabela Q, 
        se o arquivo não existir, cria uma nova tabela Q e a salva no arquivo."""
        try:
            with open(filename, "rb") as f:
                self.Q_table = pkl.load(f)
        except FileNotFoundError:
            # self.Q_table = np.random.randn(self.line_number, self.column_number)
            self.Q_table = np.zeros((self.line_number, self.column_number))
            self.save_table(filename)
    
    def create_vector_array(self, n):
        """Cria um vetor de tamanho 'n', em que cada elemento é um vetor contendo 
        as coordenadas na tabela Q correspondentes ao estado (i, 0) e (i, 1)"""
        vector_array = np.empty((n,), dtype=np.ndarray)
        for i in range(n):
            vector_array[i] = np.array([(2*i), (2*i)+1])
        return vector_array

    def get_columns_from_table(self, n_col):
        """Retorna os valores da tabela Q correspondentes à coluna 'n_col'."""
        return self.Q_table[:, n_col]

    def choose_action(self, state=None):
        """Escolhe a ação a ser tomada com base no estado atual.
        Com uma probabilidade de 'exploitation', escolhe a ação com maior valor Q na coluna correspondente ao estado,
        caso contrário, escolhe uma ação aleatória 'exploration'."""
        if state is None:
            state = np.random.choice(self.line_number), np.random.choice([0, 1]) 
        column = self.guide[state[0]][state[1]]

        # choose best action with 95% probability
        if np.random.uniform(0, 1) < self.exploitation:
            action = np.argmax(self.get_columns_from_table(column))
        # choose random action with 5% probability
        else:
            # print("random")
            action = np.random.randint(0, len(self.get_columns_from_table(column)))
        # print(state, action)
            
        return action

    def calculate_reward(self, last_decision, new_decision, feedback):
        """Calcula a recompensa com base na decisão anterior, decisão atual e feedback recebido.
        Se o feedback for 0 e a nova decisão for maior que a anterior, a recompensa é 3, 
        caso contrário, a recompensa é -20. 
        Se o feedback for 1 e a nova decisão for menor que a anterior, a recompensa é 3, 
        caso contrário, a recompensa é -20.
        Se o feedback for -1, a recompensa é 50 (melhor recompensa possível)."""
        if feedback == 0:
            if last_decision < new_decision:
                reward = 1
            else:
                reward = -5

        elif feedback == 1:
            if last_decision > new_decision:
                reward = 1
            else:
                reward = -5
        
        elif feedback == -1:
            reward = 15
            
        return reward


    def update_Q_table(self, state, line, reward):
        """Atualiza os valores da tabela Q utilizando a equação clássica de reforço, a fim de priorizar as melhores ações.
        Recebe como parâmetros o estado atual e a recompensa associada a ele."""
        
        column = self.guide[state[0]][state[1]]

        # Equação de reforço para atualizar o valor da tabela Q
        self.Q_table[line][column] = (1 - self.learn_rate) * self.Q_table[line][column] + self.learn_rate * (reward + (1 - self.discount) * 15)

        if self.Q_table[line][column] > 5:
            self.Q_table[line][column] = 5
        if self.Q_table[line][column] < -5:
            self.Q_table[line][column] = -5

        return None

    def real_time_heatmap(self, data_form = None, interval=3000): #Não funciona ainda
        """
        Cria um gráfico de calor em tempo real usando Matplotlib e FuncAnimation.
        """
        if data_form == None:
            data_form = (self.line_number, self.column_number)

        # Crie uma matriz de dados de exemplo
        data = np.zeros(data_form)

        # Crie o gráfico de calor inicial usando imshow
        fig, ax = plt.subplots()
        heatmap = ax.imshow(data, cmap='coolwarm')

        # Adicione uma barra lateral com os valores e cores possíveis
        cbar = plt.colorbar(heatmap)

        # Função para atualizar o gráfico de calor
        def update_heatmap(frame):
            
            # with open("Lucky_game.pkl", "rb") as file:
            #     new_data  = pkl.load(file)
            new_data  = self.Q_table  # Recebe os novos valores dos dados
            
            heatmap.set_data(new_data)  # Atualizar os dados do gráfico de calor
            return [heatmap]

        # Crie a animação
        animation = FuncAnimation(fig, update_heatmap, interval=interval)

        # Exiba o gráfico de calor em tempo real
        plt.show()

        return None

    def heatmap(self):

        # Recebe a matriz de dados
        dataL, dataG = self.separate_matrix(self.Q_table)
        arr = np.arange(0, self.line_number, 1)

        # Crie o gráfico de calor usando imshow
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(6,10))


        heatmapG = ax[0].imshow(dataG, cmap='coolwarm')
        ax[0].set_title("Grafico 'Maior'")

        # Define o intervalo das marcações de um em um no eixo x e y
        ax[0].set_xticks(arr)
        ax[0].set_yticks(arr)

        # Adiciona as legendas nos eixos x e y
        ax[0].set_xticklabels(arr)
        ax[0].set_yticklabels(arr)

        # Adicione rótulos para os eixos x e y
        ax[0].set_xlabel('Estados')
        ax[0].set_ylabel('Ações')

        heatmapL = ax[1].imshow(dataL, cmap="coolwarm")
        ax[1].set_title("Grafico 'Menor'")

        # Define o intervalo das marcações de um em um no eixo x e y
        ax[1].set_xticks(arr)
        ax[1].set_yticks(arr)

        # Adiciona as legendas nos eixos x e y
        ax[1].set_xticklabels(arr)
        ax[1].set_yticklabels(arr)

        # Adicione uma barra de cores para o gráfico de calor
        fig.colorbar(heatmapG)
        fig.colorbar(heatmapL)
        
        # Adicione rótulos para os eixos x e y
        ax[1].set_xlabel('Estados')
        ax[1].set_ylabel('Ações')

        # Exiba o gráfico de calor
        plt.show()

        return None

    def separate_matrix(self, matrix):

        even_matrix_number = np.empty((self.line_number, self.line_number))  
        odd_matrix_number = np.empty((self.line_number, self.line_number))

        for i in range(self.line_number):
            for j in range(self.column_number):
                value = matrix[i][j]
                if j % 2 == 0:
                    even_matrix_number[i][j//2] = value  # adiciona value à matrix de colunas pares
                else:
                    odd_matrix_number[i][j//2] = value  # adiciona value à matrix de colunas ímpares

        return even_matrix_number, odd_matrix_number  # retorna as duas listas como tupla

if __name__ == "__main__":
    q = Q_Ai(10, "Lucky_game.pkl")
    