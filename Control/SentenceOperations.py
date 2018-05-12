import itertools


class SentenceOperations:

    @staticmethod
    def enum_sentences(size, estado_inicial, estados_aceitacao, dict_af):
        alfabeto = ""
        sentencas_aceitas = []

        # Aceita &?
        if size == 0:
            if estado_inicial in estados_aceitacao:
                sentencas_aceitas.insert(0, '&')
                return sentencas_aceitas

        # Pegar alfabeto
        for key in dict_af.keys():
            for columns in range(len(dict_af[key])):
                if dict_af[key][columns][0] not in alfabeto:
                    alfabeto += dict_af[key][columns][0]

        sentencas = list(itertools.product(alfabeto, repeat=size))

        for sentenca in sentencas:
            if SentenceOperations.accept_sentence(dict_af[estado_inicial], sentenca, estado_inicial, estados_aceitacao, dict_af):
                sentencas_aceitas.insert(len(sentencas_aceitas), ''.join(list(sentenca)))

        if len(sentencas_aceitas) == 0:
            sentencas_aceitas.insert(0, "Nenhuma sentença desse comprimento é aceita")

        return sentencas_aceitas

    @staticmethod
    def accept_sentence(producoes, sentence, cur_key, estados_aceitacao, dict_af):
        if not sentence:  # Se a sentenca esta vazia
            if cur_key in estados_aceitacao:
                return True
            else:
                return False

        for producao in producoes:
            if sentence[0] in producao:
                return SentenceOperations.accept_sentence(dict_af[producao[1]], sentence[1:], producao[1], estados_aceitacao, dict_af)

        return False
