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

    # Constantes
    CONST_ROW = 10
    CONST_COLUMN = 5

    def __init__(self, controller):
        # Cria frame raiz
        self.root = Tk()
        self.root.title('T1 de Formais')
        self.root.geometry('{}x{}'.format(800, 500))

        # Create frames principais
        self.frame_top = Frame(self.root, width=800, height=30, pady=3)
        self.frame_esq = Frame(self.root, width=266, height=50, pady=3)
        self.frame_centro = Frame(self.root, width=266, height=50, pady=3)
        self.frame_dir = Frame(self.root, width=267, height=50, pady=3)

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
        erAF = Radiobutton(conversoes, text="ER para AF", variable="Operacao", value=1, tristatevalue=0, command=lambda: self.set_operacao(1))
        grAF = Radiobutton(conversoes, text="GR para AF", variable="Operacao", value=2, tristatevalue=0, command=lambda: self.set_operacao(2))
        afGR = Radiobutton(conversoes, text="AF para GR", variable="Operacao", value=3, tristatevalue=0, command=lambda: self.set_operacao(3))

        af = LabelFrame(self.top_frame_esq, text='4 AFND/AFM')
        afd = Radiobutton(af, text="Determinização", variable="Operacao", value=4, tristatevalue=0, command=lambda: self.set_operacao(4))
        afm = Radiobutton(af, text="Minimização", variable="Operacao", value=5, tristatevalue=0, command=lambda: self.set_operacao(5))

        oper = LabelFrame(self.top_frame_esq, text='5 Obter AF')
        inter = Radiobutton(oper, text="Intersecção", variable="Operacao", value=6, tristatevalue=0, command=lambda: self.set_operacao(6))
        dif = Radiobutton(oper, text="Diferença", variable="Operacao", value=7, tristatevalue=0, command=lambda: self.set_operacao(7))
        rev = Radiobutton(oper, text="Reverso", variable="Operacao", value=8, tristatevalue=0, command=lambda: self.set_operacao(8))

        operGR = LabelFrame(self.top_frame_esq, text='6 Obter GR')
        uniao = Radiobutton(operGR, text="União", variable="Operacao", value=9, tristatevalue=0, command=lambda: self.set_operacao(9))
        concat = Radiobutton(operGR, text="Concatenação", variable="Operacao", value=10, tristatevalue=0, command=lambda: self.set_operacao(10))
        fech = Radiobutton(operGR, text="Fechamento", variable="Operacao", value=11, tristatevalue=0, command=lambda: self.set_operacao(11))

        sentence = LabelFrame(self.top_frame_esq, text='7 Sentenças')
        recog = Radiobutton(sentence, text="Reconhecimento", variable="Operacao", value=12, tristatevalue=0, command=lambda: self.set_operacao(12))
        enum = Radiobutton(sentence, text="Enumeração", variable="Operacao", value=13, tristatevalue=0, command=lambda: self.set_operacao(13))

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

        btn_salvar.grid(row=0, column=0)
        btn_continue.grid(row=0, column=1)
        btn_carregar.grid(row=0, column=2)

    # Salvar uma expressão em disco
    def salvar_expressao(self):
        self.controller.salvar_expressao(self.input)

    # Carregar uma expressão em disco
    def carregar_expressao(self):
        self.input.delete("1.0", END)
        self.input.insert(INSERT, self.controller.carregar_expressao())
        self.input.delete("end-1c", END)

    # Armazena a operação selecionada
    def set_operacao(self, op):
        self.operacao = op

    # Executar a operacao selecionada e exibe os resultados
    def exibir_resultados(self):
        self.controller.set_dict(self.input, self.input_2, self.operacao)
        self.result = self.controller.exec(self.operacao) # Faz a verificacao do tamanho e selecionar as saídas corretas

        # if self.operacao == 3:
        #     self.formata_resultado_gr()
        # elif self.operacao == 9:
        #     self.adequar_frame_resultados_gr()
        #     for result in self.result:
        #         self.output_gr.insert(END, result + '\n')
        #     self.controller.clean_estados_aceitacao()
        # elif self.operacao == 8:
        #     message = ("Resultado do reconhecimento", "A sentença pertence a linguagem" if self.result else "Resultado do reconhecimento", "A sentença não pertence a linguagem")
        #     messagebox.showinfo(message)
        # else:
        #     self.formata_resultado_af()

    def formata_resultado_af(self):
        pass

    def formata_resultado_gr(self):
        pass

