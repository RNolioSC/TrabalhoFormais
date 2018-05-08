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

        for keys in dict_gr:
            dict_swap[keys] = []
            qtd_elementos = len(dict_gr[keys])
            contador = 0
            while contador < qtd_elementos:
                if contador+1 < len(dict_gr[keys]):
                    if dict_gr[keys][contador+1].istitle():
                        dict_swap[keys].insert(0, [dict_gr[keys][contador], dict_gr[keys][contador+1]])
                        contador += 2
                    else:
                        dict_swap[keys].insert(0, [dict_gr[keys][contador], 'F'])
                        contador += 1
                else:
                    dict_swap[keys].insert(0, [dict_gr[keys][contador], 'F'])
                    contador += 1

        return dict_swap