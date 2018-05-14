from tkinter import messagebox
from tkinter import *
from Control.Controller import *

class View:

    # Frames
    root = None
    frame_info = None
    frame_af = None
    frame_expression = None
    frame_resultados_af = None
    frame_resultados_gr = None

    # Controle
    operacao = None
    controller = None

    # Armazenamento
    expression = None
    matrix = None
    result = None
    output_gr = None
    output_af = None

    # Constantes
    CONST_ROW = 9
    CONST_COLUMN = 5

    def __init__(self, controller):
        self.root = Tk()
        self.root.title('T1 de Formais')
        self.controller = controller

        # Tela principal
        self.create_frame_info()

        # Inicializacao dos frames
        self.create_insert_expression()
        self.create_af_matrix()
        self.create_frame_resultados()
        self.create_output_af()
        self.create_output_gr()
        self.sentence = Text(self.frame_af, bg='white', height=2, width=15)
        self.second_entry = Text(self.frame_expression, bg='white', height=13, width=22)

        # Frame default
        self.frame_expression.grid(row=0, column=1, padx=10, pady=10)

        self.root.mainloop()

    def create_af_matrix(self):
        self.frame_af = Frame(self.root)
        rows = self.CONST_ROW
        columns = self.CONST_COLUMN

        self.matrix = [[None for y in range(columns)] for x in range(rows)]

        for row in range(rows):
            for column in range(columns):
                entry = Entry(self.frame_af, bg='white', width=5)
                entry.grid(row=row, column=column, padx=1, pady=1)
                self.matrix[row][column] = entry

        for column in range(columns):
            self.frame_af.grid_columnconfigure(column, weight=1)

        self.matrix[0][0].insert(0, "XXXX")
        self.matrix[0][0].config(state='disabled')

    def create_insert_expression(self):
        self.frame_expression = Frame(self.root)

        self.expression = Text(self.frame_expression, bg='white', height=13, width=22)
        self.expression.pack()

    def create_frame_resultados(self):
        self.frame_resultados_af = Frame(self.root)
        self.frame_resultados_gr = Frame(self.root)

    def create_output_gr(self):
        self.output_gr = Text(self.frame_resultados_gr, bg='white', height=13, width=22)
        self.output_gr.grid(row=0, column=0)

        Button(self.frame_resultados_gr, text="Reutilizar", command=self.reutilizar_gr).grid(row=1, column=0, pady=2)

    def create_output_af(self):
        rows = self.CONST_ROW
        columns = self.CONST_COLUMN

        self.output_af = [[None for y in range(columns)] for x in range(rows)]

        for row in range(rows):
            for column in range(columns):
                entry = Entry(self.frame_resultados_af, bg='white', width=5)
                entry.grid(row=row, column=column, padx=1, pady=1)
                self.output_af[row][column] = entry

        for column in range(columns):
            self.frame_resultados_af.grid_columnconfigure(column, weight=1)

        self.output_af[0][0].insert(0, "XXXX")
        self.output_af[0][0].config(state='disabled')

        Button(self.frame_resultados_af, text="Reutilizar", command=self.reutilizar_af).grid(row=10, column=1, columnspan=2, pady=2)

    def create_frame_info(self):
        self.frame_info = Frame(self.root)
        self.frame_info.grid(row=0, column=0)

        label_info = Label(self.frame_info, text="Escolha uma das operações abaixo:")
        label_info.grid(row=0, column=0)

        Radiobutton(self.frame_info, text="Conversão de ER para AF", variable="Operacao", value=1,tristatevalue=0,
                    command=lambda: [self.set_operacao(1), self.change_window()]).grid(row=1, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Conversão de GR para AF", variable="Operacao", value=2, tristatevalue=0,
                    command=lambda: [self.set_operacao(2), self.change_window()]).grid(row=2, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Conversão de AF para GR", variable="Operacao", value=3, tristatevalue=0,
                    command=lambda: [self.set_operacao(3), self.change_window()]).grid(row=3, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Determinização de AF", variable="Operacao", value=4, tristatevalue=0,
                    command=lambda: [self.set_operacao(4), self.change_window()]).grid(row=4, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Minimização de AF", variable="Operacao", value=5, tristatevalue=0,
                    command=lambda: [self.set_operacao(5), self.change_window()]).grid(row=5, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Operações com AF", variable="Operacao", value=6, tristatevalue=0,
                    command=lambda: [self.set_operacao(6), self.change_window()]).grid(row=6, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Fechamento de GR", variable="Operacao", value=7, tristatevalue=0,
                    command=lambda: [self.set_operacao(7), self.change_window()]).grid(row=7, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Reconhecimento de sentenças de um AF", variable="Operacao", tristatevalue=0,
                    value=8, command=lambda: [self.set_operacao(8), self.change_window()]).grid(row=8, column=0, sticky=W)
        Radiobutton(self.frame_info, text="Enumeração de sentenças de um AF", variable="Operacao", tristatevalue=0,
                    value=9, command=lambda: [self.set_operacao(9), self.change_window()]).grid(row=9, column=0, sticky=W)

        btn_continue = Button(self.frame_info, text="Continuar", command=self.exec_operation)
        btn_continue.grid(row=10, column=0, pady=6, sticky=W)

        btn_salvar = Button(self.frame_info, text="Salvar Expressão", command=self.salvar_expressao)
        btn_salvar.grid(row=10, column=0, pady=6)

        btn_carregar = Button(self.frame_info, text="Carregar Expressão", command=self.carregar_expressao)
        btn_carregar.grid(row=10, column=1, pady=6, sticky=W)

    def salvar_expressao(self):
        self.controller.salvar_expressao(self.expression)

    def carregar_expressao(self):
        self.expression.delete("1.0", END)
        self.expression.insert(INSERT, self.controller.carregar_expressao())
        self.expression.delete("end-1c", END)

    def change_window(self):
        gr = [1, 2, 7]

        if self.operacao in gr:
            self.frame_af.grid_remove()
            self.frame_expression.grid(row=0, column=1, padx=10, pady=10)
            if self.operacao == 7:
                self.second_entry.pack()
            else:
                self.second_entry.grid_remove()
        elif self.operacao not in gr:
            self.frame_expression.grid_remove()
            self.frame_af.grid(row=0, column=1, padx=10, pady=10)
            if self.operacao == 8 or self.operacao == 9:
                self.sentence.grid(row=10, column=1, columnspan=5, pady=2)
    def set_operacao(self, opcao):
        self.operacao = opcao

    def exec_operation(self):
        if self.operacao == 2:
            self.controller.set_dict_gr(self.expression)
        elif self.operacao == 1:
            self.controller.set_dict_er(self.expression)
        elif self.operacao == 7:
            self.controller.set_dict_gr(self.expression)
            self.controller.set_dict_gr_op(self.second_entry)
        elif self.operacao == 8:
            self.controller.set_dict_af(self.matrix)
            self.controller.set_sentence(self.sentence)
        elif self.operacao == 9:
            self.controller.set_dict_af(self.matrix)
            self.controller.set_sentence_size(self.sentence)
        else:
            self.controller.set_dict_af(self.matrix)
        self.result = self.controller.exec(self.operacao)
        self.exibir_resultados()

    def exibir_resultados(self):
        if self.operacao == 7:
            self.formata_resultado_af()
        if self.operacao == 3:
            self.formata_resultado_gr()
        elif self.operacao == 9:
            self.adequar_frame_resultados_gr()
            #self.result.sort(key=len)
            for result in self.result:
                self.output_gr.insert(END, result + '\n')
            self.controller.clean_estados_aceitacao()
        elif self.operacao == 8:
            if self.result:
                messagebox.showinfo("Resultado do reconhecimento", "A sentença pertence a linguagem")
            else:
                messagebox.showinfo("Resultado do reconhecimento", "A sentença não pertence a linguagem")
        else:
            self.formata_resultado_af()

    # Pega o dicionario e formata visualmente em GR
    def formata_resultado_gr(self):
        self.adequar_frame_resultados_gr()
        estados_aceitacao = self.controller.get_estados_aceitacao()

        for keys in self.result:
            tmp = keys + "->"

            for list in range(len(self.result[keys])):
                tmp += self.result[keys][list]
                if list+1 < len(self.result[keys]):
                    if not self.result[keys][list+1].istitle():
                        tmp += "|"

            for estados_finais in estados_aceitacao:
               indices = [i for i, elem in enumerate(self.result[keys]) if estados_finais in elem]
               for index in indices:
                   tmp += '|' + self.result[keys][index-1]
            self.output_gr.insert(END, tmp + '\n')

        self.output_gr.delete("end-1c", END)
        self.controller.clean_estados_aceitacao()

    # Pega o dicionario e formata visualmente em AF
    def formata_resultado_af(self):
        self.adequar_frame_resultados_af()

        keys = list(self.result.keys())
        estados_aceitacao = self.controller.get_estados_aceitacao()
        alfabeto = []

        # Seta alfabeto
        for key in keys:
            for columns in range(len(self.result[key])):
                if self.result[key][columns][0] not in alfabeto:
                    alfabeto.insert(len(alfabeto), self.result[key][columns][0])

        # Seta alfabeto na GUI
        index = 0
        for char in alfabeto:
            self.output_af[0][index + 1].insert(0, char)
            index += 1

        # Seta restante da tabela
        for rows in range(len(keys)):
            key = keys[rows]
            if keys[rows] in estados_aceitacao:
                key = '*' + keys[rows]

            self.output_af[rows+1][0].insert(0, key)
            for columns in range(len(self.result[keys[rows]])):
                if len(self.output_af[rows+1][alfabeto.index(self.result[keys[rows]][columns][0])+1].get()) == 0:
                    self.output_af[rows+1][alfabeto.index(self.result[keys[rows]][columns][0])+1].insert(0, self.result[keys[rows]][columns][1])
                else:
                    self.output_af[rows + 1][alfabeto.index(self.result[keys[rows]][columns][0]) + 1].insert(0, self.result[keys[rows]][columns][1]+".")

        self.controller.clean_estados_aceitacao()

    def adequar_frame_resultados_gr(self):
        self.output_gr.delete('1.0', END)
        self.frame_resultados_af.grid_remove()
        self.frame_resultados_gr.grid(row=0, column=3)
        self.output_gr.grid()

    def adequar_frame_resultados_af(self):
        self.create_output_af()
        self.frame_resultados_gr.grid_remove()
        self.frame_resultados_af.grid(row=0, column=3)

    def reutilizar_af(self):
        for rows in range(len(self.matrix)):
            for columns in range(len(self.matrix[rows])):
                self.matrix[rows][columns].delete(0, END)
                self.matrix[rows][columns].insert(0, self.output_af[rows][columns].get())

    def reutilizar_gr(self):
        self.expression.delete('1.0', END)
        self.expression.insert(INSERT, self.output_gr.get("1.0", "end-1c"))

# Comentarios

# Falar que o codigo tenta corrigir erros, por exemplo:
# S->aS|ac é corrigido para S->aS|a|c
# S->aS|c|S é corrigido para S->aS|cS