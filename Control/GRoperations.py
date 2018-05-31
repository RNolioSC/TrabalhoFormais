from Control.AFoperations import *

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
        af1['$'] = []
        af1['$'].insert(0, ['&', ei1])

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
        return '$', ['#']

    @staticmethod
    def uniao(af1, af2, ei1, ei2, ef1, ef2):
        af3 = dict(af1, **af2)

        # Cria novo estado inicial
        af3['$'] = []

        # Uniao af1
        for transicoes in af1[ei1]:
            af3['$'].append(transicoes)

        # Uniao af2
        for transicoes in af2[ei2]:
            af3['$'].append(transicoes)

        return (af3, ef1+ef2+['$'], '$') if ei1 in ef1 or ei2 in ef2 else (af3, ef1+ef2, '$')

    @staticmethod
    def complemento(afd, estados_aceitacao):
        alfabeto = AFoperations.getAlfabeto(afd)
        AFoperations.explicitar_estados_mortos(afd, alfabeto)

        # invertendo o status de final:
        novos_estados_aceitacao = []
        for key in afd.keys():
            if key not in estados_aceitacao:
                novos_estados_aceitacao.append(key)

        return novos_estados_aceitacao

    @staticmethod
    def intersecao(af1, af2, ei1, ei2, ef1, ef2):
        ef1 = GRoperations.complemento(af1, ef1)
        ef2 = GRoperations.complemento(af2, ef2)
        af3, ef3, ei3 = GRoperations.uniao(af1, af2, ei1, ei2, ef1, ef2)
        ef3 = GRoperations.complemento(af3, ef3)
        return af3, ef3, ei3

    @staticmethod
    def diferenca(af1, af2, ei1, ei2, ef1, ef2):
        ef1 = GRoperations.complemento(af1, ef1)
        af3, ef3, ei3 = GRoperations.uniao(af1, af2, ei1, ei2, ef1, ef2)
        ef3 = GRoperations.complemento(af3, ef3)
        return af3, ef3, ei3

    @staticmethod
    def reverso(afd, estados_aceitacao, estado_inicial):
        af1 = {}

        # Novo estado inicial
        af1['$'] = []
        for ef in estados_aceitacao:
          af1['$'].insert(0, ['&', ef])

        for nao_terminais in afd:
            for producoes in afd[nao_terminais]:
                if producoes[1] not in af1.keys():
                    af1[producoes[1]] = []
                af1[producoes[1]].append([producoes[0], nao_terminais])

        return af1, [estado_inicial], '$'