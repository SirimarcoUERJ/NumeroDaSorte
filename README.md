# NumeroDaSorte
O jogo "Número da Sorte" é um jogo em que um número aleatório é escolhido dentro de um intervalo predefinido. 
O objetivo do jogo é acertar o número da sorte, sendo que o jogador e o agente (computador) escolhem um número em cada rodada. 
O jogo consiste em várias rodadas e o jogador que acertar primeiro ganha um ponto e quem tiver mais pontos no final é o vencedor.

A inteligência artificial que tenta adivinhar o número da sorte utiliza o método Q-Learning para maximizar suas chances de ganhar. 
Esse método consiste em reforçar o comportamento da IA quando ela vai no sentido de acertar o número da sorte e penalizá-la quando 
ela vai no sentido contrário. 

Por exemplo, se a inteligência artificial escolheu 5 e obteve como retorno "maior" (ou seja, que o número da sorte é maior que 5), 
na próxima rodada ela deve escolher um número menor que 5 e esse comportamento será reforçado. Já no caso de escolher um número maior 
ou igual a 5, ela terá uma penalidade nessa ação para priorizar as ações mais benéficas.
