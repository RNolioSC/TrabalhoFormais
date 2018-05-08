class AFoperations:

    @staticmethod
    def minimizacao(dict_af, estados_aceitacao):
        dict_newaf = {}
        alc_keys = [list(dict_af.keys())[0]]
        ja_visitados = []
        estados_mortos = []
        alfabeto = []

        # Pegar alfabeto
        for key in dict_af.keys():
            for columns in range(len(dict_af[key])):
                if dict_af[key][columns][0] not in alfabeto:
                    alfabeto.insert(len(alfabeto), dict_af[key][columns][0])

        # Adicionando estado de erro
        dict_newaf['Erro'] = []
        for char in alfabeto:
            dict_newaf['Erro'].insert(len(dict_newaf['Erro']), [char, 'Erro'])

        # Explicitando estado de erro nos outros estados
        for keys in dict_af.keys():
            existe = False
            for char in alfabeto:
                for producoes in dict_af[keys]:
                    if char in producoes:
                        existe = True
                if not existe:
                    dict_af[keys].insert(alfabeto.index(char), [char, 'Erro'])
                existe = False

        # Eliminacao de estados inalcancaveis e descobrindo os mortos
        while len(alc_keys) != 0:
            key = alc_keys[0]
            ja_visitados.insert(len(ja_visitados), key)
            count_dead = 0

            # Verificando se é alcançável
            dict_newaf[key] = dict_af[key]
            for transicoes in dict_newaf[key]:
                if transicoes[1] not in ja_visitados and transicoes[1] != 'Erro':
                    alc_keys.insert(len(alc_keys), transicoes[1])
                # Verificando se é morto
                if (transicoes[1] == key and transicoes[1] not in estados_aceitacao) or transicoes[1] == 'Erro':
                    count_dead += 1

            if count_dead == len(alfabeto):
                estados_mortos.insert(len(estados_mortos), key)

            del alc_keys[0]

        # Eliminando os estados mortos
        for keys in estados_mortos:
            dict_newaf.pop(keys)

        # Substituindo estados mortos pelo estado de erro
        for keys in dict_newaf.keys():
            if keys != 'Erro':
                for transicoes in dict_newaf[keys]:
                    if transicoes[1] in estados_mortos:
                        transicoes[1] = 'Erro'

        return dict_newaf