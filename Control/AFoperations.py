import copy

class AFoperations:

    @staticmethod
    def minimizacao(dict_af, estados_aceitacao):
        dict_newaf = {}
        estados_mortos = []
        alfabeto = []
        existe_erro = False

        # Pegar alfabeto
        for key in dict_af.keys():
            for columns in range(len(dict_af[key])):
                if dict_af[key][columns][0] not in alfabeto:
                    alfabeto.insert(len(alfabeto), dict_af[key][columns][0])

        # Explicitando estado de erro nos outros estados
        existe_erro = AFoperations.explicitar_estados_mortos(dict_af, alfabeto)

        # Eliminacao de estados inalcancaveis e descobrindo os mortos
        AFoperations.kill_unreachable_discover_dead(dict_newaf, dict_af, alfabeto, estados_aceitacao, estados_mortos)

        # Eliminando os estados mortos
        AFoperations.kill_dead_states(estados_mortos, dict_newaf)

        # Criando os conjuntos equivalentes
        F, KF = AFoperations.create_equivalent_sets(dict_newaf, estados_aceitacao)

        if existe_erro:
            KF['Erro'] = []

        # Separa os estados em classes de equivalencia
        new_F = F.copy()
        new_KF = KF.copy()
        old_F = {}
        old_KF = {}

        while len(old_F.keys()) != len(new_F.keys()) or len(old_KF.keys()) != len(new_KF.keys()):
            old_F = new_F.copy()
            old_KF = new_KF.copy()

            new_F = AFoperations.conjuntosEquivalentes(new_F, alfabeto, dict_newaf, old_F, old_KF)
            new_KF = AFoperations.conjuntosEquivalentes(new_KF, alfabeto, dict_newaf, old_F, old_KF)

        # Cria AFD Minimo
        dict_afmin = {}
        AFoperations.afdminimo(new_F, dict_afmin, dict_newaf, new_F, new_KF)
        AFoperations.afdminimo(new_KF, dict_afmin, dict_newaf, new_F, new_KF)

        return dict_afmin

    @staticmethod
    def afdminimo(ce, dict_afmin, dict_newaf, new_F, new_KF):
        for keys in ce.keys():
            dict_afmin[keys] = []
            for transicoes in dict_newaf[keys]:
                for key in new_F.keys():
                    if transicoes[1] in new_F[key] or transicoes[1] == key:
                        dict_afmin[keys].insert(len(dict_afmin[keys]), [transicoes[0], key])
                        break
                for key in new_KF.keys():
                    if transicoes[1] in new_KF[key] or transicoes[1] == key:
                        dict_afmin[keys].insert(len(dict_afmin[keys]), [transicoes[0], key])
                        break


    @staticmethod
    def conjuntosEquivalentes(conjunto, alfabeto, dict_newaf, F, KF):
        new_conjunto = copy.deepcopy(conjunto)
        estados_separados = []

        if len(conjunto.keys()) >= 1:
            for keys in conjunto.keys():
                if not (len(conjunto[keys]) == 0):
                    for estados in conjunto[keys]:
                        if not (AFoperations.compare(keys, estados, alfabeto, dict_newaf, F, KF)):
                            new_conjunto[estados] = []
                            new_conjunto[keys].remove(estados)
                            estados_separados.insert(len(estados_separados), estados)

        ja_visitados = []
        for key_1 in estados_separados:
            ja_visitados.insert(len(ja_visitados), key_1)
            for key_2 in estados_separados:
                if key_2 not in ja_visitados:
                    if not(AFoperations.compare(keys, estados, alfabeto, dict_newaf, F, KF)):
                        new_conjunto[key_1].insert(len(new_conjunto[key_1]), key_2)
                        del new_conjunto[key_2]

        return new_conjunto

    @staticmethod
    def compare(key, keyCompare, alfabeto, dict_newaf, F, KF):
        for char in range(len(alfabeto)):
            key_1 = dict_newaf[key][char][1]
            key_2 = dict_newaf[keyCompare][char][1]
            if not(key_1 == key_2 or AFoperations.equivalencia(key_1, key_2, F, KF)):
                return False
        return True

    # Verifica se está na mesma classe de equivalência
    @staticmethod
    def equivalencia(key, keyCompare, F, KF):
        for keys in F.keys():
            if (keyCompare in F[keys] or keyCompare == keys) and (key in F[keys] or key == keys):
                return True

        for keys in KF.keys():
            if (keyCompare in KF[keys] or keyCompare == keys) and (key in KF[keys] or key == keys):
                return True
        return False

    @staticmethod
    def explicitar_estados_mortos(dict_af, alfabeto):
        existe_erro = False
        for keys in dict_af.keys():
            existe = False
            for char in alfabeto:
                for producoes in dict_af[keys]:
                    if char in producoes:
                        existe = True
                if not existe:
                    dict_af[keys].insert(alfabeto.index(char), [char, 'Erro'])
                    existe_erro = True
                existe = False

        if existe_erro:
            # Adicionando estado de erro
            dict_af['Erro'] = []
            for char in alfabeto:
                dict_af['Erro'].insert(len(dict_af['Erro']), [char, 'Erro'])

        return existe_erro

    @staticmethod
    def kill_unreachable_discover_dead(dict_newaf, dict_af, alfabeto, estados_aceitacao, estados_mortos):
        alc_keys = [list(dict_af.keys())[0]]
        ja_visitados = []
        estados_vivos = estados_aceitacao.copy()
        count_dead = 0
        while len(alc_keys) != 0:
            dict_newaf[alc_keys[0]] = []
            for estados in dict_af[alc_keys[0]]:
                dict_newaf[alc_keys[0]].insert(len(dict_newaf), estados)
                if estados[1] not in ja_visitados:
                    alc_keys.insert(len(alc_keys), estados[1])
                if estados[1] in estados_vivos:
                    estados_vivos.insert(0, alc_keys[0])
                else:
                    count_dead += 1
            count_dead = 0
            ja_visitados.insert(0, alc_keys[0])
            if count_dead == len(alfabeto):
                estados_mortos.insert(0, alc_keys[0])
            del alc_keys[0]

    @staticmethod
    def kill_dead_states(estados_mortos, dict_newaf):
        for keys in estados_mortos:
            dict_newaf.pop(keys)

        # Substituindo estados mortos pelo estado de erro
        for keys in dict_newaf.keys():
            if keys != 'Erro':
                for transicoes in dict_newaf[keys]:
                    if transicoes[1] in estados_mortos:
                        transicoes[1] = 'Erro'

    @staticmethod
    def create_equivalent_sets(dict_newaf, estados_aceitacao):
        F = {}
        key_F = estados_aceitacao[0]
        F[key_F] = []
        for estados in estados_aceitacao:
            if estados != key_F:
                F[key_F].insert(len(F[key_F]), estados)

        KF = {}
        key_KF = None
        for keys in dict_newaf.keys():
            if keys not in estados_aceitacao and keys != 'Erro':
                KF[keys] = []
                key_KF = keys
                break

        for keys in dict_newaf.keys():
            if keys not in estados_aceitacao and keys != 'Erro' and key_KF != keys:
                KF[key_KF].insert(len(KF[key_KF]), keys)

        return F, KF

    # alc_keys = [list(dict_af.keys())[0]]
    # ja_visitados = []
    # while len(alc_keys) != 0:
    #     key = alc_keys[0]
    #     ja_visitados.insert(len(ja_visitados), key)
    #     count_dead = 0
    #
    #     # Verificando se é alcançável
    #     dict_newaf[key] = dict_af[key]
    #     if key not in estados_aceitacao:
    #         for transicoes in dict_newaf[key]:
    #             if transicoes[1] not in ja_visitados and transicoes[1] != 'Erro':
    #                 alc_keys.insert(len(alc_keys), transicoes[1])
    #             # Verificando se é morto
    #             if (transicoes[1] == key and transicoes[1] not in estados_aceitacao) or transicoes[1] == 'Erro':
    #                 count_dead += 1
    #
    #     if count_dead == len(alfabeto):
    #         estados_mortos.insert(len(estados_mortos), key)
    #
    #     del alc_keys[0]