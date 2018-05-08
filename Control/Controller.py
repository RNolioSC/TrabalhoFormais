from Control.AFGRoperations import *
from Control.AFoperations import *
from View.View import *

#TODO
# - Corrigir bug que suja a GR se for feito uma operacao qualquer (?) antes dela
# - Quando editar uma GR e retirar um estado dos estados final, (corrigir) verificar se o que era final antes volta a ser nao final
# - Gravação de GR/ER (Verificar se é necessário salvar em disco)
# - Explicitar caso de erro e definir as transicoes do estado final como estado de erro

class Controller:

    # Armazenamento
    dict_af = {}
    dict_gr = {}
    dict_er = {}
    estados_aceitacao = []
    sentence = None

    # View
    view = None

    # Enum
    CONST_PROFUNDIDADE = 5

    def __init__(self):
        view = View(self)

    # Modulo AF to GR vice-versa

    def af_to_gr(self):
        return AFGR.af_to_gr(self.dict_af)

    def gr_to_af(self):
        return AFGR.gr_to_af(self.dict_gr, self.estados_aceitacao)
    # ---------------------------

    # Módulo determinização e minimização

    def minimizacao(self):
        return AFoperations.minimizacao(self.dict_af, self.estados_aceitacao)

    # -----------------------------------

    # Modulo reconhecimento e enumeracao
    def enum_af(self):
        enum_sentencas_aceitas = []
        string = ""
        profundidade = 0
        primeiras_producoes = self.dict_af['S']
        print(self.estados_aceitacao)
        self.enum_op(primeiras_producoes, profundidade, 'S', enum_sentencas_aceitas, string)

        return enum_sentencas_aceitas

    def enum_op(self, prim_prod, prof, cur_key, enum_acc, string):

        if prof < self.CONST_PROFUNDIDADE:
            old_string = string
            for producoes in prim_prod:
                string += producoes[0]
                key = producoes[1]
                if key in self.estados_aceitacao and string not in enum_acc:
                    enum_acc.insert(len(enum_acc), string)
                self.enum_op(self.dict_af[key], prof+1, key, enum_acc, string)
                string = old_string

    def accept_sentence(self, producoes, sentence, cur_key):
        if not sentence:
            if cur_key in self.estados_aceitacao:
                return True
            else:
                return False

        for producao in producoes:
            if sentence[0] in producao:
                return self.accept_sentence(self.dict_af[producao[1]], sentence[1:], producao[1])

        return False

    # --------------------------------

    def exec(self, operacao):
        if operacao == 1:
            return self.get_dict_af()
        elif operacao == 2:
            return self.gr_to_af()
        elif operacao == 3:
            return self.af_to_gr()
        elif operacao == 4:
            return self.get_dict_af()
        elif operacao == 5:
            return self.minimizacao()
        elif operacao == 6:
            return self.get_dict_af()
        elif operacao == 7:
            return self.get_dict_gr()
        elif operacao == 8:
            return self.accept_sentence(self.dict_af['S'], list(self.sentence)[:-1], 'S')
        else:
            return self.enum_af()

    # Pega o af em forma de matriz e transforma na forma
    # {'EstadoAtual': ['simbolo','ProxEstado'],...}
    def set_dict_af(self, af_matrix):
        self.clean_dict_af()
        for rows in range(len(af_matrix)):
            if af_matrix[rows][0].get() == "":
                break

            if rows is not 0:
                key = af_matrix[rows][0].get()

                if '*' in key:
                    key = key[1:]
                    self.estados_aceitacao.insert(len(self.estados_aceitacao), key)

                self.dict_af[key] = []
                for columns in range(len(af_matrix[0])):
                    if columns is not 0 and af_matrix[0][columns].get() is not "":
                        if af_matrix[rows][columns].get() != "":
                            self.dict_af[key].insert(columns, [af_matrix[0][columns].get(), af_matrix[rows][columns].get()])
        print(self.dict_af)

    # Pega o af em forma de texto e transforma na forma
    # {'NaoTerminal': 'terminal', 'naoterminal', 'terminal', ....}
    def set_dict_gr(self, gr_text):
        self.clean_dict_gr()
        gr = gr_text.get("1.0", END).splitlines()
        for lines in gr:
            self.dict_gr[lines[0]] = []
            contador = 3
            index = 0
            while contador < len(lines):
                if lines[contador] is "|":
                    contador += 1
                else:
                    self.dict_gr[lines[0]].insert(index, lines[contador])
                    contador += 1
                    index += 1
        print(self.dict_gr)

    def set_dict_er(self, gr_text):
        return self.dict_er

    def set_sentence(self, sentence):
        self.sentence = sentence.get("1.0", END)

    def get_dict_af(self):
        return self.dict_af

    def get_dict_gr(self):
        return self.dict_gr

    def get_estados_aceitacao(self):
        return self.estados_aceitacao

    def clean_estados_aceitacao(self):
        self.estados_aceitacao = []

    def clean_dict_af(self):
        self.dict_af = {}

    def clean_dict_gr(self):
        self.dict_gr = {}

    # def set_dict_gr(self, gr_text):
    #     gr = gr_text.get("1.0", END).splitlines()
    #     for lines in gr:
    #         self.dict_gr[lines[0]] = []
    #         contador = 3
    #         index = 0
    #         while contador < len(lines):
    #             if lines[contador] is "|":
    #                 contador += 1
    #             else:
    #                 if contador+1 <= len(lines)-1:
    #                     if lines[contador+1] is not "|":
    #                         self.dict_gr[lines[0]].insert(index, [lines[contador], lines[contador + 1]])
    #                         contador += 2
    #                         index += 1
    #                     else:
    #                         self.dict_gr[lines[0]].insert(index, [lines[contador]])
    #                         contador += 1
    #                         index += 1
    #                 else:
    #                     self.dict_gr[lines[0]].insert(index, [lines[contador]])
    #                     contador += 1
    #                     index += 1
    #     print(self.dict_gr)
    #     return 0

