class Nodo:
    enum = 0

    def __init__(self, simbolo, pai, lado_pai, eh_folha, eh_raiz):
        self._simbolo = simbolo
        self._pai = pai
        self._lado_pai = lado_pai
        self._eh_folha = eh_folha
        self._eh_raiz = eh_raiz
        self._filho_esquerda = None
        self._filho_direita = None
        self._costura = None
        self._enum = None
        if eh_folha:
            self.enum = Nodo.enum
            Nodo.enum += 1

    def get_simbolo(self):
        return self._simbolo

    def get_eh_folha(self):
        return self._eh_folha

    def get_eh_raiz(self):
        return self._eh_raiz

    def get_pai(self):
        return self._pai

    def get_lado_pai(self):
        return self._lado_pai

    def get_simbolo(self):
        return self._simbolo

    def get_filho_esquerda(self):
        return self._filho_esquerda

    def get_filho_direita(self):
        return self._filho_direita

    def set_filho_esquerda(self, filho_esquerda):
        self._filho_esquerda = filho_esquerda

    def set_filho_direita(self, filho_direita):
        self._filho_direita = filho_direita

    def get_costura(self):
        return self._costura

    def set_costura(self, costura):
        self._costura = costura

