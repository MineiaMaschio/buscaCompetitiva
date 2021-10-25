import platform
import time
from os import system
from random import choice
from math import inf as infinity

HUMANO = -1
IA = +1

# Cria tabuleiro vazio
tabuleiro = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

def exibe():
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                print(" _ ", end=' ')
            elif tabuleiro[i][j] == HUMANO:
                print(" X ", end=' ')
            elif tabuleiro[i][j] == IA:
                print(" O ", end=' ')

        print()

def limpar():
    so_nome = platform.system().lower();
    if 'windows' in so_nome:
        system('cls')
    else:
        system('clear')

def ganhou(tabuleiro, jogador):

    #Todos os estados em que o jogador pode vencer
    estados_ganhador = [
        [[0,0], [0,1], [0,2]],
        [[1,0], [1,1], [1,2]],
        [[2,0], [2,1], [2,2]],
        [[0,0], [1,0], [2,0]],
        [[0,1], [1,1], [2,1]],
        [[0,2], [1,2], [2,2]],
        [[0,0], [1,1], [2,2]],
        [[2,0], [1,1], [0,2]]
    ]

    #Verifica se o jogador venceu em algum estado
    for i in estados_ganhador:
        if tabuleiro[i[0][0]][i[0][1]] == jogador and tabuleiro[i[1][0]][i[1][1]] == jogador and tabuleiro[i[2][0]][i[2][1]] == jogador:
            return True

    return False

def alguem_ganhou(tabuleiro):
    return ganhou(tabuleiro, HUMANO) or ganhou(tabuleiro, IA)

def verifica_posicoes_vazias(tabuleiro):
    campos = []

    for x, lista in enumerate(tabuleiro):
        for y, elemento in enumerate(lista):
            if elemento == 0:
                campos.append([x, y])

    return campos

def avaliacao(tabuleiro):
    if ganhou(tabuleiro, IA):
        pontos = +1
    elif ganhou(tabuleiro, HUMANO):
        pontos = -1
    else:
        pontos = 0

    return pontos

def escolha_valida(x, y):
    if [x, y] in verifica_posicoes_vazias(tabuleiro):
        return True
    else:
        return False

def set_escolha(x, y, jogador):
    if escolha_valida(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False

def minimax(tabuleiro, profundidade, jogador):

    if jogador == IA:
        melhor = [-1, -1, -infinity];
    else:
        melhor = [-1, -1, +infinity];

    if profundidade == 0 or alguem_ganhou(tabuleiro):
        pontos = avaliacao(tabuleiro)
        return [-1,-1, pontos]


    for vazios in verifica_posicoes_vazias(tabuleiro):
        x = vazios[0]
        y = vazios[1]
        tabuleiro[x][y] = jogador
        pontos = minimax(tabuleiro, profundidade - 1, -jogador)
        tabuleiro[x][y] = 0
        pontos[0] = x
        pontos[1] = y

        if jogador == IA:
            if pontos[2] > melhor[2]:
                melhor = pontos #Valor maximo
        else:
            if pontos[2] < melhor[2]:
                melhor = pontos

    return melhor

def vez_ia():

    # Se nao existir mais posições vazias ou já tiver um ganhador então finaliza
    profundidade = len(verifica_posicoes_vazias(tabuleiro))
    if profundidade == 0 or alguem_ganhou(tabuleiro):
        return

    limpar()
    print('Vez do computador O')
    exibe()

    #Primeira jogada com uma posição aleatoria e de resto utiliza minimax
    if profundidade == 9:
        x = choice([0,1,2])
        y = choice([0,1,2])
    else:
        escolha = minimax(tabuleiro, profundidade, IA)
        x = escolha[0]
        y = escolha[1]

    set_escolha(x, y, IA)
    time.sleep(1)

def vez_humano():

    # Se nao existir mais posições vazias ou já tiver um ganhador então finaliza
    profundidade = len(verifica_posicoes_vazias(tabuleiro))
    if profundidade == 0 or alguem_ganhou(tabuleiro):
        return

    #Posições que o humano pode escolher
    escolha = -1
    escolhas = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpar()
    print('Sua vez')
    exibe()

    # Enquanto a esolha não for valida continua pedindo uma posição
    while escolha < 1 or escolha > 9:
        escolha = int(input('Escolha uma posição ente 1 a 9'))
        posxy = escolhas[escolha]
        valida = set_escolha(posxy[0], posxy[1], HUMANO)

        if not valida:
            print('Escolha não valida')
            escolha = -1

def main():
    # Humano sempre joga com X e máquina sempre com 0

    # Escolhe se quer iniciar jogando ou não
    primeiro = input("Você deseja iniciar? [s/n]: ").upper();

    # Enquanto existir posições vazias e ninguem ganhar continua jogando
    while len(verifica_posicoes_vazias(tabuleiro)) > 0 and not alguem_ganhou(tabuleiro):
        if primeiro == 'N':
            vez_ia()
            primeiro = ''

        vez_humano()
        vez_ia()

    #Finalizar jogo
    if ganhou(tabuleiro,HUMANO):
        print('Você ganhou!')
    elif ganhou(tabuleiro, IA):
        print('Você perdeu!')
    else:
        print('Empate')

    #Exibir tabuleiro
    exibe();

    exit()


if __name__ == '__main__':
    main()