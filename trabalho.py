class Gramatica:
    def __init__(self, producoes):
        self.producoes = producoes
        self.nao_terminais = set(producoes.keys())
        self.terminais = set()
        for regras in producoes.values():
            for regra in regras:
                for simbolo in regra:
                    if not simbolo.isupper():
                        self.terminais.add(simbolo)

    def remover_simbolos_inuteis(self):
        acessiveis = set()
        acessiveis.add('S')
        visitados = set()

        while acessiveis:
            simbolo = acessiveis.pop()
            visitados.add(simbolo)
            for regra in self.producoes.get(simbolo, []):
                for s in regra:
                    if s in self.nao_terminais and s not in visitados:
                        acessiveis.add(s)

        nao_terminais_acessiveis = visitados
        self.nao_terminais = nao_terminais_acessiveis
        self.producoes = {k: v for k, v in self.producoes.items() if k in nao_terminais_acessiveis}

        geradores = set()
        mudanca = True

        while mudanca:
            mudanca = False
            for nao_terminal, regras in self.producoes.items():
                if nao_terminal not in geradores:
                    for regra in regras:
                        if all(s in geradores or s in self.terminais for s in regra):
                            geradores.add(nao_terminal)
                            mudanca = True

        self.nao_terminais = geradores
        self.producoes = {k: v for k, v in self.producoes.items() if k in geradores}

    def remover_producoes_vazias(self):
        epsilon_producoes = {nt for nt, regras in self.producoes.items() if '' in regras}
        if not epsilon_producoes:
            return

        while epsilon_producoes:
            epsilon_producao = epsilon_producoes.pop()
            novas_producoes = {}
            for nt, regras in self.producoes.items():
                novas_regras = set()
                for regra in regras:
                    if epsilon_producao in regra:
                        novas_regras.add(regra.replace(epsilon_producao, ''))
                    novas_regras.add(regra)
                novas_producoes[nt] = novas_regras

            self.producoes = {nt: list(regras) for nt, regras in novas_producoes.items() if '' not in regras}

        for nt, regras in self.producoes.items():
            self.producoes[nt] = [r for r in regras if r]

    def substituir_producoes(self):
        substituicoes = {}
        for nt in self.nao_terminais:
            if len(nt) > 1:
                substituicoes[nt] = f"N{len(substituicoes) + 1}"

        novas_producoes = {}
        for nt, regras in self.producoes.items():
            novo_nt = substituicoes.get(nt, nt)
            novas_regras = []
            for regra in regras:
                nova_regra = ''.join([substituicoes.get(s, s) for s in regra])
                novas_regras.append(nova_regra)
            novas_producoes[novo_nt] = novas_regras

        self.producoes = novas_producoes
        self.nao_terminais = set(self.producoes.keys())

    def para_forma_normal_chomsky(self):
        # Eliminar produções unitárias
        unitarios = {nt: set() for nt in self.nao_terminais}
        for nt, regras in self.producoes.items():
            for regra in regras:
                if len(regra) == 1 and regra in self.nao_terminais:
                    unitarios[nt].add(regra)

        while True:
            novos_unitarios = {nt: set(unitarios[nt]) for nt in self.nao_terminais}
            for nt in self.nao_terminais:
                for u in unitarios[nt]:
                    novos_unitarios[nt].update(unitarios[u])
            if novos_unitarios == unitarios:
                break
            unitarios = novos_unitarios

        novas_producoes = {}
        for nt in self.nao_terminais:
            novas_producoes[nt] = []
            for regra in self.producoes[nt]:
                if len(regra) == 1 and regra in self.nao_terminais:
                    novas_producoes[nt].extend(self.producoes[regra])
                else:
                    novas_producoes[nt].append(regra)

        self.producoes = novas_producoes

        # Substituir terminais em produções com mais de um símbolo
        novas_producoes = {}
        terminais_substituicoes = {}
        for nt in self.nao_terminais:
            novas_regras = []
            for regra in self.producoes[nt]:
                if len(regra) > 1:
                    nova_regra = []
                    for simbolo in regra:
                        if simbolo in self.terminais:
                            if simbolo not in terminais_substituicoes:
                                novo_nao_terminal = f"T{len(terminais_substituicoes) + 1}"
                                terminais_substituicoes[simbolo] = novo_nao_terminal
                                novas_producoes[novo_nao_terminal] = [simbolo]
                            nova_regra.append(terminais_substituicoes[simbolo])
                        else:
                            nova_regra.append(simbolo)
                    novas_regras.append(''.join(nova_regra))
                else:
                    novas_regras.append(regra)
            novas_producoes[nt] = novas_regras

        self.producoes.update(novas_producoes)

        # Transformar em forma normal de Chomsky
        novas_producoes = {}
        contador = 1
        for nt, regras in self.producoes.items():
            novas_regras = []
            for regra in regras:
                if len(regra) > 2:
                    novo_nt = f"X{contador}"
                    contador += 1
                    novas_regras.append(regra[0] + novo_nt)
                    for i in range(1, len(regra) - 2):
                        novas_producoes[novo_nt] = [regra[i] + f"X{contador}"]
                        novo_nt = f"X{contador}"
                        contador += 1
                    novas_producoes[novo_nt] = [regra[-2:]]
                else:
                    novas_regras.append(regra)
            novas_producoes[nt] = novas_regras

        self.producoes = novas_producoes

    def para_forma_normal_greibach(self):
        # A transformação para a forma normal de Greibach é complexa e requer a remoção de recursão à esquerda e a transformação de produções para garantir que cada produção comece com um terminal seguido de não-terminais.

        def substitui(nt, producoes):
            novas_regras = []
            for regra in producoes[nt]:
                if regra[0] in self.nao_terminais:
                    for sub_regra in producoes[regra[0]]:
                        novas_regras.append(sub_regra + regra[1:])
                else:
                    novas_regras.append(regra)
            return novas_regras

        def move_terminais(producoes):
            novas_producoes = {}
            contador = 1
            for nt, regras in producoes.items():
                novas_regras = []
                for regra in regras:
                    if regra and regra[0] in self.terminais:
                        novas_regras.append(regra)
                    else:
                        novo_nt = f"T{contador}"
                        contador += 1
                        novas_producoes[novo_nt] = [regra[0]]
                        novas_regras.append(novo_nt + regra[1:])
                novas_producoes[nt] = novas_regras
            return novas_producoes

        for nt in list(self.nao_terminais):
            self.producoes[nt] = substitui(nt, self.producoes)

        self.producoes = move_terminais(self.producoes)

    def fatoracao_a_esquerda(self):
        # Implementação da fatoração à esquerda
        novas_producoes = {}
        for nt in self.nao_terminais:
            prefixos = {}
            for regra in self.producoes[nt]:
                prefixo = regra[0]
                if prefixo not in prefixos:
                    prefixos[prefixo] = []
                prefixos[prefixo].append(regra[1:])
            for prefixo, sufixos in prefixos.items():
                if len(sufixos) > 1:
                    novo_nt = f"{nt}'"
                    novas_producoes[nt] = [prefixo + novo_nt]
                    novas_producoes[novo_nt] = [s if s else 'ε' for s in sufixos]
                else:
                    novas_producoes[nt] = prefixos[prefixo]
        self.producoes = novas_producoes

    def remover_recursao_a_esquerda(self):
        # Implementação da remoção de recursão à esquerda
        novos_nao_terminais = list(self.nao_terminais)
        for i in range(len(novos_nao_terminais)):
            nt_i = novos_nao_terminais[i]
            for j in range(i):
                nt_j = novos_nao_terminais[j]
                novas_regras = []
                for regra in self.producoes[nt_i]:
                    if regra.startswith(nt_j):
                        for regra_j in self.producoes[nt_j]:
                            novas_regras.append(regra_j + regra[1:])
                    else:
                        novas_regras.append(regra)
                self.producoes[nt_i] = novas_regras

            recursivas = []
            nao_recursivas = []
            for regra in self.producoes[nt_i]:
                if regra.startswith(nt_i):
                    recursivas.append(regra[1:])
                else:
                    nao_recursivas.append(regra)

            if recursivas:
                novo_nt = f"{nt_i}'"
                self.nao_terminais.add(novo_nt)
                self.producoes[nt_i] = [r + novo_nt for r in nao_recursivas]
                self.producoes[novo_nt] = [r + novo_nt for r in recursivas] + ['ε']

    def __str__(self):
        resultado = []
        for nao_terminal, regras in self.producoes.items():
            resultado.append(f"{nao_terminal} -> {' | '.join(regras)}")
        return "\n".join(resultado)

# Exemplo de uso
producoes = {
    'S': ['aAa', 'bBv'],
    'A': ['a', 'aA'],
    'B': []
}

gramatica = Gramatica(producoes)
print("Gramática Original:")
print(gramatica)

# Simplificação
gramatica.remover_simbolos_inuteis()
gramatica.remover_producoes_vazias()
gramatica.substituir_producoes()

print("\nGramática Simplificada:")
print(gramatica)

# Normalização
gramatica.para_forma_normal_chomsky()
print("\nForma Normal de Chomsky:")
print(gramatica)

gramatica.para_forma_normal_greibach()
print("\nForma Normal de Greibach:")
print(gramatica)

# Melhorias
gramatica.fatoracao_a_esquerda()
gramatica.remover_recursao_a_esquerda()

print("\nGramática Melhorada:")
print(gramatica)
