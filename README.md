# Aut-mato-Finito

importando as bibliotecas:
{
import json
import csv
import time
}

Criando uma função que lê e carrega o arquivo .json:
{
def ler_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
}

Criando uma função que lê e carrega o arquivo .csv:
{
def ler_csv(file_path):
    with open(file_path, 'r') as f:
        return [row[0] for row in csv.reader(f, delimiter=';')]
}

Encontra as transições baseadas no estado atual do automato:
{
    def encontrar_transicao(transicoes, estado_atual, leitura):
    for transicao in transicoes:
        if transicao['from'] == estado_atual and transicao['read'] == leitura:
            return transicao['to']
    return None
}

O automato recebe uma variavel do tipo string e retorna uma saida com base no processamento com base no dado:
{
    def simular(automato, input_string):
    estado_atual = automato['initial']
    for simbolo in input_string:
        estado_atual = encontrar_transicao(automato['transitions'], estado_atual, simbolo)
        if estado_atual is None:
            return 0  
    return 1 if estado_atual in automato['final'] else 0

}

Função main, lê o arquivo .json e o .csv, começa a marcar o inicio do processamento do automato, compara e marca caso a entrada seja aceita ou não e após isso printa se ela foi aceita ou não. Printa o tempo de execução ao final dos processos e a linha do if garante que o main seja executado apenas se o codigo for executado diretamente.
{
def main():
    automato = ler_json('ex1/ex1.json')
    entradas = ler_csv('ex1/ex1_input.csv')
    
    tempo_inicio = time.time()

    for entrada in entradas:
        aceita = simular(automato, entrada)
        print(f"Entrada: {entrada} - Aceita: {aceita}")

    tempo_total = time.time() - tempo_inicio
    print(f"Tempo de execução: {tempo_total:.4f} segundos")

if __name__ == "__main__":
    main()
}

Para um teste de funcionamento do automato foi utilizado essas entradas:
ba;1
aaaabbbbbaaaaa;1
abababab;0
bbbbbbbb;0
aaaaaaaaaaaa;0
aaaaabaaaaa;1

E consequentemente tivemos o resultado:
Entrada: ba - Aceita: 0
Entrada: aaaabbbbbaaaaa - Aceita: 0
Entrada: abababab - Aceita: 0
Entrada: bbbbbbbb - Aceita: 0
Entrada: aaaaaaaaaaaa - Aceita: 0
Entrada: aaaaabaaaaa - Aceita: 0
Tempo de execução: 0.0140 segundos

Uma saida que aparentemente não é correspondente ao que deveria ter sido executado, obtendo resultados apenas '0'.
De forma resumida, eu acredito que isso seja um bug no código para indentificar as saídas como '0' ou '1'.
