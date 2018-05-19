from Control.AFGRoperations import *
from Control.AFoperations import *
from Control.SentenceOperations import *
from Control.GRoperations import *
from Control.ERoperations import *
from View.View import *


class Controller:

    def __init__(self):
        self.view = View(self)
        self.dict_af = {}
        self.dict_gr = {}
        self.dict_gr_op = {}
        self.er_expression = {}
        self.estado_inicial = None
        self.estados_aceitacao = []
        self.sentence = ""
        self.sentence_size = 0

    def exec(self, operacao):
        if operacao == 1:
            self.er_to_af()
        elif operacao == 2:
            self.gr_to_af()
        elif operacao == 3:
            self.af_to_gr()
        elif operacao == 4:
            self.determinizacao()
        elif operacao == 5:
            self.minimizacao()
        elif operacao == 6:
            self.intersecao()
        elif operacao == 7:
            self.diferenca()
        elif operacao == 8:
            self.reverso()
        elif operacao == 9:
            self.uniao()
        elif operacao == 10:
            self.concatenacao()
        elif operacao == 11:
            self.fechamento()
        elif operacao == 12:
            self.accept_sentence(self.dict_af[self.estado_inicial], list(self.sentence)[:-1], self.estado_inicial, self.estados_aceitacao, self.dict_af)
        elif operacao == 13:
            self.enum_sentences(self.sentence_size, self.estado_inicial, self.estados_aceitacao, self.dict_af)

    # Salvar/Carregar arquivo
    def salvar_expressao(self, expressao):
        with open('Expressao.txt', 'w') as file:
            file.write(expressao.get("1.0", END))

    def carregar_expressao(self):
        with open('Expressao.txt', 'r') as file:
            return file.read()
    # -------------------------------

    # Modulo AF to GR vice-versa
    def af_to_gr(self):
        return AFGR.af_to_gr(self.dict_af)

    def gr_to_af(self):
        return AFGR.gr_to_af(self.dict_gr, self.estados_aceitacao)
    # ---------------------------

    # Módulo determinização e minimização
    def minimizacao(self):
        return AFoperations.minimizacao(self.dict_af, self.estados_aceitacao, self.estado_inicial)

    def determinizacao(self):
        pass
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

    def uniao(self, af1, af2):
        return AFoperations.uniao_afnds(af1, af2)

    def concatenacao(self, af1, af2, ei1, ei2, ef1, ef2):
        return GRoperations.concatenacao(af1, af2, ei1, ei2, ef1, ef2)
    # -----------------------

    # Modulo ER->AF
    def er_to_af(self):
        self.dict_af, self.estados_aceitacao, self.estado_inicial = ERoperations.er_to_af(self.er_expression)
        return self.dict_af
    # -------------

    # Modulo de novos AF
    def intersecao(self, af1, af2):
        return AFoperations.intersecao(af1, af2)

    def diferenca(self):
        pass

    def reverso(self):
        pass
    # --------------------

    # Armazenar GR/AF/ER

    # Op = 0(GR), 1(ER), 2( 2 GRs), 3 (Precisa descobrir)
    def set_dict(self, input1, input2, op):
        if op == 0:
            self.set_dict_gr(input1, self.dict_gr)
        elif op == 1:
            self.set_dict_er(input1)
        elif op == 2:
            self.set_dict_gr(input1, self.dict_gr)
            self.set_dict_gr(input2, self.dict_gr_op)
        elif op == 3:
            try:
                input1.get("1.0", END).index("->")
                self.set_dict_gr(input1, self.dict_gr)
            except ValueError:
                self.set_dict_er(input1)

    # Pega o af em forma de texto e transforma na forma
    # {'NaoTerminal': 'terminal', 'naoterminal', 'terminal', ....}
    def set_dict_gr(self, gr_text, dict):
        self.clean_all()
        gr = gr_text.get("1.0", END).splitlines()
        self.set_estado_inicial(gr[0][0])

        for lines in gr:
            dict[lines[0]] = []
            contador = 3
            while contador < len(lines):
                if lines[contador] is "|":
                    contador += 1
                else:
                    dict[lines[0]].append(lines[contador])
                    contador += 1
        print(dict)

    # Pega o af em forma de matriz e transforma na forma
    # {'EstadoAtual': ['simbolo','ProxEstado'],...}
    def set_dict_af(self, af_matrix):
        self.clean_all()
        key = af_matrix[1][0].get()  # Estado inicial
        self.set_estado_inicial(key[1:] if '*' in key else key)

        for rows in range(len(af_matrix)):
            if af_matrix[rows][0].get() == "":
                break

            if rows is not 0:
                key = af_matrix[rows][0].get()

                if '*' in key:
                    self.estados_aceitacao.append(key[1:])

                self.dict_af[key] = []
                for columns in range(len(af_matrix[0])):
                    if columns is not 0 and af_matrix[0][columns].get() is not "":
                        if af_matrix[rows][columns].get() != "":
                            self.dict_af[key].insert(columns, [af_matrix[0][columns].get(), af_matrix[rows][columns].get()])

        print(self.dict_af)

    # Armazena a ER completa
    def set_dict_er(self, gr_text):
        self.er_expression = gr_text.get("1.0", END)

    # ------------------------------------

    # Limpeza de variavel
    def clean_all(self):
        self.dict_af = {}
        self.dict_gr = {}
        self.er_expression = {}
        self.estados_aceitacao = []
    # --------

    # Getters e Setters

    def set_estado_inicial(self, estado_inicial):
        self.estado_inicial = estado_inicial

    # -----------------
