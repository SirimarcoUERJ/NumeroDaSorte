import numpy as np
import pickle as pkl

class Q_Ai:
    
    def __init__(self, line_number, filename, exploitation=0.95, learn_rate=0.01, discount=0.9):
        """Inicializa a classe Q_Ai."""
        self.line_number = line_number + 1
        self.column_number = 2 * self.line_number
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
            #self.Q_table = np.random.randn(self.line_number, self.column_number)
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
            action = np.random.choice([0, len(self.get_columns_from_table(column)) - 1])
            
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
                reward = 3
            else:
                reward = -20

        elif feedback == 1:
            if last_decision > new_decision:
                reward = 3
            else:
                reward = -20
        
        elif feedback == -1:
            reward = 50
            
        return reward


    def update_Q_table(self, state, reward):
        """Atualiza os valores da tabela Q utilizando a equação clássica de reforço, a fim de priorizar as melhores ações.
        Recebe como parâmetros o estado atual e a recompensa associada a ele."""
        column = self.guide[state[0]][state[1]]
        line = self.choose_action(state)

        # Equação de reforço para atualizar o valor da tabela Q
        self.Q_table[line][column] = (1 - self.learn_rate) * self.Q_table[line][column] + self.learn_rate * (reward + (1 - self.discount) * 50)

        return None
