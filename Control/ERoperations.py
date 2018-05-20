from Control.Nodo import *


class ERoperations:

    @staticmethod
    def er_to_af(er_expression):
        lambda_ = Nodo('λ', None, None, False, False)
        arvore = []
        pilha = [lambda_]

        # Explicitar concatenacao
        new_er_expression = ERoperations.explicitar_concatenacao(er_expression)

        # Criar arvore
        ERoperations.nodo_raiz(arvore, new_er_expression)

        # Costurar arvore
        ERoperations.costurar_arvore(pilha, arvore[0])

        # Criar tabela
        return ERoperations.criacao_tabela(arvore)

    @staticmethod
    def costurar_arvore(pilha, elemento):
        if elemento.get_filho_esquerda() is not None:
            pilha.insert(len(pilha), elemento)
            ERoperations.costurar_arvore(pilha, elemento.get_filho_esquerda())
            pilha.remove(elemento)
        if elemento.get_filho_direita() is not None:
            ERoperations.costurar_arvore(pilha, elemento.get_filho_direita())
        else:
            elemento.set_costura(pilha[len(pilha) - 1])

    @staticmethod
    def nodo_raiz(arvore, new_er_expression):
        operador_atual = '$'
        operador_atual, posicao_operador_atual = ERoperations.new_operator(operador_atual, new_er_expression)

        if operador_atual == '$':
            new_er_expression, operador_atual = ERoperations.remover_parenteses(new_er_expression)
            operador_atual, posicao_operador_atual = ERoperations.new_operator(operador_atual, new_er_expression)

        nodo_raiz = Nodo(operador_atual, None, None, False, True)
        arvore.insert(len(arvore), nodo_raiz)

        if operador_atual == '.' or operador_atual == '|':
            nodo_esq = ERoperations.criar_arvore(arvore, new_er_expression[:posicao_operador_atual], nodo_raiz, 'e')
            nodo_dir = ERoperations.criar_arvore(arvore, new_er_expression[posicao_operador_atual+1:], nodo_raiz, 'd')
            arvore.insert(len(arvore), nodo_esq)
            arvore.insert(len(arvore), nodo_dir)
            nodo_raiz.set_filho_direita(nodo_dir)
            nodo_raiz.set_filho_esquerda(nodo_esq)
        if operador_atual == '*' or operador_atual == '?':
            nodo_esq = ERoperations.criar_arvore(arvore, new_er_expression[:posicao_operador_atual], nodo_raiz, 'e')
            arvore.insert(len(arvore), nodo_esq)
            nodo_raiz.set_filho_esquerda(nodo_esq)

    @staticmethod
    def criacao_tabela(arvore):
        number_states = 1
        state = 'Q'

        novos_estados = []
        historico = {}
        lista_estados_atual = []
        dict_associacao = {}
        dict_simbolo_estado = {}
        dict_af = {}
        ja_add = []
        estados_excluidos = []
        excluido_por = {}
        estados_aceitacao = []

        # Estado inicial
        ERoperations.criar_tabela(lista_estados_atual, arvore[0], 'DESCER')
        dict_af['Q0'] = []
        for simbolos in lista_estados_atual:
            if simbolos.get_simbolo() not in ja_add and simbolos.get_simbolo() != 'λ':
                novo_estado = state + str(number_states)
                dict_af['Q0'].insert(len(dict_af['Q0']), [simbolos.get_simbolo(), novo_estado])
                novos_estados.insert(len(novos_estados), novo_estado)
                dict_associacao[novo_estado] = [simbolos]
                dict_simbolo_estado[simbolos.get_simbolo()] = novo_estado
                number_states += 1
                ja_add.insert(0, simbolos.get_simbolo())
            elif simbolos.get_simbolo() != 'λ':
                dict_associacao[dict_simbolo_estado[simbolos.get_simbolo()]].append(simbolos)
            else:
                estados_aceitacao.insert(len(estados_aceitacao), 'Q0')
        historico['Q0'] = lista_estados_atual.copy()
        count = 0
        while len(novos_estados) != 0 and count < 4:
            ja_add = []
            estado_atual = novos_estados.pop(0)
            lista_estados_atual = []

            # Analiso a arvore
            for simbolos in dict_associacao[estado_atual]:
                if simbolos.get_simbolo() != 'λ':
                    ERoperations.criar_tabela(lista_estados_atual, simbolos.get_costura(), 'SUBIR')

            # Se só tem λ como simbolo
            if not lista_estados_atual:
                dict_af[estado_atual] = []
                estados_aceitacao.insert(len(estados_aceitacao), estado_atual)
            else:
                # Verifico se estado já existe
                for keys in historico.keys():
                    if historico[keys] == lista_estados_atual:
                        estados_excluidos.insert(len(estados_excluidos), estado_atual)
                        excluido_por[estado_atual] = keys

                if estado_atual not in estados_excluidos:
                    # Crio novos estados
                    dict_af[estado_atual] = []
                    for simbolos in lista_estados_atual:
                        if simbolos.get_simbolo() not in ja_add and simbolos.get_simbolo() != 'λ':
                            novo_estado = state+str(number_states)
                            dict_af[estado_atual].insert(len(dict_af[estado_atual]), [simbolos.get_simbolo(), novo_estado])
                            novos_estados.insert(len(novos_estados), novo_estado)
                            dict_associacao[novo_estado] = [simbolos]
                            dict_simbolo_estado[simbolos.get_simbolo()] = novo_estado
                            number_states += 1
                            ja_add.insert(0, simbolos.get_simbolo())
                        elif simbolos.get_simbolo() != 'λ':
                            dict_associacao[dict_simbolo_estado[simbolos.get_simbolo()]].insert(0, simbolos)
                        else:
                            estados_aceitacao.insert(len(estados_aceitacao), estado_atual)
                    historico[estado_atual] = lista_estados_atual.copy()
                else:
                    # Apagar referencias desse estado
                    for keys in dict_af.keys():
                        for transicoes in dict_af[keys]:
                            for simbolos in estados_excluidos:
                                if transicoes[1] == simbolos:
                                    transicoes[1] = excluido_por[simbolos]

        return dict_af, estados_aceitacao, 'Q0'


    @staticmethod
    def criar_tabela(lista_elementos, elemento, direcao):
        if (elemento.get_eh_folha() or elemento.get_simbolo() == 'λ') and elemento not in lista_elementos:
            lista_elementos.insert(len(lista_elementos), elemento)
            return

        if elemento.get_simbolo() == '*':
            ERoperations.criar_tabela(lista_elementos, elemento.get_filho_esquerda(), 'DESCER')
            ERoperations.criar_tabela(lista_elementos, elemento.get_costura(), 'SUBIR')
        if elemento.get_simbolo() == '.':
            if direcao == 'DESCER':
                ERoperations.criar_tabela(lista_elementos, elemento.get_filho_esquerda(), 'DESCER')
            else:
                ERoperations.criar_tabela(lista_elementos, elemento.get_filho_direita(), 'DESCER')
        if elemento.get_simbolo() == '|':
            if direcao == 'DESCER':
                ERoperations.criar_tabela(lista_elementos, elemento.get_filho_esquerda(), 'DESCER')
                ERoperations.criar_tabela(lista_elementos, elemento.get_filho_direita(), 'DESCER')
            else:
                tmp_elemento = elemento.get_filho_direita()
                while tmp_elemento.get_costura() is None:
                    tmp_elemento = tmp_elemento.get_filho_direita()
                ERoperations.criar_tabela(lista_elementos, tmp_elemento.get_costura(), 'SUBIR')
        if elemento.get_simbolo() == '?':
            if direcao == 'DESCER':
                ERoperations.criar_tabela(lista_elementos, elemento.get_filho_esquerda(), 'DESCER')
            ERoperations.criar_tabela(lista_elementos, elemento.get_costura(), 'SUBIR')

    @staticmethod
    def criar_arvore(arvore, er_expression, pai, lado_pai):
        er_expression, operador_atual = ERoperations.remover_parenteses(er_expression)

        if operador_atual == '*':
            nodo = Nodo('*', pai, lado_pai, False, False)
            posicao_operador_atual = len(er_expression)-1
        else:
            # Condicao de parada, nodo folha
            if len(er_expression) == 1:
                novo = Nodo(er_expression, pai, lado_pai, True, False)
                return novo

            operador_atual, posicao_operador_atual = ERoperations.new_operator(operador_atual, er_expression)

            nodo = Nodo(operador_atual, pai, lado_pai, False, False)

        if operador_atual == '.' or operador_atual == '|':
            nodo_esq = ERoperations.criar_arvore(arvore, er_expression[:posicao_operador_atual], nodo, 'e')
            nodo_dir = ERoperations.criar_arvore(arvore, er_expression[posicao_operador_atual+1:], nodo, 'd')
            arvore.insert(len(arvore), nodo_esq)
            arvore.insert(len(arvore), nodo_dir)
            nodo.set_filho_direita(nodo_dir)
            nodo.set_filho_esquerda(nodo_esq)
        if operador_atual == '*' or operador_atual == '?':
            nodo_esq = ERoperations.criar_arvore(arvore, er_expression[:posicao_operador_atual], nodo, 'e')
            arvore.insert(len(arvore), nodo_esq)
            nodo.set_filho_esquerda(nodo_esq)
        return nodo

    @staticmethod
    def new_operator(operador_atual, er_expression):
        simbolos_validos = ['?', '*', '.', '|', '?']
        posicao_operador_atual = 0
        contador_parenteses = 0

        for char in range(len(er_expression)):
            if contador_parenteses == 0 and er_expression[char] is not '(':
                if er_expression[char] in simbolos_validos and ERoperations.ordem_precedencia(er_expression[char], operador_atual):
                    operador_atual = er_expression[char]
                    posicao_operador_atual = char
            else:
                if er_expression[char] == '(':
                    contador_parenteses += 1
                if er_expression[char] == ')':
                    contador_parenteses -= 1

        return operador_atual, posicao_operador_atual

    @staticmethod
    def remover_parenteses(er_expression):
        contador_parenteses = 0
        posicao_inicial = -1
        posicao_final = -1
        operador = '$'

        for char in range(len(er_expression)):
            if er_expression[char] == '(' and posicao_inicial == -1:
                posicao_inicial = char
                contador_parenteses += 1
            elif er_expression[char] == '(':
                contador_parenteses += 1
            elif er_expression[char] == ')':
                contador_parenteses -= 1
                if contador_parenteses == 0:
                    posicao_final = char
            elif contador_parenteses == 0 and char + 1 < len(er_expression):
                if er_expression[char] in ['*', '|', '.', '?']:
                    posicao_inicial = -1
                    break

        if posicao_inicial == -1 or posicao_final == -1:
            return er_expression, operador
        else:
            new_er_expression = er_expression[:posicao_final] + er_expression[posicao_final+1:]
            new_er_expression = new_er_expression[:posicao_inicial] + new_er_expression[posicao_inicial+1:]
            if new_er_expression[len(new_er_expression)-1] == '*':
                operador = '*'
            return new_er_expression, operador

    @staticmethod
    def ordem_precedencia(operador, operador_atual):
        if operador_atual == '$':
            return True

        ordem_precedencia = ['?', '*', '.', '|']
        novo = ordem_precedencia.index(operador)
        atual = ordem_precedencia.index(operador_atual)

        if novo > atual:
            return True

        return False

    @staticmethod
    def explicitar_concatenacao(er_expression):
        new_er_expression = ""

        for char in range(len(er_expression)):
            if char+2 < len(er_expression):
                if er_expression[char] not in ['|', '.', '('] and er_expression[char+1] not in ['|', '.', ')', '*', '?']:
                    new_er_expression += er_expression[char]
                    new_er_expression += '.'
                else:
                    new_er_expression += er_expression[char]
            else:
                new_er_expression += er_expression[char]

        return new_er_expression[:len(new_er_expression)-1]

