import json
import csv
import time

#função pra ler o arquivo json
def ler_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#função pra ler o csv
def ler_csv(file_path):
    with open(file_path, 'r') as f:
        return [row[0] for row in csv.reader(f, delimiter=';')]

#encontra as transições baseadas no estado atual do automato
def encontrar_transicao(transicoes, estado_atual, leitura):
    for transicao in transicoes:
        if transicao['from'] == estado_atual and transicao['read'] == leitura:
            return transicao['to']
    return None

#automato recebe uma string e processa a entrada e gera uma saida
def simular(automato, input_string):
    estado_atual = automato['initial']
    for simbolo in input_string:
        estado_atual = encontrar_transicao(automato['transitions'], estado_atual, simbolo)
        if estado_atual is None:
            return 0  
    return 1 if estado_atual in automato['final'] else 0

def main():
    #le o arquivo json
    automato = ler_json('ex1/ex1.json')
    #le o arquivo csv
    entradas = ler_csv('ex1/ex1_input.csv')
    
    #marca o tempo de inicio
    tempo_inicio = time.time()

    #marca se a entrada é aceita ou não
    for entrada in entradas:
        aceita = simular(automato, entrada)
        print(f"Entrada: {entrada} - Aceita: {aceita}")

    tempo_total = time.time() - tempo_inicio
    print(f"Tempo de execução: {tempo_total:.4f} segundos")

#garante que main seja executado apenas se o codigo for executado diretamente
if __name__ == "__main__":
    main()
