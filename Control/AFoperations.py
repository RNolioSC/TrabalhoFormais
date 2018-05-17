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
    
        @staticmethod
    def afnd_to_afd(afnd):
        afnd_s_e = AFoperations.eliminar_epsilon_transicoes(afnd)
        afnd_s_e = AFoperations.renomear_estados(afnd_s_e)

        # TODO: pode ocorrer problemas por ter estados do tipo A.B. renomear?

        afd = {}
        afnd_sf = AFoperations.deleta_asterisco_dicionario(afnd_s_e)  # ignoramos se sao ou nao finais

        # marcamos todos os estados como nao visitados
        estados_a_visitar = list(afnd_sf.keys())
        estados_visitados = []

        # empty sequences are false. Fazemos pop para controlar isto.
        while estados_a_visitar:  # ate visitarmos todos os estados
            estado_atual = estados_a_visitar.pop(0)
            # determinimizamos todos os estados:

            estados_atuais = estado_atual.split('.')  # estado_atual pode ser do tipo A.B
            # empty sequences are false. Fazemos pop para controlar isto.
            while estados_atuais:
                ts_sn_afnd = []
                while estados_atuais:
                    ts_sn_afnd += afnd_sf[estados_atuais.pop(0)]  # copiamos todas as transicoes do estado n
                ts_sn_afnd = AFoperations.remove_duplicatas_lista(ts_sn_afnd)  # pode ter duplicatas (eg: A.B)

                ts_sn_afd = [ts_sn_afnd.pop(0)]  # add a 1ra transicao do n-esismo estado da afnd as da afd

                VTs_ja_tratados = [ts_sn_afd[0][0]]  # para garantir q para cada Vt vamos para um unico estado

                # empty sequences are false. Fazemos pop para controlar isto.
                while range(0, len(ts_sn_afnd)):  # pras demais transicoes deste estado
                    if ts_sn_afnd[0][0] in VTs_ja_tratados:  # ja existe uma transicao com este Vt?
                        posicao = VTs_ja_tratados.index(ts_sn_afnd[0][0])
                        transicao_temporaria = ts_sn_afnd.pop(posicao)  # a transicao q vamos tratar no formato ['b', 'C']

                        transicao_antiga = ts_sn_afd.pop(posicao)
                        # remove a antiga no afd, eg: remove ['a', 'A'] pra evitar [['a', 'A'], ['a', 'A.B']]
                        novo_estado = transicao_antiga[1] + '.' + transicao_temporaria[1]  # eg: B + C = B.C

                        if novo_estado not in estados_visitados and novo_estado not in estados_a_visitar:
                            estados_a_visitar.append(novo_estado)

                        ts_sn_afd.append([transicao_temporaria[0], novo_estado])  # eg:  ['b', 'B.C']

                    else:  # este Vt apareceu pela 1a vez (ie, nao combinamos estados)
                        t1_sn_afnd = ts_sn_afnd.pop(0)  # adicionar esta transicao
                        ts_sn_afd.append(t1_sn_afnd)
                        VTs_ja_tratados.append(t1_sn_afnd[0])  # esta Vt ja foi tratada
                        #if novo_estado not in estados_visitados and novo_estado not in estados_a_visitar:
                        #   estados_a_visitar.append(novo_estado)

            # acabamos de processar este estado
            estados_visitados.append(estado_atual)
            afd[estado_atual] = ts_sn_afd

        # TODO: marcar quais estados sao finais

        return AFoperations.marca_estados_finais(afnd_s_e, afd)

    @staticmethod
    def remove_duplicatas_lista(lista):
        lista_temp = []
        for i in lista:
            if i not in lista_temp:
                lista_temp.append(i)
        return lista_temp

    @staticmethod
    def deleta_asterisco_dicionario(afnd):
        dic_aux = {}
        for i in afnd:

            j = i.replace('*', '')
            dic_aux[j] = afnd[i]
        return dic_aux

    @staticmethod
    def marca_estados_finais(afnd, afd):
    # args: AF de referencia, AF que vamos marcar (pode conter estados do tipo A.B)
        afd_aux = {}
        for estado in afd:

            if AFoperations.eh_final(afnd, estado):
                str_aux = '*' + estado
                afd_aux[str_aux] = afd[estado]
            else:
                afd_aux[estado] = afd[estado]
        return afd_aux

    @staticmethod
    def eh_final(afnd, estado):  # suporta estados A.B
        subestados = estado.split('.')
        for i in subestados:
            try:  # nao eh final
                _ = afnd[i]
            except KeyError:  # eh final
                temp = '*' + i
                _ = afnd[temp]  # nao deveria falhar nunca
                return True
        return False


    @staticmethod
    def eliminar_epsilon_transicoes(afnd):
        # TODO: checar pag 56, sipser. completo?
        afnd_sf = AFoperations.deleta_asterisco_dicionario(afnd)  # ignoramos se sao ou nao finais
        estados = list(afnd_sf.keys())
        afnd_sem_epsilon = {}
        for i in estados:
            fech_epsilon = AFoperations.fechamento_epsilon(i, afnd_sf)
            novo_estado = fech_epsilon[0]
            for j in range(1, len(fech_epsilon)):  # nomeamos o novo estado. eg: A.B
                novo_estado += '.' + fech_epsilon[j]
            transicoes = []
            for k in fech_epsilon:  # adicionamos as transicoes (exceto as epsilon)
                estado_atual = afnd_sf[k]
                for transicao in range(0, len(afnd_sf[k])):  # para cada transicao
                    if afnd_sf[k][transicao][0] != '&':
                        transicoes.append(afnd_sf[k][transicao])
            afnd_sem_epsilon[novo_estado] = transicoes

            # procuramos transicoes de outro estado a algum estado do fechamento

        for m in afnd_sem_epsilon:
            transicoes_2 = list(afnd_sem_epsilon[m])
            transicoes_novas = []
            for transicao in transicoes_2:
                for n in afnd_sem_epsilon:
                    print(n)
                    if transicao[1] in n:
                        transicoes_novas.append([transicao[0], n])
                        #if transicao[1] in :  #
                    #transicoes_novas.append([transicao[0], nov_estado])
                #else:
                 #   transicoes_novas.append(transicao)
            afnd_sem_epsilon[m] = transicoes_novas

        return AFoperations.marca_estados_finais(afnd, afnd_sem_epsilon)



    @staticmethod
    def fechamento_epsilon(estado, afnd):
        fechamento = [estado]
        fechamento_anterior = []
        while fechamento != fechamento_anterior:
            fechamento_anterior = list(fechamento)

            for i in fechamento:
                transicoes = afnd[i]  # copiamos as transicoes [['a' , 'A'], ...]
                for j in range(0, len(transicoes)):
                    if transicoes[j][0] == '&':
                        if not transicoes[j][1] in fechamento:
                            fechamento.append(transicoes[j][1])

        return fechamento

    @staticmethod
    def renomear_estados(af): # renomeia estados do tipo A.B
        af_sf = AFoperations.deleta_asterisco_dicionario(af)

        estados_existentes = list(af_sf.keys())
        estados_todos = list(string.ascii_uppercase)
        estados_possiveis = []
        estados_finais = []
        for k in estados_existentes:
            if AFoperations.eh_final(af, k):
                estados_finais.append(k)

        for i in estados_todos:
            if i not in estados_existentes:
                estados_possiveis.append(i)

        for j in estados_existentes:
            if '.' in j:  # este estado eh do tipo A.B
                novo_nome = estados_possiveis.pop(0)
                estados_finais.append(novo_nome)
                # renomeia as transicoes q vao pra este estado no resto do af
                for i in af_sf:  # todas as transicoes do estado 'i'
                    transicoes = list(af_sf[i])
                    transicoes_novas = []
                    while transicoes:
                        transicao = transicoes.pop(0)
                        if transicao[1] == j:
                            transicoes_novas.append([transicao[0], novo_nome])
                        else:
                            transicoes_novas.append(transicao)
                    del af_sf[i]
                    af_sf[i] = transicoes_novas

                # renomeia este estado (key) e o marca como final se necesario
                if novo_nome in estados_finais:
                    temp = '*' + novo_nome
                    af_sf[temp] = af_sf[j]
                    del af_sf[j]
                else:
                    af_sf[novo_nome] = af_sf[j]
                    del af_sf[j]

            else:  # este estado nao eh do tipo A.B, marcamos se é final ou nao
                if j in estados_finais:
                    temp = '*' + j
                    af_sf[temp] = af_sf[j]
                    del af_sf[j]
                # else: nao precisa modificar
        return af_sf
