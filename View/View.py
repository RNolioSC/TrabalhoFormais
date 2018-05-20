from tkinter import messagebox
from tkinter import *
from Control.Controller import *

class View:
    # Controle
    operacao = None
    controller = None

    # Armazenamento
    result = None
    arg1 = None
    arg2 = None
    op = None
    output_gr = None
    output_af = None
    aceitacao_reutilizavel = None

    # Constantes
    CONST_ROW = 10
    CONST_COLUMN = 7

    def __init__(self, controller):
        # Cria frame raiz
        self.root = Tk()
        self.root.title('T1 de Formais')
        self.root.geometry('{}x{}'.format(800, 500))

        # Create frames principais
        self.frame_top = Frame(self.root, width=800, height=30, pady=3)
        self.frame_esq = Frame(self.root, width=266, height=50, pady=3)
        self.frame_centro = Frame(self.root, width=266, height=50, pady=3)
        self.frame_dir = Frame(self.root, width=267, height=50, pady=3, padx=10)

        # Layout dos containers principais
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Colocar frames na tela
        self.frame_top.grid(row=0, sticky="ew")
        self.frame_esq.grid(row=1, sticky="nsw")
        self.frame_centro.grid(row=1, sticky="ns")
        self.frame_dir.grid(row=1, sticky="nse")

        # Criar widgets frames da esquerda
        self.frame_esq.grid_rowconfigure(0, weight=1)
        self.frame_esq.grid_columnconfigure(1, weight=1)

        self.top_frame_esq = Frame(self.frame_esq, width=266, height=50)
        self.btn_frame_esq = Frame(self.frame_esq, width=266, height=70)

        self.top_frame_esq.grid(row=0, column=0, sticky="nsew")
        self.btn_frame_esq.grid(row=1, column=0, sticky="nsew")

        self.create_widgets_left_frame()

        # Criar widgets frames do centro
        self.frame_centro.grid_rowconfigure(1, weight=1)
        self.frame_centro.grid_columnconfigure(0, weight=1)

        self.top_frame_centro = Frame(self.frame_centro, width=266, height=230)
        self.btn_frame_centro = Frame(self.frame_centro, width=266, height=50)

        self.top_frame_centro.grid(row=0, column=0, sticky="nsew")
        self.btn_frame_centro.grid(row=1, column=0, sticky="nsew")

        self.top_frame_centro.grid_rowconfigure(1, weight=1)
        self.top_frame_centro.grid_columnconfigure(0, weight=1)

        self.btn_frame_centro.grid_rowconfigure(1, weight=1)
        self.btn_frame_centro.grid_columnconfigure(1, weight=1)

        self.input = Text(self.top_frame_centro, bg='white', width=30, height=15)
        self.input_2 = Text(self.btn_frame_centro, bg='white', width=30, height=13)

        self.input.grid(row=0, column=0, sticky="ew")
        self.input_2.grid(row=0, column=0, sticky="ew")

        # Criar widgets frames da direita
        self.frame_dir.grid_rowconfigure(1, weight=1)
        self.frame_dir.grid_columnconfigure(0, weight=1)

        self.lista_operacoes = Listbox(self.frame_dir, width=40, height=14)
        self.lista_operacoes.grid(row=11, column=0, columnspan=12, rowspan=12, sticky='wse')

        # Criar widgets frame do topo
        self.frame_top.grid_rowconfigure(1, weight=1)
        self.frame_top.grid_columnconfigure(0, weight=1)

        opcoes = Label(self.frame_top, text="Escolha uma das opções abaixo:")
        input = Label(self.frame_top, text="Input:")
        output = Label(self.frame_top, text="Output:")

        opcoes.grid(row=0, column=0, sticky="w")
        input.grid(row=0, column=0)
        output.grid(row=0, column=1, sticky="e")

        self.controller = controller

        self.root.mainloop()

    def create_widgets_left_frame(self):
        self.top_frame_esq.grid_rowconfigure(15, weight=1)
        self.top_frame_esq.grid_columnconfigure(1, weight=1)

        conversoes = LabelFrame(self.top_frame_esq, text='2 - 3 Conversões')
        erAF = Radiobutton(conversoes, text="ER para AF", variable="Operacao", value=1, tristatevalue=0, command=lambda: self.set_operacao(1, 1))
        grAF = Radiobutton(conversoes, text="GR para AF", variable="Operacao", value=2, tristatevalue=0, command=lambda: self.set_operacao(2, 0))
        afGR = Radiobutton(conversoes, text="AF para GR", variable="Operacao", value=3, tristatevalue=0, command=lambda: self.set_operacao(3, 0))

        af = LabelFrame(self.top_frame_esq, text='4 AFND/AFM')
        afd = Radiobutton(af, text="Determinização", variable="Operacao", value=4, tristatevalue=0, command=lambda: self.set_operacao(4, 0))
        afm = Radiobutton(af, text="Minimização", variable="Operacao", value=5, tristatevalue=0, command=lambda: self.set_operacao(5, 0))

        oper = LabelFrame(self.top_frame_esq, text='5 Obter AF')
        inter = Radiobutton(oper, text="Intersecção", variable="Operacao", value=6, tristatevalue=0, command=lambda: self.set_operacao(6, 2))
        dif = Radiobutton(oper, text="Diferença", variable="Operacao", value=7, tristatevalue=0, command=lambda: self.set_operacao(7, 2))
        rev = Radiobutton(oper, text="Reverso", variable="Operacao", value=8, tristatevalue=0, command=lambda: self.set_operacao(8, 3))

        operGR = LabelFrame(self.top_frame_esq, text='6 Obter GR')
        uniao = Radiobutton(operGR, text="União", variable="Operacao", value=9, tristatevalue=0, command=lambda: self.set_operacao(9, 2))
        concat = Radiobutton(operGR, text="Concatenação", variable="Operacao", value=10, tristatevalue=0, command=lambda: self.set_operacao(10, 2))
        fech = Radiobutton(operGR, text="Fechamento", variable="Operacao", value=11, tristatevalue=0, command=lambda: self.set_operacao(11, 0))

        sentence = LabelFrame(self.top_frame_esq, text='7 Sentenças')
        recog = Radiobutton(sentence, text="Reconhecimento", variable="Operacao", value=12, tristatevalue=0, command=lambda: self.set_operacao(12, 4))
        enum = Radiobutton(sentence, text="Enumeração", variable="Operacao", value=13, tristatevalue=0, command=lambda: self.set_operacao(13, 5))

        btn_continue = Button(self.btn_frame_esq, text="Continuar", command=self.exibir_resultados)
        btn_salvar = Button(self.btn_frame_esq, text="Salvar Expressão", command=self.salvar_expressao)
        btn_carregar = Button(self.btn_frame_esq, text="Carregar Expressão", command=self.carregar_expressao)

        conversoes.grid(row=0, column=0, columnspan=3, sticky='we')
        erAF.grid(row=1, column=0, sticky='w')
        grAF.grid(row=2, column=0, sticky='w')
        afGR.grid(row=3, column=0, sticky='w')

        af.grid(row=4, column=0, columnspan=3, sticky='wne')
        afd.grid(row=5, column=0, sticky='w')
        afm.grid(row=6, column=0, sticky='w')

        oper.grid(row=7, column=0, columnspan=3, sticky='we')
        inter.grid(row=8, column=0, sticky='w')
        dif.grid(row=9, column=0, sticky='w')
        rev.grid(row=10, column=0, sticky='w')

        operGR.grid(row=11, column=0, columnspan=3, sticky='we')
        uniao.grid(row=12, column=0, sticky='w')
        concat.grid(row=13, column=0, sticky='w')
        fech.grid(row=14, column=0, sticky='w')

        sentence.grid(row=15, column=0, columnspan=3, sticky='wesn')
        recog.grid(row=16, column=0, sticky='w')
        enum.grid(row=17, column=0, sticky='w')

        btn_continue.grid(row=0, column=0)
        btn_salvar.grid(row=0, column=1)
        btn_carregar.grid(row=0, column=2)

    def reutilizar_af(self):
        try:
            self.result = self.controller.af_to_ger_reutilizado(self.result)
            self.input.delete("1.0", END)

            # Estado inicial
            tmp = self.controller.get_estado_inicial() + "->"
            for list in range(len(self.result[self.controller.get_estado_inicial()])):
                tmp += self.result[self.controller.get_estado_inicial()][list]
                print(tmp)
                if list + 1 < len(self.result[self.controller.get_estado_inicial()]):
                    if not self.result[self.controller.get_estado_inicial()][list + 1].istitle():
                        tmp += "|"
            self.input.insert(END, tmp + '\n')

            for estados_finais in self.aceitacao_reutilizavel:
                indices = [i for i, elem in enumerate(self.result[self.controller.get_estado_inicial()]) if estados_finais in elem]
                for index in indices:
                    tmp += '|' + self.result[self.controller.get_estado_inicial()][index - 1]

            for keys in self.result:
                if keys != self.controller.get_estado_inicial():
                    tmp = keys + "->"
                    for list in range(len(self.result[keys])):
                        tmp += self.result[keys][list]
                        if list + 1 < len(self.result[keys]):
                            if not self.result[keys][list + 1].istitle():
                                tmp += "|"

                    for estados_finais in self.aceitacao_reutilizavel:
                        indices = [i for i, elem in enumerate(self.result[keys]) if estados_finais in elem]
                        for index in indices:
                            tmp += '|' + self.result[keys][index - 1]
                    self.input.insert(END, tmp + '\n')

            self.input.delete("end-1c", END)
        except IndexError:
            pass

    # Salvar uma expressão em disco
    def salvar_expressao(self):
        self.controller.salvar_expressao(self.input)

    # Carregar uma expressão em disco
    def carregar_expressao(self):
        self.input.delete("1.0", END)
        self.input.insert(INSERT, self.controller.carregar_expressao())
        self.input.delete("end-1c", END)

    # Armazena a operação selecionada
    def set_operacao(self, op, op_dict):
        self.operacao = op
        self.op = op_dict

    # Executar a operacao selecionada e exibe os resultados
    def exibir_resultados(self):
        self.controller.clean_all()
        self.controller.set_dict(self.input, self.input_2, self.op)
        self.result = self.controller.exec(self.operacao) # Faz a verificacao do tamanho e selecionar as saídas corretas

        lista_operacao = self.controller.get_lista_operacoes()
        self.lista_operacoes.delete(0, END)
        for keys in lista_operacao.keys():
            self.lista_operacoes.insert(END, keys)
        self.lista_operacoes.bind("<Double-1>", self.exibir)

        if self.operacao == 3:
            self.formata_resultado_gr()
        elif self.operacao == 12:
            msg = "A sentença pertence a linguagem" if self.result else "A sentença não pertence a linguagem"
            messagebox.showinfo("Resultado do reconhecimento", msg)
        elif self.operacao == 13:
            self.clear_matriz()
            self.criar_output_gr()
            for result in self.result:
                self.output_gr.insert(END, result + '\n')
                self.output_gr.grid(row=0, column=2, columnspan=3, sticky="ew")
        else:
            self.formata_resultado_af()

    # Criar tabela pra exibir AF
    def criar_tabela_af(self):
        rows = self.CONST_ROW
        columns = self.CONST_COLUMN

        self.output_af = [[None for y in range(columns)] for x in range(rows)]

        for row in range(rows):
            for column in range(columns):
                entry = Entry(self.frame_dir, bg='white', width=5)
                entry.grid(row=row, column=column, padx=1, pady=1)
                self.output_af[row][column] = entry

        for column in range(columns):
            self.frame_dir.grid_columnconfigure(column, weight=1)

        self.output_af[0][0].insert(0, "XXXX")
        self.output_af[0][0].config(state='disabled')

        Button(self.frame_dir, text="Reutilizar", command=self.reutilizar_af).grid(row=10, column=2, columnspan=3, pady=2)

    def formata_resultado_af(self):
        self.clear_text()
        self.criar_tabela_af()

        keys = list(self.result.keys()).copy()
        estados_aceitacao = self.controller.get_estados_aceitacao()
        init_key = self.controller.get_estado_inicial()
        alfabeto = []

        # Seta alfabeto
        for key in keys:
            for columns in range(len(self.result[key])):
                if self.result[key][columns][0] not in alfabeto:
                    alfabeto.insert(len(alfabeto), self.result[key][columns][0])

        # Seta alfabeto na GUI
        for char in range(len(alfabeto)):
            self.output_af[0][char + 1].insert(0, alfabeto[char])

        # Seta estado inicial como primeiro elemento
        tmp_key = '*' + init_key if init_key in estados_aceitacao else init_key
        self.output_af[1][0].insert(0, tmp_key)

        for transicoes in range(len(self.result[init_key])):
            resultado = self.result[init_key][transicoes][1] if len(self.output_af[1][alfabeto.index(self.result[init_key][transicoes][0]) + 1].get()) == 0 else self.result[init_key][transicoes][1]+"."
            self.output_af[1][alfabeto.index(self.result[init_key][transicoes][0]) + 1].insert(0, resultado)

        keys.remove(init_key)

        # Seta restante da tabela
        for rows in range(len(keys)):
            key = '*' + keys[rows] if keys[rows] in estados_aceitacao else keys[rows]

            self.output_af[rows+2][0].insert(0, key)
            for columns in range(len(self.result[keys[rows]])):
                resultado = self.result[keys[rows]][columns][1] if len(self.output_af[rows+2][alfabeto.index(self.result[keys[rows]][columns][0])+1].get()) == 0 else self.result[keys[rows]][columns][1]+"."
                self.output_af[rows+2][alfabeto.index(self.result[keys[rows]][columns][0]) + 1].insert(0, resultado)

    def formata_resultado_gr(self):
        self.clear_matriz()
        self.criar_output_gr()

        estados_aceitacao = self.controller.get_estados_aceitacao()
        estado_inicial = self.controller.get_estado_inicial()

        tmp = estado_inicial + "->"
        self.formata_gr(tmp, estado_inicial, estados_aceitacao)

        for keys in self.result:
            if keys != estado_inicial:
                tmp = keys + "->"
                self.formata_gr(tmp, keys, estados_aceitacao)

        self.output_gr.delete("end-1c", END)

    # Só para evitar código redundante
    def formata_gr(self, tmp, keys, estados_aceitacao):
        for list in range(len(self.result[keys])):
            tmp += self.result[keys][list]
            if list + 1 < len(self.result[keys]):
                if not self.result[keys][list + 1].istitle():
                    tmp += "|"

        for estados_finais in estados_aceitacao:
            indices = [i for i, elem in enumerate(self.result[keys]) if estados_finais in elem]
            for index in indices:
                tmp += '|' + self.result[keys][index - 1]
        self.output_gr.insert(END, tmp + '\n')
        self.output_gr.grid(row=0, column=2, columnspan=3, sticky="ew")


    def clear_matriz(self):
        if not self.output_af:
            return

        for row in range(self.CONST_ROW):
            for column in range(self.CONST_COLUMN):
                self.output_af[row][column].destroy()

    def clear_text(self):
        try:
            self.output_gr.destroy()
        except AttributeError:
            pass

    def criar_output_gr(self):
        self.output_gr = Text(self.frame_dir, bg='white', width=30, height=12)
        self.output_gr.delete("1.0", END)
        Button(self.frame_dir, text="Reutilizar", command=self.reutilizar_af).grid(row=10, column=2, columnspan=3, pady=2)

    def exibir(self, event):
        select = self.lista_operacoes.curselection()
        self.result = self.controller.get_lista_operacoes()[self.lista_operacoes.get(select[0])][0]
        self.aceitacao_reutilizavel = self.controller.get_lista_operacoes()[self.lista_operacoes.get(select[0])][1]
        self.formata_resultado_af()
