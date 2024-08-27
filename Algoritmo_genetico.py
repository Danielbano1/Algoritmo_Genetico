from random import randint, random

# variaveis globais
tam_individuo = 13 
tam_populacao = 3000
max_geracoes = 100


# Função para imprimir um bytearray em binário
def print_bytearray(byte_array):
    for byte in byte_array:
        # Converte cada byte para sua representação binária e imprime
        print(format(byte, '05b'), end=' ')

def testar_cromossomo(cromossomo, tabela_frequencia, vidas_time):
    tabela_falsa = tabela_frequencia[:]
    vidas_falsa = vidas_time    
    # arvore binaria
    n = 16
    for indice, valor in enumerate((8, 4, 2, 1, 0)):
        if cromossomo < n:
            n -= valor
        else:
            tabela_falsa[indice] += 1
            vidas_falsa -= 1
            n += valor

    # teste
    if vidas_falsa <= 0:
        return 0, tabela_frequencia, vidas_time
    
    for i in range(5):
        if tabela_falsa[i] > 5:
            return 0, tabela_frequencia, vidas_time  
    
    #aprovado
    return 1, tabela_falsa, vidas_falsa   

def gerar_individuo():
    individuo = bytearray(tam_individuo)
    tabela_frequencia = [0] * 5
    vidas_time = 25

    for i in range(tam_individuo):
        while True:
            cromossomo = randint(1, 31)    # gera um cromossomo
            aprovado, tabela_frequencia, vidas_time = testar_cromossomo(cromossomo, tabela_frequencia, vidas_time)   # verifica se o cromossomo é valido

            if vidas_time < (tam_individuo - i):        # verifica se o individuo será válido
                return None
            if aprovado:
                break

        individuo[i] = cromossomo      # atribui cromossomo ao individuo 

    if vidas_time != 1:                # verifica se o individuo está usando todas as vidas possiveis
            return None
    #print(tabela_frequencia)
    #print(vidas_time)
    return individuo  

def gerar_populacao_aleatoria():
    populacao = []

    for i in range(tam_populacao):
        while True:
            individuo = gerar_individuo()
            if individuo != None:
                break

        populacao.append(individuo)

    #print_bytearray(individuo)
    return populacao

def testar_individuo(individuo):
    tabela_frequencia = [0] * 5
    vidas_time = 25

    for i in range(tam_individuo):
        aprovado, tabela_frequencia, vidas_time = testar_cromossomo(individuo[i], tabela_frequencia, vidas_time)   # verifica se o cromossomo é valido
        if not aprovado:
                #print("\n")
                #print(tabela_frequencia)
                #print(vidas_time)
                return 0
        
    #print("\n")
    #print(tabela_frequencia)
    #print(vidas_time)
    return 1    

def calcular_poder_cromossomo(cromossomo):
    poder = 0
    # arvore binaria
    n = 16
    for indice, valor in enumerate((8, 4, 2, 1, 0)):
        if cromossomo < n:
            n -= valor
        else:
            poder += (1.5 - (indice*0.1))
            n += valor
    
    return poder

def calcular_tempo_ginasio(poder, ginasio):
    dificuldade_ginasio = 35 + (ginasio * 5)
    return (dificuldade_ginasio / poder)

def calcular_tempo_individuo(individuo):    
    tempo_individuo = 0
    for i in range(tam_individuo):
        poder = calcular_poder_cromossomo(individuo[i])
        tempo_ginasio = calcular_tempo_ginasio(poder, i)
        tempo_individuo += tempo_ginasio
    
    return tempo_individuo



def fitness(populacao):
    populacao_ordenada = []
    for individuo in populacao:
        tempo_individuo = calcular_tempo_individuo(individuo)
        instancia = {"individuo": individuo, "tempo": tempo_individuo}
        populacao_ordenada.append(instancia)

    populacao_ordenada = sorted(populacao_ordenada, key=lambda x: x["tempo"])

    return populacao_ordenada


def roleta(populacao_ordenada):
    tamanho_populacao = tam_populacao
    inicial = randint(0, 5)

    if(inicial == 0):
        return populacao_ordenada[randint(0, tamanho_populacao//20)]['individuo']
    elif(inicial == 1):
        return populacao_ordenada[randint((tamanho_populacao//20) + 1, tamanho_populacao//6)]['individuo']
    elif(inicial == 2):
        return populacao_ordenada[randint((tamanho_populacao//6) + 1, tamanho_populacao//2.8)]['individuo']
    elif(inicial == 3):
        return populacao_ordenada[randint((tamanho_populacao//2.8) + 1, tamanho_populacao//1.6)]['individuo']
    else:
        return populacao_ordenada[randint((tamanho_populacao//1.6) + 1, tamanho_populacao - 1)]['individuo']

def crossover(pai1, pai2):
    filho1 = [None] * 13
    filho2 = [None] * 13
    for i in range(13):
        # Seleciona aleatoriamente se o gene vem do pai1 ou pai2
        if random() < 0.5:
            filho1[i] = pai1[i]
            filho2[i] = pai2[i]
        else:
            filho1[i] = pai2[i]
            filho2[i] = pai1[i]

    

    return filho1, filho2
    


def gerar_nova_populacao(populacao_atual):
    #populacao_atual = fitness(populacao)
    nova_populacao = []
    for i in range(int(tam_populacao)):
        while True:
            filho1, filho2 = crossover(roleta(populacao_atual), roleta(populacao_atual))
            if (testar_individuo(filho1) == 1):
                nova_populacao.append(filho1)
                break
            elif (testar_individuo(filho2) == 1):
                nova_populacao.append(filho2)
                break

    return nova_populacao


def GA(populacao_inicial):
    geracao = 1
    populacao_atual = populacao_inicial
    valores = []
    populacao_ordenada = fitness(populacao_atual)
    print(populacao_ordenada[0])
    
    while(geracao < max_geracoes):
        populacao_ordenada = fitness(populacao_atual)
        valores.append(populacao_ordenada[0])
        populacao_atual = gerar_nova_populacao(populacao_ordenada)
        geracao += 1    

    return valores
    



#main

valores = GA(gerar_populacao_aleatoria())

lista_de_tempos = [dicionario['tempo'] for dicionario in valores]

#GERADOR DE GRAFICO
from matplotlib import pyplot as plt
plt.plot(range(len(lista_de_tempos)), lista_de_tempos)
plt.grid(True, zorder=0)
plt.title("Tempo total de lutas")
plt.xlabel("Geracao")
plt.ylabel("Tempo")
plt.show()

valores = sorted(valores, key=lambda x: x['tempo'])
print(valores[0])
print(len(valores))





