class AFGR:

    @staticmethod
    def af_to_gr(dict_af):
        dict_swap = {}
        for keys in dict_af:
            dict_swap[keys] = []
            for list in dict_af[keys]:
                dict_swap[keys].insert(len(dict_swap[keys]), list[0])
                dict_swap[keys].insert(len(dict_swap[keys]), list[1])
        return dict_swap

    @staticmethod
    def gr_to_af(dict_gr, estados_aceitacao):
        dict_swap = {}

        # Adicionando estado final
        dict_swap['F'] = []
        estados_aceitacao.append('F')

        for keys in dict_gr:
            dict_swap[keys] = []
            qtd_elementos = len(dict_gr[keys])
            contador = 0
            while contador < qtd_elementos:
                if contador+1 < len(dict_gr[keys]):
                    if dict_gr[keys][contador+1].istitle():
                        dict_swap[keys].insert(len(dict_swap[keys]), [dict_gr[keys][contador], dict_gr[keys][contador+1]])
                        contador += 2
                    else:
                        dict_swap[keys].insert(len(dict_swap[keys]), [dict_gr[keys][contador], 'F'])
                        contador += 1
                else:
                    dict_swap[keys].insert(len(dict_swap[keys]), [dict_gr[keys][contador], 'F'])
                    contador += 1

        # Descobrindo se o inicial é final TODO ARRUMAR ISSO DEPOIS
        for keys in dict_swap.keys():
            for transicoes in dict_swap[keys]:
                if transicoes[1] == 'S':
                    for keysF in dict_swap.keys():
                        for transicoesF in dict_swap[keysF]:
                            if transicoesF[1] == 'F':
                                if transicoes[0] == transicoesF[0]:
                                    estados_aceitacao.append('S')


        return dict_swap
