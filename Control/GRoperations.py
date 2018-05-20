class GRoperations:

    @staticmethod
    def fechamento(af, estado_inicial, estados_aceitacao):
        # Novo estado inicial
        af['$'] = []
        af['$'].insert(0, ['&', estado_inicial])
        af['$'].insert(1, ['&', '#'])
        af['#'] = []

        # Estados finais transitando para o estado inicial
        for estado in estados_aceitacao:
            af[estado].insert(len(af[estado]), ['&', '$'])

        return '$', ['#']

    @staticmethod
    def concatenacao(af1, af2, ei1, ei2, ef1, ef2):
        # Novo estado inicial
        af1['I'] = []
        af1['I'].insert(0, ['&', ei1])
        af1['I'].insert(0, ['&', ei2])

        # Estado(s) final(is) de af1 apontando para inicial de af2
        for estado in ef1:
            af1[estado].insert(0, ['&', ei2])

        # Estado(s) final(is) de af2 apontando para novo estado final
        for estado in ef2:
            af2[estado].insert(0, ['&', '#'])

        # Setando estados do af2 em af1
        for keys in af2.keys():
            af1[keys] = af2[keys]

        af1['#'] = []
        return 'I', ['#']

