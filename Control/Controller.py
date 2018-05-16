from Control.AFGRoperations import *
from Control.AFoperations import *
from Control.SentenceOperations import *
from Control.GRoperations import *
from Control.ERoperations import *
from View.View import *

#TODO
# - Corrigir bug que suja a GR se for feito uma operacao qualquer (?) antes dela
# - Quando editar uma GR e retirar um estado dos estados final, (corrigir) verificar se o que era final antes volta a ser nao final
# - Explicitar caso de erro e definir as transicoes do estado final como estado de erro
# - Trocar como faz o reconhecimento de estados finais pra GR
# - Nem sempre o estado de erro precisa aparecer, corrigir isso
# - Generalizar um monte de coisas

class Controller:

    # Armazenamento
    dict_af = {}
    dict_gr = {}
    er_expression = {}
    dict_gr_op = {}
    estados_aceitacao = []
    sentence = None
    sentence_size = None
    estado_inicial = None

    # View
    view = None

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
    def enum_sentences(self, size, estado_inicial, estados_aceitacao, dict_af):
        return SentenceOperations.enum_sentences(size, estado_inicial, estados_aceitacao, dict_af)

    def accept_sentence(self, producoes, sentence, cur_key, estados_aceitacao, dict_af):
        return SentenceOperations.accept_sentence(producoes, sentence, cur_key, estados_aceitacao, dict_af)
    # --------------------------------

    # Modulo operacoes com GR
    def fechamento(self):
        self.dict_af = self.gr_to_af()
        self.estado_inicial, self.estados_aceitacao = GRoperations.fechamento(self.dict_af, self.estado_inicial, self.estados_aceitacao)
        return self.dict_af

    # -----------------------

    # Modulo ER->AF
    def er_to_af(self):
        self.dict_af, self.estados_aceitacao, self.estado_inicial = ERoperations.er_to_af(self.er_expression)
        return self.dict_af
    # -------------

    # Salvar/Carregar arquivo

    def salvar_expressao(self, expressao):
        with open('Expressao.txt', 'w') as file:
            file.write(expressao.get("1.0", END))

    def carregar_expressao(self):
        with open('Expressao.txt', 'r') as file:
           return file.read()

    # -------------------------------

    def exec(self, operacao):
        if operacao == 1:
            return self.er_to_af()
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
            return self.fechamento()
        elif operacao == 8:
            return self.accept_sentence(self.dict_af[self.estado_inicial], list(self.sentence)[:-1], self.estado_inicial, self.estados_aceitacao, self.dict_af)
        elif operacao == 9:
            return self.GRoperations.uniao(af1, af2, ei1, ei2, ef1, ef2)
        elif operacao == 10:
            return self.GRoperations.concatenacao(af1, af2, ei1, ei2, ef1, ef2)
        else:
            return self.enum_sentences(self.sentence_size, self.estado_inicial, self.estados_aceitacao, self.dict_af)

    # Pega o af em forma de matriz e transforma na forma
    # {'EstadoAtual': ['simbolo','ProxEstado'],...}
    def set_dict_af(self, af_matrix):
        self.clean_dict_af()

        # Estado inicial
        key = af_matrix[1][0].get()
        if '*' in key:
            self.set_estado_inicial(key[1:])
        else:
            self.set_estado_inicial(key)

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
        self.set_estado_inicial(gr[0][0])
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
        self.er_expression = gr_text.get("1.0", END)

    def set_sentence(self, sentence):
        self.sentence = sentence.get("1.0", END)

    def get_estado_inicial(self):
        return self.estado_inicial

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

    def set_sentence_size(self, size):
        self.sentence_size = int(size.get("1.0",END))

    def set_estado_inicial(self, estado_inicial):
        self.estado_inicial = estado_inicial

    # TODO generalizar o set_dict_gr e apagar isso
    def set_dict_gr_op(self, gr_text):
        self.dict_gr_op = {}
        gr = gr_text.get("1.0", END).splitlines()
        self.set_estado_inicial(gr[0][0])
        for lines in gr:
            self.dict_gr_op[lines[0]] = []
            contador = 3
            index = 0
            while contador < len(lines):
                if lines[contador] is "|":
                    contador += 1
                else:
                    self.dict_gr_op[lines[0]].insert(index, lines[contador])
                    contador += 1
                    index += 1
        print(self.dict_gr_op)