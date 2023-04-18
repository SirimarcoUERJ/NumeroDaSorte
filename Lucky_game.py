import numpy as np

class Game:
    def __init__(self, menor_possivel = 0, maior_possivel = 10):
        # Inicializa o objeto Game com um limite superior n para o número aleatório a ser gerado
        self.maior_possivel = maior_possivel
        self.menor_possivel = menor_possivel
        self.limit = maior_possivel - menor_possivel
        self.number = np.random.randint(menor_possivel, maior_possivel)
        self.times = 0
        
    def Get_choice(self):
        """ Obtém a escolha do usuário e verifica se está dentro do intervalo permitido."""
        running = True

        while running:
            try:
                choice = float(input("Escolha um numero entre {} e {}: ".format(self.menor_possivel ,self.maior_possivel)))
                
                if choice <= self.maior_possivel and choice >= self.menor_possivel :                    
                    running = False

            except ValueError as e:
                # Se a entrada do usuário não puder ser convertida em um número, exibe uma mensagem de erro
                print("Erro: Entrada inválida. Digite um número entre 0 e 10.")

        print()

        return choice
            
    def Set_choice(self, choice):
        """ Verifica se o palpite do usuário é maior, menor ou igual ao número gerado aleatoriamente. Retorna um sinal (-1, 0 ou 1) para indicar a resposta."""

        self.times += 1
        
        if choice > self.number:
            response = 1 # O palpite é maior que o número aleatório gerado
        elif choice < self.number:
            response = 0 # O palpite é menor que o número aleatório gerado
        else:
            response = -1 # O palpite é igual ao número aleatório gerado

        return response

    def restart_game(self):
        """Reinicia o jogo gerando um novo número aleatório e reiniciando o contador de tentativas."""
        
        self.number = np.random.randint(0,self.limit+1)
        self.times = 0
        
    def won(self, choice):
        """ Verifica se o palpite do usuário é igual ao número aleatório gerado. Retorna True se o usuário ganhar, False caso contrário."""
        
        win = False

        if self.number == choice:
            win = True

        return win    

    def run(self):
        """ Executa o jogo principal."""
        
        running = True

        while running:
            
            choice = self.Get_choice()

            response = self.Set_choice(choice)
            
            if response == 1:
                print("{} é maior que o número da sorte!\n".format(choice))
                
            if response == 0:
                print("{} é menor que o número da sorte!\n".format(choice))
                
            if response == -1:
                print("{} é o número da sorte! \nVocê acertou o número da sorte em {} rodadas! \nQuer jogar novamente? (S/N)\n".format(choice,self.times))
                
                new_play = input()
                
                if new_play.lower() == "s":
                    self.restart_game()

                else:
                    running = False

