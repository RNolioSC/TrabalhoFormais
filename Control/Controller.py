from Control.AFGRoperations import *
from Control.AFoperations import *
from Control.SentenceOperations import *
from Control.GRoperations import *
from Control.ERoperations import *
from View.View import *

# TODO ER_TO_AF tem quer gerar numeros diferentes

class Controller:
    def __init__(self):
        self.dict_af = {}
        self.dict_af_op = {}
        self.dict_gr = {}
        self.dict_gr_op = {}
        self.er_expression = {}

        self.estado_inicial = None
        self.estado_inicial_op = None
        self.estados_aceitacao = []
        self.estados_aceitacao_op = []

        self.sentence = ""
        self.sentence_size = 0

        self.lista_operacoes = {}

        self.view = View(self)

    # Define a operacao a ser executada
    def exec(self, operacao):
        if operacao == 1:
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.er_to_af(self.er_expression, 0)
            return self.dict_af
        elif operacao == 2:
            return self.gr_to_af(self.dict_gr, self.estados_aceitacao)
        elif operacao == 3:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = [self.dict_af, self.estados_aceitacao]
            return self.af_to_gr()
        elif operacao == 4:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = [self.dict_af, self.estados_aceitacao]
            af = self.determinizacao()
            self.explicitar_estados_finais(self.dict_af)
            return af
        elif operacao == 5:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = [self.dict_af, self.estados_aceitacao]

            if self.eh_afnd(self.dict_af):
                self.dict_af = self.determinizacao()
                self.lista_operacoes["Determinização do AFND"] = [self.dict_af, self.estados_aceitacao]
                self.explicitar_estados_finais(self.dict_af)

            afm = self.minimizacao()
            self.explicitar_estados_finais(afm)
            return afm
        elif operacao == 6:
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.er_to_af(self.er_expression, 0)
            self.dict_af_op, self.estados_aceitacao_op, self.estado_inicial_op = self.er_to_af(self.er_expression_op, 5)
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.intersecao(self.dict_af, self.dict_af_op, self.estado_inicial, self.estado_inicial_op, self.estados_aceitacao, self.estados_aceitacao_op)
            return self.dict_af
        elif operacao == 7:
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.er_to_af(self.er_expression, 0)
            self.dict_af_op, self.estados_aceitacao_op, self.estado_inicial_op = self.er_to_af(self.er_expression_op, 5)
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.diferenca(self.dict_af, self.dict_af_op,  self.estado_inicial, self.estado_inicial_op, self.estados_aceitacao, self.estados_aceitacao_op)
            return self.dict_af
        elif operacao == 8:
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.er_to_af(self.er_expression, 0)
            self.lista_operacoes["ER para AF"] = [self.dict_af, self.estados_aceitacao]
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.reverso(self.dict_af)
            return self.dict_af
        elif operacao == 9:
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.er_to_af(self.er_expression, 0)
            self.dict_af_op, self.estados_aceitacao_op, self.estado_inicial_op = self.er_to_af(self.er_expression_op, 5)
            self.dict_af, self.estados_aceitacao, self.estado_inicial = self.uniao(self.dict_af, self.dict_af_op, self.estado_inicial, self.estado_inicial_op, self.estados_aceitacao, self.estados_aceitacao_op)
            return self.dict_af
        elif operacao == 10:
            return self.concatenacao()
        elif operacao == 11:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = [self.dict_af, self.estados_aceitacao]
            return self.fechamento()
        elif operacao == 12:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = [self.dict_af, self.estados_aceitacao]
            if self.eh_afnd(self.dict_af):
                self.dict_af = self.determinizacao()
                self.lista_operacoes["Determinização do AFND"] = [self.dict_af, self.estados_aceitacao]
                self.explicitar_estados_finais(self.dict_af)
            return self.accept_sentence(self.dict_af[self.estado_inicial], list(self.sentence)[:-1], self.estado_inicial, self.estados_aceitacao, self.dict_af)
        elif operacao == 13:
            self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
            self.lista_operacoes["GR para AF"] = self.dict_af
            if self.eh_afnd(self.dict_af):
                self.dict_af = self.determinizacao()
                self.explicitar_estados_finais(self.dict_af)
                self.lista_operacoes["Determinização do AFND"] = [self.dict_af, self.estados_aceitacao]
            return self.enum_sentences(self.sentence_size, self.estado_inicial, self.estados_aceitacao, self.dict_af)

    # Gambiarra
    def explicitar_estados_finais(self, dict_af):
        ea = self.estados_aceitacao.copy()
        self.estados_aceitacao = []
        for ef in ea:
            for key in dict_af:
                try:
                    key.index(ef)
                    self.estados_aceitacao.append(key)
                except ValueError:
                    pass
    # ------------

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

    def gr_to_af(self, dict_gr, estados_aceitacao):
        return AFGR.gr_to_af(dict_gr, estados_aceitacao)

    def af_to_ger_reutilizado(self, result):
        result = AFGR.af_to_gr(result)
        return result
    # ---------------------------

    # Módulo determinização e minimização
    def minimizacao(self):
        return AFoperations.minimizacao(self.dict_af, self.estados_aceitacao, self.estado_inicial)

    def determinizacao(self):
        return AFoperations.afnd_to_afd(self.dict_af, self.estados_aceitacao)
    # -----------------------------------

    # Modulo reconhecimento e enumeracao
    def enum_sentences(self, size, estado_inicial, estados_aceitacao, dict_af):
        return SentenceOperations.enum_sentences(size, estado_inicial, estados_aceitacao, dict_af)

    def accept_sentence(self, producoes, sentence, cur_key, estados_aceitacao, dict_af):
        return SentenceOperations.accept_sentence(producoes, sentence, cur_key, estados_aceitacao, dict_af)
    # --------------------------------

    # Modulo operacoes com GR
    def fechamento(self):
        self.estado_inicial, self.estados_aceitacao = GRoperations.fechamento(self.dict_af, self.estado_inicial, self.estados_aceitacao)
        return self.dict_af

    def uniao(self, af1, af2, ei1, ei2, ef1, ef2):
        return GRoperations.uniao(af1, af2, ei1, ei2, ef1, ef2)

    def concatenacao(self):
        self.dict_af = self.gr_to_af(self.dict_gr, self.estados_aceitacao)
        self.dict_af_op = self.gr_to_af(self.dict_gr_op, self.estados_aceitacao_op)
        self.estado_inicial, self.estados_aceitacao = GRoperations.concatenacao(self.dict_af, self.dict_af_op, self.estado_inicial, self.estado_inicial_op, self.estados_aceitacao, self.estados_aceitacao_op)
        return self.dict_af
    # -----------------------

    # Modulo ER->AF
    def er_to_af(self, er_expression, number_states):
        dict_af, estados_aceitacao, estado_inicial = ERoperations.er_to_af(er_expression, number_states)
        return dict_af, estados_aceitacao, estado_inicial
    # -------------

    # Modulo de novos AF
    def intersecao(self, af1, af2, ei1, ei2, ef1, ef2):
        return GRoperations.intersecao(af1, af2, ei1, ei2, ef1, ef2)

    def diferenca(self, af1, af2, ei1, ei2, ef1, ef2):
        return GRoperations.diferenca(af1, af2, ei1, ei2, ef1, ef2)

    def reverso(self, afd):
        return GRoperations.reverso(afd, self.estados_aceitacao, self.estado_inicial)
    # --------------------

    # Checagens
    def eh_afnd(self, af):
        elementos = []
        for keys in af.keys():
            for list in af[keys]:
                elementos.append(list[0])
            if len(elementos) != len(set(elementos)):
                return True
            elementos = []
        return False
    # ----------

    # Armazenar GR/AF/ER

    # TODO Reduzir código
    # Op = 0(GR), 1(ER), 2(2 GRs), 3 (Precisa descobrir), 4 (Reconhecimento), 5 (Enumeracao)
    def set_dict(self, input1, input2, op):
        self.clean_all()
        if op == 0:
            self.dict_gr = self.set_dict_gr(input1, 1)
        elif op == 1:
            self.set_dict_er(input1, 1)
        elif op == 2:
            self.dict_gr = self.set_dict_gr(input1, 1)
            self.dict_gr_op = self.set_dict_gr(input2, 0)
        elif op == 3:
            try:
                input1.get("1.0", END).index("->")
                self.dict_gr = self.set_dict_gr(input1, 1)
                self.dict_gr_op = self.set_dict_gr(input2, 0)
            except ValueError:
                self.set_dict_er(input1, 1)
                self.set_dict_er(input2, 0)
        elif op == 4:
            self.dict_gr = self.set_dict_gr(input1, 1)
            self.set_sentence(input2)
        elif op == 5:
            self.dict_gr = self.set_dict_gr(input1, 1)
            self.set_sentence_size(input2)

    # Pega o af em forma de texto e transforma na forma
    # {'NaoTerminal': 'terminal', 'naoterminal', 'terminal', ....}
    def set_dict_gr(self, gr_text, op):
        gr = gr_text.get("1.0", END).splitlines()
        gramatica = {}
        existe_epsilon = False
        ei_lado_direito = False

        for lines in gr:
            contador = 0
            tmp_p = ''

            while lines[contador] != '-':
                tmp_p += lines[contador]
                contador += 1

            if gr.index(lines) == 0:
                self.set_estado_inicial(tmp_p, op)
            gramatica[tmp_p] = []

            contador += 1
            while contador < len(lines):
                if lines[contador] != ' ' and lines[contador] != '>':
                    if lines[contador] is "|":
                        contador += 1
                    else:
                        if lines[contador] == '&':
                            existe_epsilon = True
                        if lines[contador] == self.get_estado_inicial():
                            ei_lado_direito = True
                        if not (lines[contador].istitle()):
                            if lines[contador - 1].islower():
                                raise SyntaxError("Não é uma LR")
                            try:
                                int(lines[contador - 1])
                                raise SyntaxError("Não é uma LR")
                            except ValueError:
                                pass
                        tmp = ''
                        if lines[contador].islower() or lines[contador] == '&':
                            gramatica[tmp_p].append(lines[contador])
                            contador += 1
                        else:
                            try:
                                int(lines[contador])
                                gramatica[tmp_p].append(lines[contador])
                                contador += 1
                            except ValueError:
                                while contador < len(lines) and lines[contador] != '|':
                                    if not(lines[contador].islower()):
                                        tmp += lines[contador]
                                    contador += 1
                                gramatica[tmp_p].append(tmp)
                else:
                    contador += 1

        if existe_epsilon and ei_lado_direito:
            raise SyntaxError("Não é uma LR")

        print(gramatica)
        return gramatica

    # Armazena a ER completa
    def set_dict_er(self, gr_text, op):
        if op:
            self.er_expression = gr_text.get("1.0", END)
        else:
            self.er_expression_op = gr_text.get("1.0", END)

    def set_estado_inicial(self, estado_inicial, op):
        if op:
            self.estado_inicial = estado_inicial
        else:
            self.estado_inicial_op = estado_inicial

    def set_sentence(self, sentence):
        self.sentence = sentence.get("1.0", END)

    def set_sentence_size(self, size):
        self.sentence_size = int(size.get("1.0", END))

    def get_estados_aceitacao(self):
        return self.estados_aceitacao

    def get_estado_inicial(self):
        return self.estado_inicial

    def get_lista_operacoes(self):
        return self.lista_operacoes
    # ------------------------------------

    # Limpeza de variavel
    def clean_all(self):
        self.dict_af = {}
        self.dict_gr = {}
        self.er_expression = {}
        self.estados_aceitacao = []
        self.lista_operacoes = {}
    # --------