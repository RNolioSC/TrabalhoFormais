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
        estados_aceitacao.insert(len(estados_aceitacao), 'F')

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
                        if AFGR.verifica_estado_final(dict_swap, dict_gr, keys, contador, True):
                            dict_swap[keys].insert(len(dict_swap[keys]), [dict_gr[keys][contador], 'F'])

                        contador += 1
                else:
                    if AFGR.verifica_estado_final(dict_swap, dict_gr, keys, contador, True):
                        dict_swap[keys].insert(len(dict_swap[keys]), [dict_gr[keys][contador], 'F'])
                    contador += 1

            # Caso o ultimo elemento seja um nao terminal
            if not(AFGR.verifica_estado_final(dict_swap, dict_gr, keys, contador-2, False)):
                del dict_swap[keys][contador-2]

        return dict_swap

    # Verifica os estados finais, tem que ver uma forma melhor no futuro
    # op -> True - Substitui o estado, False - Elimina o estado
    @staticmethod
    def verifica_estado_final(dict_swap, dict_gr, keys, contador, op):
        for estados in dict_swap[keys]:
            if estados[0] == dict_gr[keys][contador] and estados[1] != 'F' and op:
                estados[1] = 'F'
                return False
            elif estados[0] == dict_gr[keys][contador] and estados[1] != 'F' and not op:
                return False
        return True
