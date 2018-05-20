import copy
import string

class AFoperations:

    @staticmethod
    def minimizacao(dict_af, estados_aceitacao, estado_inicial):
        dict_newaf = {}
        estados_mortos = []
        alfabeto = []

        # Pegar alfabeto
        for key in dict_af.keys():
            for columns in range(len(dict_af[key])):
                if dict_af[key][columns][0] not in alfabeto:
                    alfabeto.insert(len(alfabeto), dict_af[key][columns][0])

        # Explicitando estado de erro nos outros estados
        existe_erro = AFoperations.explicitar_estados_mortos(dict_af, alfabeto)

        # Eliminacao de estados inalcancaveis e descobrindo os mortos
        AFoperations.kill_unreachable_discover_dead(dict_newaf, dict_af, alfabeto, estado_inicial, estados_aceitacao, estados_mortos)

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
                    if not(AFoperations.compare(key_1, key_2, alfabeto, dict_newaf, F, KF)):
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
    def kill_unreachable_discover_dead(dict_newaf, dict_af, alfabeto, estado_inicial, estados_aceitacao, estados_mortos):
        alc_keys = [estado_inicial]
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

        keys = dict_newaf.keys()
        for estado in estados_aceitacao:
            if estado not in keys:
                estados_aceitacao.remove(estado)

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
    
      @staticmethod
    def afnd_to_afd(afnd, estados_aceitacao):
        # suporta afnds com &
        AFoperations.eliminar_epsilon_transicoes(afnd)
        AFoperations.explicitar_estados_mortos(afnd, AFoperations.getAlfabeto(afnd))
        afd = {}

        # marcamos todos os estados como nao visitados
        estados_a_visitar = list(afnd.keys())
        estados_visitados = []

        # listas vazias retornam falso. Fazemos pop para controlar isto.
        while estados_a_visitar:  # ate visitarmos todos os estados
            estado_atual = estados_a_visitar.pop(0)
            subestados_atuais = estado_atual.split('.')  # estado_atual pode ser do tipo A.B

            ts_sn_afnd = []  # transicoes do estado atual do afnd

            # listas vazias retornam falso. Fazemos pop para controlar isto.
            while subestados_atuais:
                ts_sn_afnd += afnd[subestados_atuais.pop(0)]  # copiamos todas as transicoes do estado n

            # pode ter transicoes duplicadas
            ts_sn_afnd = AFoperations.remove_duplicatas_lista(ts_sn_afnd)
            ts_sn_afd = [ts_sn_afnd.pop(0)]  # add a 1ra transicao do n-esismo estado da afnd as da afd
            VTs_ja_tratados = [ts_sn_afd[0][0]]  # para garantir q para cada Vt vamos para um unico estado

            while ts_sn_afnd:  # pras demais transicoes deste estado
                if ts_sn_afnd[0][0] in VTs_ja_tratados:  # ja existe uma transicao com este Vt?
                    transicao_temporaria = ts_sn_afnd.pop(0)  # a transicao q vamos tratar no formato ['b', 'C']

                    # removemos a antiga no afd, eg: remove ['a', 'A'] pra evitar ter [['a', 'A'], ['a', 'A.B']]
                    posicao = 0
                    for j in range(0, len(ts_sn_afd)):
                        if ts_sn_afd[j][0] == transicao_temporaria[0]:
                            posicao = j
                            break
                    transicao_antiga = ts_sn_afd.pop(posicao)
                    novo_estado = transicao_antiga[1] + '.' + transicao_temporaria[1]  # eg: B + C = B.C
                    if novo_estado not in estados_visitados and novo_estado not in estados_a_visitar:
                        estados_a_visitar.append(novo_estado)
                    ts_sn_afd.append([transicao_temporaria[0], novo_estado])  # eg:  ['b', 'B.C']

                else:  # este Vt apareceu pela 1a vez (ie, nao combinamos estados)
                    t1_sn_afnd = ts_sn_afnd.pop(0)  # adicionar esta transicao
                    ts_sn_afd.append(t1_sn_afnd)
                    VTs_ja_tratados.append(t1_sn_afnd[0])  # marcamos este Vt como tratado

            # acabamos de processar este estado
            estados_visitados.append(estado_atual)
            # ja foi removido dos estados a visitar
            afd[estado_atual] = ts_sn_afd
            AFoperations.marca_estados_finais(afd, estados_aceitacao)
        return afd

    @staticmethod
    def remove_duplicatas_lista(lista):
        lista_temp = []
        for i in lista:
            if i not in lista_temp:
                lista_temp.append(i)
        return lista_temp

    '''
    # nao usado
    @staticmethod
    def deleta_asterisco_dicionario(afnd):
        dic_aux = {}
        for i in afnd:

            j = i.replace('*', '')
            dic_aux[j] = afnd[i]
        return dic_aux
    '''

    '''
    #nao usado
    @staticmethod
    def marca_estados_finais_old(afnd, afd):
        # args: AF de referencia, AF que vamos marcar (pode conter estados do tipo A.B)
        afd_aux = {}
        for estado in afd:
            if AFoperations.eh_final(afnd, estado):
                str_aux = '*' + estado
                afd_aux[str_aux] = afd[estado]
            else:
                afd_aux[estado] = afd[estado]
        return afd_aux
    '''
    @staticmethod
    def marca_estados_finais(afd, estados_aceitacao):
        # marca os estados compostos de afd como finais ou nao

        estados_aceitacao_new = estados_aceitacao
        for estado in afd:
            subestados = estado.split('.')
            for i in subestados:
                if i in estados_aceitacao:
                    estados_aceitacao_new.append(estado)
                    break
        # pode ter duplicatas
        estados_aceitacao = AFoperations.remove_duplicatas_lista(estados_aceitacao_new)

    @staticmethod
    def eliminar_epsilon_transicoes(afnd):
        afnd_s_epsilon = {}
        for estado in afnd:
            fechamento = AFoperations.fechamento_epsilon(estado, afnd)
            transicoes = []
            # adicionamos as transicoes de cada estado do fechamento. Obs: o fechamento inclui o proprio estado
            for estado_fech in fechamento:
                transicoes_temp = afnd[estado_fech]
                for i in transicoes_temp:
                    if i[0] != '&':  # nao queremos transicoes epsilon no afnd resultante
                        transicoes.append(i)
            # podemos ter transicoes repetidas
            transicoes_sem_repet = AFoperations.remove_duplicatas_lista(transicoes)
            afnd_s_epsilon[estado] = transicoes_sem_repet
            afnd = afnd_s_epsilon

    @staticmethod
    def fechamento_epsilon(estado, afnd):
        # param: estado, afnd
        fechamento = [estado]
        fechamento_anterior = []
        while fechamento != fechamento_anterior:
            fechamento_anterior = list(fechamento)  # copiamos

            for i in fechamento_anterior:
                transicoes = afnd[i]  # copiamos as transicoes [['a' , 'A'], ...]
                for j in range(0, len(transicoes)):
                    if transicoes[j][0] == '&' and not transicoes[j][1] in fechamento:
                        fechamento.append(transicoes[j][1])

        return fechamento

    @staticmethod
    def renomear_estados_compostos(afd, estados_aceitacao, estado_inicial):
        estados_existentes = list(afd.keys())
        estados_todos = list(string.ascii_uppercase)
        nomes_possiveis_estados = []
        nome_velho_novo = {}  # usamos para renomear as transicoes

        for i in estados_todos:
            if i not in estados_existentes:
                nomes_possiveis_estados.append(i)

        # renomeando estados:
        for estado in estados_existentes:
            novo_nome = estado
            if '.' in estado:  # este estado sera renomeado

                # definimos um nome pro novo estado inicial:
                novo_nome = ''
                if not nomes_possiveis_estados:  # se nao vazia
                    novo_nome = nomes_possiveis_estados.pop(0)
                    nome_velho_novo[estado] = novo_nome
                numeroQ = 0  # caso usemos mais do q A..Z estados, usaremos Q0,Q1....
                while novo_nome == '':  # usamos mais do q A..Z estados
                    QEstado = 'Q' + str(numeroQ)
                    numeroQ = numeroQ + 1
                    if QEstado not in estados_existentes:  # este Qn ainda nao existe
                        novo_nome = QEstado
                        nome_velho_novo[estado] = novo_nome

            # else: este estado nao sera renomeado

        # renomeamos os estados nas transicoes
        af_final = {}
        for estado in afd:
            transicoes_velhas = list(afd[estado])  # copiamos as transicoes deste estado
            transicoes_novas = []
            while transicoes_velhas:
                transicao = transicoes_velhas.pop(0)
                if '.' in transicao[1]:  # esta transicao vai para um estado composto

                    for nome_velho in nome_velho_novo:  # encontra qual eh o novo nome pra este estado
                        if transicao[1] == nome_velho:
                            transicoes_novas.append([transicao[0], nome_velho_novo[nome_velho]])
                            break
                else:  # esta transicao vai para um estado nao composto
                    transicoes_novas.append(transicao)

                af_final[estado] = transicoes_novas
        afd = af_final

        try:  # estamos renomeando o estado inicial?
            estado_inicial = nome_velho_novo[estado_inicial]
        except KeyError:  # nao precisamos fazer nada
            estado_inicial = estado_inicial

        estados_aceitacao_aux = []
        for estado_aceit in estados_aceitacao:
            try:  # este estado sera renomeado
                estados_aceitacao_aux.append(nome_velho_novo[estado_aceit])
            except KeyError:  # este estado nao sera renomeado
                estados_aceitacao_aux.append(estado_aceit)
        estados_aceitacao = estados_aceitacao_aux

    @staticmethod
    def uniao_afnds(afnd1, estados_aceitacao_afnd1, estado_inicial_afnd1, afnd2, estados_aceitacao_afnd2, estado_inicial_afnd2,
                    afnd_resultante, estados_aceitacao_afnd_resultante, estado_inicial_afnd_resultante):

        # o novo estado inicial sera final?
        novo_estado_eh_final = False
        if estado_inicial_afnd1 in estados_aceitacao_afnd1 or estado_inicial_afnd2 in estados_aceitacao_afnd2:
            novo_estado_eh_final = True

        estados_afnd1 = []
        estados_afnd2 = []
        estados_aceitacao_afnd_resultante = []
        for i in afnd1:
            estados_afnd1.append(i)

        # para nao termos mais de 1 estado com o msm nome
        AFoperations.renomear_estados(afnd2, estados_afnd1, estados_aceitacao_afnd2, estado_inicial_afnd2)

        for j in afnd2:
            estados_afnd2.append(j)

        # definimos um nome pro novo estado inicial
        novo_estado_inicial = ''
        estados_todos = list(string.ascii_uppercase)
        for k in estados_todos:
            if k not in estados_afnd1 and k not in estados_afnd2:
                novo_estado_inicial = k
                break  # ja encontamos um nome pro nosso estado
        numeroQ = 0  # caso usemos mais do q A..Z estados, usaremos Q0,Q1....
        while novo_estado_inicial == '':  # usamos mais do q A..Z estados
            QEstado = 'Q' + str(numeroQ)
            numeroQ = numeroQ + 1
            if QEstado not in estados_afnd1 and QEstado not in estados_afnd2:  # este Qn ainda nao existe
                novo_estado_inicial = QEstado

        # criamos transicoes epsilon do novo estado inicial para os 2 antigos estados inicias dos 2 afnds
        nova_transicao = [['&', estado_inicial_afnd1], ['&', estado_inicial_afnd2]]

        if novo_estado_eh_final:
            estados_aceitacao_afnd_resultante.append(novo_estado_inicial)

        estado_inicial_afnd_resultante = novo_estado_inicial

        afnd_final = {novo_estado_inicial: nova_transicao}
        # adicionamos os estados e transicoes dos 2 afnds originais a afnd final:
        for i in afnd1:
            afnd_final[i] = afnd1[i]
        for j in afnd2:
            afnd_final[j] = afnd2[j]
        afnd_resultante = afnd_final

        # marcamos os estados de aceitacao da afnd resultante
        estados_aceitacao_afnd_resultante = []
        for i in estados_aceitacao_afnd1:
            estados_aceitacao_afnd_resultante.append(i)
        for j in estados_aceitacao_afnd2:
            estados_aceitacao_afnd_resultante.append(j)


    @staticmethod
    def renomear_estados(af, nomes_proibidos, estados_aceitacao, estado_inicial):
        # param: af a ser renomeada, estados que nao podem aparecer na af, ...

        estados_existentes = list(af.keys())
        estados_todos = list(string.ascii_uppercase)
        estados_possiveis = []
        nome_velho_novo = {}  # usamos para renomear as transicoes

        for i in estados_todos:
            if i not in nomes_proibidos:
                estados_possiveis.append(i)

        for estado in estados_existentes:

            # definimos um novo nome para este estado:
            novo_nome = ''
            if not estados_possiveis:  # se nao estiver vazia
                novo_nome = estados_possiveis.pop(0)
                nome_velho_novo[estado] = novo_nome
            else:
                numeroQ = 0  # caso usemos mais do q A..Z estados, usaremos Q0,Q1....
                while novo_nome == '':  # usamos mais do q A..Z estados
                    QEstado = 'Q' + str(numeroQ)
                    numeroQ = numeroQ + 1
                    if QEstado not in estados_existentes and QEstado not in nomes_proibidos:  # este Qn ainda nao existe
                        novo_nome = QEstado

            # renomeia este estado (key) e o marca como final se necesario
            af[novo_nome] = af[estado]
            del af[estado]

        # renomeamos os estados nas transicoes
        af_final = {}
        for estado in af:
            transicoes_velhas = af[estado]  # transicoes deste estado
            transicoes_novas = []
            while transicoes_velhas:
                transicao = transicoes_velhas.pop(0)
                for nome_velho in nome_velho_novo:  # encontra qual eh o novo nome pra este estado
                    if transicao[1] == nome_velho:
                        transicoes_novas.append([transicao[0], nome_velho_novo[nome_velho]])
            af_final[estado] = transicoes_novas

        af = af_final

    @staticmethod
    def complemento(afnd, estados_aceitacao, estado_inicial):
        # param: aceita qualquer afnd

        AFoperations.afnd_to_afd(afnd, estados_aceitacao)  # determinimizamos, pode ter estados com nome A.B
        AFoperations.renomear_estados_compostos(afnd, estados_aceitacao, estado_inicial)
        alfabeto = AFoperations.getAlfabeto(afnd)
        AFoperations.explicitar_estados_mortos(afnd, alfabeto)  # afd eh completa

        # invertendo o status de final:
        novos_estados_aceitacao = []
        for i in list(afnd.getKeys()):
            if i not in estados_aceitacao:
                novos_estados_aceitacao.append(i)
        estados_aceitacao = novos_estados_aceitacao

    @staticmethod
    def getAlfabeto(afnd):
        #copiamos o afnd:
        afnd_aux = {}
        for i in afnd:
            afnd_aux[i] = list(afnd[i])
        # nao inclui &
        alfabeto = []
        for estado in afnd_aux:
            transicoes = afnd_aux[estado]
            while transicoes:
                transicao = transicoes.pop(0)
                if transicao[0] not in alfabeto and transicao[0] != '&':
                    alfabeto.append(transicao[0])
        return alfabeto

    @staticmethod
    def intersecao(afnd1, estados_aceitacao_afnd1, estado_inicial_afnd1, afnd2, estados_aceitacao_afnd2, estado_inicial_afnd2,
                   afnd_result, estados_aceitacao_afnd_result, estado_inicial_afnd_result):

        # renomeamos a afnd2 para nao termos mais de 1 estado com o msm nome
        AFoperations.renomear_estados(afnd2, list(afnd1.getkeys()), estados_aceitacao_afnd2, estado_inicial_afnd2)

        # por De Morgan af1 intersecao af2 = compl(compl(af1) uniao compl(af2))
        afnd1_temp = {}
        estados_aceitacao_afnd1_temp = list(estados_aceitacao_afnd1)
        estado_inicial_afnd1_temp = estado_inicial_afnd1
        for i in afnd1:
            afnd1_temp[i] = afnd1[i]
        afnd2_temp = {}
        estados_aceitacao_afnd2_temp = list(estados_aceitacao_afnd2)
        estado_inicial_afnd2_temp = estado_inicial_afnd2
        for j in afnd2:
            afnd2_temp[j] = afnd2[j]

        AFoperations.complemento(afnd1_temp, estados_aceitacao_afnd1_temp, estado_inicial_afnd1_temp)
        AFoperations.complemento(afnd2_temp, estados_aceitacao_afnd2_temp, estado_inicial_afnd2_temp)
        AFoperations.uniao_afnds(afnd1_temp, estados_aceitacao_afnd1_temp, estado_inicial_afnd1_temp,
                                 afnd2_temp, estados_aceitacao_afnd2_temp, estado_inicial_afnd2_temp,
                                 afnd_result, estados_aceitacao_afnd_result, estado_inicial_afnd_result)
        AFoperations.complemento(afnd_result, estados_aceitacao_afnd_result)

    @staticmethod
    def reverso(afnd, estados_aceitacao, estado_inicial):
        # param: aceita qualquer afnd
        #print('param: ', afnd, estados_aceitacao, estado_inicial)
        AFoperations.eliminar_epsilon_transicoes(afnd)

        estados = list(afnd.keys())
        antigo_estado_inicial = estado_inicial

        # definimos um nome pro novo estado inicial:
        estados_todos = list(string.ascii_uppercase)
        novo_estado_inicial = ''
        for i in estados_todos:
            if i not in estados:
                novo_estado_inicial = i
                break
        numeroQ = 0  # caso usemos mais do q A..Z estados, usaremos Q0,Q1....
        while novo_estado_inicial == '':  # usamos mais do q A..Z estados
            QEstado = 'Q' + str(numeroQ)
            numeroQ = numeroQ + 1
            if QEstado not in estados:  # este Qn ainda nao existe
                novo_estado_inicial = QEstado

        # invertemos todas as transicoes:
        af_temp = {}
        while estados:
            estado = estados.pop(0)
            transicoes = afnd[estado]
            while transicoes:
                transicao = transicoes.pop(0)
                origem = estado
                destino = transicao[1]
                simbolo = transicao[0]
                AFoperations.add_transicao_to_afnd(af_temp, destino, [simbolo, origem])

        # adicionamos o novo_estado_inicial e as suas transicoes a afnd:
        trans_est_inic = []
        for i in estados_aceitacao:
            trans_est_inic.append(['&', i])
        af_final = {novo_estado_inicial: trans_est_inic}
        estado_inicial = novo_estado_inicial

        # adicionamos os demais estados:
        for i in af_temp:
            af_final[i] = af_temp[i]

    @staticmethod
    def add_transicao_to_afnd(afnd, estado, transicao):
        # adiciona a transicao ao estado da afnd. modifica a propria afnd
        try:
            transicoes = afnd[estado]  # ja existe este estado na afnd
            transicoes.append(transicao)
            del afnd[estado]
            afnd[estado] = transicoes
        except KeyError:  # nao existe este estado na afnd
            afnd[estado] = [transicao]
    
    @staticmethod
    def diferenca(afnd1, afnd2):
        estados_afnd1 = []
        for i in afnd1:
            if i[0] == '*':  # tiramos o * do estado final
                estados_afnd1.append(i[1:])
            else:
                estados_afnd1.append(i)

        afnd2_renom = AFoperations.renomear_estados(afnd2, estados_afnd1)  # para nao termos mais de 1 estado com o msm nome

        afnd2_complemento = AFoperations.complemento(afnd2_renom)
        return AFoperations.intersecao(afnd1, afnd2_complemento)
    
